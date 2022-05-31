import json
from django.db import transaction

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.barrios.forms import FamilyResponsibilities, FamilyForm
from core.security.mixins import PermissionMixin
from core.barrios.models import *

class FamilyResponsibilitiesListView(PermissionMixin, ListView):
    model = FamilyResponsibilities
    template_name = 'family/list.html'
    permission_required = 'view_familyresponsibilities'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        if self.request.user.groups.filter(name__in=['Cliente']):
            user = self.request.user.id
            cliente = Client.objects.get(user = user)
            print('usuario', cliente.user.last_name)
            familia = FamilyResponsibilities.objects.filter(user_id = cliente.id)
            context['s'] = familia
        else:
            todo = FamilyResponsibilities.objects.all()
            context['s'] = todo
        context['create_url'] = reverse_lazy('familyResponsibilities_create')
        context['title'] = 'Listado de Cargas Familiares'
        return context


class FamilyResponsibilitiesCreateView(PermissionMixin, CreateView):
    model = FamilyResponsibilities
    template_name = 'family/create.html'
    form_class = FamilyForm
    success_url = reverse_lazy('familyResponsibilities_list')
    permission_required = 'add_familyresponsibilities'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if Client.objects.filter(dni=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    familia = FamilyResponsibilities()
                    user = self.request.user.id
                    cliente = Client.objects.get(user = user)
                    print('usuario', cliente.user.last_name)
                    familia.user_id = cliente.id
                    familia.dni = request.POST['dni']
                    familia.name = request.POST['name']
                    familia.last_name = request.POST['last_name']
                    familia.gender = request.POST['gender']
                    familia.mobile = request.POST['mobile']
                    familia.phone = request.POST['phone']
                    familia.birthdate = request.POST['birthdate']
                    familia.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Carga Familiar'
        context['action'] = 'add'
        return context


class FamilyResponsibilitiesUpdateView(PermissionMixin, UpdateView):
    model = FamilyResponsibilities
    template_name = 'family/create.html'
    form_class = FamilyForm
    success_url = reverse_lazy('familyResponsibilities_list')
    permission_required = 'change_familyresponsibilities'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            id = self.get_object().id
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Barrio'
        context['action'] = 'edit'
        return context


class FamilyResponsibilitiesDeleteView(PermissionMixin, DeleteView):
    model = FamilyResponsibilities
    template_name = 'family/delete.html'
    success_url = reverse_lazy('familyResponsibilities_list')
    permission_required = 'delete_familyresponsibilities'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
