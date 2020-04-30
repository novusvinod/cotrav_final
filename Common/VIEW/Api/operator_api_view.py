from datetime import datetime
from threading import Thread
import string
import random
from django.http import JsonResponse
from django.db import connection
from Common.VIEW.Api.api_views import getUserinfoFromAccessToken, dictfetchall
from Common.email_settings import RejectBooking_Email


def operator_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorTaxiBookings', [operator_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type
                        cursor1.close()
                    data = {'success': 1, 'Bookings': emp, 'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def operator_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorBusBookings', [operator_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type
                        cursor1.close()
                    data = {'success': 1, 'Bookings': emp, 'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def operator_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorTrainBookings', [operator_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type
                        cursor1.close()
                    data = {'success': 1, 'Bookings': emp, 'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def operator_hotel_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorHotelBookings', [operator_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        cursor1.callproc('getAllHotelBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type
                        cursor1.close()
                    data = {'success': 1, 'Bookings': emp, 'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def operator_flight_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('operator_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllOperatorFlightBookings', [operator_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type
                        cursor1.close()
                    data = {'success': 1, 'Bookings': emp, 'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def operator_reject_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')
        user_comment = request.POST.get('user_comment', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('rejectOperatorTaxiBookings', [user_id,user_type,booking_id,user_comment])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
                    cursor.close()

                    cursor2 = connection.cursor()
                    cursor2.callproc('viewTaxiBooking', [booking_id])
                    emp = dictfetchall(cursor2)
                    cursor2.close()

                    cursor1 = connection.cursor()
                    cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                    passanger = dictfetchall(cursor1)
                    emp[0]['Passangers'] = passanger
                    cursor1.close()

                    add_booking_email = RejectBooking_Email()
                    thread = Thread(target=add_booking_email.send_email_sms_ntf, args=(emp, "Flight"))
                    thread.start()

                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)






############################ Driver API #############################################

def driver_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        operator_id = request.POST.get('driver_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')
        page_no = request.POST.get('page_no', '')
        limit_from = 0
        limit_to = 0
        print(page_no)
        if page_no:
            limit_from = (int(page_no) - 1) * 10
            limit_to = 10
        else:
            limit_from = 0
            limit_to = 2147483647

        user_token = req_token.split()
        if user_token[0] == 'Token':

            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllDriverTaxiBookings', [operator_id,booking_type,limit_from,limit_to])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type
                        cursor1.close()
                    data = {'success': 1, 'Bookings': emp, 'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def started_from_garage(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        start_km = request.POST.get('start_garage_km_reading', '')
        start_garage_lat = request.POST.get('start_garage_lat', '')
        start_garage_lng = request.POST.get('start_garage_lng', '')
        start_datetime = request.POST.get('start_datetime', '')
        if start_datetime:
            start_datetime = datetime.strptime(start_datetime, '%d-%m-%Y %H:%M:%S')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addStartFromGarage', [booking_id,start_km,start_garage_lat,start_garage_lng,start_datetime])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'data': 'Status Update Successfully'}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def arrived_at_pickup(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        to_arrived_google = request.POST.get('cal_distance_start_garage_to_arrived_google', '')
        to_arrived_self = request.POST.get('cal_distance_start_garage_to_arrived_self', '')
        arrived_datetime = request.POST.get('arrived_datetime', '')
        if arrived_datetime:
            arrived_datetime = datetime.strptime(arrived_datetime, '%d-%m-%Y %H:%M:%S')
        user = {}
        booking_type = request.POST.get('booking_type', '')
        generate_otp = ''.join(random.choice(string.digits) for _ in range(6))

        user_token = req_token.split()
        if user_token[0] == 'Token':

            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addArrivedAtPickup', [booking_id,to_arrived_google,to_arrived_self,arrived_datetime])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'data': 'Status Update Successfully', 'start_otp':generate_otp}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def started_from_pickup(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        pickup_lat = request.POST.get('pickup_lat', '')
        pickup_lng = request.POST.get('pickup_lng', '')
        pickup_km_reading = request.POST.get('pickup_km_reading', '')
        pickup_datetime = request.POST.get('pickup_datetime', '')
        if pickup_datetime:
            pickup_datetime = datetime.strptime(pickup_datetime, '%d-%m-%Y %H:%M:%S')

        user = {}
        booking_type = request.POST.get('booking_type', '')
        generate_otp = ''.join(random.choice(string.digits) for _ in range(6))

        user_token = req_token.split()
        if user_token[0] == 'Token':

            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addStartedFromPickup', [booking_id,pickup_lat,pickup_lng,pickup_km_reading,pickup_datetime])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'data': 'Status Update Successfully', 'end_otp':generate_otp}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def arrived_at_drop(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')
        drop_lat = request.POST.get('drop_lat', '')
        drop_lng = request.POST.get('drop_lng', '')
        drop_km_reading = request.POST.get('drop_km_reading', '')
        drop_google = request.POST.get('cal_distance_start_garage_to_drop_google', '')
        drop_self = request.POST.get('cal_distance_start_garage_to_drop_self', '')
        pickup_to_drop_google = request.POST.get('cal_distance_pickup_to_drop_google', '')
        end_garage = request.POST.get('est_distance_drop_to_end_garage', '')
        drop_to_end_garage = request.POST.get('est_time_drop_to_end_garage', '')
        state_tax = request.POST.get('state_tax', '')
        parking = request.POST.get('parking', '')
        toll_tax = request.POST.get('toll_tax', '')
        extras = request.POST.get('extras', '')
        drop_datetime = request.POST.get('drop_datetime', '')
        if drop_datetime:
            drop_datetime = datetime.strptime(drop_datetime, '%d-%m-%Y %H:%M:%S')

        user = {}

        user_token = req_token.split()
        if user_token[0] == 'Token':

            try:
                user = getUserinfoFromAccessToken(user_token[1], user_type)
            except Exception as e:
                data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
                return JsonResponse(data)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('addArrivedAtDrop', [booking_id,drop_lat,drop_lng,drop_km_reading,drop_google,drop_self,pickup_to_drop_google,end_garage,
                    drop_to_end_garage,state_tax,parking,toll_tax,extras,drop_datetime,'@start_garage_km_reading'])
                    emp1 = dictfetchall(cursor)
                    print(emp1)
                    cursor.execute("SELECT @start_garage_km_reading")
                    start_garage_km_reading = cursor.fetchone()[0]
                    print(start_garage_km_reading)
                    if not start_garage_km_reading:
                        start_garage_km_reading = 0
                    cursor.close()

                    cursor1 = connection.cursor()
                    cursor1.callproc('viewTaxiBooking', [booking_id])
                    emp = dictfetchall(cursor1)
                    cursor1.close()

                    payin_slip = ""
                    cotrav_billing_entity = 1
                    bb_entity = emp[0]['billing_entity_id']
                    radio_rate = emp[0]['base_rate']

                    tour_type_id = emp[0]['tour_type']

                    pickup_datetime = emp[0]['pickup_datetime']
                    if pickup_datetime:
                        pickup_datetime = datetime.strptime(pickup_datetime, '%d-%m-%Y %H:%M')

                    diff = drop_datetime - pickup_datetime

                    days, seconds = diff.days, diff.seconds

                    if tour_type_id == 1:
                        hrs_done = days * 24 + seconds // 3600
                        print("i  mheheheherhrh")
                        print(hrs_done)
                    else:
                        hrs_done = days * 24 + seconds // 3600
                        print("i  mheheheherhrh else")
                        print(hrs_done)

                    allowed_hrs = emp[0]['hours']

                    extra_hrs = hrs_done - allowed_hrs
                    print(extra_hrs)
                    if extra_hrs < 0:
                        extra_hrs = 0

                    hr_rate = emp[0]['hour_rate']
                    print(hr_rate)
                    extra_hrs_charge = hr_rate * extra_hrs
                    print(extra_hrs_charge)
                    print("end allowed_kms_per_day ")
                    print(extra_hrs_charge)
                    start_km = start_garage_km_reading
                    end_km = drop_km_reading + drop_to_end_garage
                    print(end_km)
                    print("start_km")
                    print(start_km)
                    kms_done = float(end_km) - float(start_km)
                    print("kms_done")
                    print(kms_done)
                    allowed_kms_per_day = emp[0]['kms']

                    if tour_type_id == 1 :
                        allowed_kms = allowed_kms_per_day
                    else:
                        allowed_kms = allowed_kms_per_day * hrs_done

                    extra_kms = kms_done - allowed_kms
                    if extra_kms < 0:
                        extra_kms = 0
                    km_rate = emp[0]['km_rate']
                    extra_kms_charge = km_rate * extra_kms

                    driver_allowance_per_day = emp[0]['night_rate']
                    if tour_type_id == 1:
                        driver_allowance = driver_allowance_per_day
                    else:
                        driver_allowance = driver_allowance_per_day * hrs_done
                    print("i  mheheheherhrh else")
                    base_rate_per_day = emp[0]['base_rate']
                    if tour_type_id == 1:
                        base_rate = base_rate_per_day
                    else:
                        base_rate = base_rate_per_day * hrs_done

                    total_ex_tax = base_rate + extra_kms_charge + extra_hrs_charge + driver_allowance
                    tax_rate = 12
                    igst = (total_ex_tax * 12) / 100
                    print("i  mheheheherhrh else")
                    total_after_tax = float(total_ex_tax) + float(igst) + float(state_tax) + float(parking) + float(toll_tax) + float(extras)
                    print("Total after taxxxx")
                    print(total_after_tax)
                    cursor2 = connection.cursor()
                    cursor2.callproc('addTaxiInvoice',
                                    [tax_rate, tax_rate, igst, 0,0, igst, 0, 0, igst, 0, 0,
                                     hrs_done, allowed_hrs, extra_hrs, hr_rate, days, start_km, end_km,
                                     kms_done, allowed_kms, extra_kms, km_rate, base_rate, extra_hrs_charge,
                                     extra_kms_charge, driver_allowance, total_ex_tax, extras, total_after_tax,
                                     total_after_tax, radio_rate, bb_entity, cotrav_billing_entity, booking_id, user_id,
                                     user_type, payin_slip])
                    company = dictfetchall(cursor2)

                    cursor1 = connection.cursor()
                    cursor1.callproc('viewTaxiBooking', [booking_id])
                    emp = dictfetchall(cursor1)
                    cursor1.close()


                    cursor.close()
                    data = {'success': 1, 'data': 'Status Update Successfully', 'InvoiceDetails':emp}
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