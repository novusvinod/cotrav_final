from django.urls import path,include
from Common.VIEW.Api import employee_api_view

urlpatterns = [
    path('api/employee_taxi_bookings', employee_api_view.employee_taxi_bookings),
    path('api/employee_add_taxi_booking', employee_api_view.employee_add_taxi_booking),

    path('api/employee_bus_bookings', employee_api_view.employee_bus_bookings),
    path('api/employee_add_bus_booking', employee_api_view.employee_add_bus_booking),
]