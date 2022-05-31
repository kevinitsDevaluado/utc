from django.urls import path
from core.barrios.views.province.views import *
from core.barrios.views.parish.views import *
from core.barrios.views.country.views import *
from core.barrios.views.canton.views import *
from core.barrios.views.district.views import *
from core.barrios.views.view_district.views import *
from core.barrios.views.family.views import *
from core.barrios.views.company.views import *
from core.barrios.views.companyc.views import *
from core.barrios.views.view_company.views import *
urlpatterns = [
    # province
    path('province/', ProvinceListView.as_view(), name='province_list'),
    path('province/add/', ProvinceCreateView.as_view(), name='province_create'),
    path('province/update/<int:pk>/', ProvinceUpdateView.as_view(), name='province_update'),
    path('province/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete'),
    # canton
    path('canton/', CantonListView.as_view(), name='canton_list'),
    path('canton/add/', CantonCreateView.as_view(), name='canton_create'),
    path('canton/update/<int:pk>/', CantonUpdateView.as_view(), name='canton_update'),
    path('canton/delete/<int:pk>/', CantonDeleteView.as_view(), name='canton_delete'),
    # parish
    path('parish/', ParishListView.as_view(), name='parish_list'),
    path('parish/add/', ParishCreateView.as_view(), name='parish_create'),
    path('parish/update/<int:pk>/', ParishUpdateView.as_view(), name='parish_update'),
    path('parish/delete/<int:pk>/', ParishDeleteView.as_view(), name='parish_delete'),
    # country
    path('country/', CountryListView.as_view(), name='country_list'),
    path('country/add/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),    
    # district
    path('district/', DistrictListView.as_view(), name='district_list'),
    path('district/add/', DistrictCreateView.as_view(), name='district_create'),
    path('district/update/<int:pk>/', DistrictUpdateView.as_view(), name='district_update'),
    path('district/delete/<int:pk>/', DistrictDeleteView.as_view(), name='district_delete'),
    #VER BARRIO
    path('verBarrio/<int:pk>/', VerDistrictView.as_view(), name='verBarrio'),
    #VER REUNIONES
    path('verMeeting/<int:pk>/', VerMeetingView.as_view(), name='verMeeting'),
    #VER CUOTAS
    path('verFees/<int:pk>/', VerFeesView.as_view(), name='verFees'),
    #pagos
    path('verPagos/<int:pk>/', VerPaysmentsView.as_view(), name='verPagos'),
    #Report
    path('report/<int:pk>/', report.as_view(), name='report') ,
    # Family
    path('family/', FamilyResponsibilitiesListView.as_view(), name='familyResponsibilities_list'),
    path('family/add/', FamilyResponsibilitiesCreateView.as_view(), name='familyResponsibilities_create'),
    path('family/update/<int:pk>/', FamilyResponsibilitiesUpdateView.as_view(), name='familyResponsibilities_update'),
    path('family/delete/<int:pk>/', FamilyResponsibilitiesDeleteView.as_view(), name='familyResponsibilities_delete'),
    
    # Company
    path('company/', CompanyListView.as_view(), name='company_list'),
    path('company/add/', CompanyCreateView.as_view(), name='company_create'),
    path('company/update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('company/delete/<int:pk>/', CompanyDeleteView.as_view(), name='company_delete'),


     # CompanyC
    path('companyc/', CompanycListView.as_view(), name='companyc_list'),
    path('companyc/add/', CompanycCreateView.as_view(), name='companyc_create'),
    path('companyc/update/<int:pk>/', CompanycUpdateView.as_view(), name='companyc_update'),
    path('companyc/delete/<int:pk>/', CompanycDeleteView.as_view(), name='companyc_delete'),

    #VER BARRIO
    path('viewCompany/<int:pk>/', VerCompanyView.as_view(), name='verCompanyClient'),              
]
