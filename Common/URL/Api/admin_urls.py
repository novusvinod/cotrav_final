from django.urls import path,include
from Common.VIEW.Api import admin_api_view

urlpatterns = [
    path('api/admin_taxi_bookings', admin_api_view.admin_taxi_bookings),
    path('api/admin_accept_taxi_booking', admin_api_view.admin_accept_taxi_booking),
    path('api/admin_reject_taxi_booking', admin_api_view.admin_reject_taxi_booking),

    path('api/admin_bus_bookings', admin_api_view.admin_bus_bookings),
    path('api/admin_accept_bus_booking', admin_api_view.admin_accept_bus_booking),
    path('api/admin_reject_bus_booking', admin_api_view.admin_reject_bus_booking),

    path('api/admin_train_bookings', admin_api_view.admin_train_bookings),
    path('api/admin_accept_train_booking', admin_api_view.admin_accept_train_booking),
    path('api/admin_reject_train_booking', admin_api_view.admin_reject_train_booking),

    path('api/admin_hotel_bookings', admin_api_view.admin_hotel_bookings),
    path('api/admin_accept_hotel_booking', admin_api_view.admin_accept_hotel_booking),
    path('api/admin_reject_hotel_booking', admin_api_view.admin_reject_hotel_booking),

    path('api/admin_flight_bookings', admin_api_view.admin_flight_bookings),
    path('api/admin_accept_flight_booking', admin_api_view.admin_accept_flight_booking),
    path('api/admin_reject_flight_booking', admin_api_view.admin_reject_flight_booking),

    path('api/admin_verify_taxi_bookings', admin_api_view.admin_verify_taxi_bookings),
    path('api/admin_revise_taxi_bookings', admin_api_view.admin_revise_taxi_bookings),
    path('api/admin_verify_bus_bookings', admin_api_view.admin_verify_bus_bookings),
    path('api/admin_revise_bus_bookings', admin_api_view.admin_revise_bus_bookings),
    path('api/admin_verify_train_bookings', admin_api_view.admin_verify_train_bookings),
    path('api/admin_revise_train_bookings', admin_api_view.admin_revise_train_bookings),
    path('api/admin_verify_hotel_bookings', admin_api_view.admin_verify_hotel_bookings),
    path('api/admin_revise_hotel_bookings', admin_api_view.admin_revise_hotel_bookings),
    path('api/admin_verify_flight_bookings', admin_api_view.admin_verify_flight_bookings),
    path('api/admin_revise_flight_bookings', admin_api_view.admin_revise_flight_bookings),

]