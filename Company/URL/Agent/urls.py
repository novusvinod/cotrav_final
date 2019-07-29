from django.urls import path,include
from Company.VIEW.Agent import agent_views

urlpatterns = [
    #Agent Path
    path('agents/login', agent_views.agent_login),
    path('agents/postlogin', agent_views.agent_login_action),
    path('agents/logout', agent_views.agent_logout_action),
    path('agents/agent_home', agent_views.agent_homepage),

    # agents Path

    # path('agents/billing_entities', agent_views.billing_entities),
    # path('agents/admins', agent_views.admins),
    # path('agents/groups', agent_views.groups),
    # path('agents/subgroups', agent_views.subgroups),
    # path('agents/spocs', agent_views.spocs),
    # path('agents/employees', agent_views.employees),

    path('agents/companies', agent_views.companies),
    path('agents/add-company', agent_views.add_company),
    path('agents/edit-company/<int:id>', agent_views.edit_company),
    path('agents/delete-company/<int:id>', agent_views.delete_company),

    path('agents/billing_entities/<int:id>', agent_views.company_billing_entities),
    path('agents/rates/<int:id>', agent_views.company_rates),
    path('agents/add-company-rate/<int:id>', agent_views.add_company_rate),
    path('agents/add-company-entity/<int:id>', agent_views.add_company_entity),

    path('agents/groups/<int:id>', agent_views.company_groups),
    path('agents/view-company-group/<int:id>', agent_views.view_company_group),
    path('agents/add-company-group/<int:id>', agent_views.add_company_group),
    path('agents/update-company-group/<int:id>', agent_views.update_company_group),
    path('agents/delete-company-group/<int:id>', agent_views.delete_company_group),
    path('agents/add-company-group-auth/<int:id>', agent_views.add_company_group_auth),

    path('agents/subgroups/<int:id>', agent_views.company_subgroups),
    path('agents/view-company-subgroup/<int:id>', agent_views.view_company_subgroup),
    path('agents/add-company-subgroup/<int:id>', agent_views.add_company_subgroup),
    path('agents/update-company-subgroup/<int:id>', agent_views.update_company_subgroup),
    path('agents/delete-company-subgroup/<int:id>', agent_views.delete_company_subgroup),
    path('agents/add-company-subgroup-auth/<int:id>', agent_views.add_company_subgroup_auth),

    path('agents/admins/<int:id>', agent_views.company_admins),
    path('agents/add-company-admins/<int:id>', agent_views.add_company_admins),

    path('agents/spocs/<int:id>', agent_views.company_spocs),
    path('agents/add-spoc/<int:id>', agent_views.add_spocs),

    path('agents/employees/<int:id>', agent_views.company_employees),
    path('agents/add-employee/<int:id>', agent_views.add_employee),
]