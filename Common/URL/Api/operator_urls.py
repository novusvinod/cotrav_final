from django.urls import path,include
from Common.VIEW.Api import operator_api_view

urlpatterns = [
    path('api/operator_taxi_bookings', operator_api_view.operator_taxi_bookings),
    path('api/operator_bus_bookings', operator_api_view.operator_bus_bookings),
    path('api/operator_train_bookings', operator_api_view.operator_train_bookings),
    path('api/operator_hotel_bookings', operator_api_view.operator_hotel_bookings),
    path('api/operator_flight_bookings', operator_api_view.operator_flight_bookings),

    path('api/operator_reject_taxi_booking', operator_api_view.operator_reject_taxi_bookings),

    path('api/driver_taxi_bookings', operator_api_view.driver_taxi_bookings),

    path('api/started_from_garage', operator_api_view.started_from_garage),
    path('api/arrived_at_pickup', operator_api_view.arrived_at_pickup),
    path('api/started_from_pickup', operator_api_view.started_from_pickup),
    path('api/arrived_at_drop', operator_api_view.arrived_at_drop),

]