from django.urls import path,include
from Common.VIEW.Agent import agent_views
from landing.leads_generation import lead_detail_view, leads, lead_update, lead_create, lead_delete, lead_assigned, lead_doc_delete

urlpatterns = [
    #Agent Path
    path('agents/login', agent_views.agent_login_action),
    path('agents/logout', agent_views.agent_logout_action),
    path('agents/agent_home', agent_views.agent_homepage),
    path('agents/user_profile', agent_views.user_profile),
    path('agents/upload', agent_views.upload_file_getpath),
    path('agents/pdf', agent_views.generate_pdf_file),

    path('agents/taxi-types',agent_views.taxi_types),
    path('agents/taxi-models',agent_views.taxi_models),
    path('agents/taxis',agent_views.taxis),

    path('agents/companies', agent_views.companies),
    path('agents/add-company', agent_views.add_company),
    path('agents/edit-company/<int:id>', agent_views.edit_company),
    path('agents/delete-company/<int:id>', agent_views.delete_company),

    path('agents/company-operation-management', agent_views.company_operation_management),
    path('agents/company-relationship-manager', agent_views.company_relationship_manager),

    path('agents/cotrav-billing-entities', agent_views.cotrav_billing_entities),
    path('agents/add-cotrav-billing-entity/<int:id>', agent_views.add_cotrav_billing_entities),

    path('agents/billing_entities/<int:id>', agent_views.company_billing_entities),
    path('agents/rates/<int:id>', agent_views.company_rates),
    path('agents/add-company-rate/<int:id>', agent_views.add_company_rate),
    path('agents/add-company-entity/<int:id>', agent_views.add_company_entity),
    path('agents/company-management-fees', agent_views.company_management_fees),

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

    path('agents/assessment_cities/<int:id>', agent_views.assessment_cities),
    path('agents/delete-assessment_cities/<int:id>', agent_views.delete_assessment_cities),
    path('agents/assessment_codes/<int:id>', agent_views.assessment_codes),
    path('agents/delete-assessment_codes/<int:id>', agent_views.delete_assessment_codes),

    path('agents/agents', agent_views.view_agents),
    path('agents/add-agent/<int:id>', agent_views.add_agent),

    path('agents/hotels', agent_views.hotels),
    path('agents/add-hotel/<int:id>', agent_views.add_hotel),
    path('agents/hotel_contacts/<int:id>', agent_views.hotel_contacts),
    path('agents/hotel_banks/<int:id>', agent_views.hotel_banks),

    path('agents/hotel_booking_portals', agent_views.hotel_booking_portals),
    path('agents/add-hotel-portals/<int:id>', agent_views.add_hotel_portals),

    path('agents/operators', agent_views.operators),
    path('agents/operator_contacts/<int:id>', agent_views.operator_contacts),
    path('agents/operator_banks/<int:id>', agent_views.operator_banks),
    path('agents/add-operator/<int:id>', agent_views.add_operator),
    path('agents/delete-operator/<int:id>', agent_views.delete_operator),

    path('agents/operator-rates', agent_views.operator_rates),
    path('agents/add-operator-rate/<int:id>', agent_views.add_operator_rate),
    path('agents/delete-operator-rate/<int:id>', agent_views.delete_operator_rate),

    path('agents/operator-drivers', agent_views.operator_drivers),
    path('agents/add-operator-driver/<int:id>', agent_views.add_operator_driver),
    path('agents/delete-operator-driver/<int:id>', agent_views.delete_operator_driver),

    path('agents/assign-operator-taxi-booking', agent_views.assign_operator_taxi_boooking),

    path('agents/taxi-bookings/<int:id>', agent_views.taxi_bookings),
    path('agents/add-taxi-booking/<int:id>', agent_views.add_taxi_booking),
    path('agents/view-taxi-booking/<int:id>', agent_views.view_taxi_booking),
    path('agents/accept-taxi-booking', agent_views.accept_taxi_booking),
    path('agents/assign-taxi-booking/<int:id>', agent_views.assign_taxi_booking),
    path('agents/add-taxi-invoice/<int:id>', agent_views.add_taxi_invoice),

    path('agents/bus-bookings/<int:id>', agent_views.bus_bookings),
    path('agents/add-bus-booking/<int:id>', agent_views.add_bus_booking),
    path('agents/view-bus-booking/<int:id>', agent_views.view_bus_booking),
    path('agents/accept-bus-booking', agent_views.accept_bus_booking),
    path('agents/assign-bus-booking/<int:id>', agent_views.assign_bus_booking),

    path('agents/train-bookings/<int:id>', agent_views.train_bookings),
    path('agents/add-train-booking/<int:id>', agent_views.add_train_booking),
    path('agents/view-train-booking/<int:id>', agent_views.view_train_booking),
    path('agents/accept-train-booking', agent_views.accept_train_booking),
    path('agents/assign-train-booking/<int:id>', agent_views.assign_train_booking),

    path('agents/hotel-bookings/<int:id>', agent_views.hotel_bookings),
    path('agents/add-hotel-booking/<int:id>', agent_views.add_hotel_booking),
    path('agents/view-hotel-booking/<int:id>', agent_views.view_hotel_booking),
    path('agents/accept-hotel-booking', agent_views.accept_hotel_booking),
    path('agents/assign-hotel-booking/<int:id>', agent_views.assign_hotel_booking),

    path('agents/flight-bookings/<int:id>', agent_views.flight_bookings),
    path('agents/add-flight-booking/<int:id>', agent_views.add_flight_booking),
    path('agents/view-flight-booking/<int:id>', agent_views.view_flight_booking),
    path('agents/accept-flight-booking', agent_views.accept_flight_booking),
    path('agents/assign-flight-booking/<int:id>', agent_views.assign_flight_booking),

    path('agents/download-taxi-bookings', agent_views.download_taxi_bookings),
    path('agents/download-bus-bookings', agent_views.download_bus_bookings),
    path('agents/download-train-bookings', agent_views.download_train_bookings),
    path('agents/download-flight-bookings', agent_views.download_flight_bookings),
    path('agents/download-hotel-bookings', agent_views.download_hotel_bookings),

    path('agents/lead/', leads, name='lead-list'),
    path('agents/lead-detail/<int:pk>', lead_detail_view, name='lead-detail'),
    path('agents/lead-create/', lead_create, name='lead-create'),
    path('agents/lead-update/<int:pk>', lead_update, name='lead-update'),
    path('agents/lead-delete/<int:pk>', lead_delete, name='lead-delete'),
    path('agents/lead-edit/<int:pk>', lead_update, name='lead_edit'),
    path('agents/lead-assigned', lead_assigned, name='lead_assigned'),

    path('agents/download-billing-entities', agent_views.download_billing_entities),
    path('agents/download-rates', agent_views.download_rates),
    path('agents/download-assessment_cities', agent_views.download_assessment_cities),
    path('agents/download-assessment_codes', agent_views.download_assessment_codes),
    path('agents/download-groups', agent_views.download_groups),
    path('agents/download-subgroups', agent_views.download_subgroups),
    path('agents/download-admins', agent_views.download_admins),
    path('agents/download-spocs', agent_views.download_spocs),
    path('agents/download-employees', agent_views.download_employees),

    path('agents/cancel-flight-booking-passengers/<int:id>', agent_views.cancel_flight_booking_passengers),

    path('agents/taxi-billing/<int:id>', agent_views.taxi_billing, name='agent-taxi-billing'),
    path('agents/bus-billing/<int:id>', agent_views.bus_billing, name='agent-bus-billing'),
    path('agents/train-billing/<int:id>', agent_views.train_billing, name='agent-train-billing'),
    path('agents/flight-billing/<int:id>', agent_views.flight_billing, name='agent-flight-billing'),
    path('agents/hotel-billing/<int:id>', agent_views.hotel_billing, name='agent-hotel-billing'),

    path('agents/taxi-billing/verify', agent_views.taxi_billing_verify, name='agent-taxi-billing-verify'),
    path('agents/bus-billing/verify', agent_views.bus_billing_verify, name='agent-bus-billing-verify'),
    path('agents/train-billing/verify', agent_views.train_billing_verify, name='agent-train-billing-verify'),
    path('agents/flight-billing/verify', agent_views.flight_billing_verify, name='agent-flight-billing-verify'),
    path('agents/hotel-billing/verify', agent_views.hotel_billing_verify, name='agent-hotel-billing-verify'),

    path('agents/lead-doc-delete/<int:pk>', lead_doc_delete, name='lead-doc-delete'),
    
    path('agents/bill-create', agent_views.bill_create),
    path('agents/bill-create-nontax-invoice', agent_views.bill_create_nontax_invoice),
    path('agents/bill-nontax-invoice/<int:id>', agent_views.get_all_generated_bills),
    path('agents/bill-tax-invoice', agent_views.hotel_billing),
    path('agents/bill-offline', agent_views.hotel_billing),
    path('agents/bill-report', agent_views.hotel_billing),

]