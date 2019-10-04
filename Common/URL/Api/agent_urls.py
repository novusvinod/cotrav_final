from django.urls import path,include
from Common.VIEW.Api import agent_api_view

urlpatterns = [
    path('api/operators', agent_api_view.operators),
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

]