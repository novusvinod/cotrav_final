from django.urls import path,include
from Company.Api_Views import api_views

urlpatterns = [
    path('api/companies', api_views.companies),
    path('api/company_rates', api_views.company_rates),
    path('api/billing_entities', api_views.billing_entities),
    path('api/admins', api_views.admins),
    path('api/groups', api_views.groups),
    path('api/subgroups', api_views.subgroups),
    path('api/spocs', api_views.spocs),
    path('api/employees', api_views.employee),

    path('api/cities', api_views.cities),

    path('api/add_billing_entity', api_views.add_billing_entity),
    path('api/add_group', api_views.add_group),
]