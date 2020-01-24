from datetime import datetime
import socket
from dateutil.parser import parse
import json
import requests
from django.utils import timezone
import pytz
from django.contrib import messages
from django.shortcuts import render , redirect

from django.http import JsonResponse
from django.db import connection
from Common.models import Corporate_Login
from Common.models import Corporate_Spoc_Login
from Common.models import Corporate_Employee_Login
from Common.models import Corporate_Approves_1_Login
from Common.models import Corporate_Approves_2_Login
from Common.models import Corporate_Agent
from Common.models import Operator_Login


from Common.models import Corporate_Login_Access_Token
from Common.models import Corporate_Spoc_Login_Access_Token
from Common.models import Corporate_Employee_Login_Access_Token
from Common.models import Corporate_Approves_1_Login_Access_Token
from Common.models import Corporate_Approves_2_Login_Access_Token
from Common.models import Corporate_Agent_Login_Access_Token
from Common.models import Operator_Login_Access_Token

from django.contrib.auth.hashers import check_password
import string
import random
from Common.email_settings import SignIn_OTP, AddBooking_Email, newUserAdd_Email, Assign_Booking_Email
from landing.cotrav_messeging import Flight

COTRAV_EMAILS = "balwant@taxiaxi.in,chauhanbalwant007@gmail.com"
COTRAV_NUMBERS = "9579477262,"


def login(request):
    user_name = request.POST.get('user_name', '')
    user_password = request.POST.get('user_password', '')
    user_type = request.POST.get('user_type', '')
    user_info = request.META['HTTP_USER_AGENT']

    if user_name and user_password and user_type:
        cursor = connection.cursor()
        cursor.callproc('getLoginDetails', [user_name,user_type])
        user = dictfetchall(cursor)
        if user:
            password = check_password(user_password, user[0]['password'])
            if password:
                gen_access_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(60))
                generate_otp = ''.join(random.choice(string.digits) for _ in range(6))
                add_otp = SignIn_OTP()
                email_subject = "Cotrav - Verify Your Email"
                email_body = "Dear User,<br><br>" + generate_otp + " is your verification code to access your profile and bookings on Cotrav app, you need to verify your email first. <br><br>Rgrds,<br>CoTrav."
                resp1 = add_otp.send_email(user_name, email_subject, email_body)

                if resp1:
                    if user_type == '1':
                        insert_data = Corporate_Login_Access_Token.objects.create(corporate_login_id=user[0]['id'], access_token=gen_access_token,user_agent=user_info)
                    elif user_type == '2':
                        insert_data = Corporate_Approves_1_Login_Access_Token.objects.create(subgroup_authenticater_id=user[0]['id'], access_token=gen_access_token, user_agent=user_info)
                        print(insert_data)
                    elif user_type == '3':
                        insert_data = Corporate_Approves_2_Login_Access_Token.objects.create(group_authenticater_id=user[0]['id'], access_token=gen_access_token,user_agent=user_info)
                    elif user_type == '4':
                        insert_data = Corporate_Spoc_Login_Access_Token.objects.create(spoc_id=user[0]['id'],access_token=gen_access_token,user_agent=user_info)
                    elif user_type == '6':
                        insert_data = Corporate_Employee_Login_Access_Token.objects.create(employee_id=user[0]['id'], access_token=gen_access_token, user_agent=user_info)
                    elif user_type == '10':
                        insert_data = Corporate_Agent_Login_Access_Token.objects.create(agent_id=user[0]['id'], access_token=gen_access_token, user_agent=user_info)

                    data = {'success': 1,'access_token':gen_access_token, 'message': 'Login Successfully', 'User': user,'OTP':generate_otp}
                else:
                    data = {'success': 0, 'message': 'OTP Not Send To Your Email Id Please Type Anothe Email'}
            else:
                data = {'success': 0, 'message': 'Invalid User Name Or Password'}
        else:
            data = {'success': 0, 'message': 'Invalid User Name Or Password'}
    else:
        print("in else")
        data = {'success': 0, 'message': 'Please Enter Valid Inputs...'}
    return JsonResponse(data)


