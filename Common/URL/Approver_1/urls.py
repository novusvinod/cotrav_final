from django.urls import path,include
from Common.VIEW.Approver_1 import approver_1_views

urlpatterns = [
    path('Corporate/Approver_1/home', approver_1_views.homepage),
    path('Corporate/Approver_1/company-billing_entities/<int:id>', approver_1_views.company_billing_entities),
    path('Corporate/Approver_1/company-rates/<int:id>', approver_1_views.company_rates),
    path('Corporate/Approver_1/company-groups/<int:id>', approver_1_views.company_groups),
    path('Corporate/Approver_1/view-company-group/<int:id>', approver_1_views.view_company_group),
    path('Corporate/Approver_1/company-subgroup/<int:id>', approver_1_views.company_subgroups),
    path('Corporate/Approver_1/view-company-subgroup/<int:id>', approver_1_views.view_company_subgroup),
    path('Corporate/Approver_1/company-admins/<int:id>', approver_1_views.company_admins),
    path('Corporate/Approver_1/company-spocs/<int:id>', approver_1_views.company_spocs),
    path('Corporate/Approver_1/company-employees/<int:id>', approver_1_views.company_employees),

    path('Corporate/Approver_1/taxi-bookings/<int:id>', approver_1_views.taxi_bookings),
    path('Corporate/Approver_1/view-taxi-booking/<int:id>', approver_1_views.view_taxi_booking),
    path('Corporate/Approver_1/accept-taxi-booking/<int:id>', approver_1_views.accept_taxi_booking),
    path('Corporate/Approver_1/reject-taxi-booking/<int:id>', approver_1_views.reject_taxi_booking),

    path('Corporate/Approver_1/bus-bookings/<int:id>', approver_1_views.bus_bookings),
    path('Corporate/Approver_1/view-bus-booking/<int:id>', approver_1_views.view_bus_booking),
    path('Corporate/Approver_1/accept-bus-booking/<int:id>', approver_1_views.accept_bus_booking),
    path('Corporate/Approver_1/reject-bus-booking/<int:id>', approver_1_views.reject_bus_booking),
]