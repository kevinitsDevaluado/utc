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

class VerCompanyView(CreateView):
    template_name = 'mainpage/view.html'
    form_class = CompanyForm


    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('verCompany', kwargs={'pk': pk})

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            pk = self.kwargs['pk']
            fecha = datetime.now().strftime('%Y-%m-%d')
            if type == 'fecha':
                if Client.objects.filter(code__icontains=obj):
                    data['valid'] = False
            elif type == 'code':
                if RollCall.objects.filter(user__code__icontains=obj,date=fecha):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add_president':
                with transaction.atomic():
                   pass   
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
        context['title'] = 'Empresa'

        barrio = District.objects.get(id=pk)
        compa = Company.objects.filter(district= barrio.id)
        context['companys'] = compa
        context['list_url'] = reverse_lazy('verCompany', kwargs={'pk': self.kwargs['pk']})
        return context

class VerCompanysView(CreateView):
    template_name = 'mainpage/company_view.html'
    form_class = CompanyForm


    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('verCompanys', kwargs={'pk': pk})

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            pk = self.kwargs['pk']
            fecha = datetime.now().strftime('%Y-%m-%d')
            if type == 'fecha':
                if Client.objects.filter(code__icontains=obj):
                    data['valid'] = False
            elif type == 'code':
                if RollCall.objects.filter(user__code__icontains=obj,date=fecha):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add_president':
                with transaction.atomic():
                   pass   
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
        barrio = District.objects.get(id=pk)
        compa = Company.objects.filter(district= barrio.id)
        a = 0
        for i in compa:
            a = i.id
        product = Product.objects.filter(company_id=a)
        company = Company.objects.get(id=a)
        productcount = Product.objects.filter(company_id=a).count()
        context['title'] = 'Empresa'
        context['companys'] = compa
        context['product'] = product
        context['prueba'] = company
        context['productcount'] = productcount
        context['list_url'] = reverse_lazy('verCompanys', kwargs={'pk': self.kwargs['pk']})
        return context
