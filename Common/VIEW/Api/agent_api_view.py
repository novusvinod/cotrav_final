from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from Common.models import Corporate_Login
from Common.models import Corporate_Spoc_Login
from Common.models import Corporate_Approves_1_Login
from Common.models import Corporate_Approves_2_Login
from Common.models import Corporate_Agent

from Common.models import Corporate_Login_Access_Token
from Common.models import Corporate_Spoc_Login_Access_Token
from Common.models import Corporate_Approves_1_Login_Access_Token
from Common.models import Corporate_Approves_2_Login_Access_Token
from Common.models import Corporate_Agent_Login_Access_Token


def operators(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user = {}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('AllOperators', [])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Operators': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def view_operator(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    operator_id = request.POST.get('operator_id', '')

    user = {}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewOperator', [operator_id])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Operator': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_operator(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id= request.POST.get('user_id', '')
    type = request.POST.get('type', '')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    operator_name = request.POST.get('operator_name', '')
    operator_email = request.POST.get('operator_email', '')

    operator_contact = request.POST.get('operator_contact', '')
    website = request.POST.get('website', '')
    operator_address = request.POST.get('operator_address', '')
    contact_name = request.POST.get('contact_name', '')
    contact_email = request.POST.get('contact_email', '')
    contact_no = request.POST.get('contact_no', '')
    beneficiary_name = request.POST.get('beneficiary_name', '')
    beneficiary_account_no = request.POST.get('beneficiary_account_no', '')
    bank_name = request.POST.get('bank_name', '')
    ifsc_code = request.POST.get('ifsc_code', '')

    is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
    service_tax_number = request.POST.get('service_tax_number', '')
    night_start_time = request.POST.get('night_start_time', '')
    night_end_time = request.POST.get('night_end_time', '')
    tds_rate = request.POST.get('tds_rate', '')
    gst_id = request.POST.get('gst_id', '')
    pan_no = request.POST.get('pan_no', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('addOperator', [type,username,password,operator_name,operator_email,operator_contact,website,operator_address,contact_name,contact_email,
                                                contact_no,beneficiary_name,beneficiary_account_no,bank_name,ifsc_code,is_service_tax_applicable,service_tax_number,
                                                night_start_time,night_end_time,tds_rate,gst_id,pan_no,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_operator(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id= request.POST.get('user_id', '')

    type = request.POST.get('type', '')
    username = request.POST.get('username', '')
    operator_name = request.POST.get('operator_name', '')
    operator_email = request.POST.get('operator_email', '')

    operator_contact = request.POST.get('operator_contact', '')
    website = request.POST.get('website', '')
    operator_address = request.POST.get('operator_address', '')
    contact_name = request.POST.get('contact_name', '')
    contact_email = request.POST.get('contact_email', '')
    contact_no = request.POST.get('contact_no', '')
    beneficiary_name = request.POST.get('beneficiary_name', '')
    beneficiary_account_no = request.POST.get('beneficiary_account_no', '')
    bank_name = request.POST.get('bank_name', '')
    ifsc_code = request.POST.get('ifsc_code', '')

    is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
    service_tax_number = request.POST.get('service_tax_number', '')
    night_start_time = request.POST.get('night_start_time', '')
    night_end_time = request.POST.get('night_end_time', '')
    tds_rate = request.POST.get('tds_rate', '')
    gst_id = request.POST.get('gst_id', '')
    pan_no = request.POST.get('pan_no', '')

    operator_id = request.POST.get('operator_id', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('updateOperator', [type,username,operator_name,operator_email,operator_contact,website,operator_address,contact_name,contact_email,
                                                contact_no,beneficiary_name,beneficiary_account_no,bank_name,ifsc_code,is_service_tax_applicable,service_tax_number,
                                                night_start_time,night_end_time,tds_rate,gst_id,pan_no,operator_id,user_id,user_type])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def delete_operator(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user = {}
    user_id = request.POST.get('user_id', '')
    operator_id = request.POST.get('operator_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('deleteOperators', [operator_id,user_id,user_type])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Operators': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def operator_rates(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user = {}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('AllOperatorRates', [])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Rates': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def view_operator_rate(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    rate_id = request.POST.get('rate_id', '')

    user = {}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewOperatorRate', [rate_id])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Rate': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_operator_rate(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id= request.POST.get('user_id', '')

    operator_id = request.POST.get('operator_id', '')
    city_id = request.POST.get('city_id', '')
    taxi_type_id = request.POST.get('taxi_type_id', '')
    package_name = request.POST.get('package_name', '')
    tour_type = request.POST.get('tour_type', '')
    kms = request.POST.get('kms', '')
    hours = request.POST.get('hours', '')
    km_rate = request.POST.get('km_rate', '')
    hour_rate = request.POST.get('hour_rate', '')
    base_rate = request.POST.get('base_rate', '')
    night_rate = request.POST.get('night_rate', '')
    fuel_rate = request.POST.get('fuel_rate', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('addOperatorRate', [operator_id,city_id,taxi_type_id,package_name,tour_type,kms,hours,km_rate,hour_rate,
                                base_rate,night_rate,fuel_rate,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_operator_rate(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id= request.POST.get('user_id', '')
    rate_id = request.POST.get('rate_id', '')

    operator_id = request.POST.get('operator_id', '')
    city_id = request.POST.get('city_id', '')
    taxi_type_id = request.POST.get('taxi_type_id', '')
    package_name = request.POST.get('package_name', '')
    tour_type = request.POST.get('tour_type', '')
    kms = request.POST.get('kms', '')
    hours = request.POST.get('hours', '')
    km_rate = request.POST.get('km_rate', '')
    hour_rate = request.POST.get('hour_rate', '')
    base_rate = request.POST.get('base_rate', '')
    night_rate = request.POST.get('night_rate', '')
    fuel_rate = request.POST.get('fuel_rate', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('updateOperatorRate', [operator_id,city_id,taxi_type_id,package_name,tour_type,kms,hours,km_rate,hour_rate,
                                base_rate,night_rate,fuel_rate,rate_id,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def delete_operator_rate(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user = {}
    user_id = request.POST.get('user_id', '')
    rate_id = request.POST.get('rate_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('deleteOperators', [rate_id,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Operators': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def operator_drivers(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user = {}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('AllOperatorDrivers', [])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Drivers': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def view_operator_driver(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    driver_id = request.POST.get('driver_id', '')

    user = {}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewOperatorDriver', [driver_id])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Drivers': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_operator_driver(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id= request.POST.get('user_id', '')
    operator_id = request.POST.get('operator_id', '')
    driver_name = request.POST.get('driver_name', '')
    driver_contact = request.POST.get('driver_contact', '')
    driver_email = request.POST.get('driver_email', '')
    licence_no = request.POST.get('licence_no', '')
    password = request.POST.get('password', '')
    fcm_regid = request.POST.get('fcm_regid', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('addOperatorDriver', [operator_id,driver_name,driver_contact,driver_email,licence_no,password,fcm_regid,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Drivers': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_operator_driver(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id= request.POST.get('user_id', '')
    driver_id = request.POST.get('driver_id', '')

    user_id= request.POST.get('user_id', '')
    operator_id = request.POST.get('operator_id', '')
    driver_name = request.POST.get('driver_name', '')
    driver_contact = request.POST.get('driver_contact', '')
    driver_email = request.POST.get('driver_email', '')
    licence_no = request.POST.get('licence_no', '')
    fcm_regid = request.POST.get('fcm_regid', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('updateOperatorDriver', [operator_id,driver_name,driver_contact,driver_email,licence_no,fcm_regid,driver_id,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Drivers': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def delete_operator_driver(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user = {}
    user_id = request.POST.get('user_id', '')
    driver_id = request.POST.get('driver_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('deleteOperatorDriver', [driver_id,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                data = {'success': 1, 'Operators': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)








def spoc_taxi_bookings(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('AllTaxiBookings', [])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def spoc_add_taxi_booking(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    corporate_id = request.POST.get('corporate_id', '')
    spoc_id = request.POST.get('spoc_id', '')
    group_id = request.POST.get('group_id', '')
    subgroup_id = request.POST.get('subgroup_id', '')

    tour_type = request.POST.get('tour_type', '')
    pickup_city = request.POST.get('pickup_city', '')
    pickup_location = request.POST.get('pickup_location', '')
    drop_location = request.POST.get('drop_location', '')
    pickup_datetime = request.POST.get('pickup_datetime', '')
    pickup_datetime = datetime.strptime(pickup_datetime, '%d/%m/%Y %H:%M:%S')
    taxi_type = request.POST.get('taxi_type')
    package_id = request.POST.get('package_id')
    no_of_days = request.POST.get('no_of_days', '')

    if taxi_type:
        taxi_type = taxi_type
    else:
        taxi_type = 0

    if package_id:
        package_id = package_id
    else:
        package_id = 0

    if no_of_days:
        no_of_days = no_of_days
    else:
        no_of_days = 0

    reason_booking = request.POST.get('reason_booking', '')
    no_of_seats = request.POST.get('no_of_seats', '')

    employees = request.POST.getlist('employees', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addTaxiBooking', [user_type,spoc_id,corporate_id,group_id,subgroup_id,tour_type,pickup_city,pickup_location,drop_location,pickup_datetime,
                                                             taxi_type,package_id,no_of_days,reason_booking,no_of_seats])
                    booking_id = dictfetchall(cursor)
                    cursor.close()
                    for id in booking_id:
                        for e in employees:
                            cursor = connection.cursor()
                            cursor.callproc('addEmployeeTaxiBooking',[id['id'],e])
                            cursor.close()
                    else:
                        data = {'success': 1, 'message': "Error in Data Insert"}
                        return JsonResponse(data)

                except Exception as e:
                    print(e)
                    data = {'success': 1, 'message': "Error in Data Insert"}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def accept_taxi_booking(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    booking_id = request.POST.get('booking_id', '')
    user_id = request.POST.get('user_id', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('acceptTaxiBooking', [booking_id,user_id,user_type])
                data = {'success': 1}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def reject_taxi_booking(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    booking_id = request.POST.get('booking_id', '')
    user_id = request.POST.get('user_id', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('acceptTaxiBooking', [booking_id,user_id,user_type])
                data = {'success': 1}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def assign_taxi_booking(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    booking_id = request.POST.get('booking_id', '')
    user_id = request.POST.get('user_id', '')

    vendor_booking_id = request.POST.get('vendor_booking_id', '')
    operator_id = request.POST.get('operator_id', '')
    driver_id = request.POST.get('driver_id', '')
    taxi_id = request.POST.get('taxi_id', '')

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('assignTaxiBooking', [vendor_booking_id,operator_id,driver_id,taxi_id,booking_id,user_id,user_type])
                data = {'success': 1}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)











def getUserinfoFromAccessToken(user_token=None, user_type=None):
    try:
        user = {}
        user_info = {}
        if user_type == '1':
            user = Corporate_Login_Access_Token.objects.get(access_token=user_token)

        elif user_type == '2':
            user = Corporate_Approves_1_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '3':
            user = Corporate_Approves_2_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '4':
            user = Corporate_Spoc_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '10':
            user = Corporate_Agent_Login_Access_Token.objects.get(access_token=user_token)

        present = datetime.now()

        if user.expiry_date.date() < present.date():
            return None
        else:

            if user_type == '1':
                user_info = Corporate_Login.objects.get(id=user.corporate_login_id)

            elif user_type == '2':
                user_info = Corporate_Approves_1_Login.objects.get(id=user.subgroup_authenticater_id)
            elif user_type == '3':
                user_info = Corporate_Approves_2_Login.objects.get(id=user.group_authenticater_id)
            elif user_type == '4':
                user_info = Corporate_Spoc_Login.objects.get(id=user.spoc_id)
            elif user_type == '10':
                user_info = Corporate_Agent.objects.get(id=user.agent_id)
            else:
                return None

            return user_info

    except Exception as e:
        print(e)
        return None

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]