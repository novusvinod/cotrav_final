from django.conf import settings
from django.shortcuts import render, redirect
import requests
import json
from django_global_request.middleware import get_request
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

@login_required(login_url='/login')
def homepage(request):
    if 'login_type' in request.session:
        return render(request, 'Company/Approver_2/home_page.html', {'user': request.user})
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
            return render(request, "Company/Approver_2/company_admins.html", {'admins': admins})
        else:
            return render(request, "Company/Approver_2/company_admins.html", {'admins': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_billing_entities(request, id):
    request = get_request()

    if 'login_type' in request.session:
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
            return render(request, "Company/Approver_2/billing_entities.html",
                          {'billing_entities': entities, "cities": cities, })
        else:
            return render(request, "Company/Approver_2/billing_entities.html", {'entities': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_rates(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "company_rates"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            company_rates = company['Corporate_Retes']
            return render(request, "Company/Approver_2/company_rates.html", {'corporate_rates': company_rates})
        else:
            return render(request, "Company/Approver_2/company_rates.html", {'entities': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_groups(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "groups"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            groups = company['Groups']
            return render(request, "Company/Approver_2/groups.html", {'groups': groups})
        else:
            return render(request, "Company/Approver_2/groups.html", {'groups': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_subgroups(request, id):
    request = get_request()

    if 'login_type' in request.session:
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
            return render(request, "Company/Approver_2/subgroups.html", {'subgroups': subgroups, 'groups': groups})
        else:
            return render(request, "Company/Approver_2/subgroups.html", {'subgroups': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_spocs(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "spocs"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            spocs = company['Spocs']
            return render(request, "Company/Approver_2/spocs.html", {'spocs': spocs})
        else:
            return render(request, "Company/Approver_2/spocs.html", {'spocs': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def company_employees(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "employees"
        payload = {'corporate_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            employees = company['Employees']
            return render(request, "Company/Approver_2/employees.html", {'employees': employees})
        else:
            return render(request, "Company/Approver_2/employees.html", {'employees': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def view_company_group(request, id):
    request = get_request()

    if 'login_type' in request.session:
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
            return render(request, "Company/Approver_2/view_groups.html", {'group': groups, 'grp_auths': grp_auths})
        else:
            return render(request, "Company/Approver_2/view_groups.html", {'group': {}})
    else:
        return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def view_company_subgroup(request, id):
    request = get_request()

    if 'login_type' in request.session:
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
            return render(request, "Company/Approver_2/view_subgroups.html",
                          {'subgroup': subgroups, 'subgrp_auths': subgrp_auths})
        else:
            return render(request, "Company/Approver_2/view_subgroups.html", {'group': {}})
    else:
        return HttpResponseRedirect("/login")

####################################### TAXI #################################


def taxi_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_taxi_bookings"
        payload = {'approver_2_id': user_id,'booking_id':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/taxi_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/taxi_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def view_taxi_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_taxi_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/view_taxi_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/view_taxi_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def accept_taxi_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_accept_taxi_booking"
        payload = {'booking_id': id,'user_id':user_id}
        print(payload)
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Taxi Booking Sccepted Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/taxi-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail To Accept Taxi Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/taxi-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/login")


def reject_taxi_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_reject_taxi_booking"
        payload = {'booking_id': id,'user_id':user_id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Taxi Booking Rejected Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/taxi-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail To Reject Taxi Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/taxi-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/login")

##################################### BUS  ###############################################


def bus_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_bus_bookings"
        payload = {'approver_2_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/bus_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/bus_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def view_bus_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_bus_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/view_bus_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/view_bus_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def accept_bus_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_accept_bus_booking"
        payload = {'booking_id': id,'user_id':user_id}
        print(payload)
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Bus Booking Accepted Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/bus-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Accept Bus Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/bus-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/login")


def reject_bus_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_reject_bus_booking"
        payload = {'booking_id': id,'user_id':user_id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Bus Booking Rejected Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/bus-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Reject Bus Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/bus-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/login")



##################################### TRAIN  ###############################################


def train_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_train_bookings"
        payload = {'approver_2_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/train_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/train_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def view_train_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_train_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/view_train_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/view_train_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/login")


def accept_train_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_accept_train_booking"
        payload = {'booking_id': id,'user_id':user_id}
        print(payload)
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Train Booking Accepted successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/train-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Accept Train Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/train-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/login")


def reject_train_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_reject_train_booking"
        payload = {'booking_id': id,'user_id':user_id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Train Booking Rejected Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/train-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Reject Train Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/train-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/login")

############################################## HOTELS ############################################


def hotel_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_1_hotel_bookings"
        payload = {'approver_1_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/hotel_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/hotel_bookings.html", {'': {}})
    else:
        return redirect('/login')


def view_hotel_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_hotel_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/view_hotel_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/view_hotel_booking.html", {'': {}})
    else:
        return redirect('/login')


def accept_hotel_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_hotel_train_booking"
        payload = {'booking_id': id,'user_id':user_id}
        print(payload)
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Hotel Booking Accepted Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/hotel-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Accept Hotel Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/hotel-bookings/1",{'message': "Operation Fails"})
    else:
        return redirect('/login')


def reject_hotel_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_reject_hotel_booking"
        payload = {'booking_id': id,'user_id':user_id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Hotel Booking Rejected Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/hotel-bookings/1" , {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail To Reject Hotel Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/hotel-bookings/1",{'message': "Operation Fails"})
    else:
        return redirect('/login')

############################################## FLIGHT ############################################


def flight_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_1_flight_bookings"
        payload = {'approver_1_id': user_id,'booking_type':id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/flight_bookings.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/flight_bookings.html", {'': {}})
    else:
        return redirect('/login')


def view_flight_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_flight_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Company/Approver_2/view_flight_booking.html",{'bookings': booking})
        else:
            return render(request, "Company/Approver_2/view_flight_booking.html", {'': {}})
    else:
        return redirect('/login')


def accept_flight_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_accept_flight_booking"
        payload = {'booking_id': id,'user_id':user_id}
        print(payload)
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Flight Booking Accepted Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/flight-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Accept Flight Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/flight-bookings/1",{'message': "Operation Fails"})
    else:
        return redirect('/login')


def reject_flight_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id

        url = settings.API_BASE_URL + "approver_2_reject_flight_booking"
        payload = {'booking_id': id,'user_id':user_id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            messages.success(request, 'Flight Booking Rejected Successfully..!')
            return HttpResponseRedirect("/Corporate/Approver_2/flight-bookings/1", {'message': "Operation Successfully"})
        else:
            messages.error(request, 'Fail to Reject flight Booking..!')
            return HttpResponseRedirect("/Corporate/Approver_2/flight-bookings/1",{'message': "Operation Fails"})
    else:
        return redirect('/login')



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
