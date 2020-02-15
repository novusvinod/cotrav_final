from django.urls import path,include
from Common.VIEW.Api import api_views

urlpatterns = [

######################### CORPORATE ADMIN URLS ############################
    path('', include('Common.URL.Api.admin_urls')),
    path('', include('Common.URL.Api.spoc_urls')),
    path('', include('Common.URL.Api.employee_urls')),
    path('', include('Common.URL.Api.approver_1_urls')),
    path('', include('Common.URL.Api.approver_2_urls')),
    path('', include('Common.URL.Api.agent_urls')),
    path('', include('Common.URL.Api.operator_urls')),
######################### END CORPORATE URLS ####################

    path('api/login', api_views.login),
    path('api/logout', api_views.logout),
    path('api/get_cotrav_billing_entities', api_views.get_cotrav_billing_entities),
    path('api/add_cotrav_billing_entities', api_views.add_cotrav_billing_entity),
    path('api/update_cotrav_billing_entities', api_views.update_cotrav_billing_entity),
    path('api/delete_cotrav_billing_entities', api_views.delete_cotrav_billing_entity),
    path('api/employee_dashboard', api_views.employee_dashboard),
    path('api/approver_1_dashboard', api_views.approver_1_dashboard),
    path('api/approver_2_dashboard', api_views.approver_2_dashboard),
    path('api/spoc_dashboard', api_views.spoc_dashboard),
    path('api/admin_dashboard', api_views.admin_dashboard),
    path('api/agent_dashboard', api_views.agent_dashboard),
    path('api/operator_dashboard', api_views.operator_dashboard),


    path('api/cities', api_views.cities),
    path('api/add_city_name', api_views.add_city_name),
    path('api/add_state_name', api_views.add_state_name),
    path('api/add_country_name', api_views.add_country_name),
    path('api/get_assessment_code', api_views.get_assessment_code),
    path('api/get_assessment_city', api_views.get_assessment_city),

    path('api/corporate_package', api_views.corporate_package),

    path('api/service_types', api_views.service_types),
    path('api/train_types', api_views.train_types),
    path('api/bus_types', api_views.bus_types),
    path('api/irctc_accounts', api_views.irctc_accounts),
    path('api/hotel_types', api_views.hotel_types),
    path('api/get_airports', api_views.get_airports),
    path('api/get_nationality', api_views.get_nationality),

    path('api/hotel_booking_portals', api_views.hotel_booking_portals),
    path('api/view_hotel_portal', api_views.view_hotel_portal),
    path('api/add_hotel_portal', api_views.add_hotel_portal),
    path('api/update_hotel_portal', api_views.update_hotel_portal),
    #path('api/delete_hotel_portal', api_views.delete_hotel_portal),

    path('api/room_types', api_views.room_types),
    path('api/railway_stations', api_views.railway_stations),
    path('api/bus_booking_portals', api_views.bus_booking_portals),

    path('api/corporate_management_fee', api_views.corporate_management_fee),
    path('api/add_corporate_management_fee', api_views.add_corporate_management_fee),
    path('api/update_corporate_management_fee', api_views.update_corporate_management_fee),
    path('api/delete_corporate_management_fee', api_views.delete_corporate_management_fee),
    path('api/service_fee_types', api_views.service_fee_types),

    path('api/get_corporate_management_fee', api_views.corporate_management_fees),

    path('api/taxi_types', api_views.taxi_types),
    path('api/add_taxi_type', api_views.add_taxi_type),
    path('api/update_taxi_type', api_views.update_taxi_type),
    path('api/delete_taxi_type', api_views.delete_taxi_type),

    path('api/taxi_models', api_views.taxi_models),
    path('api/add_taxi_model', api_views.add_taxi_model),
    path('api/update_taxi_model', api_views.update_taxi_model),
    path('api/delete_taxi_model', api_views.delete_taxi_model),

    path('api/taxis', api_views.taxis),
    path('api/add_taxi', api_views.add_taxi),
    path('api/update_taxi', api_views.update_taxi),
    path('api/delete_taxi', api_views.delete_taxi),


    path('api/companies', api_views.companies),
    path('api/view_company', api_views.view_company),
    path('api/add_company', api_views.add_companies),
    path('api/update_company', api_views.update_company),
    path('api/delete_company', api_views.delete_company),

    path('api/company_rates', api_views.company_rates),
    path('api/add_company_rates', api_views.add_company_rates),
    path('api/update_company_rates', api_views.update_company_rates),
    path('api/delete_company_rates', api_views.delete_company_rates),
    ##sanket added this
    path('api/taxi_packages', api_views.taxi_packages),

    path('api/billing_entities', api_views.billing_entities),
    path('api/view_billing_entitie', api_views.view_billing_entitie),
    path('api/admins', api_views.admins),
    path('api/groups', api_views.groups),
    path('api/subgroups', api_views.subgroups),
    path('api/spocs', api_views.spocs),
    path('api/employees', api_views.employee),
    path('api/spoc_employee', api_views.spoc_employee),

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

    path('api/view_auth_1', api_views.view_auth_1),
    path('api/view_auth_2', api_views.view_auth_2),

    path('api/add_admin', api_views.add_admin),
    path('api/update_admin', api_views.update_admin),
    path('api/delete_admin', api_views.delete_admin),

    path('api/view_spoc', api_views.view_spoc),
    path('api/add_spoc', api_views.add_spoc),
    path('api/update_spoc', api_views.update_spoc),
    path('api/delete_spoc', api_views.delete_spoc),
    path('api/active_spoc', api_views.active_spoc),

    path('api/view_employee', api_views.view_employee),
    path('api/add_employee', api_views.add_employee),
    path('api/update_employee', api_views.update_employee),
    path('api/delete_employee', api_views.delete_employee),

    path('api/assessment_cities', api_views.assessment_cities),
    path('api/add_assessment_cities', api_views.add_assessment_cities),
    path('api/update_assessment_cities', api_views.update_assessment_cities),
    path('api/delete_assessment_cities', api_views.delete_assessment_cities),

    path('api/assessment_codes', api_views.assessment_codes),
    path('api/add_assessment_codes', api_views.add_assessment_codes),
    path('api/update_assessment_codes', api_views.update_assessment_codes),
    path('api/delete_assessment_codes', api_views.delete_assessment_codes),

    path('api/agents', api_views.get_agents),
    path('api/view_agent', api_views.view_agent),
    path('api/add_agent', api_views.add_agent),
    path('api/update_agent', api_views.update_agent),
    path('api/delete_agent', api_views.delete_agent),
    path('api/activate_agent', api_views.activate_agent),
    path('api/get_operator_package', api_views.get_operator_package),

    ######### TAXI BOOKING API #####################

    path('api/view_taxi_booking', api_views.view_taxi_booking),
    path('api/view_bus_booking', api_views.view_bus_booking),
    path('api/view_train_booking', api_views.view_train_booking),
    path('api/view_hotel_booking', api_views.view_hotel_booking),
    path('api/view_flight_booking', api_views.view_flight_booking),

    path('api/add_taxi_booking', api_views.add_taxi_booking),
    path('api/add_bus_booking', api_views.add_bus_booking),
    path('api/add_train_booking', api_views.add_train_booking),
    path('api/add_hotel_booking', api_views.add_hotel_booking),
    path('api/add_flight_booking', api_views.add_flight_booking),

    ################ MIS API ######################
    path('api/report_taxi_booking', api_views.report_taxi_booking),
    path('api/report_bus_booking', api_views.report_bus_booking),
    path('api/report_train_booking', api_views.report_train_booking),
    path('api/report_flight_booking', api_views.report_flight_booking),
    path('api/report_hotel_booking', api_views.report_hotel_booking),


    path('api/generate_auth_token', api_views.generate_auth_token),
    path('api/get_flight_access_token', api_views.get_flight_access_token),
    path('api/get_flight_search', api_views.get_flight_search),
    path('api/get_flight_fare_search', api_views.get_flight_fare_search),
    path('api/save_flight_booking', api_views.save_flight_booking),
    path('api/get_flight_pnr_details', api_views.get_flight_pnr_details),

    path('api/cancel_flight_booking_passengers', api_views.get_flight_pnr_details),
    path('api/add_flight_booking_with_invoice', api_views.add_flight_booking_with_invoice),


    path('api/get_emp_passport_details', api_views.get_emp_passport_details),
    path('api/get_phr_detail_assign_booking', api_views.get_phr_detail_assign_booking),


]