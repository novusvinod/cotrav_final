from django.urls import path,include
from Common.VIEW.Api import admin_api_view

urlpatterns = [
    path('api/admin_taxi_bookings', admin_api_view.admin_taxi_bookings),
    path('api/admin_accept_taxi_booking', admin_api_view.admin_accept_taxi_booking),
    path('api/admin_reject_taxi_booking', admin_api_view.admin_reject_taxi_booking),
]