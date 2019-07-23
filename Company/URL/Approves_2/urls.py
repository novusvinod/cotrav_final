from django.urls import path,include
from Company.VIEW.Approves_2 import approves_2_views

urlpatterns = [
    path('Approves_2/home', approves_2_views.homepage),
    path('Approves_2/company-billing_entities/<int:id>', approves_2_views.company_billing_entities),
    path('Approves_2/company-rates/<int:id>', approves_2_views.company_rates),
    path('Approves_2/company-groups/<int:id>', approves_2_views.company_groups),
    path('Approves_2/view-company-group/<int:id>', approves_2_views.view_company_group),
    path('Approves_2/company-subgroups/<int:id>', approves_2_views.company_subgroups),
    path('Approves_2/view-company-subgroup/<int:id>', approves_2_views.view_company_subgroup),
    path('Approves_2/company-admins/<int:id>', approves_2_views.company_admins),
    path('Approves_2/company-spocs/<int:id>', approves_2_views.company_spocs),
    path('Approves_2/company-employees/<int:id>', approves_2_views.company_employees),
]