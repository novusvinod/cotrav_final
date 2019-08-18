from django.urls import path,include
from Common.VIEW.Api import api_views

urlpatterns = [

######################### CORPORATE ADMIN URLS ############################
    path('', include('Common.URL.Api.admin_urls')),
    path('', include('Common.URL.Api.spoc_urls')),
    path('', include('Common.URL.Api.approver_1_urls')),
    path('', include('Common.URL.Api.approver_2_urls')),
    path('', include('Common.URL.Api.agent_urls')),
######################### END CORPORATE URLS ####################

    path('api/login', api_views.login),

    path('api/cities', api_views.cities),
    path('api/add_city_name', api_views.add_city_name),
    path('api/add_state_name', api_views.add_state_name),
    path('api/add_country_name', api_views.add_country_name),

    path('api/taxi_types', api_views.taxi_types),

    path('api/companies', api_views.companies),
    path('api/view_company', api_views.view_company),
    path('api/add_company', api_views.add_companies),
    path('api/update_company', api_views.update_company),
    path('api/delete_company', api_views.delete_company),

    path('api/company_rates', api_views.company_rates),
    path('api/add_company_rates', api_views.add_company_rates),
    path('api/update_company_rates', api_views.update_company_rates),
    path('api/delete_company_rates', api_views.delete_company_rates),

    path('api/billing_entities', api_views.billing_entities),
    path('api/admins', api_views.admins),
    path('api/groups', api_views.groups),
    path('api/subgroups', api_views.subgroups),
    path('api/spocs', api_views.spocs),
    path('api/employees', api_views.employee),

    path('api/add_billing_entity', api_views.add_billing_entity),
    path('api/update_billing_entity', api_views.update_billing_entity),
    path('api/delete_billing_entity', api_views.delete_billing_entity),

    path('api/view_group_auth', api_views.view_group_auth),
    path('api/add_group_auth', api_views.add_group_auth),
    path('api/update_group_auth', api_views.update_group_auth),
    path('api/delete_group_auth', api_views.delete_group_auth),

    path('api/view_group', api_views.view_group),
    path('api/add_group', api_views.add_group),
    path('api/update_group', api_views.update_group),
    path('api/delete_group', api_views.delete_group),

    path('api/view_subgroup', api_views.view_subgroup),
    path('api/add_subgroup', api_views.add_subgroup),
    path('api/update_subgroup', api_views.update_subgroup),
    path('api/delete_subgroup', api_views.delete_subgroup),

    path('api/view_subgroup_auth', api_views.view_subgroup_auth),
    path('api/add_subgroup_auth', api_views.add_subgroup_auth),
    path('api/update_subgroup_auth', api_views.update_subgroup_auth),
    path('api/delete_subgroup_auth', api_views.delete_subgroup_auth),

    path('api/add_admin', api_views.add_admin),
    path('api/update_admin', api_views.update_admin),
    path('api/delete_admin', api_views.delete_admin),

    path('api/view_spoc', api_views.view_spoc),
    path('api/add_spoc', api_views.add_spoc),
    path('api/update_spoc', api_views.update_spoc),
    path('api/delete_spoc', api_views.delete_spoc),

    path('api/view_employee', api_views.view_employee),
    path('api/add_employee', api_views.add_employee),
    path('api/update_employee', api_views.update_employee),
    path('api/delete_employee', api_views.delete_employee),

    path('api/agents', api_views.get_agents),
    path('api/view_agent', api_views.view_agent),
    path('api/add_agent', api_views.add_agent),
    path('api/update_agent', api_views.update_agent),
    path('api/delete_agent', api_views.delete_agent),

    ######### TAXI BOOKING API #####################

    path('api/view_taxi_booking', api_views.view_taxi_booking),

]