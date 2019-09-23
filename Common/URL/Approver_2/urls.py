from django.urls import path,include
from Common.VIEW.Approver_2 import approver_2_views

urlpatterns = [
    path('Corporate/Approver_2/home', approver_2_views.homepage),
    path('Corporate/Approver_2/company-billing_entities/<int:id>', approver_2_views.company_billing_entities),
    path('Corporate/Approver_2/company-rates/<int:id>', approver_2_views.company_rates),
    path('Corporate/Approver_2/company-groups/<int:id>', approver_2_views.company_groups),
    path('Corporate/Approver_2/view-company-group/<int:id>', approver_2_views.view_company_group),
    path('Corporate/Approver_2/company-subgroups/<int:id>', approver_2_views.company_subgroups),
    path('Corporate/Approver_2/view-company-subgroup/<int:id>', approver_2_views.view_company_subgroup),
    path('Corporate/Approver_2/company-admins/<int:id>', approver_2_views.company_admins),
    path('Corporate/Approver_2/company-spocs/<int:id>', approver_2_views.company_spocs),
    path('Corporate/Approver_2/company-employees/<int:id>', approver_2_views.company_employees),

    path('Corporate/Approver_2/taxi-bookings/<int:id>', approver_2_views.taxi_bookings),
    path('Corporate/Approver_2/view-taxi-booking/<int:id>', approver_2_views.view_taxi_booking),
    path('Corporate/Approver_2/accept-taxi-booking/<int:id>', approver_2_views.accept_taxi_booking),
    path('Corporate/Approver_2/reject-taxi-booking/<int:id>', approver_2_views.reject_taxi_booking),

    path('Corporate/Approver_2/bus-bookings/<int:id>', approver_2_views.bus_bookings),
    path('Corporate/Approver_2/view-bus-booking/<int:id>', approver_2_views.view_bus_booking),
    path('Corporate/Approver_2/accept-bus-booking/<int:id>', approver_2_views.accept_bus_booking),
    path('Corporate/Approver_2/reject-bus-booking/<int:id>', approver_2_views.reject_bus_booking),

    path('Corporate/Approver_2/train-bookings/<int:id>', approver_2_views.train_bookings),
    path('Corporate/Approver_2/view-train-booking/<int:id>', approver_2_views.view_train_booking),
    path('Corporate/Approver_2/accept-train-booking/<int:id>', approver_2_views.accept_train_booking),
    path('Corporate/Approver_2/reject-train-booking/<int:id>', approver_2_views.reject_train_booking),

    path('Corporate/Approver_2/hotel-bookings/<int:id>', approver_2_views.hotel_bookings),
    path('Corporate/Approver_2/view-hotel-booking/<int:id>', approver_2_views.view_hotel_booking),
    path('Corporate/Approver_2/accept-hotel-booking/<int:id>', approver_2_views.accept_hotel_booking),
    path('Corporate/Approver_2/reject-hotel-booking/<int:id>', approver_2_views.reject_hotel_booking),

    path('Corporate/Approver_2/flight-bookings/<int:id>', approver_2_views.flight_bookings),
    path('Corporate/Approver_2/view-flight-booking/<int:id>', approver_2_views.view_flight_booking),
    path('Corporate/Approver_2/accept-flight-booking/<int:id>', approver_2_views.accept_flight_booking),
    path('Corporate/Approver_2/reject-flight-booking/<int:id>', approver_2_views.reject_flight_booking),
]