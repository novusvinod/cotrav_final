from django.urls import path,include
from Common.VIEW.Api import spoc_api_view

urlpatterns = [
    path('api/spoc_taxi_bookings', spoc_api_view.spoc_taxi_bookings),
    path('api/spoc_bus_bookings', spoc_api_view.spoc_bus_bookings),
    path('api/spoc_train_bookings', spoc_api_view.spoc_train_bookings),
]