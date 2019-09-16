from django.conf import settings
from django.shortcuts import render, redirect
import requests
import json
from django_global_request.middleware import get_request
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@login_required(login_url='/login')
def homepage(request):
    if 'login_type' in request.session:
        return render(request, 'Company/Spoc/home_page.html', {'user': request.user})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_admins(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "admins"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            admins = company['Admins']
            return render(request, "Company/Spoc/company_admins.html", {'admins': admins})
        else:
            return render(request, "Company/Spoc/company_admins.html", {'admins': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_billing_entities(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "billing_entities"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        url_city = settings.API_BASE_URL + "cities"
        cities = getDataFromAPI(login_type, access_token, url_city, payload)
        if company['success'] == 1:
            entities = company['Entitys']
            cities = cities["Cities"]
            return render(request, "Company/Spoc/billing_entities.html",
                          {'billing_entities': entities, "cities": cities, })
        else:
            return render(request, "Company/Spoc/billing_entities.html", {'entities': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_rates(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "company_rates"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            company_rates = company['Corporate_Retes']
            return render(request, "Company/Spoc/company_rates.html", {'corporate_rates': company_rates})
        else:
            return render(request, "Company/Spoc/company_rates.html", {'entities': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_groups(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "groups"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            groups = company['Groups']
            return render(request, "Company/Spoc/groups.html", {'groups': groups})
        else:
            return render(request, "Company/Spoc/groups.html", {'groups': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_subgroups(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "subgroups"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            url2 = settings.API_BASE_URL + "groups"
            subgroups = company['Subgroups']
            gr = getDataFromAPI(login_type, access_token, url2, payload)
            groups = gr['Groups']
            return render(request, "Company/Spoc/subgroups.html", {'subgroups': subgroups, 'groups': groups})
        else:
            return render(request, "Company/Spoc/subgroups.html", {'subgroups': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_spocs(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "spocs"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            spocs = company['Spocs']
            return render(request, "Company/Spoc/spocs.html", {'spocs': spocs})
        else:
            return render(request, "Company/Spoc/spocs.html", {'spocs': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_employees(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "employees"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            employees = company['Employees']
            return render(request, "Company/Spoc/employees.html", {'employees': employees})
        else:
            return render(request, "Company/Spoc/employees.html", {'employees': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def view_company_group(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_group"
        payload = {'group_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        url = settings.API_BASE_URL + "view_group_auth"
        grp_auths = getDataFromAPI(login_type, access_token, url, payload)
        print(grp_auths)
        if company['success'] == 1:
            groups = company['Groups']
            grp_auths = grp_auths['Groups']
            return render(request, "Company/Spoc/view_groups.html", {'group': groups, 'grp_auths': grp_auths})
        else:
            return render(request, "Company/Spoc/view_groups.html", {'group': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def view_company_subgroup(request, id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_subgroup"
        payload = {'subgroup_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        subgrp_auths = getDataFromAPI(login_type, access_token, url, payload)
        print(subgrp_auths)
        if company['success'] == 1:
            subgroups = company['SubGroups']
            subgrp_auths = subgrp_auths['SubGroups']
            return render(request, "Company/Spoc/view_subgroups.html",
                          {'subgroup': subgroups, 'subgrp_auths': subgrp_auths})
        else:
            return render(request, "Company/Spoc/view_subgroups.html", {'group': {}})
    else:
        return HttpResponseRedirect("/login")


###################################### TAXI #############################################

def taxi_bookings(request,id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "spoc_taxi_bookings"
        payload = {'spoc_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Spoc/taxi_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Spoc/taxi_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def view_taxi_booking(request,id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_taxi_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Spoc/view_taxi_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Spoc/view_taxi_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def add_taxi_booking(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            corporate_id = request.POST.get('corporate_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            group_id = request.POST.get('group_id', '')
            subgroup_id = request.POST.get('subgroup_id', '')

            tour_type = request.POST.get('tour_type', '')
            pickup_city = request.POST.get('pickup_city', '')
            pickup_location = request.POST.get('pickup_location', '')
            drop_location = request.POST.get('drop_location', '')
            pickup_datetime = request.POST.get('pickup_datetime', '')
            taxi_type = request.POST.get('taxi_type', '')
            package_id = request.POST.get('package_id', '')
            no_of_days = request.POST.get('no_of_days', '')
            assessment_code = request.POST.get('assessment_code', '')
            assessment_city_id = request.POST.get('assessment_city_id', '')

            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            pickup_details = [x.strip() for x in pickup_city.split(',')]
            city_data = {'login_type': login_type, 'access_token': access_token, 'city_country': pickup_details[2]}

            url_add_city = settings.API_BASE_URL + "add_city_name"
            url_add_state = settings.API_BASE_URL + "add_state_name"
            url_add_country = settings.API_BASE_URL + "add_country_name"

            country_id = getDataFromAPI(login_type, access_token, url_add_country, city_data)
            for conty_id in country_id['id']:
                actual_country_id = conty_id['id']

            city_data = {'login_type': login_type, 'access_token': access_token, 'city_state': pickup_details[1], 'country_id': actual_country_id}
            state_id = getDataFromAPI(login_type, access_token, url_add_state, city_data)

            for conty_id in state_id['id']:
                actual_state_id = conty_id['id']

            city_data = {'login_type': login_type, 'access_token': access_token, 'city_name': pickup_details[0],
                         'state_id': actual_state_id}
            city_id = getDataFromAPI(login_type, access_token, url_add_city, city_data)

            for conty_id in city_id['id']:
                actual_city_id = conty_id['id']

            payload = {'login_type':login_type,'access_token':access_token,'corporate_id': corporate_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'tour_type':tour_type,'pickup_city':actual_city_id,'assessment_code':assessment_code,'assessment_city_id':assessment_city_id,
                       'pickup_location':pickup_location,'drop_location':drop_location,'pickup_datetime':pickup_datetime,'taxi_type':taxi_type,
                       'package_id':package_id,'no_of_days':no_of_days,'reason_booking':reason_booking,'no_of_seats':no_of_seats,'employees':employees}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "spoc_add_taxi_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)

            if booking['success'] == 1:
                return HttpResponseRedirect("/Corporate/Spoc/taxi-bookings/" + str(request.user.corporate_id), {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/login")
    else:
        if 'login_type' in request.session:
            request = get_request()
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}

            url_emp = settings.API_BASE_URL + "employees"
            payload = {'corporate_id': id}
            r = requests.post(url_emp, data=payload, headers=headers)
            company_emp = json.loads(r.text)
            employees = company_emp['Employees']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            url_taxi = settings.API_BASE_URL + "taxi_types"
            taxies = getDataFromAPI(login_type, access_token, url_taxi, payload)
            taxies = taxies['taxi_types']

            url_enty = settings.API_BASE_URL + "billing_entities"
            entys = getDataFromAPI(login_type, access_token, url_enty, payload)
            entities = entys['Entitys']

            url_ass_code = settings.API_BASE_URL + "get_assessment_code"
            ass_code = getDataFromAPI(login_type, access_token, url_ass_code, payload)
            ass_code = ass_code['AssCodes']

            if id:
                return render(request, 'Company/Spoc/add_taxi_booking.html', {'employees':employees,'entities':entities,'cities':cities,'taxies':taxies,'assessments':ass_code})
            else:
                return render(request, 'Company/Spoc/add_taxi_booking.html', {})
        else:
            return HttpResponseRedirect("/login")


############################################# BUS #########################################


def bus_bookings(request,id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "spoc_bus_bookings"
        payload = {'spoc_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Spoc/bus_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Spoc/bus_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def view_bus_booking(request,id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_bus_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        print(company)
        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Spoc/view_bus_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Spoc/view_bus_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def add_bus_booking(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('spoc_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            group_id = request.POST.get('group_id', '')
            subgroup_id = request.POST.get('subgroup_id', '')

            from_location = request.POST.get('from', '')
            to_location = request.POST.get('to', '')
            bus_type = request.POST.get('bus_type', '')
            booking_datetime = request.POST.get('booking_datetime', '')
            journey_datetime = request.POST.get('journey_datetime', '')
            entity_id = request.POST.get('entity_id', '')
            preferred_bus = request.POST.get('preferred_bus', '')
            assessment_code = request.POST.get('assessment_code', '')
            assessment_city_id = request.POST.get('assessment_city_id', '')

            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            payload = {'login_type':login_type,'user_id':user_id,'access_token':access_token,'corporate_id': corporate_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'from':from_location,'to':to_location,'assessment_code':assessment_code,'assessment_city_id':assessment_city_id,
                       'bus_type':bus_type,'booking_datetime':booking_datetime,'journey_datetime':journey_datetime,'entity_id':entity_id,
                       'preferred_bus':preferred_bus,'reason_booking':reason_booking,'no_of_seats':no_of_seats,'employees':employees}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "add_bus_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)

            if booking['success'] == 1:
                return HttpResponseRedirect("/Corporate/Spoc/bus-bookings/" + str(request.user.corporate_id), {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/login")
    else:
        if 'login_type' in request.session:
            request = get_request()
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}

            url_emp = settings.API_BASE_URL + "employees"
            payload = {'corporate_id': id}
            r = requests.post(url_emp, data=payload, headers=headers)
            company_emp = json.loads(r.text)
            employees = company_emp['Employees']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            url_enty = settings.API_BASE_URL + "billing_entities"
            entys = getDataFromAPI(login_type, access_token, url_enty, payload)
            entities = entys['Entitys']

            url_ass_code = settings.API_BASE_URL + "get_assessment_code"
            ass_code = getDataFromAPI(login_type, access_token, url_ass_code, payload)
            ass_code = ass_code['AssCodes']

            if id:
                return render(request, 'Company/Spoc/add_bus_booking.html', {'employees':employees,'cities':cities,'entities':entities,'assessments':ass_code})
            else:
                return render(request, 'Company/Spoc/add_bus_booking.html', {})
        else:
            return HttpResponseRedirect("/login")



############################################# TRAIN #########################################


def train_bookings(request,id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "spoc_train_bookings"
        payload = {'spoc_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Spoc/train_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Spoc/train_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def view_train_booking(request,id):

    if 'login_type' in request.session:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_train_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        print(company)
        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Spoc/view_train_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Spoc/view_train_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def add_train_booking(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('spoc_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            group_id = request.POST.get('group_id', '')
            subgroup_id = request.POST.get('subgroup_id', '')

            from_location = request.POST.get('from', '')
            to_location = request.POST.get('to', '')
            train_type = request.POST.get('train_type', '')
            booking_datetime = request.POST.get('booking_datetime', '')
            journey_datetime = request.POST.get('journey_datetime', '')
            entity_id = request.POST.get('entity_id', '')
            preferred_bus = request.POST.get('preferred_bus', '')
            assessment_code = request.POST.get('assessment_code', '')
            assessment_city_id = request.POST.get('assessment_city_id', '')

            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            payload = {'login_type':login_type,'user_id':user_id,'access_token':access_token,'corporate_id': corporate_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'from':from_location,'to':to_location,'assessment_code':assessment_code,'assessment_city_id':assessment_city_id,
                       'train_type':train_type,'booking_datetime':booking_datetime,'journey_datetime':journey_datetime,'entity_id':entity_id,
                       'preferred_bus':preferred_bus,'reason_booking':reason_booking,'no_of_seats':no_of_seats,'employees':employees}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "add_bus_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)

            if booking['success'] == 1:
                return HttpResponseRedirect("/Corporate/Spoc/bus-bookings/" + str(request.user.corporate_id), {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/login")
    else:
        if 'login_type' in request.session:
            request = get_request()
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}

            url_emp = settings.API_BASE_URL + "employees"
            payload = {'corporate_id': id}
            r = requests.post(url_emp, data=payload, headers=headers)
            company_emp = json.loads(r.text)
            employees = company_emp['Employees']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            url_enty = settings.API_BASE_URL + "billing_entities"
            entys = getDataFromAPI(login_type, access_token, url_enty, payload)
            entities = entys['Entitys']

            url_ass_code = settings.API_BASE_URL + "get_assessment_code"
            ass_code = getDataFromAPI(login_type, access_token, url_ass_code, payload)
            ass_code = ass_code['AssCodes']

            if id:
                return render(request, 'Company/Spoc/add_train_booking.html', {'employees':employees,'cities':cities,'entities':entities,'assessments':ass_code})
            else:
                return render(request, 'Company/Spoc/add_train_booking.html', {})
        else:
            return HttpResponseRedirect("/login")



def getDataFromAPI(login_type, access_token, url, payload):
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    api_response = json.loads(r.text)
    return api_response


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
