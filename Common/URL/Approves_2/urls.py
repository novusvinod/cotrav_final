from django.urls import path,include
from Common.VIEW.Approves_2 import approves_2_views

urlpatterns = [
    path('Corporate/Approver_2/home', approves_2_views.homepage),
    path('Corporate/Approver_2/company-billing_entities/<int:id>', approves_2_views.company_billing_entities),
    path('Corporate/Approver_2/company-rates/<int:id>', approves_2_views.company_rates),
    path('Corporate/Approver_2/company-groups/<int:id>', approves_2_views.company_groups),
    path('Corporate/Approver_2/view-company-group/<int:id>', approves_2_views.view_company_group),
    path('Corporate/Approver_2/company-subgroups/<int:id>', approves_2_views.company_subgroups),
    path('Corporate/Approver_2/view-company-subgroup/<int:id>', approves_2_views.view_company_subgroup),
    path('Corporate/Approver_2/company-admins/<int:id>', approves_2_views.company_admins),
    path('Corporate/Approver_2/company-spocs/<int:id>', approves_2_views.company_spocs),
    path('Corporate/Approver_2/company-employees/<int:id>', approves_2_views.company_employees),

    path('Corporate/Approver_2/taxi-bookings/<int:id>', approves_2_views.taxi_bookings),
    path('Corporate/Approver_2/view-taxi-booking/<int:id>', approves_2_views.view_taxi_booking),
    path('Corporate/Approver_2/accept-taxi-booking/<int:id>', approves_2_views.accept_taxi_booking),
    path('Corporate/Approver_2/reject-taxi-booking/<int:id>', approves_2_views.reject_taxi_booking),

    path('Corporate/Approver_2/bus-bookings/<int:id>', approves_2_views.bus_bookings),
    path('Corporate/Approver_2/view-bus-booking/<int:id>', approves_2_views.view_bus_booking),
    path('Corporate/Approver_2/accept-bus-booking/<int:id>', approves_2_views.accept_bus_booking),
    path('Corporate/Approver_2/reject-bus-booking/<int:id>', approves_2_views.reject_bus_booking),
]