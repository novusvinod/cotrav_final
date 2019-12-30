from django.urls import path,include
from Common.VIEW.Spoc import spoc_views

urlpatterns = [
    path('Corporate/Spoc/logout', spoc_views.logout_action),
    path('Corporate/Spoc/home', spoc_views.homepage),
    path('Corporate/Spoc/user_profile', spoc_views.user_profile),
    path('Corporate/Spoc/company-billing_entities/<int:id>', spoc_views.company_billing_entities),
    path('Corporate/Spoc/company-rates/<int:id>', spoc_views.company_rates),
    path('Corporate/Spoc/company-groups/<int:id>', spoc_views.company_groups),
    path('Corporate/Spoc/view-company-group/<int:id>', spoc_views.view_company_group),
    path('Corporate/Spoc/company-subgroups/<int:id>', spoc_views.company_subgroups),
    path('Corporate/Spoc/view-company-subgroup/<int:id>', spoc_views.view_company_subgroup),
    path('Corporate/Spoc/company-admins/<int:id>', spoc_views.company_admins),
    path('Corporate/Spoc/company-spocs/<int:id>', spoc_views.company_spocs),
    path('Corporate/Spoc/company-employees/<int:id>', spoc_views.company_employees),

    path('Corporate/Spoc/taxi-bookings/<int:id>', spoc_views.taxi_bookings),
    path('Corporate/Spoc/add-taxi-booking/<int:id>', spoc_views.add_taxi_booking),
    path('Corporate/Spoc/view-taxi-booking/<int:id>', spoc_views.view_taxi_booking),
    path('Corporate/Spoc/reject-taxi-booking/<int:id>', spoc_views.reject_taxi_booking),

    path('Corporate/Spoc/bus-bookings/<int:id>', spoc_views.bus_bookings),
    path('Corporate/Spoc/add-bus-booking/<int:id>', spoc_views.add_bus_booking),
    path('Corporate/Spoc/view-bus-booking/<int:id>', spoc_views.view_bus_booking),
    path('Corporate/Spoc/reject-bus-booking/<int:id>', spoc_views.reject_bus_booking),

    path('Corporate/Spoc/train-bookings/<int:id>', spoc_views.train_bookings),
    path('Corporate/Spoc/add-train-booking/<int:id>', spoc_views.add_train_booking),
    path('Corporate/Spoc/view-train-booking/<int:id>', spoc_views.view_train_booking),
    path('Corporate/Spoc/reject-train-booking/<int:id>', spoc_views.reject_train_booking),

    path('Corporate/Spoc/hotel-bookings/<int:id>', spoc_views.hotel_bookings),
    path('Corporate/Spoc/add-hotel-booking/<int:id>', spoc_views.add_hotel_booking),
    path('Corporate/Spoc/view-hotel-booking/<int:id>', spoc_views.view_hotel_booking),
    path('Corporate/Spoc/reject-hotel-booking/<int:id>', spoc_views.reject_hotel_booking),

    path('Corporate/Spoc/flight-bookings/<int:id>', spoc_views.flight_bookings),
    path('Corporate/Spoc/add-flight-booking/<int:id>', spoc_views.add_flight_booking),
    path('Corporate/Spoc/view-flight-booking/<int:id>', spoc_views.view_flight_booking),
    path('Corporate/Spoc/reject-flight-booking/<int:id>', spoc_views.reject_flight_booking),

    path('Corporate/Spoc/add-flight-booking-self/<int:id>', spoc_views.add_flight_booking_self),
    path('Corporate/Spoc/add-flight-booking-self-conformation/<int:id>', spoc_views.add_flight_booking_self_conformation),
    path('Corporate/Spoc/add-flight-booking-self-final/<int:id>', spoc_views.add_flight_booking_self_final),
    path('Corporate/Spoc/get-api-flight', spoc_views.razor_charge),

    path('Corporate/Spoc/download-taxi-bookings', spoc_views.download_taxi_bookings),
    path('Corporate/Spoc/download-bus-bookings', spoc_views.download_bus_bookings),
    path('Corporate/Spoc/download-train-bookings', spoc_views.download_train_bookings),
    path('Corporate/Spoc/download-flight-bookings', spoc_views.download_flight_bookings),
    path('Corporate/Spoc/download-hotel-bookings', spoc_views.download_hotel_bookings),

    path('Corporate/Spoc/download-billing-entities', spoc_views.download_billing_entities),
    path('Corporate/Spoc/download-employees', spoc_views.download_employees),
    path('Corporate/Spoc/download-spocs', spoc_views.download_spocs),
]