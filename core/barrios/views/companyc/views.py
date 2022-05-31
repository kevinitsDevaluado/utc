import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.barrios.forms import Company, CompanyForm, Client,CompanycForm
from core.security.mixins import PermissionMixin

from django.contrib import messages

class CompanycListView(PermissionMixin, ListView):
    model = Company
    template_name = 'companyc/list.html'
    permission_required = 'view_company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = Client.objects.get(user_id = self.request.user.id)
        empresa = Company.objects.filter(user_id = cliente.id)
        context['create_url'] = reverse_lazy('companyc_create')
        context['object_list'] = empresa
        context['title'] = 'Listado de Empresas'
        return context


class CompanycCreateView(PermissionMixin, CreateView):
    model = Company
    template_name = 'companyc/create.html'
    form_class = CompanycForm
    success_url = reverse_lazy('companyc_list')
    permission_required = 'add_company'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Company.objects.filter(name__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                form = CompanycForm(request.POST, files=request.FILES)
                if form.is_valid():
                    cliente = Client.objects.get(user_id = self.request.user.id)
                    form.instance.user_id = cliente.id
                    uno = request.POST['id_lat']
                    dos = request.POST['id_lng']
                    tres = uno +','+dos
                    form.instance.coordinates = tres
                    form.save()
                    messages.info(request, 'Empresa agregada.')                        

                else:
                    messages.info(request, 'ERROr..')                        


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
        context['title'] = 'Nuevo registro de una Empresa'
        context['action'] = 'add'
        return context


class CompanycUpdateView(PermissionMixin, UpdateView):
    model = Company
    template_name = 'company/create.html'
    form_class = CompanyForm
    success_url = reverse_lazy('companyc_list')
    permission_required = 'change_company'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'name':
                if Company.objects.filter(name__iexact=obj).exclude(id=id):
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
        context['title'] = 'Edición de una Empresa'
        context['action'] = 'edit'
        return context


class CompanycDeleteView(PermissionMixin, DeleteView):
    model = Company
    template_name = 'companyc/delete.html'
    success_url = reverse_lazy('companyc_list')
    permission_required = 'delete_company'

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