def logout(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    timezone.activate(pytz.timezone("Asia/Kolkata"))
                    user.expiry_date = timezone.localtime(timezone.now())  # change field
                    user.save()  # this will update only
                    data = {'success': 1, 'message': 'User Logout Successfully'}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def service_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllServiceType', [])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Types': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def railway_stations(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllRailwayStations', [])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Stations': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)

def bus_booking_portals(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllBusBookingPortals', [])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Portals': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def companies(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateDetails', [])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Corporates': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_company(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewCorporateDetails', [corporate_id])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Corporates': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_companies(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_name = request.POST.get('corporate_name', '')
        corporate_code = request.POST.get('corporate_code', '')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        bill_corporate_name = request.POST.get('bill_corporate_name', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        billing_city_id = request.POST.get('billing_city_id', '')
        gst_id = request.POST.get('gst_id', '')

        has_billing_spoc_level = request.POST.get('has_billing_spoc_level', '')
        has_billing_admin_level = request.POST.get('has_billing_admin_level', '')
        has_auth_level = request.POST.get('has_auth_level', '')
        no_of_auth_level = request.POST.get('no_of_auth_level', '')
        has_assessment_codes = request.POST.get('has_assessment_codes', '')
        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')
        has_self_booking_access = request.POST.get('has_self_booking_access', '')
        will_do_realtime_payment = request.POST.get('will_do_realtime_payment', '')
        is_spoc = request.POST.get('is_spoc', '')

        cotrav_agent_id = request.POST.get('cotrav_agent_id', '')
        user_type = request.POST.get('user_type', '')
        password = request.POST.get('password', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('create_corporate_with_basic_details',[corporate_name, corporate_code,contact_person_name,contact_person_no,contact_person_email,bill_corporate_name,address_line_1,
                      address_line_2,address_line_3,gst_id,has_billing_spoc_level,has_auth_level,no_of_auth_level,has_assessment_codes,is_radio,is_local,is_outstation, is_bus,
                       is_train, is_hotel, is_meal, is_flight,is_water_bottles,  is_reverse_logistics,is_spoc,password,cotrav_agent_id,user_type,
                    billing_city_id,has_self_booking_access,will_do_realtime_payment,has_billing_admin_level])
                    company = dictfetchall(cursor)
                    print(company)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(contact_person_name, contact_person_email, "taxi123", "Admin")
                        if is_spoc:
                            resp1 = add_user.new_user_send_email(contact_person_name, contact_person_email, "taxi123", "Spoc")
                            resp1 = add_user.new_user_send_email(contact_person_name, contact_person_email, "taxi123", "Employee")

                        data = {'success': 1, 'message': "Corporate Added Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_company(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_name = request.POST.get('corporate_name', '')
        corporate_code = request.POST.get('corporate_code', '')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        contact_person_email = request.POST.get('contact_person_email', '')

        has_billing_spoc_level = request.POST.get('has_billing_spoc_level', '')
        has_billing_admin_level = request.POST.get('has_billing_admin_level', '')
        has_auth_level = request.POST.get('has_auth_level', '')
        no_of_auth_level = request.POST.get('no_of_auth_level', '')
        has_assessment_codes = request.POST.get('has_assessment_codes', '')
        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')
        has_self_booking_access = request.POST.get('has_self_booking_access', '')
        will_do_realtime_payment = request.POST.get('will_do_realtime_payment', '')

        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')
        user_type = request.POST.get('user_type', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporate',[corporate_name, corporate_code,contact_person_name,contact_person_no,contact_person_email,
                      has_billing_spoc_level,has_auth_level,no_of_auth_level,has_assessment_codes,is_radio,is_local, is_outstation, is_bus,
                       is_train, is_hotel, is_meal, is_flight,is_water_bottles,  is_reverse_logistics,corporate_id,user_id,user_type,
                        has_self_booking_access,will_do_realtime_payment,has_billing_admin_level])
                    company = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Updated Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_company(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteCorporate',[corporate_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Deleted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_company_rates(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        package_name = request.POST.get('package_name', '')
        city_id = request.POST.get('city_id')
        taxi_type = request.POST.get('taxi_type', '')
        tour_type = request.POST.get('tour_type', '')
        kms = request.POST.get('kms', '')
        hours = request.POST.get('hours', '')
        km_rate = request.POST.get('km_rate', '')
        hour_rate = request.POST.get('hour_rate', '')
        base_rate = request.POST.get('base_rate', '')
        night_rate = request.POST.get('night_rate', '')

        rate_id = request.POST.get('rate_id')

        if rate_id:
            pass
        else:
            rate_id = 0
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addCorporateRate',[corporate_id,package_name,city_id,taxi_type,tour_type,kms,hours,km_rate,hour_rate,base_rate,
                                                        night_rate,user_id,user_type,rate_id])
                    company = dictfetchall(cursor)
                    print(company)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Rate Added Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_company_rates(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        package_name = request.POST.get('package_name', '')
        city_id = request.POST.get('city_id')
        taxi_type = request.POST.get('taxi_type', '')
        tour_type = request.POST.get('tour_type', '')
        kms = request.POST.get('kms', '')
        hours = request.POST.get('hours', '')
        km_rate = request.POST.get('km_rate', '')
        hour_rate = request.POST.get('hour_rate', '')
        base_rate = request.POST.get('base_rate', '')
        night_rate = request.POST.get('night_rate', '')

        rate_id = request.POST.get('rate_id')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporateRate',[corporate_id,package_name,city_id,taxi_type,tour_type,kms,hours,km_rate,hour_rate,base_rate,
                                                        night_rate,user_id,user_type,rate_id])
                    company = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Rate Updated Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_company_rates(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        rate_id = request.POST.get('rate_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteCorporateRate',[rate_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Rate Deleted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def company_rates(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateRatesDetails', [corporate_id])
                    corporate_rates = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Corporate_Retes': corporate_rates}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def billing_entities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateBillingEntitiesDetails', [corporate_id])
                    entity = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Entitys': entity}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_billing_entitie(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        entity_id = request.POST.get('entity_id', '')
        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewBillingEntitiesDetails', [entity_id])
                    entity = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Entitys': entity}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def corporate_management_fee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateManagementFeesDetails', [])
                    entity = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Fees': entity}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def service_fee_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllServiceFeesTypes', [])
                    entity = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Types': entity}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admins(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateAdminsDetails', [corporate_id])
                    admin = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Admins': admin}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def groups(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'
        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateGroupsDetails', [corporate_id])
                    group = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Groups': group}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def subgroups(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateSubgroupsDetails', [corporate_id])
                    subgroup = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Subgroups': subgroup}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def spocs(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateSpocsDetails', [corporate_id])
                    spoc = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Spocs': spoc}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def employee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = 0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateEmployeesDetails', [corporate_id])
                    employee = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Employees': employee}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def spoc_employee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        if spoc_id:
            spoc_id = spoc_id
        else:
            spoc_id = 0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateSpocEmployeesDetails', [spoc_id])
                    employee = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Employees': employee}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def corporate_package(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        city_id = request.POST.get('city_id', '')
        taxi_type = request.POST.get('taxi_type', '')
        tour_type = request.POST.get('tour_type', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getCorporatePackage', [corporate_id,city_id,taxi_type,tour_type])
                    employee = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Package': employee}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_assessment_code(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAssessmentCodes', [corporate_id])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'AssCodes': cities}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_assessment_city(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAssessmentCity', [corporate_id])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'AssCity': cities}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def cities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCity', [])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Cities': cities}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def taxi_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllTaxiTypes', [])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'taxi_types': cities}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def train_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllTrainTypes', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Types': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def bus_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllBusTypes', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Types': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def irctc_accounts(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllIrctcAccounts', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Accounts': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def hotel_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllHotelTypes', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Types': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_airports(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAirports', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Airports': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)
    


def hotel_booking_portals(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllHotelBookingPortals', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Portals': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_hotel_portal(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        hotel_id = request.POST.get('hotel_id', '')
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewHotelBookingPortals', [hotel_id])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Portals': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_hotel_portal(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        hotel_name = request.POST.get('hotel_name', '')
        hotel_email = request.POST.get('hotel_email', '')
        hotel_contact = request.POST.get('hotel_contact', '')
        website = request.POST.get('website', '')

        print(hotel_email)

        hotel_address = request.POST.get('hotel_address', '')
        contact_name = request.POST.get('contact_name', '')
        contact_email = request.POST.get('contact_email', '')
        contact_no = request.POST.get('contact_no', '')

        beneficiary_name = request.POST.get('beneficiary_name', '')
        beneficiary_account_no = request.POST.get('beneficiary_account_no', '')
        bank_name = request.POST.get('bank_name', '')
        ifsc_code = request.POST.get('ifsc_code', '')

        is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
        tds_rate = request.POST.get('tds_rate', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        if tds_rate:
            tds_rate = tds_rate
        else:
            tds_rate = 0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addHotelPortal', [hotel_name,hotel_email,hotel_contact,website,hotel_address,contact_name,contact_email,contact_no,beneficiary_name,beneficiary_account_no,
                                                    ifsc_code,is_service_tax_applicable,tds_rate,gst_id,pan_no,user_id,user_type,bank_name])
                    emp = dictfetchall(cursor)
                    print(emp)
                    data = {'success': 1, 'message': "Hotel Added Successfully", 'id':emp}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_hotel_portal(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        hotel_name = request.POST.get('hotel_name', '')
        hotel_email = request.POST.get('hotel_email', '')
        hotel_contact = request.POST.get('hotel_contact', '')
        website = request.POST.get('website', '')

        is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
        tds_rate = request.POST.get('tds_rate', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')
        portal_vendor_id = request.POST.get('portal_vendor_id', '')
        hotel_id = request.POST.get('hotel_id', '')


        if tds_rate:
            tds_rate = tds_rate
        else:
            tds_rate = 0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateHotelPortal', [hotel_name,hotel_email,hotel_contact,website,is_service_tax_applicable,tds_rate,gst_id,pan_no,user_id,user_type,hotel_id,portal_vendor_id])
                    emp = dictfetchall(cursor)
                    print(emp)
                    data = {'success': 1, 'message': "Hotel Added Successfully", 'id':emp}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def room_types(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllRoomTypes', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Types': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_corporate_management_fee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        service_fees_type_id = request.POST.get('service_fees_type_id', '')
        service_fees_type_value = request.POST.get('service_fees_type_value', '')
        service_fees_type = request.POST.get('service_fees_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addCorporateManagementFees', [corporate_id,service_fees_type_id,service_fees_type_value,service_fees_type,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': 'Management Fee Added Successfully'}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_corporate_management_fee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        service_fees_type_id = request.POST.get('service_fees_type_id', '')
        service_fees_type_value = request.POST.get('service_fees_type_value', '')
        service_fees_type = request.POST.get('service_fees_type', '')
        fees_id = request.POST.get('fees_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporateManagementFees', [corporate_id,service_fees_type_id,service_fees_type_value,service_fees_type,fees_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Management Fee Updated Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_corporate_management_fee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        fees_id = request.POST.get('fees_id', '')
        user_id = request.POST.get('user_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteCorporateManagementFees', [fees_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Management Fee Deleted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_taxi_type(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')
        type_name = request.POST.get('type_name', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addTaxiTypes', [type_name,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company,'id':company}
                    else:
                        data = {'success': 1, 'message': "Taxi Type Added Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_taxi_type(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        type_name = request.POST.get('type_name', '')
        taxitype_id = request.POST.get('taxitype_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateTaxiTypes', [type_name,taxitype_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Type Updated Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_taxi_type(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        taxitype_id = request.POST.get('taxitype_id', '')
        user_id = request.POST.get('user_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteTaxiTypes', [taxitype_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Type Deleted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_taxi_model(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        brand_name = request.POST.get('brand_name', '')
        model_name = request.POST.get('model_name', '')
        taxi_type_id = request.POST.get('taxitype_id', '')
        no_of_seats = request.POST.get('no_of_seats', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addTaxiModel', [brand_name,model_name,taxi_type_id,no_of_seats,user_id,user_type])
                    cities = dictfetchall(cursor)
                    print(cities)
                    data = {'success': 1, 'message': "Taxi Model Added Successfully", 'id' : cities}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_taxi_model(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        brand_name = request.POST.get('brand_name', '')
        model_name = request.POST.get('model_name', '')
        taxi_type_id = request.POST.get('taxitype_id', '')
        no_of_seats = request.POST.get('no_of_seats', '')
        model_id = request.POST.get('model_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateTaxiModel', [brand_name,model_name,taxi_type_id,no_of_seats,model_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Model Updated Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_taxi_model(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        model_id = request.POST.get('model_id', '')
        user_id = request.POST.get('user_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteTaxiModel', [model_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Model Deleted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def taxis(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllTaxis', [])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Taxis': cities}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_taxi(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        model_id = request.POST.get('model_id', '')
        taxi_reg_no = request.POST.get('taxi_reg_no', '')
        make_year = request.POST.get('make_year', '')
        garage_location = request.POST.get('garage_location', '')
        garage_distance = request.POST.get('garage_distance', '')

        if garage_distance:
            garage_distance = float(garage_distance)
        else:
            garage_distance = 0

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addTaxi', [model_id,taxi_reg_no,make_year,garage_location,garage_distance,user_id,user_type])
                    cities = dictfetchall(cursor)
                    print(cities)
                    data = {'success': 1, 'message': "Taxi Added Successfully",'id':cities}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_taxi(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        model_id = request.POST.get('model_id', '')
        taxi_reg_no = request.POST.get('taxi_reg_no', '')
        make_year = request.POST.get('make_year', '')
        garage_location = request.POST.get('garage_location', '')
        garage_distance = request.POST.get('garage_distance', '')

        if garage_distance:
            garage_distance = float(garage_distance)
        else:
            garage_distance = 0

        taxi_id = request.POST.get('taxi_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateTaxi', [model_id,taxi_reg_no,make_year,garage_location,garage_distance,taxi_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Updated Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_taxi(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        taxi_id = request.POST.get('taxi_id', '')
        user_id = request.POST.get('user_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteTaxi', [taxi_id,user_id,user_type])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Deleted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def taxi_models(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllTaxiModels', [])
                    cities = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Models': cities}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_billing_entity(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')
        entity_name = request.POST.get('entity_name', '')
        billing_city_id = request.POST.get('billing_city_id')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        entity_id = request.POST.get('entity_id')
        is_delete = request.POST.get('is_delete')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateBillingEntity', [user_id,corporate_id,user_type,entity_name,billing_city_id,contact_person_name,
                                                                        contact_person_email,contact_person_no,address_line_1,address_line_2,address_line_3,
                                                                        gst_id,pan_no,entity_id,is_delete])
                    result = dictfetchall(cursor)
                    cursor.close()

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Billing Entity Added Successfully"}
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_billing_entity(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')
        entity_name = request.POST.get('entity_name', '')
        billing_city_id = request.POST.get('billing_city_id')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        entity_id = request.POST.get('entity_id')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateCorporateBillingEntity', [user_id,corporate_id,user_type,entity_name,billing_city_id,contact_person_name,
                                                                        contact_person_email,contact_person_no,address_line_1,address_line_2,address_line_3,
                                                                        gst_id,pan_no,entity_id])
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Billing Entity Updated Successfully"}
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_billing_entity(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        entity_id = request.POST.get('entity_id')
        is_delete = request.POST.get('is_delete')

        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateBillingEntity',
                                    [user_id, user_type, entity_id])
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Billing Entity Deleted Successfully"}
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_cotrav_billing_entity(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')
        entity_name = request.POST.get('entity_name', '')
        billing_city_id = request.POST.get('billing_city_id')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        entity_id = request.POST.get('entity_id')
        is_delete = request.POST.get('is_delete')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCotravBillingEntity', [user_id,user_type,entity_name,billing_city_id,contact_person_name,
                                                                        contact_person_email,contact_person_no,address_line_1,address_line_2,address_line_3,
                                                                        gst_id,pan_no,entity_id,is_delete])
                    result = dictfetchall(cursor)
                    print(result)
                    cursor.close()

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Billing Entity Added Successfully"}
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_cotrav_billing_entity(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')
        entity_name = request.POST.get('entity_name', '')
        billing_city_id = request.POST.get('billing_city_id')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        entity_id = request.POST.get('entity_id')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateCotravBillingEntity', [user_id,user_type,entity_name,billing_city_id,contact_person_name,
                                                                        contact_person_email,contact_person_no,address_line_1,address_line_2,address_line_3,
                                                                        gst_id,pan_no,entity_id])
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Billing Entity Updated Successfully"}
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_cotrav_billing_entity(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        entity_id = request.POST.get('entity_id')
        is_delete = request.POST.get('is_delete')
        print("enitititi id")
        print(entity_id)
        if entity_id:
            entity_id = entity_id
        else:
            entity_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCotravBillingEntity',[user_id, user_type, entity_id])
                    cursor.close()
                    company = dictfetchall(cursor)
                    print(company)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Billing Entity Deleted Successfully"}
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_group(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')
        group_name = request.POST.get('group_name', '')
        zone_name = request.POST.get('zone_name')

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cid = request.POST.get('cid', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')
        access_token = request.POST.get('access_token_auth', '')
        password = request.POST.get('password', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateGroup', [user_id,corporate_id,user_type,group_name,zone_name,name,email,cid,contact_no,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,access_token,password])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(name, email, "taxi123", "Approver 2")
                        data = {'success': 1, 'message': "Company Group Added Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_group(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        group_id = request.POST.get('group_id', '')

        user_id = request.POST.get('user_id', '')
        group_name = request.POST.get('group_name', '')
        zone_name = request.POST.get('zone_name')

        if group_id:
            group_id = group_id
        else:
            group_id = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateGroupDetails', [group_id,group_name,zone_name,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company Group Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_group(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        group_id = request.POST.get('group_id', '')
        user_id = request.POST.get('user_id', '')

        if group_id:
            group_id = group_id
        else:
            group_id = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteGroupDetails', [group_id,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company Group Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_subgroup(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        print("dsasdasdasd")
        user_id = request.POST.get('user_id', '')
        subgroup_name = request.POST.get('subgroup_name', '')
        group_id = request.POST.get('group_id', '')

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cid = request.POST.get('cid', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')
        access_token = request.POST.get('access_token_auth', '')
        password = request.POST.get('password', '')
        print(password)
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateSubGroup', [user_id,corporate_id,user_type,subgroup_name,group_id,name,email,cid,contact_no,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,access_token,password])
                    print(subgroup_name)
                    company = dictfetchall(cursor)
                    print(company)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(name, email, "taxi123", "Approver 1")
                        data = {'success': 1, 'message': "Data Insert Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    print(e)
                    print("Exception")
                    data = {'success': 0, 'message': "Error in Data Insert"+e}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_subgroup(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')
        user_id = request.POST.get('user_id', '')
        subgroup_name = request.POST.get('group_name', '')

        if subgroup_id:
            subgroup_id = subgroup_id
        else:
            subgroup_id = '0'

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateSubGroupDetails', [subgroup_id,subgroup_name,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company SubGroup Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_subgroup(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        subgroup_id = request.POST.get('subgroup_id', '')
        user_id = request.POST.get('user_id', '')

        if subgroup_id:
            subgroup_id = subgroup_id
        else:
            subgroup_id = '0'

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteSubGroupDetails', [subgroup_id,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company SubGroup Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_group_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cid = request.POST.get('cid', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        group_id = request.POST.get('group_id')

        is_delete = request.POST.get('delete_id')
        access_token = request.POST.get('access_token_auth', '')
        password = request.POST.get('password', '')
        group_auth_id = request.POST.get('group_auth_id', '')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if group_id:
            group_id = group_id
        else:
            group_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateGroupAuthenticator', [user_id,corporate_id,user_type,name,email,cid,contact_no,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,group_id,is_delete,access_token,password,group_auth_id])

                    company = dictfetchall(cursor)

                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(name, email, "taxi123", "Approver 2")
                        data = {'success': 1, 'message': "Company Group Authenticator Added Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_group_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        user_id = request.POST.get('user_id', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cid = request.POST.get('cid', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        group_auth_id = request.POST.get('group_auth_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateCorporateGroupAuthenticator', [user_id,corporate_id,user_type,name,email,cid,contact_no,is_radio,is_local,
                        is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,is_water_bottles,is_reverse_logistics,group_auth_id])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company Group Authenticator Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_group_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        group_auth_id = request.POST.get('group_auth_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteGroupAuthenticator', [group_auth_id,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company Group Authenticator Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_subgroup_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cid = request.POST.get('cid', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        subgroup_id = request.POST.get('subgroup_id')

        is_delete = request.POST.get('delete_id')
        access_token = request.POST.get('access_token_auth', '')
        password = request.POST.get('password', '')
        subgroup_auth_id = request.POST.get('subgroup_auth_id', '')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if subgroup_id:
            subgroup_id = subgroup_id
        else:
            subgroup_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateSubGroupAuthenticator', [user_id,corporate_id,user_type,name,email,cid,contact_no,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,subgroup_id,is_delete,access_token,password,subgroup_auth_id])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(name, email, "taxi123", "Approver 1")
                        data = {'success': 1, 'message': "Company SubGroup Authenticator Added Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_subgroup_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        user_id = request.POST.get('user_id', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        cid = request.POST.get('cid', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')
        subgroup_auth_id = request.POST.get('subgroup_auth_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateCorporateSubGroupAuthenticator', [user_id,corporate_id,user_type,name,email,cid,contact_no,is_radio,is_local,
                        is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,is_water_bottles,is_reverse_logistics,subgroup_auth_id])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company SubGroup Authenticator Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_subgroup_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        subgroup_auth_id = request.POST.get('subgroup_auth_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteSubGroupAuthenticator', [subgroup_auth_id,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Company SubGroup Authenticator Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_admin(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')

        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        is_delete = request.POST.get('delete_id')
        access_token = request.POST.get('access_token_auth', '')
        password = request.POST.get('password', '')
        admin_id = request.POST.get('admin_id', '')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '0'

        if admin_id:
            admin_id = admin_id
        else:
            admin_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateAdmin', [user_id,corporate_id,user_type,name,email,contact_no,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,is_delete,access_token,password,admin_id])
                    company = dictfetchall(cursor)
                    
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(name, email, "taxi123", "Admin")

                        data = {'success': 1, 'message': "Corporate Admin Added Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_admin(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        user_id = request.POST.get('user_id', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        contact_no = request.POST.get('contact_no', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        admin_id = request.POST.get('admin_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateCorporateAdmin', [user_id,corporate_id,user_type,name,email,contact_no,is_radio,is_local,
                        is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,is_water_bottles,is_reverse_logistics,admin_id])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Admin Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_admin(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        admin_id = request.POST.get('admin_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateAdmin', [admin_id,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Admin Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_spoc(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')

        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')
        user_cid = request.POST.get('user_cid', '')

        user_name = request.POST.get('user_name', '')
        user_contact = request.POST.get('user_contact', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        budget = request.POST.get('budget')
        expense = request.POST.get('expense')

        is_radio = request.POST.get('is_radio')
        is_local = request.POST.get('is_local')
        is_outstation = request.POST.get('is_outstation')
        is_bus = request.POST.get('is_bus')
        is_train = request.POST.get('is_train')
        is_hotel = request.POST.get('is_hotel')
        is_meal = request.POST.get('is_meal')
        is_flight = request.POST.get('is_flight')
        is_water_bottles = request.POST.get('is_water_bottles')
        is_reverse_logistics = request.POST.get('is_reverse_logistics')

        is_delete = request.POST.get('delete_id')
        access_token = request.POST.get('access_token_auth', '')
        password = request.POST.get('password', '')
        spoc_id = request.POST.get('spoc_id')

        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = 0

        if budget:
            budget = budget
        else:
            budget = 0

        if expense:
            expense = expense
        else:
            expense = 0

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = 0
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateSpoc', [user_id,corporate_id,user_type,group_id,subgroup_id,user_cid,user_name,user_contact,email,username,
                                                            budget,expense,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,is_delete,access_token,password,spoc_id])
                    company = dictfetchall(cursor)
                    print(company)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(user_name, email, "taxi123", "Spoc")
                        data = {'success': 1, 'message': "Corporate Spoc Added Successfully"}
                    cursor.close()

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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_spoc(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        user_id = request.POST.get('user_id', '')

        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')
        user_cid = request.POST.get('user_cid', '')

        user_name = request.POST.get('user_name', '')
        user_contact = request.POST.get('user_contact', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        budget = request.POST.get('budget', '')
        expense = request.POST.get('expense', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        is_delete = request.POST.get('delete_id')
        access_token = request.POST.get('access_token_auth', '')
        spoc_id = request.POST.get('spoc_id')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateCorporateSpoc', [user_id,corporate_id,user_type,group_id,subgroup_id,user_cid,user_name,user_contact,email,username,
                                                            budget,expense,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,is_delete,spoc_id])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Spoc Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_spoc(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        spoc_id = request.POST.get('spoc_id', '')
        delete_id = request.POST.get('delete_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateSpoc', [spoc_id,user_id,user_type,delete_id])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Spoc Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def active_spoc(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        spoc_id = request.POST.get('spoc_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('activeCorporateSpoc', [spoc_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Spoc Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_employee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')

        user_id = request.POST.get('user_id', '')

        spoc_id = request.POST.get('spoc_id')
        billing_entity_id = request.POST.get('billing_entity_id', '')
        core_employee_id = request.POST.get('core_employee_id', '')
        employee_cid = request.POST.get('employee_cid', '')

        employee_name = request.POST.get('employee_name', '')
        employee_email = request.POST.get('employee_email', '')
        employee_contact = request.POST.get('employee_contact', '')
        age = request.POST.get('age', '')
        gender = request.POST.get('gender')
        id_proof_type = request.POST.get('id_proof_type')

        id_proof_no = request.POST.get('id_proof_no', '')
        is_active = request.POST.get('is_active', '')
        has_dummy_email = 0
        fcm_regid = request.POST.get('fcm_regid', '')
        is_cxo = request.POST.get('is_cxo', '')
        designation = request.POST.get('designation', '')
        home_city = request.POST.get('home_city', '')
        home_address = request.POST.get('home_address', '')
        reporting_manager = request.POST.get('reporting_manager', '')
        employee_band = request.POST.get('employee_band', '')
        
        
        assistant_id = request.POST.get('assistant_id', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        if date_of_birth:
            date_of_birth = datetime.strptime(date_of_birth, '%d-%m-%Y')
        else:
            date_of_birth = None

        is_delete = request.POST.get('delete_id')
        password = request.POST.get('password', '')
        employee_id = request.POST.get('employee_id')
        username = request.POST.get('username')

        if employee_id:
            employee_id = employee_id
        else:
            employee_id = '0'

        if is_delete:
            is_delete = is_delete
        else:
            is_delete = '0'

        if assistant_id:
            assistant_id = assistant_id
        else:
            assistant_id = 0
        
        if reporting_manager:
            reporting_manager = reporting_manager
        else:
            reporting_manager = 0

        if age:
            pass
        else:
            age = 0
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('addNewCorporateEmployee', [user_id,user_type,spoc_id, core_employee_id, employee_cid,
                    employee_name, employee_email, employee_contact, age, gender, id_proof_type, id_proof_no, is_active, has_dummy_email,
                    fcm_regid, is_cxo, designation, home_city, home_address, assistant_id, date_of_birth,is_delete,employee_id,
                    billing_entity_id,corporate_id,password,username,reporting_manager,employee_band])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(employee_name, employee_email, "taxi123", "Employee")
                        data = {'success': 1, 'message': "Corporate Employee Added Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_employee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        user_id = request.POST.get('user_id', '')

        spoc_id = request.POST.get('spoc_id')
        billing_entity_id = request.POST.get('billing_entity_id', '')
        core_employee_id = request.POST.get('core_employee_id', '')
        employee_cid = request.POST.get('employee_cid', '')

        employee_name = request.POST.get('employee_name', '')
        employee_email = request.POST.get('employee_email', '')
        employee_contact = request.POST.get('employee_contact', '')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        id_proof_type = request.POST.get('id_proof_type')

        id_proof_no = request.POST.get('id_proof_no', '')
        is_active = request.POST.get('is_active')
        has_dummy_email = 0
        fcm_regid = request.POST.get('fcm_regid')
        is_cxo = request.POST.get('is_cxo')
        designation = request.POST.get('designation', '')
        home_city = request.POST.get('home_city', '')
        home_address = request.POST.get('home_address', '')
        assistant_id = request.POST.get('assistant_id', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        reporting_manager = request.POST.get('reporting_manager', '')
        employee_band = request.POST.get('employee_band', '')

        if date_of_birth and date_of_birth != 'None':
            date_of_birth = datetime.strptime(date_of_birth, '%d-%m-%Y')
        else:
            date_of_birth = None

        if is_cxo == '0':
            assistant_id = 0

        employee_id = request.POST.get('employee_id')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('updateEmployeeDetails', [user_id,user_type,spoc_id, core_employee_id, employee_cid,
                    employee_name, employee_email, employee_contact, age, gender, id_proof_type, id_proof_no, is_active, has_dummy_email,
                    fcm_regid, is_cxo, designation, home_city, home_address, assistant_id, date_of_birth,employee_id,billing_entity_id,reporting_manager,employee_band])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Employee Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_employee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        employee_id = request.POST.get('employee_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateEmployee', [employee_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Corporate Employee Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)

def add_agent(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        emp_id = request.POST.get('emp_id', '')
        username = request.POST.get('username', '')
        contact_no = request.POST.get('contact_no', '')
        email = request.POST.get('email', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        has_billing_access = request.POST.get('has_billing_access', '')
        has_voucher_payment_access = request.POST.get('has_voucher_payment_access', '')
        has_voucher_approval_access = request.POST.get('has_voucher_approval_access', '')
        is_super_admin = request.POST.get('is_super_admin', '')

        password = request.POST.get('password', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('addAgent', [emp_id, username, contact_no,email,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,
                                                          is_meal,is_flight,is_water_bottles,is_reverse_logistics,has_billing_access,
                                                          has_voucher_payment_access,has_voucher_approval_access,is_super_admin,password,user_id,
                                                          user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        add_user = newUserAdd_Email()
                        resp1 = add_user.new_user_send_email(username, email, "taxi123", "Agent")
                        data = {'success': 1, 'message': "Agent Added Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_agent(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        emp_id = request.POST.get('emp_id', '')
        username = request.POST.get('username', '')
        contact_no = request.POST.get('contact_no', '')
        email = request.POST.get('email', '')

        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')

        has_billing_access = request.POST.get('has_billing_access', '')
        has_voucher_payment_access = request.POST.get('has_voucher_payment_access', '')
        has_voucher_approval_access = request.POST.get('has_voucher_approval_access', '')
        is_super_admin = request.POST.get('is_super_admin', '')

        agent_id = request.POST.get('agent_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('updateAgent', [emp_id, username, contact_no,email,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,
                                                          is_meal,is_flight,is_water_bottles,is_reverse_logistics,has_billing_access,
                                                          has_voucher_payment_access,has_voucher_approval_access,is_super_admin,user_id,
                                                          user_type,agent_id])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Agent Updated Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_agent(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        agent_id = request.POST.get('agent_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteAgent', [user_id,user_type,agent_id])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Agent Deleted Successfully"}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_group(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        group_id = request.POST.get('group_id', '')

        if group_id:
            group_id = group_id
        else:
            group_id = '0'
        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewGroupDetails', [group_id])
                    group = dictfetchall(cursor)
                    data = {'success': 1, 'Groups': group}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_group_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        group_id = request.POST.get('group_id', '')

        if group_id:
            group_id = group_id
        else:
            group_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateGroupsAuthenticator', [group_id])
                    group = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Groups': group}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_subgroup(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        subgroup_id = request.POST.get('subgroup_id', '')

        if subgroup_id:
            subgroup_id = subgroup_id
        else:
            subgroup_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewSubGroupDetails', [subgroup_id])
                    group = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'SubGroups': group}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_subgroup_auth(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        subgroup_id = request.POST.get('subgroup_id', '')

        if subgroup_id:
            subgroup_id = subgroup_id
        else:
            subgroup_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateSubGroupsAuthenticator', [subgroup_id])
                    group = dictfetchall(cursor)
                    data = {'success': 1, 'SubGroups': group}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_auth_1(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        auth_id = request.POST.get('auth_id', '')

        if auth_id:
            auth_id = auth_id
        else:
            auth_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewSubGroupsAuthenticator', [auth_id])
                    group = dictfetchall(cursor)
                    data = {'success': 1, 'Authenticator': group}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_auth_2(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        auth_id = request.POST.get('auth_id', '')

        if auth_id:
            auth_id = auth_id
        else:
            auth_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewGroupsAuthenticator', [auth_id])
                    group = dictfetchall(cursor)
                    data = {'success': 1, 'Authenticator': group}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)
    

def view_spoc(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')

        if spoc_id:
            spoc_id = spoc_id
        else:
            spoc_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewSpocDetails', [spoc_id])
                    spoc = dictfetchall(cursor)
                    data = {'success': 1, 'Spoc': spoc}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_employee(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        employee_id = request.POST.get('employee_id', '')

        if employee_id:
            employee_id = employee_id
        else:
            employee_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewEmployeeDetails', [employee_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Employee': emp}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_agent(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        agent_id = request.POST.get('agent_id', '')

        if agent_id:
            agent_id = agent_id
        else:
            agent_id = '0'
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewAgentDetails', [agent_id])
                    agent = dictfetchall(cursor)
                    data = {'success': 1, 'Agent': agent}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def assessment_codes(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id;
        else:
            corporate_id = 0;

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateAssessmentCodes', [corporate_id])
                    agent = dictfetchall(cursor)
                    data = {'success': 1, 'Codes': agent}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_assessment_codes(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        code_desc = request.POST.get('code_desc', '')
        from_date = request.POST.get('from_date', '')
        from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('to_date', '')
        to_date = datetime.strptime(to_date, '%d-%m-%Y')
        service_from = request.POST.get('service_from', '')
        service_from = datetime.strptime(service_from, '%d-%m-%Y')
        service_to = request.POST.get('service_to', '')
        service_to = datetime.strptime(service_to, '%d-%m-%Y')

        if from_date:
            pass
        else:
            from_date = None

        if to_date:
            pass
        else:
            to_date = None

        if service_from:
            pass
        else:
            service_from = None

        if service_to:
            pass
        else:
            service_to = None

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addCorporateAssessmentCodes', [corporate_id,assessment_code,code_desc,from_date,to_date,user_id,user_type,service_from,service_to])
                    agent = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Assessment Code Added Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_assessment_codes(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        code_desc = request.POST.get('code_desc', '')
        from_date = request.POST.get('from_date', '')
        from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('to_date', '')
        to_date = datetime.strptime(to_date, '%d-%m-%Y')
        code_id = request.POST.get('code_id', '')
        service_from = request.POST.get('service_from', '')
        service_from = datetime.strptime(service_from, '%d-%m-%Y')
        service_to = request.POST.get('service_to', '')
        service_to = datetime.strptime(service_to, '%d-%m-%Y')

        if from_date:
            pass
        else:
            from_date = None

        if to_date:
            pass
        else:
            to_date = None

        if service_from:
            pass
        else:
            service_from = None

        if service_to:
            pass
        else:
            service_to = None
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporateAssessmentCodes', [corporate_id,assessment_code,code_desc,from_date,to_date,code_id,user_id,user_type,service_from,service_to])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Assessment Code Updated Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_assessment_codes(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        code_id = request.POST.get('code_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteCorporateAssessmentCodes', [code_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Assessment Code Deleted Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def assessment_cities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id;
        else:
            corporate_id = 0;
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateAssessmentCities', [corporate_id])
                    agent = dictfetchall(cursor)
                    data = {'success': 1, 'Cities': agent}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_assessment_cities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        city_name = request.POST.get('city_name', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addCorporateAssessmentCity', [corporate_id,city_name,user_id,user_type])
                    company = dictfetchall(cursor)
                    print(company)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Assessment City Added Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error11': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def update_assessment_cities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        city_name = request.POST.get('city_name', '')
        city_id = request.POST.get('city_id')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporateAssessmentCity', [corporate_id,city_name,city_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Assessment City Updated Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def delete_assessment_cities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        city_id = request.POST.get('city_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteCorporateAssessmentCity', [city_id,user_id,user_type])

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Assessment City Deleted Successfully"}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_agents(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAgentsDetails', [])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Agents': emp}
                    cursor.close()
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


################################## Taxi Booking  ###############################

def view_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewTaxiBooking', [booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    cursor1 = connection.cursor()
                    booking_id = emp[0]['id']
                    print(booking_id)
                    cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    cursor1.close()

                    cursor3 = connection.cursor()
                    cursor3.callproc('getAllTaxiBookingsActionLogs', [booking_id])
                    actions = dictfetchall(cursor3)
                    cursor3.close()

                    if emp[0]['is_invoice']:
                        cursor2 = connection.cursor()
                        invoice_id = emp[0]['invoice_id']
                        print(invoice_id)
                        print("iiiiiiinnnnnvvvvvoooo")
                        cursor2.callproc('getallTaxiInvoiceActionLog', [invoice_id])
                        invoicess = dictfetchall(cursor2)
                        emp[0]['InvoiceActionLog'] = invoicess
                        cursor2.close()

                    emp[0]['Passangers'] = passanger
                    emp[0]['ActionLogs'] = actions
                    data = {'success': 1, 'Bookings': emp}

                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewBusBooking', [booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    cursor1 = connection.cursor()
                    booking_id = emp[0]['id']
                    print(booking_id)
                    cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    cursor1.close()

                    cursor3 = connection.cursor()
                    cursor3.callproc('getAllBusBookingsActionLogs', [booking_id])
                    actions = dictfetchall(cursor3)
                    cursor3.close()

                    if emp[0]['is_invoice']:
                        cursor2 = connection.cursor()
                        invoice_id = emp[0]['invoice_id']
                        print(invoice_id)
                        print("iiiiiiinnnnnvvvvvoooo")
                        cursor2.callproc('getallTaxiInvoiceActionLog', [invoice_id])
                        invoicess = dictfetchall(cursor2)
                        emp[0]['InvoiceActionLog'] = invoicess
                        cursor2.close()

                    emp[0]['Passangers'] = passanger
                    emp[0]['ActionLogs'] = actions
                    data = {'success': 1, 'Bookings': emp}

                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_train_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewTrainBooking', [booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    cursor1 = connection.cursor()
                    booking_id = emp[0]['id']

                    cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    cursor1.close()

                    cursor3 = connection.cursor()
                    cursor3.callproc('getAllTrainBookingsActionLogs', [booking_id])
                    actions = dictfetchall(cursor3)
                    cursor3.close()

                    if emp[0]['is_invoice']:
                        cursor2 = connection.cursor()
                        invoice_id = emp[0]['invoice_id']
                        print(invoice_id)
                        print("iiiiiiinnnnnvvvvvoooo")
                        cursor2.callproc('getallTaxiInvoiceActionLog', [invoice_id])
                        invoicess = dictfetchall(cursor2)
                        emp[0]['InvoiceActionLog'] = invoicess
                        cursor2.close()

                    emp[0]['Passangers'] = passanger
                    emp[0]['ActionLogs'] = actions

                    data = {'success': 1, 'Bookings': emp}

                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_hotel_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:

                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewHotelBooking', [booking_id])
                    emp = dictfetchall(cursor)
                    print(emp)
                    cursor.close()
                    cursor1 = connection.cursor()
                    booking_id = emp[0]['id']
                    print(booking_id)

                    cursor1.callproc('getAllHotelBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    cursor1.close()

                    cursor3 = connection.cursor()
                    cursor3.callproc('getAllHotelBookingsActionLogs', [booking_id])
                    actions = dictfetchall(cursor3)
                    cursor3.close()

                    if emp[0]['is_invoice']:
                        cursor2 = connection.cursor()
                        invoice_id = emp[0]['invoice_id']
                        print(invoice_id)
                        print("iiiiiiinnnnnvvvvvoooo")
                        cursor2.callproc('getallTaxiInvoiceActionLog', [invoice_id])
                        invoicess = dictfetchall(cursor2)
                        emp[0]['InvoiceActionLog'] = invoicess
                        cursor2.close()

                    emp[0]['Passangers'] = passanger
                    emp[0]['ActionLogs'] = actions

                    data = {'success': 1, 'Bookings': emp}

                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def view_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewFlightBooking', [booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    cursor1 = connection.cursor()
                    booking_id = emp[0]['id']


                    cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    cursor1.close()

                    cursor2 = connection.cursor()
                    cursor2.callproc('getAllFlightBookingFlights', [booking_id])
                    flights = dictfetchall(cursor2)
                    cursor2.close()

                    cursor3 = connection.cursor()
                    cursor3.callproc('getAllFlightBookingsActionLogs', [booking_id])
                    actions = dictfetchall(cursor3)
                    cursor3.close()

                    if emp[0]['is_invoice']:
                        cursor2 = connection.cursor()
                        invoice_id = emp[0]['invoice_id']
                        cursor2.callproc('getallTaxiInvoiceActionLog', [invoice_id])
                        invoicess = dictfetchall(cursor2)
                        emp[0]['InvoiceActionLog'] = invoicess
                        cursor2.close()

                    emp[0]['Passangers'] = passanger
                    emp[0]['Flights'] = flights
                    emp[0]['ActionLogs'] = actions
                    data = {'success': 1, 'Bookings': emp}

                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_city_name(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        city_name = request.POST.get('city_name', '')
        state_id = request.POST.get('state_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addCities', [city_name,state_id])
                    result = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Data Insert Successfully",'id':result}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_state_name(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        city_state = request.POST.get('city_state', '')
        country_id = request.POST.get('country_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addState', [city_state,country_id])
                    result = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Data Insert Successfully",'id':result}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_country_name(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        city_country = request.POST.get('city_country', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addCountry', [city_country])
                    result = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Data Insert Successfully",'id':result}
                    cursor.close()
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        booking_email = request.POST.get('booking_email', '')
        entity_id = request.POST.get('entity_id', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        tour_type = request.POST.get('tour_type', '')
        pickup_city = request.POST.get('pickup_city', '')
        pickup_location = request.POST.get('pickup_location', '')
        drop_location = request.POST.get('drop_location', '')
        pickup_datetime = request.POST.get('pickup_datetime', '')
        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            booking_datetime = datetime.strptime(booking_datetime, '%d-%m-%Y %H:%M:%S')
        else:
            timezone.activate(pytz.timezone("Asia/Kolkata"))
            booking_datetime = timezone.localtime(timezone.now())
            print(booking_datetime)
        pickup_datetime = datetime.strptime(pickup_datetime, '%d-%m-%Y %H:%M:%S')
        taxi_type = request.POST.get('taxi_type')
        package_id = request.POST.get('package_id')
        no_of_days = request.POST.get('no_of_days', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')
        is_sms = request.POST.get('is_sms', '')
        is_email = request.POST.get('is_email', '')

        if booking_email:
            pass
        else:
            booking_email=''

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

        if assessment_code:
            pass
        else:
            assessment_code =0

        if assessment_city_id:
            pass
        else:
            assessment_city_id =0

        if booking_datetime:
            pass
        else:
            timezone.activate(pytz.timezone("Asia/Kolkata"))
            booking_datetime = timezone.localtime(timezone.now())  # change field

        reason_booking = request.POST.get('reason_booking', '')
        no_of_seats = request.POST.get('no_of_seats', '')

        employees = request.POST.getlist('employees', '')
        employees = ",".join(employees)
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addTaxiBooking', [user_type,user_id,entity_id,corporate_id,spoc_id,group_id,subgroup_id,tour_type,pickup_city,pickup_location,drop_location,pickup_datetime,
                                                             taxi_type,package_id,no_of_days,reason_booking,no_of_seats,assessment_code,assessment_city_id,employees,booking_datetime,booking_email,'@last_booking_id'])
                    booking_id = dictfetchall(cursor)
                    if booking_id:
                        data = {'success': 0, 'message': booking_id}
                    else:
                        cursor.execute("SELECT @last_booking_id")
                        last_booking_id = cursor.fetchone()[0]
                        print(last_booking_id)
                        cursor.close()
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewTaxiBooking', [last_booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllTaxiBookingPassangers', [last_booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        cursor3 = connection.cursor()
                        cursor3.callproc('getAllApproverByBookingID', [last_booking_id])
                        approvers = dictfetchall(cursor3)
                        cursor3.close()

                        add_booking_email = AddBooking_Email()
                        if is_email == '1':
                            resp6 = add_booking_email.send_taxi_email(emp, approvers, "Taxi")
                        if is_sms == '1':
                            resp1 = add_booking_email.send_taxi_msg(emp, approvers, "Taxi")


                        data = {'success': 1, 'message': "Insert Successfully"}
                        return JsonResponse(data)
                    return JsonResponse(data)
                except Exception as e:
                    print(e)
                    data = {'success': 0, 'message': e}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        booking_email = request.POST.get('booking_email', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        from_location = request.POST.get('from', '')
        to_location = request.POST.get('to', '')
        bus_type = request.POST.get('bus_type', '')
        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            booking_datetime = datetime.strptime(booking_datetime, '%d-%m-%Y %H:%M:%S')
        else:
            timezone.activate(pytz.timezone("Asia/Kolkata"))
            booking_datetime = timezone.localtime(timezone.now())
            print(booking_datetime)

        journey_datetime = request.POST.get('journey_datetime', '')
        journey_datetime = datetime.strptime(journey_datetime, '%d-%m-%Y %H:%M:%S')
        journey_datetime_to = request.POST.get('journey_datetime_to', '')
        journey_datetime_to = datetime.strptime(journey_datetime_to, '%d-%m-%Y %H:%M:%S')
        entity_id = request.POST.get('entity_id', '')
        preferred_bus = request.POST.get('preferred_bus', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')
        is_email = request.POST.get('is_email', '')
        is_sms = request.POST.get('is_sms', '')

        if booking_email:
            pass
        else:
            booking_email=''

        if assessment_code:
            pass
        else:
            assessment_code=0

        if assessment_city_id:
            pass
        else:
            assessment_city_id=0

        reason_booking = request.POST.get('reason_booking', '')
        no_of_seats = request.POST.get('no_of_seats', '')

        employees = request.POST.getlist('employees', '')
        employees = ",".join(employees)
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addBusBooking', [user_type,user_id,corporate_id,spoc_id,group_id,subgroup_id,from_location,
                                                      to_location,bus_type,bus_type,bus_type,booking_datetime,journey_datetime,
                                                             entity_id,preferred_bus,reason_booking,no_of_seats,assessment_code,assessment_city_id,employees,booking_email,journey_datetime_to,'@last_booking_id'])
                    booking_id = dictfetchall(cursor)
                    if booking_id:
                        data = {'success': 0, 'message': booking_id}
                    else:
                        cursor.execute("SELECT @last_booking_id")
                        last_booking_id = cursor.fetchone()[0]
                        print(last_booking_id)
                        cursor.close()
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewBusBooking', [last_booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllBusBookingPassangers', [last_booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        cursor3 = connection.cursor()
                        cursor3.callproc('getAllApproverByBookingID', [last_booking_id])
                        approvers = dictfetchall(cursor3)
                        cursor3.close()

                        add_booking_email = AddBooking_Email()
                        if is_email  == '1':
                            resp6 = add_booking_email.send_taxi_email(emp, approvers, "Bus")
                        if is_sms == '1':
                            resp1 = add_booking_email.send_taxi_msg(emp, approvers, "Bus")


                    cursor.close()
                    data = {'success': 1, 'message': "Insert Success"}
                    return JsonResponse(data)

                except Exception as e:
                    print(e)
                    data = {'success': 0, 'message': "Error in Data Insert"}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_train_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        booking_email = request.POST.get('booking_email', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        from_location = request.POST.get('from', '')
        to_location = request.POST.get('to', '')
        train_type = request.POST.get('train_type', '')
        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            booking_datetime = datetime.strptime(booking_datetime, '%d-%m-%Y %H:%M:%S')
        else:
            timezone.activate(pytz.timezone("Asia/Kolkata"))
            booking_datetime = timezone.localtime(timezone.now())
            print(booking_datetime)

        journey_datetime = request.POST.get('journey_datetime', '')
        journey_datetime = datetime.strptime(journey_datetime, '%d-%m-%Y %H:%M:%S')
        journey_datetime_to = request.POST.get('journey_datetime_to', '')
        journey_datetime_to = datetime.strptime(journey_datetime_to, '%d-%m-%Y %H:%M:%S')
        entity_id = request.POST.get('entity_id', '')
        preferred_train = request.POST.get('preferred_train', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')
        is_email = request.POST.get('is_email', '')
        is_sms = request.POST.get('is_sms', '')

        if booking_email:
            pass
        else:
            booking_email=''

        if assessment_code:
            pass
        else:
            assessment_code=0

        if assessment_city_id:
            pass
        else:
            assessment_city_id=0

        reason_booking = request.POST.get('reason_booking', '')
        no_of_seats = request.POST.get('no_of_seats', '')

        employees = request.POST.getlist('employees', '')
        employees = ",".join(employees)
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addTrainBooking', [user_type,user_id,corporate_id,spoc_id,group_id,subgroup_id,from_location,
                                                      to_location,train_type,train_type,train_type,booking_datetime,journey_datetime,
                                                             entity_id,preferred_train,reason_booking,no_of_seats,assessment_code,assessment_city_id,employees,booking_email,journey_datetime_to,'@last_booking_id'])
                    booking_id = dictfetchall(cursor)
                    print(booking_id)
                    if booking_id:
                        data = {'success': 0, 'message': booking_id}
                    else:
                        cursor.execute("SELECT @last_booking_id")
                        last_booking_id = cursor.fetchone()[0]
                        print(last_booking_id)
                        cursor.close()
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewTrainBooking', [last_booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllTrainBookingPassangers', [last_booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        cursor3 = connection.cursor()
                        cursor3.callproc('getAllApproverByBookingID', [last_booking_id])
                        approvers = dictfetchall(cursor3)
                        cursor3.close()

                        add_booking_email = AddBooking_Email()
                        if is_email == '1':
                            resp6 = add_booking_email.send_taxi_email(emp, approvers, "Train")
                        if is_sms == '1':
                            resp1 = add_booking_email.send_taxi_msg(emp, approvers, "Train")


                    cursor.close()
                    for id in booking_id:
                        for e in employees:
                            try:
                                cursor = connection.cursor()
                                cursor.callproc('addEmployeeTrainBooking',[id['id'],e])
                                booking_id = dictfetchall(cursor)

                                cursor.close()
                                data = {'success': 1, 'message': "Insert Success"}
                                return JsonResponse(data)
                            except Exception as e:
                                data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                                return JsonResponse(data)
                    else:
                        data = {'success': 1, 'message': "Insert Success"}
                        return JsonResponse(data)

                except Exception as e:
                    print(e)
                    data = {'success': 0, 'message': "Error in Data Insert"}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_hotel_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        booking_email = request.POST.get('booking_email', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        from_city_id = request.POST.get('from_city_id', '')
        from_area_id = request.POST.get('from_area_id', '')
        preferred_area = request.POST.get('preferred_area', '')
        bucket_priority_1 = request.POST.get('bucket_priority_1', '')
        bucket_priority_2 = request.POST.get('bucket_priority_2', '')
        room_type_id = request.POST.get('room_type_id', '')

        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            booking_datetime = datetime.strptime(booking_datetime, '%d-%m-%Y %H:%M:%S')
        else:
            timezone.activate(pytz.timezone("Asia/Kolkata"))
            booking_datetime = timezone.localtime(timezone.now())
            print(booking_datetime)
        
        checkin_datetime = request.POST.get('checkin_datetime', '')
        checkin_datetime = datetime.strptime(checkin_datetime, '%d-%m-%Y %H:%M:%S')
        checkout_datetime = request.POST.get('checkout_datetime', '')
        checkout_datetime = datetime.strptime(checkout_datetime, '%d-%m-%Y %H:%M:%S')

        preferred_hotel= request.POST.get('preferred_hotel','')
        billing_entity_id = request.POST.get('billing_entity_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')
        is_email = request.POST.get('is_email', '')
        is_sms = request.POST.get('is_sms', '')

        if booking_email:
            pass
        else:
            booking_email=''

        if assessment_code:
            pass
        else:
            assessment_code=0

        if assessment_city_id:
            pass
        else:
            assessment_city_id=0

        reason_booking = request.POST.get('reason_booking', '')
        no_of_seats = request.POST.get('no_of_seats', '')

        employees = request.POST.getlist('employees', '')
        employees = ",".join(employees)
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addHotelBooking', [from_city_id,from_area_id,preferred_area,checkin_datetime,checkout_datetime,bucket_priority_1,bucket_priority_2,
                                                      room_type_id,preferred_hotel,booking_datetime,assessment_code,assessment_city_id,no_of_seats,
                                                             group_id,subgroup_id,spoc_id,corporate_id,billing_entity_id,reason_booking,user_id,user_type,employees,booking_email,'@last_booking_id'])
                    booking_id = dictfetchall(cursor)
                    if booking_id:
                        data = {'success': 0, 'message': booking_id}
                    else:
                        cursor.execute("SELECT @last_booking_id")
                        last_booking_id = cursor.fetchone()[0]
                        print(last_booking_id)
                        cursor.close()
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewHotelBooking', [last_booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllHotelBookingPassangers', [last_booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        cursor3 = connection.cursor()
                        cursor3.callproc('getAllApproverByBookingID', [last_booking_id])
                        approvers = dictfetchall(cursor3)
                        cursor3.close()

                        add_booking_email = AddBooking_Email()
                        if is_email == '1':
                            resp6 = add_booking_email.send_taxi_email(emp, approvers, "Hotel")
                        if is_sms == '1':
                            resp1 = add_booking_email.send_taxi_msg(emp, approvers, "Hotel")



                    data = {'success': 1, 'message': "Insert Success"}
                    return JsonResponse(data)

                except Exception as e:
                    print("EXCEPTION")
                    print(e)
                    data = {'success': 0, 'message': "Error in Data Insert"}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        booking_email = request.POST.get('booking_email', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        usage_type = request.POST.get('usage_type', '')
        journey_type = request.POST.get('trip_type', '')
        flight_class = request.POST.get('seat_type', '')
        from_location = request.POST.get('from_city', '')
        to_location = request.POST.get('to_city', '')

        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            booking_datetime = datetime.strptime(booking_datetime, '%d-%m-%Y %H:%M:%S')
        else:
            timezone.activate(pytz.timezone("Asia/Kolkata"))
            booking_datetime = timezone.localtime(timezone.now())
            print(booking_datetime)

        departure_datetime = request.POST.get('departure_datetime', '')
        departure_datetime = datetime.strptime(departure_datetime, '%d-%m-%Y')

        preferred_flight= request.POST.get('preferred_flight','')
        billing_entity_id = request.POST.get('billing_entity_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')
        is_sms = request.POST.get('is_sms', '')
        is_email = request.POST.get('is_email', '')

        if booking_email:
            pass
        else:
            booking_email=''

        if assessment_code:
            pass
        else:
            assessment_code=0

        if assessment_city_id:
            pass
        else:
            assessment_city_id=0

        reason_booking = request.POST.get('reason_booking', '')
        no_of_seats = request.POST.get('no_of_seats', '')
        employees = request.POST.getlist('employees', '')
        employees = ",".join(employees)
        print(employees)

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addFlightBooking', [usage_type,journey_type,flight_class,from_location,to_location,booking_datetime,departure_datetime,
                                                      preferred_flight,assessment_code,no_of_seats,
                                                             group_id,subgroup_id,spoc_id,corporate_id,billing_entity_id,reason_booking,user_id,user_type,employees,booking_email,assessment_city_id,'@last_booking_id'])
                    booking_id = dictfetchall(cursor)
                    print(booking_id)
                    if booking_id:
                        data = {'success': 0, 'message': booking_id}
                    else:
                        cursor.execute("SELECT @last_booking_id")
                        last_booking_id = cursor.fetchone()[0]
                        print(last_booking_id)
                        cursor.close()
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewFlightBooking', [last_booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllFlightBookingPassangers', [last_booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        cursor3 = connection.cursor()
                        cursor3.callproc('getAllApproverByBookingID', [last_booking_id])
                        approvers = dictfetchall(cursor3)
                        cursor3.close()

                        add_booking_email = AddBooking_Email()
                        if is_email == '1':
                            resp6 = add_booking_email.send_taxi_email(emp, approvers, "Flight")
                        if is_sms == '1':
                            resp1 = add_booking_email.send_taxi_msg(emp, approvers, "Flight")



                    cursor.close()
                    data = {'success': 1, 'message': "Insert Success",'last_booking_id':last_booking_id}
                    return JsonResponse(data)

                except Exception as e:
                    print(e)
                    data = {'success': 0, 'message': "Error in Data Insert"}
                    return JsonResponse(data)

            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)

########## sanket added this #########

def taxi_packages(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateTaxiPackages', [])
                    packages = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'packages': packages}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)












def employee_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        employee_id = request.POST.get('employee_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('employeeHomePage', [employee_id])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def approver_2_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        approver_2 = request.POST.get('approver_2_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('Approver_2HomePage', [approver_2])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def approver_1_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        approver_1 = request.POST.get('approver_1_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('Approver_1HomePage', [approver_1])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def spoc_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        spoc_id = request.POST.get('spoc_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('spocHomePage', [spoc_id])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        admin_id = request.POST.get('admin_id', '')
        print(admin_id)
        print("admin id")
        user_token = req_token.split()
        print("aaaaacccccc")
        print(user_token)
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('adminHomePage', [admin_id])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def agent_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('agentsHomePage', [])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def operator_dashboard(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        operator_id = request.POST.get('operator_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('OperatorHomePage', [operator_id])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Dashboard': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_cotrav_billing_entities(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCotravBillingEntities', [])
                    company = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Enitity': company}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)

def corporate_management_fees(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
        if corporate_id:
            corporate_id = corporate_id
        else:
            corporate_id = '2'
        service_type = 1
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllCorporateManagementFees', [corporate_id, service_type])
                    entity = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Fees': entity}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


#################################### FOR MIS ################################


def report_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        filter_by = request.POST.get('filter_by', '')
        from_date = request.POST.get('booking_from_datetime', '')
        if from_date:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('booking_to_datetime', '')
        if to_date:
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
        booking_status = request.POST.get('booking_status', '')
        company_name = request.POST.get('company_name', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('reportTaxiBookings', [filter_by,from_date,to_date,booking_status,company_name,user_id,user_type])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        #print(booking_id)
                        cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                        cursor2 = connection.cursor()
                        booking_id = e['id']
                        #print(booking_id)
                        cursor2.callproc('getAllTaxiBookingsActionLogs', [booking_id])
                        action = dictfetchall(cursor2)
                        e['Actions'] = action
                        cursor2.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)

                #data = {'success': 1, 'Bookings': emp}
                #return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def report_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        filter_by = request.POST.get('filter_by', '')
        from_date = request.POST.get('booking_from_datetime', '')
        if from_date:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('booking_to_datetime', '')
        if to_date:
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
        booking_status = request.POST.get('booking_status', '')
        company_name = request.POST.get('company_name', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('reportBusBookings', [filter_by,from_date,to_date,booking_status,company_name,user_id,user_type ])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        #print(booking_id)
                        cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                        cursor2 = connection.cursor()
                        booking_id = e['id']
                        #print(booking_id)
                        cursor2.callproc('getAllBusBookingsActionLogs', [booking_id])
                        action = dictfetchall(cursor2)
                        e['Actions'] = action
                        cursor2.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)

                #data = {'success': 1, 'Bookings': emp}
                #return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def report_train_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        filter_by = request.POST.get('filter_by', '')
        from_date = request.POST.get('booking_from_datetime', '')
        if from_date:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('booking_to_datetime', '')
        if to_date:
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
        booking_status = request.POST.get('booking_status', '')
        company_name = request.POST.get('company_name', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('reportTrainBookings', [filter_by,from_date,to_date,booking_status,company_name,user_id,user_type ])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        #print(booking_id)
                        cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                        cursor2 = connection.cursor()
                        booking_id = e['id']
                        #print(booking_id)
                        cursor2.callproc('getAllTrainBookingsActionLogs', [booking_id])
                        action = dictfetchall(cursor2)
                        e['Actions'] = action
                        cursor2.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)

                #data = {'success': 1, 'Bookings': emp}
                #return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def report_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        filter_by = request.POST.get('filter_by', '')
        from_date = request.POST.get('booking_from_datetime', '')
        if from_date:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('booking_to_datetime', '')
        if to_date:
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
        booking_status = request.POST.get('booking_status', '')
        company_name = request.POST.get('company_name', '')


        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('reportFlightBookings', [filter_by, from_date, to_date, booking_status, company_name,user_id,user_type])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        # print(booking_id)
                        cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                        cursor2 = connection.cursor()
                        booking_id = e['id']
                        # print(booking_id)
                        cursor2.callproc('getAllFlightBookingsActionLogs', [booking_id])
                        action = dictfetchall(cursor2)
                        e['Actions'] = action
                        cursor2.close()

                        cursor3 = connection.cursor()
                        cursor3.callproc('getAllFlightBookingFlights', [booking_id])
                        flights = dictfetchall(cursor3)
                        e['Flights'] = flights
                        cursor3.close()

                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)

                # data = {'success': 1, 'Bookings': emp}
                # return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def report_hotel_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        filter_by = request.POST.get('filter_by', '')
        from_date = request.POST.get('booking_from_datetime', '')
        if from_date:
            from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = request.POST.get('booking_to_datetime', '')
        if to_date:
            to_date = datetime.strptime(to_date, '%d-%m-%Y')
        booking_status = request.POST.get('booking_status', '')
        company_name = request.POST.get('company_name', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('reportHotelBookings', [filter_by, from_date, to_date, booking_status, company_name ,user_id,user_type])
                emp = dictfetchall(cursor)
                print(emp)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        # print(booking_id)
                        cursor1.callproc('getAllHotelBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                        cursor2 = connection.cursor()
                        booking_id = e['id']
                        # print(booking_id)
                        cursor2.callproc('getAllHotelBookingsActionLogs', [booking_id])
                        action = dictfetchall(cursor2)
                        e['Actions'] = action
                        cursor2.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
                return JsonResponse(data)

                # data = {'success': 1, 'Bookings': emp}
                # return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_flight_access_token(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getFlightAccessToken', [])
                    train = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Token': train}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def generate_auth_token(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    url = "http://auth.ksofttechnology.com/API/AUTH"
                    payload = {
                        "TYPE": "AUTH",
                        "NAME": "GET_AUTH_TOKEN",
                        "STR": [
                            {
                                "A_ID": "27286260",
                                "U_ID": "test",
                                "PWD": "test",
                                "MODULE": "B2B",
                                "HS": "D"
                            }
                        ]
                    }

                    headers = {}
                    r = requests.post(url, json=payload)
                    api_response = r.json()
                    data = {'success': 1, 'Data': api_response}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'Data': ''}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_flight_search(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        try:
            trip_type = request.POST.get('trip_type', '')
            return_date = request.POST.get('return_date', '')
            fl_class = request.POST.get('fl_class', '')
            no_of_seats = request.POST.get('no_of_seats', '')
            from_city = request.POST.get('from_city', '')
            to_city = request.POST.get('to_city', '')
            departure_date = request.POST.get('departure_date', '')
            d_date = parse(departure_date).strftime("%Y-%m-%d")
            print(d_date)
            if return_date:
                return_date = parse(return_date).strftime("%Y-%m-%d")
            else:
                return_date = ""

            user = {}
            user_token = req_token.split()
            if user_token[0] == 'Token':
                user = getUserinfoFromAccessToken(user_token[1], user_type)
                if user:
                    try:

                        cursor = connection.cursor()
                        cursor.callproc('getFlightAccessToken', [])
                        token = dictfetchall(cursor)
                        cursor.close()
                        AUTH_TOKEN = token[0]['access_token']
                        url = "http://auth.ksofttechnology.com/API/AUTH"
                        payload = {
                            "TYPE": "AUTH",
                            "NAME": "VERIFY_AUTH_TOKEN",
                            "STR": [
                                {"TOKEN": AUTH_TOKEN, "MODULE": "B2B", "HS": "D"}
                            ]
                        }
                        print(payload)
                        r = requests.post(url, json=payload)
                        print(r)
                        db_token = r.json()
                        print(db_token)
                        print("old DADADA")

                        if db_token['STATUS'] == "FAILED":
                            url = "http://auth.ksofttechnology.com/API/AUTH"
                            payload = {
                                "TYPE": "AUTH",
                                "NAME": "GET_AUTH_TOKEN",
                                "STR": [
                                    {
                                        "A_ID": "79394396",
                                        "U_ID": "Taxivaxi",
                                        "PWD": "Taxi$Vaxi1234",
                                        "MODULE": "B2B",
                                        "HS": "D"
                                    }
                                ]
                            }

                            headers = {}
                            r = requests.post(url, json=payload)
                            new_token = r.json()
                            print(new_token)
                            NEW_AUTH_TOKEN = new_token['RESULT']

                            #old_token = db_token['RESULT']
                            cursor = connection.cursor()
                            cursor.callproc('addFlightAccessToken', [AUTH_TOKEN,NEW_AUTH_TOKEN])
                            token = dictfetchall(cursor)
                            cursor.close()

                        else:
                            AUTH_TOKEN = db_token['RESULT']

                        url = "http://mdt.ksofttechnology.com/API/FLIGHT"
                        payload = {
                                "TYPE": "AIR",
                                "NAME": "GET_FLIGHT",
                                "STR": [
                                    {
                                        "AUTH_TOKEN": ""+AUTH_TOKEN,
                                        "SESSION_ID": "XKWP9TWKSDJ4PAKXKUHE1WM72GTBPO13FTUGF454CIGLQYM6F9",
                                        "TRIP": ""+trip_type,
                                        "SECTOR": "",
                                        "SRC": ""+from_city,
                                        "DES": ""+to_city,
                                        "DEP_DATE": ""+d_date,
                                        "RET_DATE": ""+return_date,
                                        "ADT": ""+no_of_seats,
                                        "CHD": "0",
                                        "INF": "0",
                                        "PC": ""+fl_class,
                                        "PF": "",
                                        "HS": "D"
                                    }
                                ]
                            }

                        headers = {}
                        print(payload)
                        r = requests.post(url, json=payload)
                        api_response = r.json()
                        data = {'success': 1, 'Data': api_response}
                        return JsonResponse(data)
                    except Exception as e:
                        data = {'success': 0, 'Data': e}
                        return JsonResponse(data)
                else:
                    data = {'success': 0, 'error': "User Information Not Found"}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'Corporates': "Token Not Found"}
                return JsonResponse(data)
        except Exception as e:
            print("EXCEPTION API")
            data = {'success': 0, 'Data': e}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)



def get_flight_fare_search(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        flight_1 = ""
        flight_2 = ""
        trip_string = request.POST.get('trip_string', '')
        UID = request.POST.get('UID', '')
        ID = request.POST.get('ID', '')
        TID = request.POST.get('TID', '')
        
        UID2 = request.POST.get('UID2', '')
        ID2 = request.POST.get('ID2', '')
        TID2 = request.POST.get('TID2', '')

        src = request.POST.get('src', '')
        des = request.POST.get('des', '')
        ret_date = request.POST.get('ret_date', '')
        adt = request.POST.get('adt', '')
        chd = request.POST.get('chd', '')
        inf = request.POST.get('inf', '')
        L_OW = request.POST.get('L_OW', '')
        H_OW = request.POST.get('H_OW', '')
        T_TIME = request.POST.get('T_TIME', '')
        L_RT = request.POST.get('L_RT', '')
        H_RT = request.POST.get('H_RT', '')

        dep_date = request.POST.get('dep_date', '')
        d_date = parse(dep_date).strftime("%Y-%m-%d")

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    url = "http://mdt.ksofttechnology.com/API/AVLT"
                    payload = {
                        "NAME": "FARE_CHECK",
                        "TYPE": "AIR",
                        "STR": [
                            {
                                "FLIGHT" : {
                                    "UID": str(UID),
                                    "ID": str(ID),
                                    "TID": str(TID)
                                },
                                "PARAM": {
                                    "src": str(src),
                                    "des": str(des),
                                    "dep_date": str(d_date),
                                    "ret_date": ""+ret_date,
                                    "adt": ""+adt,
                                    "chd": ""+chd,
                                    "inf": ""+inf,
                                    "L_OW": ""+L_OW,
                                    "H_OW": ""+H_OW,
                                    "T_TIME": ""+T_TIME,
                                    "Trip_String": ""+trip_string
                                },
                                "GSTINFO": {
                                    "Address": "1/1075/1/2 GF 4, Mehrauli, New Delhi 110030",
                                    "Company": "BAI INFOSOLUTIONS PRIVATE LIMITED",
                                    "Email": "vinod@taxivaxi.com",
                                    "Mobile": "11321654654",
                                    "Number": "07AAGCB3556P1Z7",
                                    "Pin": "110030",
                                    "State": "New Delhi",
                                    "Type": "GST Type",
                                    "hasGST": 'true'
                                  }
                            }
                        ],

                    }

                    payload2 = {
                        "NAME": "FARE_CHECK",
                        "TYPE": "AIR",
                        "STR": [
                            {

                                "FLIGHTOW" : {
                                    "UID": str(UID),
                                    "ID": str(ID),
                                    "TID": str(TID)
                                },
                                "FLIGHTRT": {
                                    "UID": str(UID2),
                                    "ID": str(ID2),
                                    "TID": str(TID2)
                                },
                                "PARAM": {
                                    "src": str(src),
                                    "des": str(des),
                                    "dep_date": str(d_date),
                                    "ret_date": ""+ret_date,
                                    "adt": ""+adt,
                                    "chd": ""+chd,
                                    "inf": ""+inf,
                                    "L_OW": ""+L_OW,
                                    "H_OW": ""+H_OW,
                                    "L_RT": ""+L_RT,
                                    "H_RT": ""+H_RT,
                                    "T_TIME": ""+T_TIME,
                                    "Trip_String": ""+trip_string
                                },
                                "GSTINFO": {
                                    "Address": "1/1075/1/2 GF 4, Mehrauli, New Delhi 110030",
                                    "Company": "BAI INFOSOLUTIONS PRIVATE LIMITED",
                                    "Email": "vinod@taxivaxi.com",
                                    "Mobile": "11321654654",
                                    "Number": "07AAGCB3556P1Z7",
                                    "Pin": "110030",
                                    "State": "New Delhi",
                                    "Type": "GST Type",
                                    "hasGST": 'true'
                                  }
                            }
                        ],

                    }
                    #print(payload)
                    #print(payload2)
                    headers = {}
                    r = {}
                    if UID2:
                        r = requests.post(url, json=payload2)
                    else:
                        r = requests.post(url, json=payload)
                    api_response = r.json()
                    print("API TYPE")
                    print(type(api_response))
                    data = {'success': 1, 'Data': api_response}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'Data': ''}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def save_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        flightdata = request.POST.get('flightdata', '')
        print("SAVER DATAF TYpe")
        print(type(flightdata))
        UID2 = request.POST.get('UID2', '')
        is_mobile = request.POST.get('is_mobile', '')

        employees_name = request.POST.getlist('employee_name_1', '')
        dict = []  # create an empty array

        for name in employees_name:
            dict.append({
                "apnr": "",
                "baggage": "",
                "dob": "",
                "fare": "",
                "ffn": "",
                "fn": name,
                "gpnr": "",
                "ln": "TestA",
                "meal": "",
                "mn": "",
                "nat": "",
                "other_info": "",
                "pi": "",
                "refundable": "",
                "status": "",
                "tc": "",
                "tktno": "",
                "ttl": "Mr",
                "type": "adult",
                "year": ""
            })

        user = {}
        payload = {}
        payload2 = {}

        r = ""
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    if is_mobile:
                        print("type of ini_object", type(flightdata))
                        flightdata = json.loads(flightdata, strict=False) 
                    else:
                        flightdata = eval(flightdata)

                    va = flightdata
                    url = "http://mdt.ksofttechnology.com/API/flight"

                    if UID2:
                        payload2 = {
                            "PARAM": va['PARAM'],
                            "STATUSOW": va['STATUSOW'],
                            "FLIGHTOW": va['FLIGHTOW'],
                            "CON_FLIGHTOW": va['CON_FLIGHTOW'],
                            "FAREOW": va['FAREOW'],
                            "PARAMOW": va['PARAMOW'],
                            "STATUSRT": va['STATUSRT'],
                            "FLIGHTRT": va['FLIGHTRT'],
                            "CON_FLIGHTRT": va['CON_FLIGHTRT'],
                            "FARERT": va['FARERT'],
                            "PARAMRT": va['PARAMRT'],
                            "Deal": va['Deal'],
                            "FARE_RULE": va['FARE_RULE'],
                            "PAX": dict,
                            "TYPE": "DC",
                            "NAME": "PNR_CREATION",
                            "Others": [
                                {
                                    "REMARK": "79394396",
                                    "CUSTOMER_EMAIL": "balwant@taxivaxi.in",
                                    "CUSTOMER_MOBILE": "8669152900"
                                }
                            ]
                        }
                    else:
                        payload = {
                            "STATUS": va['STATUS'],
                            "FLIGHT": va['FLIGHT'],
                            "CON_FLIGHT": va['CON_FLIGHT'],
                            "FARE": va['FARE'],
                            "PARAM": va['PARAM'],
                            "Deal": va['Deal'],
                            "FARE_RULE": va['FARE_RULE'],
                            "GSTINFO": va['GSTINFO'],
                            "PAX": dict,
                            "TYPE": "DC",
                            "NAME": "PNR_CREATION",
                            "Others": [
                                {
                                    "REMARK": "79394396",
                                    "CUSTOMER_EMAIL": "balwant@taxivaxi.in",
                                    "CUSTOMER_MOBILE": "8669152900"
                                }
                            ]
                        }
                    headers = {}
                    if UID2:
                        r = requests.post(url, json=payload2)
                    else:
                        r = requests.post(url, json=payload)
                    api_response = r.json()
                    data = {'success': 1, 'Data':api_response}
                    return JsonResponse(data)
                except Exception as e:
                    print("in EXCEPTION sss")
                    print(e)
                    data = {'success': 0, 'Data': ""}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def get_flight_pnr_details(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        pnr = request.POST.get('pnr', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    client_session = user_token[1]
                    CLIENT_SESSIONID =  client_session[0:40]
                    url = "http://mdt.ksofttechnology.com/API/flight"
                    payload = {
                            "NAME": "PNR_RETRIVE",
                            "TYPE": "DC",
                            "STR": [
                                {
                                    "BOOKINGID": ""+pnr,
                                    "CLIENT_SESSIONID": "XKWP9TWKSDJ4PAKXKUHE1WM72GTBPO13FTUGF454CIGLQYM6F9",
                                    "HS": "D",
                                    "MODULE": "B2B",
                                }
                            ],
                    }

                    headers = {}
                    #print(payload)
                    r = requests.post(url, json=payload)
                    api_response = r.json()
                    #print(api_response)
                    data = {'success': 1, 'Data': api_response}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'Data': ""}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def add_flight_booking_with_invoice(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        flightdata = request.POST.get('flightdata', '')
        UID2 = request.POST.get('UID2', '')

        user_id = request.POST.get('spoc_id', '')
        corporate_id = request.POST.get('corporate_id', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')
        billing_entity_id = request.POST.get('entity_id', '')
        reason_booking = request.POST.get('reason_booking', '')
        no_of_seats = request.POST.get('no_of_seats', '')
        flight_type = request.POST.get('flight_class', '')


        employee_name_1 = request.POST.get('employee_name_1', '')
        employee_name_2 = request.POST.get('employee_name_2', '')
        employee_name_3 = request.POST.get('employee_name_3', '')
        employee_name_4 = request.POST.get('employee_name_4', '')
        employee_name_5 = request.POST.get('employee_name_5', '')
        employee_name_6 = request.POST.get('employee_name_6', '')

        kafila_booking_id = request.POST.get('kafila_booking_id', '')
        timezone.activate(pytz.timezone("Asia/Kolkata"))
        booking_datetime = timezone.localtime(timezone.now())

        is_email = 1
        is_sms = 1
        client_ticket =""

        if billing_entity_id:
            pass
        else:
            billing_entity_id = 0

        employees = []
        employees_name = []
        no_of_emp = int(no_of_seats) + 1
        for i in range(1, no_of_emp):
            employees.append(request.POST.get('employee_id_' + str(i), ''))
            employees_name.append(request.POST.get('employee_name_' + str(i), ''))
            #print(employees)

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    client_session = user_token[1]
                    CLIENT_SESSIONID =  client_session[0:40]
                    url = "http://mdt.ksofttechnology.com/API/flight"
                    payload = {
                            "NAME": "PNR_RETRIVE",
                            "TYPE": "DC",
                            "STR": [
                                {
                                    "BOOKINGID": ""+kafila_booking_id,
                                    "CLIENT_SESSIONID": "XKWP9TWKSDJ4PAKXKUHE1WM72GTBPO13FTUGF454CIGLQYM6F9",
                                    "HS": "D",
                                    "MODULE": "B2B",
                                }
                            ],
                    }

                    headers = {}
                    #print(payload)
                    r = requests.post(url, json=payload)
                    booking1 = r.json()

                    print(booking1)
                    if UID2:
                        if not ('FLIGHTOW' in booking1):
                            data = {'success': 0, 'error': "Pnr Not Generated"}
                            return JsonResponse(data)
                    else:
                        if not ('FLIGHT' in booking1 or 'FLIGHTOW' in booking1):
                            data = {'success': 0, 'error': "Pnr Not Generated"}
                            return JsonResponse(data)

                    ticket_number = []
                    pnr_no = []
                    flight_no = []
                    flight_name = []
                    arrival_time = []
                    departure_time = []
                    flight_to = []
                    flight_from = []
                    is_return_flight = []
                    flight_type = flight_type
                    journey_type = ""
                    from_location =""
                    to_location = ""

                    departure_datetime =""
                    preferred_flight =""
                    booking_email = ""
                    meal_is_include = ''
                    last_booking_id = 0

                    if UID2:
                        print("in trip two")
                        print(UID2)
                        no_of_stops = booking1['FLIGHTOW'][0]['STOP']
                        flight_type = flight_type
                        fare_type = booking1['FLIGHTOW'][0]['FARE_TYPE']
                        meal_is_include = ''
                        no_of_passanger = booking1['PARAM'][0]['adt']
                        employee_booking_id = employees
                        ticket_price = booking1['FLIGHTOW'][0]['AMOUNT']
                        journey_type = "Round Trip"
                        from_location = booking1['FLIGHTOW'][0]['DES_NAME']
                        to_location = booking1['FLIGHTOW'][0]['ORG_NAME']
                        departure_datetime = datetime.strptime(booking1['FLIGHTOW'][0]['DEP_DATE'] + " " + booking1['FLIGHTOW'][0]['DEP_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")

                        if booking1['CON_FLIGHTOW']:
                            for flightt in booking1['CON_FLIGHTOW']:
                                ticket_number.append(booking1['FLIGHTOW'][0]['PCC'])
                                pnr_no.append(booking1['PAXOW'][0]['apnr'])
                                flight_no.append(flightt['FLIGHT_NO'])
                                flight_name.append(flightt['FLIGHT_NAME'])
                                arrival_time1 = datetime.strptime(
                                    flightt['ARRV_DATE'] + " " + flightt['ARRV_TIME'] + ":00",
                                    "%Y-%m-%d %H:%M:%S")
                                arrival_time.append(arrival_time1)
                                arrival_time2 = datetime.strptime(
                                    flightt['DEP_DATE'] + " " + flightt['DEP_TIME'] + ":00",
                                    "%Y-%m-%d %H:%M:%S")
                                departure_time.append(arrival_time2)
                                flight_to.append(flightt['DES_NAME'])
                                flight_from.append(flightt['ORG_NAME'])
                                is_return_flight.append('0')
                        else:
                            ticket_number.append(booking1['FLIGHTOW'][0]['PCC'])
                            pnr_no.append(booking1['PAXOW'][0]['apnr'])
                            flight_no.append(booking1['FLIGHTOW'][0]['FLIGHT_NO'])
                            flight_name.append(booking1['FLIGHTOW'][0]['FLIGHT_NAME'])
                            arrival_time1 = datetime.strptime(
                                booking1['FLIGHTOW'][0]['ARRV_DATE'] + " " +
                                booking1['FLIGHTOW'][0][
                                    'ARRV_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")
                            arrival_time.append(arrival_time1)
                            arrival_time2 = datetime.strptime(
                                booking1['FLIGHTOW'][0]['DEP_DATE'] + " " + booking1['FLIGHTOW'][0][
                                    'DEP_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")
                            departure_time.append(arrival_time2)
                            flight_to.append(booking1['FLIGHTOW'][0]['DES_NAME'])
                            flight_from.append(booking1['FLIGHTOW'][0]['ORG_NAME'])
                            is_return_flight.append('0')

                        if booking1['CON_FLIGHTRT']:
                            for flightt in booking1['CON_FLIGHTRT']:
                                ticket_number.append(booking1['FLIGHTRT'][0]['PCC'])
                                pnr_no.append(booking1['PAXRT'][0]['apnr'])
                                flight_no.append(flightt['FLIGHT_NO'])
                                flight_name.append(flightt['FLIGHT_NAME'])
                                arrival_time1 = datetime.strptime(
                                    flightt['ARRV_DATE'] + " " + flightt['ARRV_TIME'] + ":00",
                                    "%Y-%m-%d %H:%M:%S")
                                arrival_time.append(arrival_time1)
                                arrival_time2 = datetime.strptime(
                                    flightt['DEP_DATE'] + " " + flightt['DEP_TIME'] + ":00",
                                    "%Y-%m-%d %H:%M:%S")
                                departure_time.append(arrival_time2)
                                flight_to.append(flightt['DES_NAME'])
                                flight_from.append(flightt['ORG_NAME'])
                                is_return_flight.append('1')
                        else:
                            ticket_number.append(booking1['FLIGHTRT'][0]['PCC'])
                            pnr_no.append(booking1['PAXRT'][0]['apnr'])
                            flight_no.append(booking1['FLIGHTRT'][0]['FLIGHT_NO'])
                            flight_name.append(booking1['FLIGHTRT'][0]['FLIGHT_NAME'])
                            arrival_time1 = datetime.strptime(
                                booking1['FLIGHTRT'][0]['ARRV_DATE'] + " " +
                                booking1['FLIGHTRT'][0][
                                    'ARRV_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")
                            arrival_time.append(arrival_time1)
                            arrival_time2 = datetime.strptime(
                                booking1['FLIGHTRT'][0]['DEP_DATE'] + " " + booking1['FLIGHTRT'][0][
                                    'DEP_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")
                            departure_time.append(arrival_time2)
                            flight_to.append(booking1['FLIGHTRT'][0]['DES_NAME'])
                            flight_from.append(booking1['FLIGHTRT'][0]['ORG_NAME'])
                            is_return_flight.append('1')

                            print("INNNNNNNNNNNN ELSEEEEEEEEEEEEEEEE")


                    else:
                        print("in trip one")
                        print(UID2)
                        no_of_stops = booking1['FLIGHT'][0]['STOP']
                        flight_type = flight_type
                        fare_type = booking1['FLIGHT'][0]['FARE_TYPE']
                        meal_is_include = ''
                        no_of_passanger = booking1['FLIGHT'][0]['SEAT']
                        employee_booking_id = employees
                        ticket_price = booking1['FLIGHT'][0]['AMOUNT']
                        journey_type = "One Way"
                        from_location = booking1['FLIGHT'][0]['DES_NAME']
                        to_location = booking1['FLIGHT'][0]['ORG_NAME']
                        departure_datetime = datetime.strptime(booking1['FLIGHT'][0]['DEP_DATE'] + " " + booking1['FLIGHT'][0]['DEP_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")

                        if booking1['CON_FLIGHT']:
                            for flightt in booking1['CON_FLIGHT']:
                                ticket_number.append(booking1['FLIGHT'][0]['PCC'])
                                pnr_no.append(booking1['PAX'][0]['apnr'])
                                flight_no.append(flightt['FLIGHT_NO'])
                                flight_name.append(flightt['FLIGHT_NAME'])
                                arrival_time1 = datetime.strptime(
                                    flightt['ARRV_DATE'] + " " + flightt['ARRV_TIME'] + ":00",
                                    "%Y-%m-%d %H:%M:%S")
                                arrival_time.append(arrival_time1)
                                arrival_time2 = datetime.strptime(
                                    flightt['DEP_DATE'] + " " + flightt['DEP_TIME'] + ":00",
                                    "%Y-%m-%d %H:%M:%S")
                                departure_time.append(arrival_time2)
                                flight_to.append(flightt['DES_NAME'])
                                flight_from.append(flightt['ORG_NAME'])
                                is_return_flight.append('0')
                            print("INNNNNNNNNNNN IFFFFFFFFFFFFF")
                        else:
                            ticket_number.append(booking1['FLIGHT'][0]['PCC'])
                            pnr_no.append(booking1['PAX'][0]['apnr'])
                            flight_no.append(booking1['FLIGHT'][0]['FLIGHT_NO'])
                            flight_name.append(booking1['FLIGHT'][0]['FLIGHT_NAME'])
                            arrival_time1 = datetime.strptime(booking1['FLIGHT'][0]['ARRV_DATE'] + " " + booking1['FLIGHT'][0]['ARRV_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")
                            arrival_time.append(arrival_time1)
                            arrival_time2 = datetime.strptime(booking1['FLIGHT'][0]['DEP_DATE'] + " " + booking1['FLIGHT'][0]['DEP_TIME'] + ":00", "%Y-%m-%d %H:%M:%S")
                            departure_time.append(arrival_time2)
                            flight_to.append(booking1['FLIGHT'][0]['DES_NAME'])
                            flight_from.append(booking1['FLIGHT'][0]['ORG_NAME'])
                            is_return_flight.append('0')
                            print("INNNNNNNNNNNN ELSEEEEEEEEEEEEEEEE")

                    cursor = connection.cursor()
                    print(employees)
                    try:
                        cursor.callproc('addFlightBooking',
                                        ["Flight", journey_type, flight_type, from_location, to_location,
                                         booking_datetime, departure_datetime,
                                         preferred_flight, assessment_code, no_of_seats,
                                         group_id, subgroup_id, spoc_id, corporate_id, billing_entity_id,
                                         reason_booking, user_id, user_type, employees, booking_email,
                                         assessment_city_id, '@last_booking_id'])
                        booking_id = dictfetchall(cursor)

                        if booking_id:
                            data = {'success': 0, 'message': booking_id}
                        else:
                            cursor.execute("SELECT @last_booking_id")
                            last_booking_id = cursor.fetchone()[0]
                            print("booking id")
                            print(last_booking_id)
                            cursor.close()
                            cursor2 = connection.cursor()
                            cursor2.callproc('viewFlightBooking', [last_booking_id])
                            emp = dictfetchall(cursor2)
                            cursor2.close()

                            cursor1 = connection.cursor()
                            cursor1.callproc('getAllFlightBookingPassangers', [last_booking_id])
                            passanger = dictfetchall(cursor1)
                            emp[0]['Passangers'] = passanger
                            cursor1.close()

                            cursor3 = connection.cursor()
                            cursor3.callproc('getAllApproverByBookingID', [last_booking_id])
                            approvers = dictfetchall(cursor3)
                            cursor3.close()

                            cursor4 = connection.cursor()
                            cursor4.callproc('assignFlightBooking',
                                            [flight_type, flight_type, journey_type, no_of_stops, last_booking_id,
                                             meal_is_include, fare_type, user_id, user_type, ticket_price,100, 18,
                                             18, 118, 1,18, 0, 0, 18, 0,0, 18,0, 0, 0,ticket_price, 0, 1,1, 18, 9, 9,"", "", 0, 0,0, 1, 1])
                            result = dictfetchall(cursor4)

                            cursor4.close()
                            no_of_stops = int(no_of_stops)
                            print("no of stops")
                            print(no_of_stops)
                            if UID2:
                                final_stop = no_of_stops + 2
                            else:
                                final_stop = no_of_stops+1
                            for x in range(final_stop):
                                cursor5 = connection.cursor()
                                cursor5.callproc('addFlightBookingFlights',
                                                 [flight_name[x], flight_no[x], pnr_no[x], flight_from[x],
                                                  flight_to[x], departure_time[x], arrival_time[x], last_booking_id,
                                                  user_id, user_type, is_return_flight[x]])
                                result = dictfetchall(cursor5)
                                print("addFlightBookingFloght")
                                print(result)
                                cursor5.close()

                            for xx in range(int(no_of_seats)):
                                cursor26 = connection.cursor()
                                cursor26.callproc('updateFlightPassangerTickectNo',
                                                 [ticket_number[xx], employee_booking_id[xx], last_booking_id])
                                result = dictfetchall(cursor26)
                                print("addFlightBookingticket")
                                print(result)
                                cursor26.close()

                            company = dictfetchall(cursor)
                            print(company)
                            if company:
                                data = {'success': 0, 'message': company}
                            else:
                                print("Last Booking ID")
                                cursor27 = connection.cursor()
                                cursor27.callproc('viewFlightBooking', [last_booking_id])
                                emp = dictfetchall(cursor27)
                                cursor27.close()

                                cursor11 = connection.cursor()
                                cursor11.callproc('getAllFlightBookingPassangers', [last_booking_id])
                                passanger = dictfetchall(cursor11)
                                emp[0]['Passangers'] = passanger
                                cursor11.close()

                                cursor22 = connection.cursor()
                                cursor22.callproc('getAllFlightBookingFlights', [last_booking_id])
                                flights = dictfetchall(cursor22)
                                cursor22.close()

                                emp[0]['Flights'] = flights

                                get_voucher_path = ''
                                if client_ticket:
                                    voucher = emp[0]
                                    bus_pdf = Flight(voucher)
                                    get_vou = bus_pdf.get(request)
                                    get_voucher_path = get_vou[1]
                                else:
                                    get_voucher_path = ""

                                add_booking_email = AddBooking_Email()
                                if is_email == '1':
                                    resp6 = add_booking_email.send_taxi_email(emp, approvers, "Flight")
                                if is_sms == '1':
                                    resp1 = add_booking_email.send_taxi_msg(emp, approvers, "Flight")

                                add_booking_email = Assign_Booking_Email()
                                if is_sms:
                                    resp1 = add_booking_email.send_client_sms(emp, "Flight")
                                if is_email:
                                    resp1 = add_booking_email.is_client_email(emp, "Flight", get_voucher_path)

                        cursor.close()
                        data = {'success': 1, 'message': "Insert Success", 'last_booking_id': last_booking_id}
                        return JsonResponse(data)

                    except Exception as e:
                        print(e)
                        data = {'success': 0, 'message': "Error in Data Insert"}
                        return JsonResponse(data)

                except Exception as e:
                    print("EXCEPTIONSNSNSNSN")
                    print(e)
                    data = {'success': 0, 'Data': "Exception"}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def getUserinfoFromAccessToken(user_token=None, user_type=None):
    try:
        user = {}
        user_info = {}
        if user_type == '1':
            user = Corporate_Login_Access_Token.objects.get(access_token=user_token)
            print("sdsds")
            print(user)
        elif user_type == '2':
            user = Corporate_Approves_1_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '3':
            user = Corporate_Approves_2_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '4':
            user = Corporate_Spoc_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '6':
            user = Corporate_Employee_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '10':
            user = Corporate_Agent_Login_Access_Token.objects.get(access_token=user_token)
        elif user_type == '7':
            user = Operator_Login_Access_Token.objects.get(access_token=user_token)

        timezone.activate(pytz.timezone("Asia/Kolkata"))
        present = timezone.localtime(timezone.now())

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
            elif user_type == '6':
                user_info = Corporate_Employee_Login.objects.get(id=user.employee_id)
            elif user_type == '10':
                user_info = Corporate_Agent.objects.get(id=user.agent_id)
            elif user_type == '7':
                print(user)
                user_info = Operator_Login.objects.get(id=user.operator_id)
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