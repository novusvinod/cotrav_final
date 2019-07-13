from datetime import datetime
from django.http import JsonResponse
from django.db import connection
from Company.models import Corporate_Login
from Company.models import Corporate_Spoc_Login
from Company.models import Corporate_Approves_1_Login
from Company.models import Corporate_Approves_2_Login
from Company.models import Corporate_Agent

from Company.models import Corporate_Login_Access_Token
from Company.models import Corporate_Spoc_Login_Access_Token
from Company.models import Corporate_Approves_1_Login_Access_Token
from Company.models import Corporate_Approves_2_Login_Access_Token
from Company.models import Corporate_Agent_Login_Access_Token


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
        elif user_type == 'agent':
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
            elif user_type == 'agent':
                user_info = Corporate_Agent.objects.get(id=user.agent_id)
            else:
                return None

            return user_info

    except Exception as e:
        print(e)
        return None


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



def add_group(request):
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
                    cursor.callproc('addNewCorporateGroup', [user_id,corporate_id,user_type,group_name,zone_name,name,email,cid,contact_no,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
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


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]