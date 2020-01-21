from django.urls import path,include
from Common.VIEW.Api import spoc_api_view

urlpatterns = [
    path('api/spoc_taxi_bookings', spoc_api_view.spoc_taxi_bookings),
    path('api/spoc_bus_bookings', spoc_api_view.spoc_bus_bookings),
    path('api/spoc_train_bookings', spoc_api_view.spoc_train_bookings),
    path('api/spoc_hotel_bookings', spoc_api_view.spoc_hotel_bookings),
    path('api/spoc_flight_bookings', spoc_api_view.spoc_flight_bookings),

    path('api/spoc_reject_taxi_booking', spoc_api_view.spoc_reject_taxi_bookings),
    path('api/spoc_reject_bus_booking', spoc_api_view.spoc_reject_bus_bookings),
    path('api/spoc_reject_train_booking', spoc_api_view.spoc_reject_train_bookings),
    path('api/spoc_reject_hotel_booking', spoc_api_view.spoc_reject_hotel_bookings),
    path('api/spoc_reject_flight_booking', spoc_api_view.spoc_reject_flight_bookings),

    path('api/spoc_verify_taxi_bookings', spoc_api_view.spoc_verify_taxi_bookings),
    path('api/spoc_revise_taxi_bookings', spoc_api_view.spoc_revise_taxi_bookings),
    path('api/spoc_verify_bus_bookings', spoc_api_view.spoc_verify_bus_bookings),
    path('api/spoc_revise_bus_bookings', spoc_api_view.spoc_revise_bus_bookings),
    path('api/spoc_verify_train_bookings', spoc_api_view.spoc_verify_train_bookings),
    path('api/spoc_revise_train_bookings', spoc_api_view.spoc_revise_train_bookings),
    path('api/spoc_verify_hotel_bookings', spoc_api_view.spoc_verify_hotel_bookings),
    path('api/spoc_revise_hotel_bookings', spoc_api_view.spoc_revise_hotel_bookings),
    path('api/spoc_verify_flight_bookings', spoc_api_view.spoc_verify_flight_bookings),
    path('api/spoc_revise_flight_bookings', spoc_api_view.spoc_revise_flight_bookings),

]