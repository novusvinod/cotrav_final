from django.urls import path,include
from Common.VIEW.Api import operator_api_view

urlpatterns = [
    path('api/operator_taxi_bookings', operator_api_view.operator_taxi_bookings),
    path('api/operator_bus_bookings', operator_api_view.operator_bus_bookings),
    path('api/operator_train_bookings', operator_api_view.operator_train_bookings),
    path('api/operator_hotel_bookings', operator_api_view.operator_hotel_bookings),
    path('api/operator_flight_bookings', operator_api_view.operator_flight_bookings),

    path('api/operator_reject_taxi_booking', operator_api_view.operator_reject_taxi_bookings),

]