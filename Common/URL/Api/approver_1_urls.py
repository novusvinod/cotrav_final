from django.urls import path,include
from Common.VIEW.Api import approver_1_api_view

urlpatterns = [
    path('api/approver_1_taxi_bookings', approver_1_api_view.approver_1_taxi_bookings),
    path('api/approver_1_accept_taxi_booking', approver_1_api_view.approver_1_accept_taxi_booking),
    path('api/approver_1_reject_taxi_booking', approver_1_api_view.approver_1_reject_taxi_booking),

    path('api/approver_1_bus_bookings', approver_1_api_view.approver_1_bus_bookings),
    path('api/approver_1_accept_bus_booking', approver_1_api_view.approver_1_accept_bus_booking),
    path('api/approver_1_reject_bus_booking', approver_1_api_view.approver_1_reject_bus_booking),
]