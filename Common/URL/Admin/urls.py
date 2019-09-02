from django.urls import path,include
from Common.VIEW.Admin import admin_views

urlpatterns = [
    path('Corporate/Admin/home', admin_views.homepage),
    path('Corporate/Admin/company-billing_entities/<int:id>', admin_views.company_billing_entities),
    path('Corporate/Admin/company-rates/<int:id>', admin_views.company_rates),

    path('Corporate/Admin/add-company-rate/<int:id>', admin_views.add_company_rate),
    path('Corporate/Admin/add-company-entity/<int:id>', admin_views.add_company_entity),

    path('Corporate/Admin/company-groups/<int:id>', admin_views.company_groups),
    path('Corporate/Admin/view-company-group/<int:id>', admin_views.view_company_group),
    path('Corporate/Admin/add-company-group/<int:id>', admin_views.add_company_group),
    path('Corporate/Admin/update-company-group/<int:id>', admin_views.update_company_group),
    path('Corporate/Admin/delete-company-group/<int:id>', admin_views.delete_company_group),
    path('Corporate/Admin/add-company-group-auth/<int:id>', admin_views.add_company_group_auth),

    path('Corporate/Admin/company-subgroups/<int:id>', admin_views.company_subgroups),
    path('Corporate/Admin/view-company-subgroup/<int:id>', admin_views.view_company_subgroup),
    path('Corporate/Admin/add-company-subgroup/<int:id>', admin_views.add_company_subgroup),
    path('Corporate/Admin/update-company-subgroup/<int:id>', admin_views.update_company_subgroup),
    path('Corporate/Admin/delete-company-subgroup/<int:id>', admin_views.delete_company_subgroup),
    path('Corporate/Admin/add-company-subgroup-auth/<int:id>', admin_views.add_company_subgroup_auth),

    path('Corporate/Admin/company-admins/<int:id>', admin_views.company_admins),
    path('add-company-admins/<int:id>', admin_views.add_company_admins),

    path('Corporate/Admin/company-admins/<int:id>', admin_views.company_spocs),
    path('Corporate/Admin/add-spoc/<int:id>', admin_views.add_spocs),

    path('Corporate/Admin/company-employees/<int:id>', admin_views.company_employees),
    path('Corporate/Admin/add-employee/<int:id>', admin_views.add_employee),

    path('Corporate/Admin/taxi-bookings/<int:id>', admin_views.taxi_bookings),
    path('Corporate/Admin/view-taxi-booking/<int:id>', admin_views.view_taxi_booking),
    path('Corporate/Admin/accept-taxi-booking/<int:id>', admin_views.accept_taxi_booking),
    path('Corporate/Admin/reject-taxi-booking/<int:id>', admin_views.reject_taxi_booking),

    path('Corporate/Admin/bus-bookings/<int:id>', admin_views.bus_bookings),
    path('Corporate/Admin/view-bus-booking/<int:id>', admin_views.view_bus_booking),
    path('Corporate/Admin/accept-bus-booking/<int:id>', admin_views.accept_bus_booking),
    path('Corporate/Admin/reject-bus-booking/<int:id>', admin_views.reject_bus_booking),
]