from django.urls import path,include
from Company.VIEW.Agent import agent_views

urlpatterns = [
    #Agent Path
    path('agents/login', agent_views.agent_login),
    path('agents/postlogin', agent_views.agent_login_action),
    path('agents/logout', agent_views.agent_logout_action),
    path('agents/agent_home', agent_views.agent_homepage),

    # Corporate Path
    path('agents/add-company', agent_views.add_company),
    path('agents/companies', agent_views.companies),
    path('agents/company_rates', agent_views.company_rates),
    path('agents/billing_entities', agent_views.billing_entities),
    path('agents/admins', agent_views.admins),
    path('agents/groups', agent_views.groups),
    path('agents/subgroups', agent_views.subgroups),
    path('agents/spocs', agent_views.spocs),
    path('agents/employees', agent_views.employees),

    # Corporate Edit Path
    path('agents/edit-company/<int:id>', agent_views.edit_company),
]