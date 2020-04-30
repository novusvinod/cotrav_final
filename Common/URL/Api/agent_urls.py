from django.urls import path,include
from Common.VIEW.Api import agent_api_view

urlpatterns = [
    path('api/view_hotel', agent_api_view.view_hotel),

    path('api/hotels', agent_api_view.hotels),
    path('api/hotel_contacts', agent_api_view.hotel_contacts),
    path('api/hotel_banks', agent_api_view.hotel_banks),

    path('api/add_hotel', agent_api_view.add_hotel),
    path('api/add_hotel_contact', agent_api_view.add_hotel_contact),
    path('api/add_hotel_bank', agent_api_view.add_hotel_bank),

    path('api/update_hotel', agent_api_view.update_hotel),
    path('api/update_hotel_contact', agent_api_view.update_hotel_contact),
    path('api/update_hotel_bank', agent_api_view.update_hotel_bank),

    path('api/delete_hotel', agent_api_view.delete_hotel),
    path('api/delete_hotel_contact', agent_api_view.delete_hotel_contact),
    path('api/delete_hotel_bank', agent_api_view.delete_hotel_bank),

    path('api/operators', agent_api_view.operators),
    path('api/get_operators_by_service_type', agent_api_view.operators_by_service_type),
    path('api/operator_contacts', agent_api_view.operator_contacts),
    path('api/operator_banks', agent_api_view.operator_banks),
    path('api/view_operator', agent_api_view.view_operator),

    path('api/add_operator', agent_api_view.add_operator),
    path('api/add_operator_contact', agent_api_view.add_operator_contact),
    path('api/add_operator_bank', agent_api_view.add_operator_bank),

    path('api/update_operator', agent_api_view.update_operator),
    path('api/update_operator_contact', agent_api_view.update_operator_contact),
    path('api/update_operator_bank', agent_api_view.update_operator_bank),

    path('api/delete_operator', agent_api_view.delete_operator),
    path('api/delete_operator_contact', agent_api_view.delete_operator_contact),
    path('api/delete_operator_bank', agent_api_view.delete_operator_bank),

    path('api/operator_rates', agent_api_view.operator_rates),
    path('api/view_operator_rate', agent_api_view.view_operator_rate),
    path('api/add_operator_rate', agent_api_view.add_operator_rate),
    path('api/update_operator_rate', agent_api_view.update_operator_rate),
    path('api/delete_operator_rate', agent_api_view.delete_operator_rate),

    path('api/operator_drivers', agent_api_view.operator_drivers),
    path('api/view_operator_driver', agent_api_view.view_operator_driver),
    path('api/add_operator_driver', agent_api_view.add_operator_driver),
    path('api/update_operator_driver', agent_api_view.update_operator_driver),
    path('api/delete_operator_driver', agent_api_view.delete_operator_driver),

    path('api/operation_managements', agent_api_view.operation_managements),
    path('api/relationship_managements', agent_api_view.relationship_managements),
    path('api/add_operation_managements', agent_api_view.add_operation_managements),
    path('api/add_relationship_managements', agent_api_view.add_relationship_managements),
    path('api/update_operation_managements', agent_api_view.update_operation_managements),
    path('api/update_relationship_managements', agent_api_view.update_relationship_managements),

    path('api/agent_taxi_bookings', agent_api_view.agent_taxi_bookings),
    path('api/agent_add_taxi_booking', agent_api_view.agent_add_taxi_booking),
    path('api/accept_taxi_booking', agent_api_view.accept_taxi_booking),
    path('api/reject_taxi_booking', agent_api_view.reject_taxi_booking),
    path('api/assign_taxi_booking', agent_api_view.assign_taxi_booking),

    path('api/add_new_dutyslip', agent_api_view.add_new_dutyslip),
    path('api/add_taxi_invoice', agent_api_view.add_taxi_invoice),
    path('api/assign_operator_taxi_boooking', agent_api_view.assign_operator_taxi_boooking),
    path('api/add_booking_tracking_status', agent_api_view.add_booking_tracking_status),
    path('api/add_booking_assign_to_agent', agent_api_view.add_booking_assign_to_agent),
    path('api/change_booking_status', agent_api_view.change_booking_status),

    path('api/agent_bus_bookings', agent_api_view.agent_bus_bookings),
    path('api/accept_bus_booking', agent_api_view.accept_bus_booking),
    path('api/reject_bus_booking', agent_api_view.reject_bus_booking),
    path('api/assign_bus_booking', agent_api_view.assign_bus_booking),

    path('api/agent_train_bookings', agent_api_view.agent_train_bookings),
    path('api/accept_train_booking', agent_api_view.accept_train_booking),
    path('api/reject_train_booking', agent_api_view.reject_train_booking),
    path('api/assign_train_booking', agent_api_view.assign_train_booking),

    path('api/agent_hotel_bookings', agent_api_view.agent_hotel_bookings),
    path('api/accept_hotel_booking', agent_api_view.accept_hotel_booking),
    path('api/reject_hotel_booking', agent_api_view.reject_hotel_booking),
    path('api/assign_hotel_booking', agent_api_view.assign_hotel_booking),

    path('api/agent_flight_bookings', agent_api_view.agent_flight_bookings),
    path('api/accept_flight_booking', agent_api_view.accept_flight_booking),
    path('api/reject_flight_booking', agent_api_view.reject_flight_booking),
    path('api/assign_flight_booking', agent_api_view.assign_flight_booking),

    path('api/get_city_id', agent_api_view.get_city_id),
    path('api/cancel_flight_booking_passengers', agent_api_view.cancel_flight_booking_passengers),

    path('api/agent_verify_taxi_bookings', agent_api_view.agent_verify_taxi_bookings),
    path('api/agent_revise_taxi_bookings', agent_api_view.agent_revise_taxi_bookings),
    path('api/agent_verify_bus_bookings', agent_api_view.agent_verify_bus_bookings),
    path('api/agent_revise_bus_bookings', agent_api_view.agent_revise_bus_bookings),
    path('api/agent_verify_train_bookings', agent_api_view.agent_verify_train_bookings),
    path('api/agent_revise_train_bookings', agent_api_view.agent_revise_train_bookings),
    path('api/agent_verify_hotel_bookings', agent_api_view.agent_verify_hotel_bookings),
    path('api/agent_revise_hotel_bookings', agent_api_view.agent_revise_hotel_bookings),
    path('api/agent_verify_flight_bookings', agent_api_view.agent_verify_flight_bookings),
    path('api/agent_revise_flight_bookings', agent_api_view.agent_revise_flight_bookings),

    path('api/agent_update_taxi_bookings', agent_api_view.agent_update_taxi_bookings),
    path('api/agent_update_bus_bookings', agent_api_view.agent_update_bus_bookings),
    path('api/agent_update_train_bookings', agent_api_view.agent_update_train_bookings),
    path('api/agent_update_hotel_bookings', agent_api_view.agent_update_hotel_bookings),
    path('api/agent_update_flight_bookings', agent_api_view.agent_update_flight_bookings),

    path('api/dashboard_sales_by_month', agent_api_view.dashboard_sales_by_month),
    path('api/dashboard_bookings_by_month', agent_api_view.dashboard_bookings_by_month),
    path('api/dashboard_sales_for_six_months', agent_api_view.dashboard_sales_for_six_months),
    path('api/dashboard_bookings_for_six_months', agent_api_view.dashboard_bookings_for_six_months),
    path('api/dashboard_sales_by_city', agent_api_view.dashboard_sales_by_city),
    path('api/dashboard_sales_by_city_for_month', agent_api_view.dashboard_sales_by_city_for_month),
    path('api/dashboard_taxable_amount_table', agent_api_view.dashboard_taxable_amount_table),
    path('api/dashboard_hotel_bookings_summery', agent_api_view.dashboard_hotel_bookings_summery),

    path('api/get_all_bills', agent_api_view.get_all_bills),
    path('api/get_all_generated_bills', agent_api_view.get_all_generated_bills),
    path('api/bill_create_nontax_invoice', agent_api_view.bill_create_nontax_invoice),
    path('api/bill_create_final_invoice', agent_api_view.bill_create_final_invoice),
    path('api/get_all_bill_payment_status', agent_api_view.get_all_bill_payment_status),

    path('api/get_corporate_podetails', agent_api_view.get_corporate_podetails),
    path('api/add_podetails', agent_api_view.add_podetails),
    path('api/update_podetails', agent_api_view.update_podetails),
    path('api/delete_podetails', agent_api_view.delete_podetails),

    path('api/get_corporate_accounts', agent_api_view.get_corporate_accounts),
    path('api/add_corporate_account', agent_api_view.add_corporate_account),
    path('api/update_corporate_account', agent_api_view.update_corporate_account),
    path('api/delete_corporate_account', agent_api_view.delete_corporate_account),

    path('api/get_cotrav_accounts', agent_api_view.get_cotrav_accounts),
    path('api/add_cotrav_account', agent_api_view.add_cotrav_account),
    path('api/update_cotrav_account', agent_api_view.update_cotrav_account),
    path('api/delete_cotrav_account', agent_api_view.delete_cotrav_account),

    path('api/accept_bill', agent_api_view.accept_bill),
    path('api/reject_bill', agent_api_view.reject_bill),
    path('api/view_bill', agent_api_view.view_bill),
    path('api/update_bill', agent_api_view.update_bill),

    path('api/pay_bill', agent_api_view.pay_bill),
    path('api/report_invoice', agent_api_view.report_invoice),
    path('api/report_client_bills', agent_api_view.report_client_bills),

    path('api/dashboard_search_bookings', agent_api_view.dashboard_search_bookings),
    path('api/softdeleated_operators', agent_api_view.softdeleated_operators),
    path('api/softdeleated_companies', agent_api_view.softdeleated_companies),
    path('api/softdeleated_taxi', agent_api_view.softdeleated_taxies),
    path('api/softdeleated_update', agent_api_view.update_softdeleated),
    path('api/master-select', agent_api_view.master_select_record),
    path('api/master-add', agent_api_view.master_add_record),
    path('api/master-update', agent_api_view.master_update_record),
    
    path('api/update-passanger', agent_api_view.update_passanger_for_booking),
    path('api/upload_new_ticket', agent_api_view.upload_new_ticket),

    path('api/get_visa_services', agent_api_view.get_visa_services),
    path('api/get_all_cotrav_visa_requests', agent_api_view.get_all_cotrav_visa_requests),

]