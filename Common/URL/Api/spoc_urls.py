from django.urls import path,include
from Common.VIEW.Api import spoc_api_view

urlpatterns = [
    path('api/spoc_taxi_bookings', spoc_api_view.spoc_taxi_bookings),
    path('api/spoc_add_taxi_booking', spoc_api_view.spoc_add_taxi_booking),

]