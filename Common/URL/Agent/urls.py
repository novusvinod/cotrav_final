from django.urls import path,include
from Common.VIEW.Agent import agent_views

urlpatterns = [
    #Agent Path
    path('agents/login', agent_views.agent_login_action),
    path('agents/logout', agent_views.agent_logout_action),
    path('agents/agent_home', agent_views.agent_homepage),

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

    path('agents/agents', agent_views.view_agents),
    path('agents/add-agent/<int:id>', agent_views.add_agent),

    path('agents/operators', agent_views.operators),
    path('agents/view-operator', agent_views.view_operator),
    path('agents/add-operator', agent_views.add_operator),
    path('agents/operator-rates', agent_views.operator_rates),
    path('agents/add-operator-rates', agent_views.add_operator_rate),

    path('agents/taxi-bookings/<int:id>', agent_views.taxi_bookings),
    path('agents/add-taxi-booking/<int:id>', agent_views.add_taxi_booking),
    path('agents/view-taxi-booking/<int:id>', agent_views.view_taxi_booking),



]