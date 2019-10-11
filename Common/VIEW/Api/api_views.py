from datetime import datetime
import string
import random

from django.http import JsonResponse
from django.db import connection
from Common.models import Corporate_Login
from Common.models import Corporate_Spoc_Login
from Common.models import Corporate_Employee_Login
from Common.models import Corporate_Approves_1_Login
from Common.models import Corporate_Approves_2_Login
from Common.models import Corporate_Agent

from Common.models import Corporate_Login_Access_Token
from Common.models import Corporate_Spoc_Login_Access_Token
from Common.models import Corporate_Employee_Login_Access_Token
from Common.models import Corporate_Approves_1_Login_Access_Token
from Common.models import Corporate_Approves_2_Login_Access_Token
from Common.models import Corporate_Agent_Login_Access_Token
from django.contrib.auth.hashers import check_password


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

                if user_type == '1':
                    insert_data = Corporate_Login_Access_Token.objects.create(corporate_login_id=user[0]['corporate_id'], access_token=gen_access_token,user_agent=user_info)
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

                data = {'success': 1,'access_token':gen_access_token, 'message': 'Login Successfully', 'User': user}
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
                    user.expiry_date = datetime.now()  # change field
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
                       is_train, is_hotel, is_meal, is_flight,is_water_bottles,  is_reverse_logistics,is_spoc,password,cotrav_agent_id,user_type,billing_city_id])
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
                       is_train, is_hotel, is_meal, is_flight,is_water_bottles,  is_reverse_logistics,corporate_id,user_id,user_type])
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
                    data = {'success': 1, 'message': 'Fee Added Successfully'}
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
                    data = {'success': 1, 'message': 'Record Updated Successfully'}
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
                    data = {'success': 1, 'message': 'Deleted Successfully'}
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
                    data = {'success': 1, 'taxi_models': cities}
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
                    data = {'success': 1, 'taxi_models': cities}
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
                    data = {'success': 1, 'taxi_models': cities}
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
                    data = {'success': 1, 'taxi_models': cities}
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
                    
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateGroup', [user_id,corporate_id,user_type,group_name,zone_name])

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Updated Successfully"}
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

                    data = {'success': 1, 'message': "Deleted Successfully"}
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

        user_id = request.POST.get('user_id', '')
        subgroup_name = request.POST.get('subgroup_name', '')
        group_id = request.POST.get('group_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateSubGroup', [user_id,corporate_id,user_type,subgroup_name,group_id])

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Updated Successfully"}
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

                    data = {'success': 1, 'message': "Deleted Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
                    result = cursor.callproc('addNewCorporateSpoc', [user_id,corporate_id,user_type,group_id,subgroup_id,user_cid,user_name,user_contact,email,username,
                                                            budget,expense,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,is_delete,access_token,password,spoc_id])
                    cursor.close()
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateSpoc', [spoc_id,user_id,user_type])
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
        has_dummy_email = request.POST.get('has_dummy_email', '')
        fcm_regid = request.POST.get('fcm_regid', '')
        is_cxo = request.POST.get('is_cxo', '')
        designation = request.POST.get('designation', '')
        home_city = request.POST.get('home_city', '')
        home_address = request.POST.get('home_address', '')
        assistant_id = request.POST.get('assistant_id', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        if date_of_birth:
            pass
            #date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y %H:%M:%S')
        else:
            date_of_birth = None

        is_delete = request.POST.get('delete_id')
        password = request.POST.get('password', '')
        employee_id = request.POST.get('employee_id')

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

        if age:
            age: age
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
                    fcm_regid, is_cxo, designation, home_city, home_address, assistant_id, date_of_birth,is_delete,employee_id,billing_entity_id,corporate_id])

                    company = dictfetchall(cursor)

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
        has_dummy_email = request.POST.get('has_dummy_email')
        fcm_regid = request.POST.get('fcm_regid')
        is_cxo = request.POST.get('is_cxo')
        designation = request.POST.get('designation', '')
        home_city = request.POST.get('home_city', '')
        home_address = request.POST.get('home_address', '')
        assistant_id = request.POST.get('assistant_id', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        date_of_birth = datetime.strptime(date_of_birth, '')

        employee_id = request.POST.get('employee_id')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('updateCorporateEmployee', [user_id,user_type,spoc_id, core_employee_id, employee_cid,
                    employee_name, employee_email, employee_contact, age, gender, id_proof_type, id_proof_no, is_active, has_dummy_email,
                    fcm_regid, is_cxo, designation, home_city, home_address, assistant_id, date_of_birth,employee_id,billing_entity_id])

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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

                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
                    data = {'success': 1, 'message': "Data Insert Successfully"}
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
        #from_date = datetime.strptime(from_date, '%d/%m/%Y')
        to_date = request.POST.get('to_date', '')
        #to_date = datetime.strptime(to_date, '%d/%m/%Y')
        service_from = request.POST.get('service_from', '')
        #service_from = datetime.strptime(service_from, '%d/%m/%Y')
        service_to = request.POST.get('service_to', '')
        #service_to = datetime.strptime(service_to, '%d/%m/%Y')

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


def update_assessment_codes(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        code_desc = request.POST.get('code_desc', '')
        from_date = request.POST.get('from_date', '')
        #from_date = datetime.strptime(from_date, '%d/%m/%Y')
        to_date = request.POST.get('to_date', '')
        #to_date = datetime.strptime(to_date, '%d/%m/%Y')
        code_id = request.POST.get('code_id', '')
        service_from = request.POST.get('service_from', '')
        #service_from = datetime.strptime(service_from, '%d/%m/%Y')
        service_to = request.POST.get('service_to', '')
        #service_to = datetime.strptime(service_to, '%d/%m/%Y')

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

                    data = {'success': 1, 'message': 'Operation Success'}
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
                    emp[0]['Passangers'] = passanger
                    data = {'success': 1, 'Bookings': emp}
                    cursor1.close()
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
                    emp[0]['Passangers'] = passanger
                    data = {'success': 1, 'Bookings': emp}
                    cursor1.close()
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
                    print(booking_id)
                    cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    emp[0]['Passangers'] = passanger
                    data = {'success': 1, 'Bookings': emp}
                    cursor1.close()
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
        print("hotel Booking Id")
        print(booking_id)
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
                    emp[0]['Passangers'] = passanger
                    data = {'success': 1, 'Bookings': emp}
                    cursor1.close()
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
                    print(booking_id)
                    cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    cursor1.close()

                    cursor2 = connection.cursor()
                    cursor2.callproc('getAllFlightBookingFlights', [booking_id])
                    flights = dictfetchall(cursor2)
                    cursor2.close()

                    emp[0]['Passangers'] = passanger
                    emp[0]['Flights'] = flights
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
            pass
        else:
            booking_datetime = datetime.now()
        #pickup_datetime = datetime.strptime(pickup_datetime, '%d/%m/%Y %H:%M:%S')
        taxi_type = request.POST.get('taxi_type')
        package_id = request.POST.get('package_id')
        no_of_days = request.POST.get('no_of_days', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')

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
            booking_datetime = datetime.now()  # change field

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
                                                             taxi_type,package_id,no_of_days,reason_booking,no_of_seats,assessment_code,assessment_city_id,employees,booking_datetime])
                    booking_id = dictfetchall(cursor)
                    print(booking_id)
                    cursor.close()
                    data = {'success': 1, 'message': "Insert Successfully"}
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


def add_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        from_location = request.POST.get('from', '')
        to_location = request.POST.get('to', '')
        bus_type = request.POST.get('bus_type', '')
        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            pass
        else:
            booking_datetime = datetime.now()
        #booking_datetime = datetime.strptime(booking_datetime, '%d/%m/%Y %H:%M:%S')

        journey_datetime = request.POST.get('journey_datetime', '')
        #journey_datetime = datetime.strptime(journey_datetime, '%d/%m/%Y %H:%M:%S')
        entity_id = request.POST.get('entity_id', '')
        preferred_bus = request.POST.get('preferred_bus', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')

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
                                                             entity_id,preferred_bus,reason_booking,no_of_seats,assessment_code,assessment_city_id,employees])
                    booking_id = dictfetchall(cursor)

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
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        from_location = request.POST.get('from', '')
        to_location = request.POST.get('to', '')
        train_type = request.POST.get('train_type', '')
        booking_datetime = request.POST.get('booking_datetime', '')
        if booking_datetime:
            pass
        else:
            booking_datetime = datetime.now()
        #booking_datetime = datetime.strptime(booking_datetime, '%d/%m/%Y %H:%M:%S')

        journey_datetime = request.POST.get('journey_datetime', '')
        #journey_datetime = datetime.strptime(journey_datetime, '%d/%m/%Y %H:%M:%S')
        entity_id = request.POST.get('entity_id', '')
        preferred_train = request.POST.get('preferred_train', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')

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
                                                             entity_id,preferred_train,reason_booking,no_of_seats,assessment_code,assessment_city_id,employees])
                    booking_id = dictfetchall(cursor)
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
            pass
        else:
            booking_datetime = datetime.now() 
        
        checkin_datetime = request.POST.get('checkin_datetime', '')
        checkout_datetime = request.POST.get('checkout_datetime', '')

        preferred_hotel= request.POST.get('preferred_hotel','')
        billing_entity_id = request.POST.get('billing_entity_id', '')
        assessment_code = request.POST.get('assessment_code', '')
        assessment_city_id = request.POST.get('assessment_city_id', '')

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
                                                             group_id,subgroup_id,spoc_id,corporate_id,billing_entity_id,reason_booking,user_id,user_type,employees])
                    booking_id = dictfetchall(cursor)

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
        spoc_id = request.POST.get('spoc_id', '')
        group_id = request.POST.get('group_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        usage_type = request.POST.get('usage_type', '')
        journey_type = request.POST.get('trip_type', '')
        flight_class = request.POST.get('seat_type', '')
        from_location = request.POST.get('from_city', '')
        to_location = request.POST.get('to_city', '')

        booking_datetime = request.POST.get('booking_datetime', '')
        #booking_datetime = datetime.strptime(booking_datetime, '%d/%m/%Y %H:%M:%S')
        if booking_datetime:
            pass
        else:
            booking_datetime = datetime.now()

        departure_datetime = request.POST.get('departure_datetime', '')
        #departure_datetime = datetime.strptime(departure_datetime, '%d/%m/%Y %H:%M:%S')

        preferred_flight= request.POST.get('preferred_flight','')
        billing_entity_id = request.POST.get('billing_entity_id', '')
        assessment_code = request.POST.get('assessment_code', '')


        if assessment_code:
            pass
        else:
            assessment_code=0

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

                    cursor.callproc('addFlightBooking', [usage_type,journey_type,flight_class,from_location,to_location,booking_datetime,departure_datetime,
                                                      preferred_flight,assessment_code,no_of_seats,
                                                             group_id,subgroup_id,spoc_id,corporate_id,billing_entity_id,reason_booking,user_id,user_type,employees])
                    booking_id = dictfetchall(cursor)
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
        elif user_type == '6':
            user = Corporate_Employee_Login_Access_Token.objects.get(access_token=user_token)
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
            elif user_type == '6':
                user_info = Corporate_Employee_Login.objects.get(id=user.employee_id)
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