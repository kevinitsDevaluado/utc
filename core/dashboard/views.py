import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView

from core.homepage.models import *
from core.security.models import Dashboard
from core.user.models import User
from core.barrios.models import *

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    
    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        context = self.get_context_data()
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                if self.request.user.get_group_id_session() == 1:
                    context['clients'] = User.objects.filter(groups__in=[settings.GROUPS.get('client')]).count()
                    context['datenow'] = datetime.now().date()
                else:
                    context['videos'] = Videos.objects.filter(state=True)
                    context['news'] = News.objects.filter(state=True)
                    usuario = request.user.id
                    cliente = Client.objects.get(user_id = usuario)
                    presidente = PresidentDistrict.objects.filter(district_id = cliente.district.id,state=True)

                    #print('PRESIDENTE DEL BARRIO',presidente.user_id)
                    print('presidente',cliente.id)
                    print('sd')
                    veamos = 0
                    for e in presidente:
                        veamos = e.user.id
                    print('veamos',veamos)
                    context['barrio_actual'] = cliente
                    context['id_barrio'] = cliente.district.id
                    context['presidente'] = presidente
                    context['veamos'] = veamos

                return render(request, 'vtcpanel.html', context)
        return render(request, 'hztpanel.html', context)

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
