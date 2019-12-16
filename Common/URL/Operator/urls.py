from django.urls import path,include
from Common.VIEW.Operator import operator_view

urlpatterns = [
    #Agent Path
    path('operator/login', operator_view.operator_login_action),
    path('operator/logout', operator_view.operator_logout_action),
    path('operator/operator_home', operator_view.operator_homepage),
    path('operator/user_profile', operator_view.user_profile),

    path('operator/operator-contacts/<int:id>', operator_view.operator_contacts),
    path('operator/operator-banks/<int:id>', operator_view.operator_banks),
    path('operator/operator-rates/<int:id>', operator_view.operator_rates),

    path('operator/operator-drivers/<int:id>', operator_view.operator_drivers),
    path('operator/add-operator-driver/<int:id>', operator_view.add_operator_driver),
    path('operator/delete-operator-driver/<int:id>', operator_view.delete_operator_driver),

    path('operator/taxi-bookings/<int:id>', operator_view.taxi_bookings),
    path('operator/reject-taxi-booking/<int:id>', operator_view.reject_taxi_booking),
    path('operator/view-taxi-booking/<int:id>', operator_view.view_taxi_booking),

    path('operator/bus-bookings/<int:id>', operator_view.bus_bookings),
    path('operator/view-bus-booking/<int:id>', operator_view.view_bus_booking),

    path('operator/train-bookings/<int:id>', operator_view.train_bookings),
    path('operator/view-train-booking/<int:id>', operator_view.view_train_booking),

    path('operator/hotel-bookings/<int:id>', operator_view.hotel_bookings),
    path('operator/view-hotel-booking/<int:id>', operator_view.view_hotel_booking),

    path('operator/flight-bookings/<int:id>', operator_view.flight_bookings),
    path('operator/view-flight-booking/<int:id>', operator_view.view_flight_booking),

    path('operator/download-taxi-bookings', operator_view.download_taxi_bookings),
    path('operator/download-bus-bookings', operator_view.download_bus_bookings),
    path('operator/download-train-bookings', operator_view.download_train_bookings),
    path('operator/download-flight-bookings', operator_view.download_flight_bookings),
    path('operator/download-hotel-bookings', operator_view.download_hotel_bookings),
]