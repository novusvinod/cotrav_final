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


def approver_2_taxi_bookings(request):
    req_token = request.META['HTTP_AUTHORIZATION']
    user_type = request.META['HTTP_USERTYPE']
    approver_2_id = request.POST.get('approver_2_id', '')
    user = {}

    if req_token:
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('AllApprover_2TaxiBookings', [approver_2_id])
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


def approver_2_accept_taxi_booking(request):
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
                cursor.callproc('Approver_2AcceptTaxiBookings', [user_id,user_type,booking_id])
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


def approver_2_reject_taxi_booking(request):
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
                cursor.callproc('Approver_2RejectTaxiBookings', [user_id,user_type,booking_id])
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