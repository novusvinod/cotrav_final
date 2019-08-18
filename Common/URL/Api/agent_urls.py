from django.urls import path,include
from Common.VIEW.Api import agent_api_view

urlpatterns = [
    path('api/operators', agent_api_view.operators),
    path('api/add_operator', agent_api_view.add_operator),
    path('api/update_operator', agent_api_view.update_operator),
    path('api/delete_operator', agent_api_view.delete_operator),

    path('api/agent_taxi_bookings', agent_api_view.spoc_taxi_bookings),
    path('api/agent_add_taxi_booking', agent_api_view.spoc_add_taxi_booking),
]