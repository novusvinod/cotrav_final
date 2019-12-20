from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from Common.VIEW.Api.api_views import getUserinfoFromAccessToken, dictfetchall

from Common.email_settings import Assign_Booking_Email
from landing.cotrav_messeging import Render, Bus, Flight, Hotel


def operators_by_service_type(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        service_type = request.POST.get('service_type', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorsbyServiceType', [service_type])
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


def hotels(request):
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
                    cursor.callproc('getAllHotels', [])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Hotels': emp}
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


def add_hotel(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        hotel_name = request.POST.get('hotel_name', '')
        hotel_email = request.POST.get('hotel_email', '')
        hotel_contact = request.POST.get('hotel_contact', '')
        website = request.POST.get('website', '')

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
                    cursor.callproc('addHotel', [hotel_name,hotel_email,hotel_contact,website,hotel_address,contact_name,contact_email,contact_no,beneficiary_name,beneficiary_account_no,
                                                    ifsc_code,is_service_tax_applicable,tds_rate,gst_id,pan_no,user_id,user_type,bank_name])
                    emp = dictfetchall(cursor)
                    print(emp)
                    data = {'success': 1, 'message': "Operator Added Successfully", 'id':emp}
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





def update_hotel(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        hotel_name = request.POST.get('hotel_name', '')
        hotel_email = request.POST.get('hotel_email', '')
        hotel_contact = request.POST.get('hotel_contact', '')
        website = request.POST.get('website', '')

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
                    cursor.callproc('updateHotel', [hotel_name,hotel_email,hotel_contact,website,hotel_address, is_service_tax_applicable,tds_rate,gst_id,pan_no,user_id,user_type,hotel_id])
                    emp = dictfetchall(cursor)
                    print(emp)
                    data = {'success': 1, 'message': "Operator Added Successfully", 'id':emp}
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


def view_hotel(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        hotel_id = request.POST.get('hotel_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('viewHotel', [hotel_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Hotels': emp}
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


def hotel_contacts(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('hotel_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllHotelContacts', [operator_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'HotelContacts': emp}
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


def hotel_banks(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('hotel_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllHotelBankAccount', [operator_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'HotelBanks': emp}
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

                    data = {'success': 1, 'Access': emp}
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

                    data = {'success': 1, 'Access': emp}
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
                    print(emp)
                    data = {'success': 1, 'message': "Operator Added Successfully", 'id':emp}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Contact Added Successfully"}
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

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Banks Added Successfully"}
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


def add_hotel_contact(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        operator_id = request.POST.get('hotel_id', '')
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
                    cursor.callproc('addHotelContact',
                                    [operator_id, contact_name, contact_email, contact_no, operator_address, user_id, user_type])
                    emp = dictfetchall(cursor)
                    print(emp)
                    cursor.close()
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Contact Added Successfully"}
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


def add_hotel_bank(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        operator_id = request.POST.get('hotel_id', '')
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
                    cursor.callproc('addHotelBankAccount', [operator_id,beneficiary_name, beneficiary_account_no, bank_name, ifsc_code, user_id, user_type])
                    emp = dictfetchall(cursor)

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Banks Added Successfully"}
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

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "OMS Added Successfully"}
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

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "OMS Updated Successfully"}
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

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "RMS Added Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "RMS Updated Successfully"}
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
                    company = dictfetchall(cursor)
                    print(company)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Updated Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Contact Updated Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator BankAccount Successfully"}
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


def update_hotel_contact(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user_id = request.POST.get('user_id', '')

        operator_id = request.POST.get('hotel_id', '')

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
                    cursor.callproc('updateHotelContact',[operator_id, contact_name, contact_email, contact_no, operator_address, user_id, user_type, contact_id])
                    emp = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Contact Updated Successfully"}
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


def update_hotel_bank(request):
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
                    cursor.callproc('updateHotelBankAccount', [beneficiary_name, beneficiary_account_no, bank_name, ifsc_code, user_id, user_type, bank_id])
                    emp = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator BankAccount Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Deleted Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Contact Deleted Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Contact Deleted Successfully"}
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


def delete_hotel(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        user = {}
        user_id = request.POST.get('user_id', '')
        operator_id = request.POST.get('hotel_id', '')
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('deleteHotels', [operator_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Deleted Successfully"}
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


def delete_hotel_contact(request):
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
                    cursor.callproc('deleteHotelContact', [contact_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Hotel Contact Deleted Successfully"}
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


def delete_hotel_bank(request):
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
                    cursor.callproc('deleteHotelBankAccount', [bank_id,user_id,user_type])
                    emp = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Hotel Bank Deleted Successfully"}
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


def operator_rates(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        if user_id:
            pass
        else:
            user_id = 0
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorRates', [user_id])
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Rate Deleted Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Rate Updated Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Rate Deleted Successfully"}
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


def operator_drivers(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        user_id = request.POST.get('user_id', '')
        if user_id:
            pass
        else:
            user_id =0


        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorDrivers', [user_id])
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
        taxi_id = request.POST.get('taxi_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addOperatorDriver', [operator_id,driver_name,driver_contact,driver_email,licence_no,password,fcm_regid,user_id,user_type,taxi_id])
                    emp = dictfetchall(cursor)
                    print(emp)
                    data = {'success': 1, 'message': "Operator Driver Added Successfully",'id':emp}
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
        taxi_id = request.POST.get('taxi_id', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('updateOperatorDriver', [operator_id,driver_name,driver_contact,driver_email,licence_no,fcm_regid,driver_id,user_id,user_type,taxi_id])
                    emp = dictfetchall(cursor)
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Driver Updated Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Operator Driver Deleted Successfully"}
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


def agent_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_type = request.POST.get('booking_type', '')
        user = {}
        user_token = req_token.split()
        print("Tokennnnnnn")
        print(user_token)
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
        pickup_datetime = datetime.strptime(pickup_datetime, '%d-%m-%Y %H:%M:%S')
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Booking Accepted Successfully"}
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
                    cursor.callproc('rejectTaxiBooking', [booking_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Taxi Booking Rejected Successfully"}
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


def assign_operator_taxi_boooking(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        operator_id = request.POST.get('operator_id', '')
        user_id = request.POST.get('user_id', '')
        operator_contact = request.POST.get('operator_contact', '')
        operator_email = request.POST.get('operator_email', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignOperatorTaxiBooking',[operator_id, booking_id, user_id, user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        # communication = Assign_Booking_Email()
                        # resp1 = communication.send_client_sms("", "Taxi")
                        # resp1 = communication.is_client_email("", "Taxi", "")
                        data = {'success': 1, 'message': "Taxi Booking Assign Successfully"}
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

        is_client_sms = request.POST.get('is_client_sms', '')
        is_client_email = request.POST.get('is_client_email', '')
        is_driver_sms = request.POST.get('is_driver_sms', '')

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignTaxiBooking', [vendor_booking_id,operator_id,driver_id,taxi_id,booking_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewTaxiBooking', [booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        communication = Assign_Booking_Email()
                        if is_client_sms:
                            resp1 = communication.send_client_sms(emp, "Taxi")
                        if is_client_email:
                            resp1 = communication.is_client_email(emp, "Taxi", "")
                        data = {'success': 1, 'message': "Taxi Booking Assign Successfully"}
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


def add_taxi_invoice(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')

        tax_on_management_fee = request.POST.get('tax_on_management_fee', '')
        tax_on_management_fee_percentage = request.POST.get('tax_on_management_fee_percentage', '')
        management_fee_igst = request.POST.get('management_fee_igst', '')
        management_fee_cgst = request.POST.get('management_fee_cgst', '')
        management_fee_sgst = request.POST.get('management_fee_sgst', '')
        management_fee_igst_rate = request.POST.get('management_fee_igst_rate', '')
        management_fee_cgst_rate = request.POST.get('management_fee_cgst_rate', '')
        management_fee_sgst_rate = request.POST.get('management_fee_sgst_rate', '')
        igst_amount = request.POST.get('igst_amount', '')
        cgst_amount = request.POST.get('cgst_amount', '')
        sgst_amount = request.POST.get('sgst_amount', '')

        hours_done = request.POST.get('hours_done', '')
        if not hours_done:
            hours_done=0
        allowed_hours = request.POST.get('allowed_hours', '')
        if not allowed_hours:
            allowed_hours=0
        extra_hours = request.POST.get('extra_hours', '')
        if not extra_hours:
            extra_hours=0
        charge_hour = request.POST.get('charge_hour', '')
        if not charge_hour:
            charge_hour=0
        days = request.POST.get('days', '')
        if not days:
            days=0
        start_km = request.POST.get('start_km', '')
        if not start_km:
            start_km=0
        end_km = request.POST.get('end_km', '')
        if not end_km:
            end_km=0
        kms_done = request.POST.get('kms_done', '')
        if not kms_done:
            kms_done=0
        allowed_kms = request.POST.get('allowed_kms', '')
        if not allowed_kms:
            allowed_kms=0
        extra_kms = request.POST.get('extra_kms', '')
        if not extra_kms:
            extra_kms=0
        extra_km_rate = request.POST.get('extra_km_rate', '')
        if not extra_km_rate:
            extra_km_rate=0

        cotrav_billing_entity = request.POST.get('cotrav_billing_entity', '')
        bb_entity = request.POST.get('bb_entity', '')
        radio_rate = request.POST.get('radio_rate', '')
        if not radio_rate:
            radio_rate=0

        base_rate = request.POST.get('base_rate', '')
        if not base_rate:
            base_rate=0
        extra_hr_charges = request.POST.get('extra_hr_charges', '')
        if not extra_hr_charges:
            extra_hr_charges=0
        extra_km_charges = request.POST.get('extra_km_charges', '')
        if not extra_km_charges:
            extra_km_charges=0
        driver_allowance = request.POST.get('driver_allowance', '')
        if not driver_allowance:
            driver_allowance=0
        total_excluding_tax = request.POST.get('total_excluding_tax', '')
        if not total_excluding_tax:
            total_excluding_tax=0
        other_charges = request.POST.get('other_charges', '')
        if not other_charges:
            other_charges=0
        total = request.POST.get('total', '')
        if not total:
            total=0
        sub_total = request.POST.get('sub_total', '')

        if hours_done:
            pass
        else:
            charge_hour=0
        if allowed_hours:
            pass
        else:
            allowed_hours=0

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addTaxiInvoice', [tax_on_management_fee,tax_on_management_fee_percentage,management_fee_igst,management_fee_cgst,
                    management_fee_sgst,management_fee_igst_rate,management_fee_cgst_rate, management_fee_sgst_rate,igst_amount,cgst_amount,sgst_amount,
                    hours_done,allowed_hours,extra_hours,charge_hour,days,start_km,end_km,kms_done,allowed_kms,extra_kms,extra_km_rate,base_rate,extra_hr_charges,
                    extra_km_charges,driver_allowance,total_excluding_tax,other_charges,total,sub_total,radio_rate,bb_entity,cotrav_billing_entity,booking_id,user_id,user_type])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:

                        data = {'success': 1, 'message': "Taxi Booking Assign Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Bus Booking Accepted Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Bus Booking Rejected Successfully"}
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
        boarding_datetime = datetime.strptime(boarding_datetime, '%d-%m-%Y %H:%M:%S')

        ticket_price = request.POST.get('ticket_price', '')
        management_fee = request.POST.get('management_fee', '')
        tax_mng_amt = request.POST.get('tax_mng_amt', '')
        tax_on_management_fee = request.POST.get('tax_on_management_fee', '')
        tax_on_management_fee_percentage = request.POST.get('tax_on_management_fee_percentage', '')
        sub_total = request.POST.get('sub_total', '')
        management_fee_igst = request.POST.get('management_fee_igst', '')
        management_fee_cgst = request.POST.get('management_fee_cgst', '')
        management_fee_sgst = request.POST.get('management_fee_sgst', '')
        management_fee_igst_rate = request.POST.get('management_fee_igst_rate', '')
        management_fee_cgst_rate = request.POST.get('management_fee_cgst_rate', '')
        management_fee_sgst_rate = request.POST.get('management_fee_sgst_rate', '')
        cgst = request.POST.get('cgst', '')
        sgst = request.POST.get('sgst', '')
        igst = request.POST.get('igst', '')
        cotrav_billing_entity = request.POST.get('cotrav_billing_entity', '')


        oper_ticket_price = request.POST.get('oper_ticket_price', '')

        oper_commission = request.POST.get('oper_commission', '')

        oper_commission_type = request.POST.get('oper_commission_type', '')

        oper_cotrav_billing_entity = request.POST.get('oper_cotrav_billing_entity', '')

        oper_cgst = request.POST.get('oper_cgst', '')
        oper_sgst = request.POST.get('oper_sgst', '')
        oper_igst = request.POST.get('oper_igst', '')

        igst_amount = request.POST.get('igst_amount', '')
        cgst_amount = request.POST.get('cgst_amount', '')
        sgst_amount = request.POST.get('sgst_amount', '')

        client_ticket_path = request.POST.get('client_ticket_path')

        vender_ticket_path = request.POST.get('vender_ticket_path')

        client_ticket = request.POST.get('client_ticket')

        is_client_sms = request.POST.get('is_client_sms', '')
        is_client_email = request.POST.get('is_client_email', '')
        is_driver_sms = request.POST.get('is_driver_sms', '')
        print("i m here")
        tax_on_management_fee = tax_mng_amt

        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignBusBooking', [ticket_no,pnr_no,assign_bus_type_id,seat_no,portal_used,operator_name,operator_contact,boarding_point,boarding_datetime,booking_id,user_id,user_type,ticket_price,management_fee,tax_on_management_fee,tax_on_management_fee_percentage,sub_total,cotrav_billing_entity,igst,cgst,sgst,management_fee_igst,management_fee_cgst,management_fee_sgst,management_fee_igst_rate,management_fee_cgst_rate,management_fee_sgst_rate,tax_mng_amt,oper_ticket_price,oper_commission,oper_commission_type,oper_cotrav_billing_entity,oper_igst,oper_cgst,oper_sgst,client_ticket_path,vender_ticket_path,igst_amount,cgst_amount,sgst_amount])
                    company = dictfetchall(cursor)
                    print(company)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewBusBooking', [booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()
                        print("in send page")
                        get_voucher_path = ''
                        print(client_ticket)
                        if client_ticket == 1:
                            voucher = emp[0]
                            bus_pdf = Bus(voucher)
                            get_vou = bus_pdf.get(request)
                            get_voucher_path = get_vou[1]
                        else:
                            get_voucher_path = client_ticket_path

                        add_booking_email = Assign_Booking_Email()
                        if is_client_sms:
                            resp1 = add_booking_email.send_client_sms(emp, "Bus")
                        if is_client_email:
                            resp1 = add_booking_email.is_client_email(emp, "Bus",get_voucher_path)

                        data = {'success': 1, 'message': "Bus Booking Assigned Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Train Booking Accepted Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Train Booking Reject Successfully"}
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

        train_name = request.POST.get('train_name', '')
        ticket_no = request.POST.get('ticket_no', '')
        pnr_no = request.POST.get('pnr_no', '')
        assign_bus_type_id = request.POST.get('assign_bus_type_id', '')
        seat_no = request.POST.get('seat_no', '')
        portal_used = request.POST.get('portal_used', '')
        operator_name = request.POST.get('operator_name', '')
        operator_contact = request.POST.get('operator_contact', '')
        boarding_point = request.POST.get('boarding_point', '')
        boarding_datetime = request.POST.get('boarding_datetime', '')
        boarding_datetime = datetime.strptime(boarding_datetime, '%d-%m-%Y %H:%M:%S')

        ticket_price = request.POST.get('ticket_price', '')
        management_fee = request.POST.get('management_fee', '')
        tax_mng_amt = request.POST.get('tax_mng_amt', '')
        tax_on_management_fee = request.POST.get('tax_on_management_fee', '')
        tax_on_management_fee_percentage = request.POST.get('tax_on_management_fee_percentage', '')
        sub_total = request.POST.get('sub_total', '')
        management_fee_igst = request.POST.get('management_fee_igst', '')
        management_fee_cgst = request.POST.get('management_fee_cgst', '')
        management_fee_sgst = request.POST.get('management_fee_sgst', '')
        management_fee_igst_rate = request.POST.get('management_fee_igst_rate', '')
        management_fee_cgst_rate = request.POST.get('management_fee_cgst_rate', '')
        management_fee_sgst_rate = request.POST.get('management_fee_sgst_rate', '')
        cgst = request.POST.get('cgst', '')
        sgst = request.POST.get('sgst', '')
        igst = request.POST.get('igst', '')
        cotrav_billing_entity = request.POST.get('cotrav_billing_entity', '')

        tax_on_management_fee = tax_mng_amt;

        client_ticket_path = request.POST.get('client_ticket_path')

        is_client_sms = request.POST.get('is_client_sms', '')
        is_client_email = request.POST.get('is_client_email', '')


        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('assignTrainBooking', [ticket_no,pnr_no,assign_bus_type_id,seat_no,portal_used,operator_name,operator_contact,boarding_point,boarding_datetime,booking_id,user_id,user_type,train_name,ticket_price,management_fee,tax_on_management_fee,tax_on_management_fee_percentage,sub_total,cotrav_billing_entity,igst,cgst,sgst,management_fee_igst,management_fee_cgst,management_fee_sgst,management_fee_igst_rate,management_fee_cgst_rate,management_fee_sgst_rate,tax_mng_amt,client_ticket_path])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:

                        cursor2 = connection.cursor()
                        cursor2.callproc('viewTrainBooking', [booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        add_booking_email = Assign_Booking_Email()
                        if is_client_sms:
                            resp1 = add_booking_email.send_client_sms(emp, "Train")
                        if is_client_email:
                            resp1 = add_booking_email.is_client_email(emp, "Train", client_ticket_path)
                        data = {'success': 1, 'message': "Train Booking Assign Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Hotel Booking Accepted Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Hotel Booking Reject Successfully"}
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

        ticket_price = request.POST.get('ticket_price', '')
        management_fee = request.POST.get('management_fee', '')
        tax_mng_amt = request.POST.get('tax_mng_amt', '')
        tax_on_management_fee = request.POST.get('tax_on_management_fee', '')
        tax_on_management_fee_percentage = request.POST.get('tax_on_management_fee_percentage', '')
        sub_total = request.POST.get('sub_total', '')
        management_fee_igst = request.POST.get('management_fee_igst', '')
        management_fee_cgst = request.POST.get('management_fee_cgst', '')
        management_fee_sgst = request.POST.get('management_fee_sgst', '')
        management_fee_igst_rate = request.POST.get('management_fee_igst_rate', '')
        management_fee_cgst_rate = request.POST.get('management_fee_cgst_rate', '')
        management_fee_sgst_rate = request.POST.get('management_fee_sgst_rate', '')
        cgst = request.POST.get('cgst', '')
        sgst = request.POST.get('sgst', '')
        igst = request.POST.get('igst', '')
        cotrav_billing_entity = request.POST.get('oper_cotrav_billing_entity', '')
        tax_mng_amt = 100

        oper_ticket_price = request.POST.get('oper_ticket_price', '')

        oper_commission = request.POST.get('oper_commission', '')

        oper_commission_type = request.POST.get('oper_commission_type', '')

        oper_cotrav_billing_entity = request.POST.get('oper_cotrav_billing_entity', '')

        oper_cgst = request.POST.get('oper_cgst', '')
        oper_sgst = request.POST.get('oper_sgst', '')
        oper_igst = request.POST.get('oper_igst', '')

        igst_amount = request.POST.get('igst_amount', '')
        cgst_amount = request.POST.get('cgst_amount', '')
        sgst_amount = request.POST.get('sgst_amount', '')

        client_ticket = request.POST.get('client_ticket')
        client_ticket_path = request.POST.get('client_ticket_path')
        vender_ticket_path = request.POST.get('vender_ticket_path')

        is_client_sms = request.POST.get('is_client_sms', '')
        is_client_email = request.POST.get('is_client_email', '')


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
                    cursor.callproc('assignHotelBooking', [assign_hotel_id,assign_room_type,is_ac_room,daily_brakefast,is_prepaid,agent_booking_id,
                     comment,booking_id,user_id,user_type,total_room_price,voucher_number,portal_used, commission_earned,ticket_price,management_fee,
                      tax_on_management_fee,tax_on_management_fee_percentage,sub_total,cotrav_billing_entity,igst,cgst,sgst,management_fee_igst,
                       management_fee_cgst,management_fee_sgst,management_fee_igst_rate,management_fee_cgst_rate,management_fee_sgst_rate,tax_mng_amt,
                      oper_ticket_price,oper_commission,oper_commission_type,oper_igst,oper_cgst,oper_sgst,client_ticket_path,vender_ticket_path,
                       igst_amount,cgst_amount,sgst_amount])
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:

                        cursor2 = connection.cursor()
                        cursor2.callproc('viewHotelBooking', [booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllHotelBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        get_voucher_path = ''
                        print(client_ticket)
                        if client_ticket:
                            voucher = emp[0]
                            bus_pdf = Hotel(voucher)
                            get_vou = bus_pdf.get(request)
                            get_voucher_path = get_vou[1]
                        else:
                            get_voucher_path = client_ticket_path

                        add_booking_email = Assign_Booking_Email()
                        if is_client_sms:
                            resp1 = add_booking_email.send_client_sms(emp, "Hotel")
                        if is_client_email:
                            resp1 = add_booking_email.is_client_email(emp, "Hotel", get_voucher_path)

                        data = {'success': 1, 'message': "Hotel Booking Assign Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Flight Booking Accept Successfully"}
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
                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        data = {'success': 1, 'message': "Flight Booking Reject Successfully"}
                    cursor.close()
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

        operator_id = request.POST.get('operator_id', '')
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

        ##################

        ticket_price = request.POST.get('ticket_price', '')
        management_fee = request.POST.get('management_fee', '')
        tax_mng_amt = request.POST.get('tax_mng_amt', '')
        tax_on_management_fee = request.POST.get('tax_on_management_fee', '')
        tax_on_management_fee_percentage = request.POST.get('tax_on_management_fee_percentage', '')
        sub_total = request.POST.get('sub_total', '')
        management_fee_igst = request.POST.get('management_fee_igst', '')
        management_fee_cgst = request.POST.get('management_fee_cgst', '')
        management_fee_sgst = request.POST.get('management_fee_sgst', '')
        management_fee_igst_rate = request.POST.get('management_fee_igst_rate', '')
        management_fee_cgst_rate = request.POST.get('management_fee_cgst_rate', '')
        management_fee_sgst_rate = request.POST.get('management_fee_sgst_rate', '')
        cgst = request.POST.get('cgst', '')
        sgst = request.POST.get('sgst', '')
        igst = request.POST.get('igst', '')
        cotrav_billing_entity = request.POST.get('cotrav_billing_entity', '')
        tax_on_management_fee = tax_mng_amt;

        oper_ticket_price = request.POST.get('oper_ticket_price', '')

        oper_commission = request.POST.get('oper_commission', '')

        oper_commission_type = request.POST.get('oper_commission_type', '')

        oper_cotrav_billing_entity = request.POST.get('oper_cotrav_billing_entity', '')

        oper_cgst = request.POST.get('oper_cgst', '')
        oper_sgst = request.POST.get('oper_sgst', '')
        oper_igst = request.POST.get('oper_igst', '')

        igst_amount = request.POST.get('igst_amount', '')
        cgst_amount = request.POST.get('cgst_amount', '')
        sgst_amount = request.POST.get('sgst_amount', '')

        client_ticket_path = request.POST.get('client_ticket_path')
        client_ticket = request.POST.get('client_ticket')

        vender_ticket_path = request.POST.get('vender_ticket_path')

        print(client_ticket_path)

        print(vender_ticket_path)

        is_client_sms = request.POST.get('is_client_sms', '')
        is_client_email = request.POST.get('is_client_email', '')


        #####################

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
                    cursor.callproc('assignFlightBooking', [flight_type,seat_type,trip_type,no_of_stops,booking_id,meal_is_include,fare_type,user_id,user_type,ticket_price,management_fee,tax_on_management_fee,tax_on_management_fee_percentage,sub_total,cotrav_billing_entity,igst,cgst,sgst,management_fee_igst,management_fee_cgst,management_fee_sgst,management_fee_igst_rate,management_fee_cgst_rate,management_fee_sgst_rate,tax_mng_amt,oper_ticket_price,oper_commission,oper_commission_type,oper_cotrav_billing_entity,oper_igst,oper_cgst,oper_sgst,client_ticket_path,vender_ticket_path,igst_amount,cgst_amount,sgst_amount,operator_id])
                    result = dictfetchall(cursor)

                    cursor.close()

                    for x in range(final_no_of_stop+1):

                        cursor1 = connection.cursor()
                        departure_time[x] = datetime.strptime(departure_time[x], '%d-%m-%Y %H:%M:%S')
                        arrival_time[x] = datetime.strptime(arrival_time[x], '%d-%m-%Y %H:%M:%S')
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

                    company = dictfetchall(cursor)
                    if company:
                        data = {'success': 0, 'message': company}
                    else:
                        cursor2 = connection.cursor()
                        cursor2.callproc('viewFlightBooking', [booking_id])
                        emp = dictfetchall(cursor2)
                        cursor2.close()

                        cursor1 = connection.cursor()
                        cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        emp[0]['Passangers'] = passanger
                        cursor1.close()

                        cursor2 = connection.cursor()
                        cursor2.callproc('getAllFlightBookingFlights', [booking_id])
                        flights = dictfetchall(cursor2)
                        cursor2.close()

                        emp[0]['Flights'] = flights

                        get_voucher_path = ''
                        if client_ticket:
                            voucher = emp[0]
                            bus_pdf = Flight(voucher)
                            get_vou = bus_pdf.get(request)
                            get_voucher_path = get_vou[1]
                        else:
                            get_voucher_path = client_ticket_path

                        add_booking_email = Assign_Booking_Email()
                        if is_client_sms:
                            resp1 = add_booking_email.send_client_sms(emp, "Flight")
                        if is_client_email:
                            resp1 = add_booking_email.is_client_email(emp, "Flight", get_voucher_path)

                        data = {'success': 1, 'message': "Flight Booking Assign Successfully"}
                    cursor.close()
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

def generate_pdf_voucher(data,template):
    render = Render()
    path = render.render_to_file(template,data)
    print(path)
    return path