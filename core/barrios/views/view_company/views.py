from itertools import count
import json
from datetime import datetime
from re import A
from django.contrib import messages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
import smtplib
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook

from core.barrios.forms import *
from core.barrios.models import *

class VerCompanyView(LoginRequiredMixin,CreateView):
    template_name = 'view_company/company.html'
    form_class = DistrictForm


    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('verCompany', kwargs={'pk': pk})

    def validate_data(self):
        data = {'valid': True}
        try:
            name = self.request.POST['name'].strip()
            category = self.request.POST['category']
            if len(category):
                if Product.objects.filter(name__iexact=name, category_id=category):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)


    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add_company':
                with transaction.atomic():
                    print('INGRESANDO A LA OPCION')
                    form = CategoryForm(request.POST, files=request.FILES)
                    if form.is_valid():
                        pk = self.kwargs['pk']
                        form.instance.company_id = pk
                        form.save()
                        messages.info(request, 'Categoría agregada.')                        

                    else:
                        messages.info(request, 'ERROr..')  
            elif action == 'add_product':
                with transaction.atomic():
                    print('INGRESANDO A LA OPCION PRODUCTO')
                    pk = self.kwargs['pk']
                    product = Product()
                    product.company_id = pk
                    product.name = request.POST['name']
                    product.category_id = request.POST['category']
                    if 'image' in request.FILES:
                        product.image = request.FILES['image']
                    product.pvp = float(request.POST['pvp'])
                    product.save()     
                    messages.info(request, 'Producto agregado.')                        

                    
            elif action == 'search_category_id':
                data = Category.objects.get(pk=request.POST['id']).toJSON()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        company = Company.objects.get(id = pk)
        context['company'] = company
        context['category'] = Category.objects.filter(company_id=company)
        context['product'] = Product.objects.filter(company_id=company)
        context['formCategory'] = CategoryForm()
        context['formProduct'] = ProductForm()
        context['title'] = '“Beneficio es vanidad, liquidez es sobrevivencia”'
        context['list_url'] = reverse_lazy('verCompany', kwargs={'pk': self.kwargs['pk']})
        return context

