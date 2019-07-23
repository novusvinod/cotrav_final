from django.urls import path,include
from Company.VIEW.Spoc import spoc_views

urlpatterns = [
    path('Spoc/home', spoc_views.homepage),
    path('Spoc/company-billing_entities/<int:id>', spoc_views.company_billing_entities),
    path('Spoc/company-rates/<int:id>', spoc_views.company_rates),
    path('Spoc/company-groups/<int:id>', spoc_views.company_groups),
    path('Spoc/view-company-group/<int:id>', spoc_views.view_company_group),
    path('Spoc/company-subgroups/<int:id>', spoc_views.company_subgroups),
    path('Spoc/view-company-subgroup/<int:id>', spoc_views.view_company_subgroup),
    path('Spoc/company-admins/<int:id>', spoc_views.company_admins),
    path('Spoc/company-spocs/<int:id>', spoc_views.company_spocs),
    path('Spoc/company-employees/<int:id>', spoc_views.company_employees),
]