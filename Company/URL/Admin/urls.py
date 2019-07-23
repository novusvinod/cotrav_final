from django.urls import path,include
from Company.VIEW.Admin import admin_views

urlpatterns = [
    path('Corporate/home', admin_views.homepage),
    path('Corporate/company-billing_entities/<int:id>', admin_views.company_billing_entities),
    path('Corporate/company-rates/<int:id>', admin_views.company_rates),

    path('Corporate/add-company-rate/<int:id>', admin_views.add_company_rate),
    path('Corporate/add-company-entity/<int:id>', admin_views.add_company_entity),

    path('Corporate/company-groups/<int:id>', admin_views.company_groups),
    path('Corporate/view-company-group/<int:id>', admin_views.view_company_group),
    path('Corporate/add-company-group/<int:id>', admin_views.add_company_group),
    path('Corporate/update-company-group/<int:id>', admin_views.update_company_group),
    path('Corporate/delete-company-group/<int:id>', admin_views.delete_company_group),
    path('Corporate/add-company-group-auth/<int:id>', admin_views.add_company_group_auth),

    path('Corporate/company-subgroups/<int:id>', admin_views.company_subgroups),
    path('Corporate/view-company-subgroup/<int:id>', admin_views.view_company_subgroup),
    path('Corporate/add-company-subgroup/<int:id>', admin_views.add_company_subgroup),
    path('Corporate/update-company-subgroup/<int:id>', admin_views.update_company_subgroup),
    path('Corporate/delete-company-subgroup/<int:id>', admin_views.delete_company_subgroup),
    path('Corporate/add-company-subgroup-auth/<int:id>', admin_views.add_company_subgroup_auth),

    path('Corporate/company-admins/<int:id>', admin_views.company_admins),
    path('add-company-admins/<int:id>', admin_views.add_company_admins),

    path('Corporate/company-spocs/<int:id>', admin_views.company_spocs),
    path('Corporate/add-spoc/<int:id>', admin_views.add_spocs),

    path('Corporate/company-employees/<int:id>', admin_views.company_employees),
    path('Corporate/add-employee/<int:id>', admin_views.add_employee),
]