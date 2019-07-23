from django.urls import path,include
from Company.VIEW.Approves_1 import approves_1_views

urlpatterns = [
    path('Approves_1/home', approves_1_views.homepage),
    path('Approves_1/company-billing_entities/<int:id>', approves_1_views.company_billing_entities),
    path('Approves_1/company-rates/<int:id>', approves_1_views.company_rates),
    path('Approves_1/company-groups/<int:id>', approves_1_views.company_groups),
    path('Approves_1/view-company-group/<int:id>', approves_1_views.view_company_group),
    path('Approves_1/company-subgroups/<int:id>', approves_1_views.company_subgroups),
    path('Approves_1/view-company-subgroup/<int:id>', approves_1_views.view_company_subgroup),
    path('Approves_1/company-admins/<int:id>', approves_1_views.company_admins),
    path('Approves_1/company-spocs/<int:id>', approves_1_views.company_spocs),
    path('Approves_1/company-employees/<int:id>', approves_1_views.company_employees),
]