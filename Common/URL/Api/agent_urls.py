from django.urls import path,include
from Common.VIEW.Api import agent_api_view

urlpatterns = [
    path('api/operators', agent_api_view.operators),
    path('api/view_operator', agent_api_view.view_operator),
    path('api/add_operator', agent_api_view.add_operator),
    path('api/update_operator', agent_api_view.update_operator),
    path('api/delete_operator', agent_api_view.delete_operator),

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


    path('api/agent_taxi_bookings', agent_api_view.spoc_taxi_bookings),
    path('api/agent_add_taxi_booking', agent_api_view.spoc_add_taxi_booking),
    path('api/accept_taxi_booking', agent_api_view.accept_taxi_booking),
    path('api/reject_taxi_booking', agent_api_view.reject_taxi_booking),
    path('api/assign_taxi_booking', agent_api_view.assign_taxi_booking),



]