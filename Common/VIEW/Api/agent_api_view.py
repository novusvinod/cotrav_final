from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from Common.models import Corporate_Login, Corporate_Employee_Login_Access_Token
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


def operators(request):
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
                    cursor.callproc('getAllOperators', [])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Operators': emp}
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


def operator_contacts(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorContacts', [operator_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'OperatorContacts': emp}
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


def operator_banks(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorBankAccountDetails', [operator_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'OperatorBanks': emp}
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


def view_operator(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewOperator', [operator_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Operator': emp}
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


def operation_managements(request):
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
                    cursor.callproc('getAllCorporateOMSAccess', [])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Access': emp}
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


def operation_managements(request):
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
                    cursor.callproc('getAllCorporateOMSAccess', [])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Access': emp}
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


def relationship_managements(request):
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
                    cursor.callproc('getAllCorporateRMSAccess', [])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Access': emp}
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


def add_operator(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')
        type = request.POST.get('type', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        operator_name = request.POST.get('operator_name', '')
        operator_email = request.POST.get('operator_email', '')
        operator_contact = request.POST.get('operator_contact', '')
        website = request.POST.get('website', '')

        is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
        service_tax_number = request.POST.get('service_tax_number', '')
        night_start_time = request.POST.get('night_start_time', '')
        night_end_time = request.POST.get('night_end_time', '')
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
                    cursor.callproc('addOperator', [type,username,password,operator_name,operator_email,operator_contact,website,is_service_tax_applicable,service_tax_number,
                                                    night_start_time,night_end_time,tds_rate,gst_id,pan_no,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def add_operator_contact(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        operator_id = request.POST.get('operator_id', '')
        operator_address = request.POST.get('operator_address', '')
        contact_name = request.POST.get('contact_name', '')
        contact_email = request.POST.get('contact_email', '')
        contact_no = request.POST.get('contact_no', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addOperatorContact',
                                    [operator_id, contact_name, contact_email, contact_no, operator_address, user_id, user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def add_operator_bank(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        operator_id = request.POST.get('operator_id', '')
        beneficiary_name = request.POST.get('beneficiary_name', '')
        beneficiary_account_no = request.POST.get('beneficiary_account_no', '')
        bank_name = request.POST.get('bank_name', '')
        ifsc_code = request.POST.get('ifsc_code', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addOperatorBankAccount', [operator_id,beneficiary_name, beneficiary_account_no, bank_name, ifsc_code, user_id, user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def add_operation_managements(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        service_type_id = request.POST.get('service_type_id', '')
        om_id = request.POST.get('agent_id', '')
        is_active = request.POST.get('is_active', '')
        print(om_id)

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addCorporateOMSAccess', [corporate_id,service_type_id, om_id, user_id, user_type,is_active])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'message': 'Insert Successfully'}
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


def update_operation_managements(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        service_type_id = request.POST.get('service_type_id', '')
        om_id = request.POST.get('agent_id', '')
        oms_id = request.POST.get('oms_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporateOMSAccess', [corporate_id,service_type_id, om_id, oms_id, user_id, user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'message': 'Updated Successfully'}
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


def add_relationship_managements(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        rm_level_1_id = request.POST.get('rm_level_1_id', '')
        rm_level_2_id = request.POST.get('rm_level_2_id', '')
        is_active = request.POST.get('is_active', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addCorporateRMSAccess', [corporate_id,rm_level_1_id, rm_level_2_id, user_id, user_type,is_active])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'message': 'Insert Successfully'}
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


def update_relationship_managements(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        corporate_id = request.POST.get('corporate_id', '')
        rm_level_1_id = request.POST.get('rm_level_1_id', '')
        rm_level_2_id = request.POST.get('rm_level_2_id', '')
        rms_id = request.POST.get('rms_id', '')
        is_active = request.POST.get('is_active', '')


        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateCorporateRMSAccess', [corporate_id,rm_level_1_id, rm_level_2_id,rms_id, user_id, user_type,is_active])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def update_operator(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

        type = request.POST.get('type', '')
        username = request.POST.get('username', '')
        operator_name = request.POST.get('operator_name', '')
        operator_email = request.POST.get('operator_email', '')

        operator_contact = request.POST.get('operator_contact', '')
        website = request.POST.get('website', '')

        is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
        service_tax_number = request.POST.get('service_tax_number', '')
        night_start_time = request.POST.get('night_start_time', '')
        night_end_time = request.POST.get('night_end_time', '')
        tds_rate = request.POST.get('tds_rate', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        operator_id = request.POST.get('operator_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateOperator', [type,username,operator_name,operator_email,operator_contact,website,is_service_tax_applicable,service_tax_number,
                                                    night_start_time,night_end_time,tds_rate,gst_id,pan_no,operator_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def update_operator_contact(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        operator_id = request.POST.get('operator_id', '')

        contact_id = request.POST.get('contact_id')
        operator_address = request.POST.get('operator_address', '')
        contact_name = request.POST.get('contact_name', '')
        contact_email = request.POST.get('contact_email', '')
        contact_no = request.POST.get('contact_no', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateOperatorContact',[operator_id, contact_name, contact_email, contact_no, operator_address, user_id, user_type, contact_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def update_operator_bank(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        bank_id = request.POST.get('bank_id', '')
        beneficiary_name = request.POST.get('beneficiary_name', '')
        beneficiary_account_no = request.POST.get('beneficiary_account_no', '')
        bank_name = request.POST.get('bank_name', '')
        ifsc_code = request.POST.get('ifsc_code', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateOperatorBankAccount', [beneficiary_name, beneficiary_account_no, bank_name, ifsc_code, user_id, user_type, bank_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def delete_operator(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_id = request.POST.get('user_id', '')
        operator_id = request.POST.get('operator_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteOperators', [operator_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Operators': emp}
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


def delete_operator_contact(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_id = request.POST.get('user_id', '')
        contact_id = request.POST.get('contact_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteOperatorContact', [contact_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Operators': emp}
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


def delete_operator_bank(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_id = request.POST.get('user_id', '')
        bank_id = request.POST.get('bank_id', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteOperatorBankAccount', [bank_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Operators': emp}
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


def operator_rates(request):
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
                    cursor.callproc('getAllOperatorRates', [])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Rates': emp}
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


def view_operator_rate(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        rate_id = request.POST.get('rate_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewOperatorRate', [rate_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Rate': emp}
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


def add_operator_rate(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

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
        fuel_rate = request.POST.get('fuel_rate')

        if fuel_rate:
            fuel_rate = fuel_rate
        else:
            fuel_rate = 0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addOperatorRate', [operator_id,city_id,taxi_type_id,package_name,tour_type,kms,hours,km_rate,hour_rate,
                                    base_rate,night_rate,fuel_rate,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def update_operator_rate(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
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
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateOperatorRate', [operator_id,city_id,taxi_type_id,package_name,tour_type,kms,hours,km_rate,hour_rate,
                                    base_rate,night_rate,fuel_rate,rate_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
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


def delete_operator_rate(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_id = request.POST.get('user_id', '')
        rate_id = request.POST.get('rate_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteOperatorRate', [rate_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Operators': emp}
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


def operator_drivers(request):
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
                    cursor.callproc('getAllOperatorDrivers', [])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Drivers': emp}
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


def view_operator_driver(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        driver_id = request.POST.get('driver_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewOperatorDriver', [driver_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Drivers': emp}
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


def add_operator_driver(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        operator_id = request.POST.get('operator_id', '')
        driver_name = request.POST.get('driver_name', '')
        driver_contact = request.POST.get('driver_contact', '')
        driver_email = request.POST.get('driver_email', '')
        licence_no = request.POST.get('licence_no', '')
        password = request.POST.get('password', '')
        fcm_regid = request.POST.get('fcm_regid', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addOperatorDriver', [operator_id,driver_name,driver_contact,driver_email,licence_no,password,fcm_regid,user_id,user_type])
                    emp = dictfetchall(cursor)
                    print(emp)
                    cursor.close()
                    data = {'success': 1, 'Drivers': emp}
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


def update_operator_driver(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        driver_id = request.POST.get('driver_id', '')

        user_id = request.POST.get('user_id', '')
        operator_id = request.POST.get('operator_id', '')
        driver_name = request.POST.get('driver_name', '')
        driver_contact = request.POST.get('driver_contact', '')
        driver_email = request.POST.get('driver_email', '')
        licence_no = request.POST.get('licence_no', '')
        fcm_regid = request.POST.get('fcm_regid', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateOperatorDriver', [operator_id,driver_name,driver_contact,driver_email,licence_no,fcm_regid,driver_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Drivers': emp}
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


def delete_operator_driver(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_id = request.POST.get('user_id', '')
        driver_id = request.POST.get('driver_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteOperatorDriver', [driver_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Operators': emp}
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


def agent_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_type = request.POST.get('booking_type', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllTaxiBookings', [booking_type])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
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


def agent_add_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')

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
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = {}
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                try:

                    cursor.callproc('addTaxiBooking', [user_type,user_id,corporate_id,spoc_id,group_id,subgroup_id,tour_type,pickup_city,pickup_location,drop_location,pickup_datetime,
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
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def accept_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('acceptTaxiBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def reject_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('acceptTaxiBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def assign_taxi_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        vendor_booking_id = request.POST.get('vendor_booking_id', '')
        operator_id = request.POST.get('operator_id', '')
        driver_id = request.POST.get('driver_id', '')
        taxi_id = request.POST.get('taxi_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignTaxiBooking', [vendor_booking_id,operator_id,driver_id,taxi_id,booking_id,user_id,user_type])
                    data = {'success': 1}
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

################################################### BUS #############################


def agent_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_type = request.POST.get('booking_type', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAgentBusBookings', [booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
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


def accept_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('acceptBusBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def reject_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('rejectBusBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def assign_bus_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        ticket_no = request.POST.get('ticket_no', '')
        pnr_no = request.POST.get('pnr_no', '')
        assign_bus_type_id = request.POST.get('assign_bus_type_id', '')
        seat_no = request.POST.get('seat_no', '')
        portal_used = request.POST.get('portal_used', '')
        operator_name = request.POST.get('operator_name', '')
        operator_contact = request.POST.get('operator_contact', '')
        boarding_point = request.POST.get('boarding_point', '')
        boarding_datetime = request.POST.get('boarding_datetime', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignBusBooking', [ticket_no,pnr_no,assign_bus_type_id,seat_no,portal_used,operator_name,operator_contact,boarding_point,boarding_datetime,booking_id,user_id,user_type])
                    data = {'success': 1}
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


################################################### TRAIN  #############################


def agent_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_type = request.POST.get('booking_type', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAgentTrainBookings', [booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
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


def accept_train_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('acceptTrainBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def reject_train_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('rejectTrainBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def assign_train_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        ticket_no = request.POST.get('ticket_no', '')
        pnr_no = request.POST.get('pnr_no', '')
        assign_bus_type_id = request.POST.get('assign_bus_type_id', '')
        seat_no = request.POST.get('seat_no', '')
        portal_used = request.POST.get('portal_used', '')
        operator_name = request.POST.get('operator_name', '')
        operator_contact = request.POST.get('operator_contact', '')
        boarding_point = request.POST.get('boarding_point', '')
        boarding_datetime = request.POST.get('boarding_datetime', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignTrainBooking', [ticket_no,pnr_no,assign_bus_type_id,seat_no,portal_used,operator_name,operator_contact,boarding_point,boarding_datetime,booking_id,user_id,user_type])
                    data = {'success': 1}
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


################################################### Hotels  #############################


def agent_hotel_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_type = request.POST.get('booking_type', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllAgentHotelBookings', [booking_type])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllHotelBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
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


def accept_hotel_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('acceptHotelBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def reject_hotel_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('rejectHotelBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def assign_hotel_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        assign_hotel_id = request.POST.get('assign_hotel_id', '')
        assign_room_type = request.POST.get('assign_room_type', '')

        total_room_price = request.POST.get('total_room_price', '')
        voucher_number = request.POST.get('voucher_number', '')
        portal_used = request.POST.get('portal_used', '')
        commission_earned = request.POST.get('commission_earned', '')

        is_ac_room = request.POST.get('is_ac_room', '')
        daily_brakefast = request.POST.get('daily_brakefast', '')
        is_prepaid = request.POST.get('is_prepaid', '')
        agent_booking_id = request.POST.get('agent_booking_id', '')
        comment = request.POST.get('comment', '')

        if commission_earned:
            pass
        else:
            commission_earned = 0

        if agent_booking_id:
            pass
        else:
            agent_booking_id = 0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignHotelBooking', [assign_hotel_id,assign_room_type,is_ac_room,daily_brakefast,is_prepaid,agent_booking_id,comment,booking_id,user_id,user_type,total_room_price,voucher_number,portal_used,commission_earned])
                    data = {'success': 1}
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

################################################### Flight  #############################


def agent_flight_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_type = request.POST.get('booking_type', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllAgentFlightBookings', [booking_type])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        cursor1.close()
                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp}
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


def accept_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('acceptFlightBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def reject_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('rejectFlightBooking', [booking_id,user_id,user_type])
                    data = {'success': 1}
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


def assign_flight_booking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')
        no_of_passanger = request.POST.get('no_of_passanger', '')
        finalpass = int(no_of_passanger)

        meal_is_include = request.POST.get('meal_is_include', '')
        fare_type = request.POST.get('fare_type', '')
        trip_type = request.POST.get('trip_type', '')
        flight_type = request.POST.get('flight_type', '')
        seat_type = request.POST.get('seat_type', '')
        no_of_stops = request.POST.get('no_of_stops', '')
        final_no_of_stop = int(no_of_stops)

        ticket_number = request.POST.getlist('ticket_no', '')

        employee_booking_id = request.POST.getlist('employee_booking_id', '')

        flight_from = request.POST.getlist('flight_from', '')
        flight_to = request.POST.getlist('flight_to', '')
        departure_time = request.POST.getlist('departure_time', '')
        arrival_time = request.POST.getlist('arrival_time', '')
        flight_name = request.POST.getlist('flight_name', '')
        flight_no = request.POST.getlist('flight_no', '')
        pnr_no = request.POST.getlist('pnr_no', '')

        print("Stop")
        print(flight_from)
        print(final_no_of_stop)
        for x in range(final_no_of_stop+1):
            print(flight_from[x])
        print(pnr_no)

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    print("i m here")
                    cursor.callproc('assignFlightBooking', [flight_type,seat_type,trip_type,no_of_stops,booking_id,meal_is_include,fare_type,user_id,user_type])
                    result = dictfetchall(cursor)

                    cursor.close()

                    for x in range(final_no_of_stop+1):

                        cursor1 = connection.cursor()
                        cursor1.callproc('addFlightBookingFlights',[flight_name[x], flight_no[x], pnr_no[x], flight_from[x], flight_to[x], departure_time[x], arrival_time[x], booking_id, user_id, user_type])
                        result = dictfetchall(cursor1)
                        cursor1.close()

                    for xx in range(finalpass):
                        print("1i m here")
                        print(employee_booking_id[xx])
                        print(booking_id)
                        print("herer 2")
                        cursor2 = connection.cursor()
                        cursor2.callproc('updateFlightPassangerTickectNo',[ticket_number[xx],employee_booking_id[xx],booking_id])
                        result = dictfetchall(cursor2)

                        cursor2.close()

                    data = {'success': 1}
                    return JsonResponse(data)
                except Exception as e:
                    print(e)
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

#########################################3

def get_city_id(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        post_str = request.POST.get('search_string')


        my_list = post_str.split(",")

        li = []
        for i in my_list:
            v = i.strip()
            li.append(v)

        search_str = ",".join(map(str, li))

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getCityId', [search_str])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'city_id': emp}
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
