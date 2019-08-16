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
from django.contrib.auth.hashers import check_password


def login(request):
    user_name = request.POST.get('user_name', '')
    user_password = request.POST.get('user_password', '')
    user_type = request.POST.get('user_type', '')
    if user_type:
        user_type=user_type
    else:
        user_type=10

    cursor = connection.cursor()
    cursor.callproc('getLoginDetails', [user_name,user_type])
    user = dictfetchall(cursor)
    if user:
        print(user[0]['id'])
        password = check_password(user_password, user[0]['password'])
        if password:
            data = {'success': 1,'access_token':user[0]['access_token'], 'User': user}
        else:
            data = {'success': 1, 'message': 'Invalide User Name Or Password'}
    else:
        data = {'success': 0, 'User': ''}
    return JsonResponse(data)


def companies(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateDetails', [])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def view_company(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewCorporateDetails', [corporate_id])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def add_companies(request):
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

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('create_corporate_with_basic_details',[corporate_name, corporate_code,contact_person_name,contact_person_no,contact_person_email,bill_corporate_name,address_line_1,
                  address_line_2,address_line_3,gst_id,has_billing_spoc_level,has_auth_level,no_of_auth_level,has_assessment_codes,is_radio,is_local,is_outstation, is_bus,
                   is_train, is_hotel, is_meal, is_flight,is_water_bottles,  is_reverse_logistics,is_spoc,password,cotrav_agent_id,user_type])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def update_company(request):
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

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('updateCorporate',[corporate_name, corporate_code,contact_person_name,contact_person_no,contact_person_email,
                  has_billing_spoc_level,has_auth_level,no_of_auth_level,has_assessment_codes,is_radio,is_local, is_outstation, is_bus,
                   is_train, is_hotel, is_meal, is_flight,is_water_bottles,  is_reverse_logistics,corporate_id,user_id,user_type])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def delete_company(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id = request.POST.get('user_id', '')
    corporate_id = request.POST.get('corporate_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('deleteCorporate',[corporate_id,user_id,user_type])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def add_company_rates(request):
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
        rate_id=0

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('addCorporateRate',[corporate_id,package_name,city_id,taxi_type,tour_type,kms,hours,km_rate,hour_rate,base_rate,
                                                    night_rate,user_id,user_type,rate_id])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def update_company_rates(request):
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

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('updateCorporateRate',[corporate_id,package_name,city_id,taxi_type,tour_type,kms,hours,km_rate,hour_rate,base_rate,
                                                    night_rate,user_id,user_type,rate_id])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def delete_company_rates(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user_id = request.POST.get('user_id', '')
    rate_id = request.POST.get('rate_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('deleteCorporateRate',[rate_id,user_id,user_type])
                company = dictfetchall(cursor)
                data = {'success': 1, 'Corporates': company}
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


def company_rates(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateRatesDetails', [corporate_id])
                corporate_rates = dictfetchall(cursor)
                data = {'success': 1, 'Corporate_Retes': corporate_rates}
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




def billing_entities(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateBillingEntitiesDetails', [corporate_id])
                entity = dictfetchall(cursor)
                data = {'success': 1, 'Entitys': entity}
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


def admins(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'

    user ={}
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateAdminsDetails', [corporate_id])
                admin = dictfetchall(cursor)
                print(admin)
                data = {'success': 1, 'Admins': admin}
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


def groups(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'
    user ={}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateGroupsDetails', [corporate_id])
                group = dictfetchall(cursor)
                data = {'success': 1, 'Groups': group}
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


def subgroups(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateSubgroupsDetails', [corporate_id])
                subgroup = dictfetchall(cursor)
                data = {'success': 1, 'Subgroups': subgroup}
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


def spocs(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateSpocsDetails', [corporate_id])
                spoc = dictfetchall(cursor)
                data = {'success': 1, 'Spocs': spoc}
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


def employee(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'
    user ={}
    print(user_type)
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : "+user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateEmployeesDetails', [corporate_id])
                employee = dictfetchall(cursor)
                data = {'success': 1, 'Employees': employee}
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





def cities(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : " + user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCity', [])
                cities = dictfetchall(cursor)
                data = {'success': 1, 'Cities': cities}
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


def taxi_types(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            print("ACCESS TOKEN : " + user_token[1])
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllTaxiTypes', [corporate_id])
                cities = dictfetchall(cursor)
                data = {'success': 1, 'Taxies': cities}
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



def add_billing_entity(request):
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

    if req_token:
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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_billing_entity(request):
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

    if req_token:
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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def delete_billing_entity(request):
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

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateBillingEntity',
                                    [user_id, user_type, entity_id])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_group(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')

    user_id = request.POST.get('user_id', '')
    group_name = request.POST.get('group_name', '')
    zone_name = request.POST.get('zone_name')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateGroup', [user_id,corporate_id,user_type,group_name,zone_name])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_group(request):
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

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateGroupDetails', [group_id,group_name,zone_name,user_id,user_type])

                    data = {'success': 1, 'message': "Updated Successfully"}
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


def delete_group(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    group_id = request.POST.get('group_id', '')
    user_id = request.POST.get('user_id', '')

    if group_id:
        group_id = group_id
    else:
        group_id = '0'

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteGroupDetails', [group_id,user_id,user_type])

                    data = {'success': 1, 'message': "Deleted Successfully"}
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


def add_subgroup(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')

    user_id = request.POST.get('user_id', '')
    subgroup_name = request.POST.get('subgroup_name', '')
    group_id = request.POST.get('group_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('addNewCorporateSubGroup', [user_id,corporate_id,user_type,subgroup_name,group_id])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_subgroup(request):
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

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('updateSubGroupDetails', [subgroup_id,subgroup_name,user_id,user_type])

                    data = {'success': 1, 'message': "Updated Successfully"}
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


def delete_subgroup(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    subgroup_id = request.POST.get('subgroup_id', '')
    user_id = request.POST.get('user_id', '')

    if subgroup_id:
        subgroup_id = subgroup_id
    else:
        subgroup_id = '0'

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteSubGroupDetails', [subgroup_id,user_id,user_type])

                    data = {'success': 1, 'message': "Deleted Successfully"}
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


def add_group_auth(request):
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
    access_token = request.POST.get('access_token_auth','')
    password = request.POST.get('password','')
    group_auth_id = request.POST.get('group_auth_id','')

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

    if req_token:
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


def update_group_auth(request):
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

    group_auth_id = request.POST.get('group_auth_id','')

    if req_token:
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


def delete_group_auth(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id = request.POST.get('user_id', '')

    group_auth_id = request.POST.get('group_auth_id','')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteGroupAuthenticator', [group_auth_id,user_id,user_type])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_subgroup_auth(request):
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
    access_token = request.POST.get('access_token_auth','')
    password = request.POST.get('password','')
    subgroup_auth_id = request.POST.get('subgroup_auth_id','')

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

    if req_token:
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


def update_subgroup_auth(request):
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

    subgroup_auth_id = request.POST.get('subgroup_auth_id','')

    if req_token:
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


def delete_subgroup_auth(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id = request.POST.get('user_id', '')

    subgroup_auth_id = request.POST.get('subgroup_auth_id','')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteSubGroupAuthenticator', [subgroup_auth_id,user_id,user_type])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_admin(request):
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
    access_token = request.POST.get('access_token_auth','')
    password = request.POST.get('password','')
    admin_id = request.POST.get('admin_id','')

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

    if req_token:
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


def update_admin(request):
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

    admin_id = request.POST.get('admin_id','')

    if req_token:
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


def delete_admin(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id = request.POST.get('user_id', '')

    admin_id = request.POST.get('admin_id','')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateAdmin', [admin_id,user_id,user_type])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_spoc(request):
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
    access_token = request.POST.get('access_token_auth','')
    password = request.POST.get('password','')
    spoc_id = request.POST.get('spoc_id')

    if corporate_id:
        corporate_id = corporate_id
    else:
        corporate_id = '0'

    if spoc_id:
        admin_id = spoc_id
    else:
        admin_id = '0'

    if is_delete:
        is_delete = is_delete
    else:
        is_delete = '0'

    if req_token:
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

                    print(result)

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_spoc(request):
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
    access_token = request.POST.get('access_token_auth','')
    spoc_id = request.POST.get('spoc_id')

    if req_token:
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


def delete_spoc(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id = request.POST.get('user_id', '')

    spoc_id = request.POST.get('spoc_id','')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateSpoc', [spoc_id,user_id,user_type])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_employee(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')

    user_id = request.POST.get('user_id', '')

    spoc_id = request.POST.get('spoc_id')
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

    is_delete = request.POST.get('delete_id')
    password = request.POST.get('password','')
    employee_id = request.POST.get('employee_id')

    if employee_id:
        employee_id = employee_id
    else:
        employee_id = '0'

    if is_delete:
        is_delete = is_delete
    else:
        is_delete = '0'



    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('addNewCorporateEmployee', [user_id,user_type,spoc_id, core_employee_id, employee_cid,
                    employee_name, employee_email, employee_contact, age, gender, id_proof_type, id_proof_no, is_active, has_dummy_email,
                    fcm_regid, is_cxo, designation, home_city, home_address, assistant_id, date_of_birth,is_delete,employee_id])

                    print(result)

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_employee(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    corporate_id = request.POST.get('corporate_id', '')
    user_id = request.POST.get('user_id', '')

    spoc_id = request.POST.get('spoc_id')
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

    is_delete = request.POST.get('delete_id')
    employee_id = request.POST.get('employee_id')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    result = cursor.callproc('updateCorporateEmployee', [user_id,user_type,spoc_id, core_employee_id, employee_cid,
                    employee_name, employee_email, employee_contact, age, gender, id_proof_type, id_proof_no, is_active, has_dummy_email,
                    fcm_regid, is_cxo, designation, home_city, home_address, assistant_id, date_of_birth,is_delete,employee_id])
                    print(result)
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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def delete_employee(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id = request.POST.get('user_id', '')

    employee_id = request.POST.get('employee_id','')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteCorporateEmployee', [employee_id,user_id,user_type])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)

def add_agent(request):
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

    if req_token:
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

                    print(result)

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def update_agent(request):
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

    if req_token:
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
                    print(result)
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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def delete_agent(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    user_id = request.POST.get('user_id', '')

    agent_id = request.POST.get('agent_id','')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:
                    cursor.callproc('deleteAgent', [user_id,user_type,agent_id])

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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def view_group(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    group_id = request.POST.get('group_id', '')

    if group_id:
        group_id = group_id
    else:
        group_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewGroupDetails', [group_id])
                group = dictfetchall(cursor)
                data = {'success': 1, 'Groups': group}
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


def view_group_auth(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    group_id = request.POST.get('group_id', '')

    if group_id:
        group_id = group_id
    else:
        group_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateGroupsAuthenticator', [group_id])
                group = dictfetchall(cursor)
                data = {'success': 1, 'Groups': group}
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


def view_subgroup(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    subgroup_id = request.POST.get('subgroup_id', '')

    if subgroup_id:
        subgroup_id = subgroup_id
    else:
        subgroup_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewSubGroupDetails', [subgroup_id])
                group = dictfetchall(cursor)
                data = {'success': 1, 'SubGroups': group}
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


def view_subgroup_auth(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    subgroup_id = request.POST.get('subgroup_id', '')

    if subgroup_id:
        subgroup_id = subgroup_id
    else:
        subgroup_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllCorporateSubGroupsAuthenticator', [subgroup_id])
                group = dictfetchall(cursor)
                data = {'success': 1, 'SubGroups': group}
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


def view_spoc(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    spoc_id = request.POST.get('spoc_id', '')

    if spoc_id:
        spoc_id = spoc_id
    else:
        spoc_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewSpocDetails', [spoc_id])
                spoc = dictfetchall(cursor)
                data = {'success': 1, 'Spoc': spoc}
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


def view_employee(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    employee_id = request.POST.get('employee_id', '')

    if employee_id:
        employee_id = employee_id
    else:
        employee_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewEmployeeDetails', [employee_id])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Employee': emp}
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


def view_agent(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    agent_id = request.POST.get('agent_id', '')

    if agent_id:
        agent_id = agent_id
    else:
        agent_id = '0'
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewAgentDetails', [agent_id])
                agent = dictfetchall(cursor)
                data = {'success': 1, 'Agent': agent}
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


def get_agents(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllAgentsDetails', [])
                emp = dictfetchall(cursor)
                data = {'success': 1, 'Agents': emp}
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


################################## Taxi Booking  ###############################

def taxi_bookings(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    spoc_id = request.POST.get('spoc_id', '')
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('AllSPOCTaxiBookings', [spoc_id])
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


def view_taxi_booking(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    booking_id = request.POST.get('booking_id', '')
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('viewTaxiBooking', [booking_id])
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


def add_taxi_booking(request):
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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_employee_taxi_booking(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    booking_id = request.POST.get('booking_id', '')
    employee_id = request.POST.get('booking_id', '')

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    result = cursor.callproc('addEmployeeTaxiBooking', [booking_id,employee_id])
                    print(result)
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
        data = {'success': 0, 'error': "Access Token Empty"}
        return JsonResponse(data)


def add_city_name(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    city_name = request.POST.get('city_name', '')
    state_id = request.POST.get('state_id', '')

    if req_token:
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


def add_state_name(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    city_state = request.POST.get('city_state', '')
    country_id = request.POST.get('country_id', '')

    if req_token:
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


def add_country_name(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']

    city_country = request.POST.get('city_country', '')

    if req_token:
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