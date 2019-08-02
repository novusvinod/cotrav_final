from django.urls import path,include
from Common.VIEW.Spoc import spoc_views

urlpatterns = [
    path('Corporate/Spoc/home', spoc_views.homepage),
    path('Corporate/Spoc/company-billing_entities/<int:id>', spoc_views.company_billing_entities),
    path('Corporate/Spoc/company-rates/<int:id>', spoc_views.company_rates),
    path('Corporate/Spoc/company-groups/<int:id>', spoc_views.company_groups),
    path('Corporate/Spoc/view-company-group/<int:id>', spoc_views.view_company_group),
    path('Corporate/Spoc/company-subgroups/<int:id>', spoc_views.company_subgroups),
    path('Corporate/Spoc/view-company-subgroup/<int:id>', spoc_views.view_company_subgroup),
    path('Corporate/Spoc/company-admins/<int:id>', spoc_views.company_admins),
    path('Corporate/Spoc/company-spocs/<int:id>', spoc_views.company_spocs),
    path('Corporate/Spoc/company-employees/<int:id>', spoc_views.company_employees),

    path('Corporate/Spoc/add-taxi-booking/<int:id>', spoc_views.add_taxi_booking),
]