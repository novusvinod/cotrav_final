"""CoTrav URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Company.Agent_Web_Views import agent_web_views
from Company.Company_Web_Views import company_web_views



urlpatterns = [
    path('admin/', admin.site.urls),

######################### CORPORATE PATH URLS ################

    path('login', company_web_views.login),
    path('postlogin', company_web_views.login_action),
    path('logout', company_web_views.logout_action),
    path('home', company_web_views.homepage),
    path('company-billing_entities/<int:id>', company_web_views.company_billing_entities),
    path('company-rates/<int:id>', company_web_views.company_rates),
    path('company-admins/<int:id>', company_web_views.company_admins),
    path('company-groups/<int:id>', company_web_views.company_groups),
    path('company-subgroups/<int:id>', company_web_views.company_subgroups),
    path('company-spocs/<int:id>', company_web_views.company_spocs),
    path('company-employees/<int:id>', company_web_views.company_employees),


    path('add-company-rate/<int:id>', company_web_views.add_company_rate),
    path('add-company-entity/<int:id>', company_web_views.add_company_entity),
    path('add-company-group/<int:id>', company_web_views.add_company_group),


    path('view-company-group/<int:id>', company_web_views.view_company_group),
######################### END CORPORATE PATH URLS ###############


######################### AGENTS URLS ############################

    #Agent Path
    path('agents/login', agent_web_views.agent_login),
    path('agents/postlogin', agent_web_views.agent_login_action),
    path('agents/logout', agent_web_views.agent_logout_action),
    path('agents/agent_home', agent_web_views.agent_homepage),

    # Corporate Path
    path('agents/add-company', agent_web_views.add_company),
    path('agents/companies', agent_web_views.companies),
    path('agents/company_rates', agent_web_views.company_rates),
    path('agents/billing_entities', agent_web_views.billing_entities),
    path('agents/admins', agent_web_views.admins),
    path('agents/groups', agent_web_views.groups),
    path('agents/subgroups', agent_web_views.subgroups),
    path('agents/spocs', agent_web_views.spocs),
    path('agents/employees', agent_web_views.employees),

    # Corporate Edit Path
    path('agents/edit-company/<int:id>', agent_web_views.edit_company),

######################### END AGENTS URLS ################



######################### API URLS ############################

    path('', include('Company.urls')),

######################### END API URLS ####################







]
