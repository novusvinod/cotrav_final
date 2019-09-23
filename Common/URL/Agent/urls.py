from django.urls import path,include
from Common.VIEW.Agent import agent_views

urlpatterns = [
    #Agent Path
    path('agents/login', agent_views.agent_login_action),
    path('agents/logout', agent_views.agent_logout_action),
    path('agents/agent_home', agent_views.agent_homepage),

    path('agents/taxi-types',agent_views.taxi_types),
    path('agents/taxi-models',agent_views.taxi_models),
    path('agents/taxis',agent_views.taxis),

    path('agents/companies', agent_views.companies),
    path('agents/add-company', agent_views.add_company),
    path('agents/edit-company/<int:id>', agent_views.edit_company),
    path('agents/delete-company/<int:id>', agent_views.delete_company),

    path('agents/billing_entities/<int:id>', agent_views.company_billing_entities),
    path('agents/rates/<int:id>', agent_views.company_rates),
    path('agents/add-company-rate/<int:id>', agent_views.add_company_rate),
    path('agents/add-company-entity/<int:id>', agent_views.add_company_entity),

    path('agents/groups/<int:id>', agent_views.company_groups),
    path('agents/view-company-group/<int:id>', agent_views.view_company_group),
    path('agents/add-company-group/<int:id>', agent_views.add_company_group),
    path('agents/update-company-group/<int:id>', agent_views.update_company_group),
    path('agents/delete-company-group/<int:id>', agent_views.delete_company_group),
    path('agents/add-company-group-auth/<int:id>', agent_views.add_company_group_auth),

    path('agents/subgroups/<int:id>', agent_views.company_subgroups),
    path('agents/view-company-subgroup/<int:id>', agent_views.view_company_subgroup),
    path('agents/add-company-subgroup/<int:id>', agent_views.add_company_subgroup),
    path('agents/update-company-subgroup/<int:id>', agent_views.update_company_subgroup),
    path('agents/delete-company-subgroup/<int:id>', agent_views.delete_company_subgroup),
    path('agents/add-company-subgroup-auth/<int:id>', agent_views.add_company_subgroup_auth),

    path('agents/admins/<int:id>', agent_views.company_admins),
    path('agents/add-company-admins/<int:id>', agent_views.add_company_admins),

    path('agents/spocs/<int:id>', agent_views.company_spocs),
    path('agents/add-spoc/<int:id>', agent_views.add_spocs),

    path('agents/employees/<int:id>', agent_views.company_employees),
    path('agents/add-employee/<int:id>', agent_views.add_employee),

    path('agents/assessment_cities/<int:id>', agent_views.assessment_cities),
    path('agents/delete-assessment_cities/<int:id>', agent_views.delete_assessment_cities),
    path('agents/assessment_codes/<int:id>', agent_views.assessment_codes),
    path('agents/delete-assessment_codes/<int:id>', agent_views.delete_assessment_codes),

    path('agents/agents', agent_views.view_agents),
    path('agents/add-agent/<int:id>', agent_views.add_agent),

    path('agents/operators', agent_views.operators),
    path('agents/operator_contacts/<int:id>', agent_views.operator_contacts),
    path('agents/operator_banks/<int:id>', agent_views.operator_banks),
    path('agents/add-operator/<int:id>', agent_views.add_operator),
    path('agents/delete-operator/<int:id>', agent_views.delete_operator),

    path('agents/operator-rates', agent_views.operator_rates),
    path('agents/add-operator-rate/<int:id>', agent_views.add_operator_rate),
    path('agents/delete-operator-rate/<int:id>', agent_views.delete_operator_rate),

    path('agents/operator-drivers', agent_views.operator_drivers),
    path('agents/add-operator-driver/<int:id>', agent_views.add_operator_driver),
    path('agents/delete-operator-driver/<int:id>', agent_views.delete_operator_driver),

    path('agents/taxi-bookings/<int:id>', agent_views.taxi_bookings),
    path('agents/add-taxi-booking/<int:id>', agent_views.add_taxi_booking),
    path('agents/view-taxi-booking/<int:id>', agent_views.view_taxi_booking),
    path('agents/accept-taxi-booking', agent_views.accept_taxi_booking),
    path('agents/assign-taxi-booking/<int:id>', agent_views.assign_taxi_booking),

    path('agents/bus-bookings/<int:id>', agent_views.bus_bookings),
    path('agents/add-bus-booking/<int:id>', agent_views.add_bus_booking),
    path('agents/view-bus-booking/<int:id>', agent_views.view_bus_booking),
    path('agents/accept-bus-booking', agent_views.accept_bus_booking),
    path('agents/assign-bus-booking/<int:id>', agent_views.assign_bus_booking),

    path('agents/train-bookings/<int:id>', agent_views.train_bookings),
    path('agents/add-train-booking/<int:id>', agent_views.add_train_booking),
    path('agents/view-train-booking/<int:id>', agent_views.view_train_booking),
    path('agents/accept-train-booking', agent_views.accept_train_booking),
    path('agents/assign-train-booking/<int:id>', agent_views.assign_train_booking),

    path('agents/hotel-bookings/<int:id>', agent_views.hotel_bookings),
    path('agents/add-hotel-booking/<int:id>', agent_views.add_hotel_booking),
    path('agents/view-hotel-booking/<int:id>', agent_views.view_hotel_booking),
    path('agents/accept-hotel-booking', agent_views.accept_hotel_booking),
    path('agents/assign-hotel-booking/<int:id>', agent_views.assign_hotel_booking),

    path('agents/flight-bookings/<int:id>', agent_views.flight_bookings),
    path('agents/add-flight-booking/<int:id>', agent_views.add_flight_booking),
    path('agents/view-flight-booking/<int:id>', agent_views.view_flight_booking),
    path('agents/accept-flight-booking', agent_views.accept_flight_booking),
    path('agents/assign-flight-booking/<int:id>', agent_views.assign_flight_booking),

]