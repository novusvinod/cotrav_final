from django.urls import path,include
from Common.VIEW.Employee import employee_views

urlpatterns = [
    path('Corporate/Employee/home', employee_views.homepage),
    path('Corporate/Employee/company-billing_entities/<int:id>', employee_views.company_billing_entities),
    path('Corporate/Employee/company-rates/<int:id>', employee_views.company_rates),
    path('Corporate/Employee/company-groups/<int:id>', employee_views.company_groups),
    path('Corporate/Employee/view-company-group/<int:id>', employee_views.view_company_group),
    path('Corporate/Employee/company-subgroups/<int:id>', employee_views.company_subgroups),
    path('Corporate/Employee/view-company-subgroup/<int:id>', employee_views.view_company_subgroup),
    path('Corporate/Employee/company-admins/<int:id>', employee_views.company_admins),
    path('Corporate/Employee/company-spocs/<int:id>', employee_views.company_spocs),
    path('Corporate/Employee/company-employees/<int:id>', employee_views.company_employees),

    path('Corporate/Employee/taxi-bookings/<int:id>', employee_views.taxi_bookings),
    path('Corporate/Employee/add-taxi-booking/<int:id>', employee_views.add_taxi_booking),
    path('Corporate/Employee/view-taxi-booking/<int:id>', employee_views.view_taxi_booking),

]