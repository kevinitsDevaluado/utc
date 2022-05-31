import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.barrios.forms import District, DistrictForm
from core.security.mixins import PermissionMixin


class DistrictListView(PermissionMixin, ListView):
    model = District
    template_name = 'district/list.html'
    permission_required = 'view_district'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in District.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('district_create')
        context['title'] = 'Listado de Barrios'
        return context


class DistrictCreateView(PermissionMixin, CreateView):
    model = District
    template_name = 'district/create.html'
    form_class = DistrictForm
    success_url = reverse_lazy('district_list')
    permission_required = 'add_district'

    def validate_data(self):
        data = {'valid': True}
        try:
            name = self.request.POST['name'].strip()
            parroquia = self.request.POST['parroquia']
            if len(parroquia):
                if District.objects.filter(name__iexact=name, parroquia_id=parroquia):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
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
        context['title'] = 'Nuevo registro de un Barrio'
        context['action'] = 'add'
        return context


class DistrictUpdateView(PermissionMixin, UpdateView):
    model = District
    template_name = 'district/create.html'
    form_class = DistrictForm
    success_url = reverse_lazy('district_list')
    permission_required = 'change_district'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            id = self.get_object().id
            name = self.request.POST['name'].strip()
            parroquia = self.request.POST['parroquia']
            if len(parroquia):
                if District.objects.filter(name__iexact=name, parroquia_id=parroquia).exclude(id=id):
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


class DistrictDeleteView(PermissionMixin, DeleteView):
    model = District
    template_name = 'district/delete.html'
    success_url = reverse_lazy('district_list')
    permission_required = 'delete_district'

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
