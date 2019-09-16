from django.urls import path,include
from Common.VIEW.Api import approver_2_api_view

urlpatterns = [
    path('api/approver_2_taxi_bookings', approver_2_api_view.approver_2_taxi_bookings),
    path('api/approver_2_accept_taxi_booking', approver_2_api_view.approver_2_accept_taxi_booking),
    path('api/approver_2_reject_taxi_booking', approver_2_api_view.approver_2_reject_taxi_booking),

    path('api/approver_2_bus_bookings', approver_2_api_view.approver_2_bus_bookings),
    path('api/approver_2_accept_bus_booking', approver_2_api_view.approver_2_accept_bus_booking),
    path('api/approver_2_reject_bus_booking', approver_2_api_view.approver_2_reject_bus_booking),

    path('api/approver_2_train_bookings', approver_2_api_view.approver_2_train_bookings),
    path('api/approver_2_accept_train_booking', approver_2_api_view.approver_2_accept_train_booking),
    path('api/approver_2_reject_train_booking', approver_2_api_view.approver_2_reject_train_booking),


]