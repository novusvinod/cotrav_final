from datetime import datetime

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


def employee_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllEmployeeTaxiBookings', [spoc_id])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    cursor1 = connection.cursor()
                    booking_id = e['id']
                    cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    e['Passangers'] = passanger
                    cursor1.close()
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


def employee_add_taxi_booking(request):
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


def employee_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllEmployeeBusBookings', [spoc_id])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    cursor1 = connection.cursor()
                    booking_id = e['id']
                    cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    e['Passangers'] = passanger
                    cursor1.close()
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


def employee_add_bus_booking(request):
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

                    cursor.callproc('addBusBooking', [user_type,user_id,corporate_id,spoc_id,group_id,subgroup_id,tour_type,pickup_city,pickup_location,drop_location,pickup_datetime,
                                                             taxi_type,package_id,no_of_days,reason_booking,no_of_seats])
                    booking_id = dictfetchall(cursor)
                    cursor.close()
                    for id in booking_id:
                        for e in employees:
                            cursor = connection.cursor()
                            cursor.callproc('addEmployeeBusBooking',[id['id'],e])
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


def employee_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllEmployeeTrainBookings', [spoc_id])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    cursor1 = connection.cursor()
                    booking_id = e['id']
                    cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    e['Passangers'] = passanger
                    cursor1.close()
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


def employee_add_train_booking(request):
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

                    cursor.callproc('addBusBooking', [user_type,user_id,corporate_id,spoc_id,group_id,subgroup_id,tour_type,pickup_city,pickup_location,drop_location,pickup_datetime,
                                                             taxi_type,package_id,no_of_days,reason_booking,no_of_seats])
                    booking_id = dictfetchall(cursor)
                    cursor.close()
                    for id in booking_id:
                        for e in employees:
                            cursor = connection.cursor()
                            cursor.callproc('addEmployeeBusBooking',[id['id'],e])
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
            print(user)
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
                print(user_info)
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