from datetime import datetime
import sys
from django.http import JsonResponse
from django.db import connection

from Common.VIEW.Api.api_views import getUserinfoFromAccessToken, dictfetchall


def admin_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
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
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAdminTaxiBookings', [corporate_id,booking_type,limit_from,limit_to])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllTaxiBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        cursor1.close()
                        if e['is_invoice']:
                            cursor2 = connection.cursor()
                            invoice_id = e['invoice_id']
                            print(invoice_id)
                            print("iiiiiiinnnnnvvvvvoooo")
                            cursor2.callproc('getallTaxiInvoiceActionLog', [invoice_id])
                            invoicess = dictfetchall(cursor2)
                            e['InvoiceActionLog'] = invoicess
                            cursor2.close()

                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type

                    data = {'success': 1, 'Bookings': emp,'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_accept_taxi_booking(request):
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
                    cursor.callproc('acceptAdminTaxiBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Accepted Successfully"}
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


def admin_reject_taxi_booking(request):
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
                    cursor.callproc('rejectAdminTaxiBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    print(emp)
                    cursor.close()
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
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
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAdminBusBookings', [corporate_id,booking_type,limit_from,limit_to])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllBusBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        cursor1.close()
                        if e['is_invoice']:
                            cursor2 = connection.cursor()
                            invoice_id = e['invoice_id']
                            print(invoice_id)
                            print("iiiiiiinnnnnvvvvvoooo")
                            cursor2.callproc('getallBusInvoiceActionLog', [invoice_id])
                            invoicess = dictfetchall(cursor2)
                            e['InvoiceActionLog'] = invoicess
                            cursor2.close()

                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type

                    data = {'success': 1, 'Bookings': emp,'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_accept_bus_booking(request):
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
                    cursor.callproc('acceptAdminBusBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Accepted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_reject_bus_booking(request):
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
                    cursor.callproc('rejectAdminBusBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Rejected Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)

############################### TRAIN #################################

def admin_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
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
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAdminTrainBookings', [corporate_id,booking_type,limit_from,limit_to])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllTrainBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        cursor1.close()
                        if e['is_invoice']:
                            cursor2 = connection.cursor()
                            invoice_id = e['invoice_id']
                            print(invoice_id)
                            print("iiiiiiinnnnnvvvvvoooo")
                            cursor2.callproc('getallTrainInvoiceActionLog', [invoice_id])
                            invoicess = dictfetchall(cursor2)
                            e['InvoiceActionLog'] = invoicess
                            cursor2.close()

                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type

                    data = {'success': 1, 'Bookings': emp,'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_accept_train_booking(request):
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
                    cursor.callproc('acceptAdminTrainBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Accepted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_reject_train_booking(request):
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
                    cursor.callproc('rejectAdminTrainBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Rejected Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


############################### Hotels #################################

def admin_hotel_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
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
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllAdminHotelBookings', [corporate_id,booking_type,limit_from,limit_to])
                    emp = dictfetchall(cursor)

                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllHotelBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        cursor1.close()
                        if e['is_invoice']:
                            cursor2 = connection.cursor()
                            invoice_id = e['invoice_id']
                            print(invoice_id)
                            print("iiiiiiinnnnnvvvvvoooo")
                            cursor2.callproc('getallHotelInvoiceActionLog', [invoice_id])
                            invoicess = dictfetchall(cursor2)
                            e['InvoiceActionLog'] = invoicess
                            cursor2.close()

                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type

                    data = {'success': 1, 'Bookings': emp,'booking_type':booking_type}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_accept_hotel_booking(request):
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
                    cursor.callproc('acceptAdminHotelBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Accepted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_reject_hotel_booking(request):
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
                    cursor.callproc('rejectAdminHotelBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Rejected Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)

############################### Flight #################################


def admin_flight_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        corporate_id = request.POST.get('corporate_id', '')
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
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                cursor = connection.cursor()
                cursor.callproc('getAllAdminFlightBookings', [corporate_id,booking_type,limit_from,limit_to])
                emp = dictfetchall(cursor)
                cursor.close()
                for e in emp:
                    try:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
                        print(booking_id)
                        cursor1.callproc('getAllFlightBookingPassangers', [booking_id])
                        passanger = dictfetchall(cursor1)
                        cursor1.close()
                        if e['is_invoice']:
                            cursor2 = connection.cursor()
                            invoice_id = e['invoice_id']
                            print(invoice_id)
                            print("iiiiiiinnnnnvvvvvoooo")
                            cursor2.callproc('getallFlightInvoiceActionLog', [invoice_id])
                            invoicess = dictfetchall(cursor2)
                            e['InvoiceActionLog'] = invoicess
                            cursor2.close()

                        e['Passangers'] = passanger
                        e['booking_type'] = booking_type

                    except Exception as e:
                        data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                        return JsonResponse(data)
                data = {'success': 1, 'Bookings': emp,'booking_type':booking_type}
                return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_accept_flight_booking(request):
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
                    cursor.callproc('acceptAdminFlightBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Accepted Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_reject_flight_booking(request):
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
                    cursor.callproc('rejectAdminFlightBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    data = {'success': 1, 'Bookings': emp, 'message': "Booking Rejected Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}
        return JsonResponse(data)


def admin_verify_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id in zip(verify_id, invoice_ids):
                        print(booking_id)
                        cursor.callproc('verifyInvoiceAdminTaxiBookings', [booking_id,user_id,user_type,invoice_id])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Verify Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_revise_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        invoice_comments = request.POST.getlist('invoice_comments', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id, invoice_comment in zip(verify_id, invoice_ids, invoice_comments):
                        print(booking_id)
                        cursor.callproc('correctionInvoiceRequestAdminTaxiBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Revise Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_verify_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:

                    for booking_id, invoice_id in zip(verify_id, invoice_ids):
                        cursor = connection.cursor()
                        cursor.callproc('verifyInvoiceAdminBusBookings', [booking_id,user_id,user_type,invoice_id])
                        emp = dictfetchall(cursor)
                        print(emp)
                        cursor.close()

                    data = {'success': 1, 'message': "invoice Verify Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_revise_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        invoice_comments = request.POST.getlist('invoice_comments', '')
        user_id = request.POST.get('user_id', '')
        print(verify_id)
        print(corporate_ids)
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id, invoice_comment in zip(verify_id, invoice_ids, invoice_comments):
                        print(booking_id)

                        cursor.callproc('correctionInvoiceRequestAdminBusBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Revise Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_verify_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        user_id = request.POST.get('user_id', '')
        print(verify_id)
        print(corporate_ids)
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id in zip(verify_id, invoice_ids):
                        print(booking_id)
                        cursor.callproc('verifyInvoiceAdminTrainBookings', [booking_id,user_id,user_type,invoice_id])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Verify Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_revise_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        invoice_comments = request.POST.getlist('invoice_comments', '')
        user_id = request.POST.get('user_id', '')
        print(verify_id)
        print(corporate_ids)
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id, invoice_comment in zip(verify_id, invoice_ids, invoice_comments):
                        print(booking_id)
                        cursor.callproc('correctionInvoiceRequestAdminTrainBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Revise Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_verify_hotel_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id in zip(verify_id, invoice_ids):
                        cursor.callproc('verifyInvoiceAdminHotelBookings', [booking_id,user_id,user_type,invoice_id])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Verify Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_revise_hotel_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        invoice_comments = request.POST.getlist('invoice_comments', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id, invoice_comment in zip(verify_id, invoice_ids, invoice_comments):
                        cursor.callproc('correctionInvoiceRequestAdminHotelBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Revise Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_verify_flight_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id in zip(verify_id, invoice_ids):
                        cursor.callproc('verifyInvoiceAdminFlightBookings', [booking_id,user_id,user_type,invoice_id])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Verify Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)


def admin_revise_flight_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']

        verify_id = request.POST.getlist('verify_id', '')
        corporate_ids = request.POST.getlist('corporate_id', '')
        invoice_ids = request.POST.getlist('invoice_id', '')
        invoice_comments = request.POST.getlist('invoice_comments', '')
        user_id = request.POST.get('user_id', '')
        user = {}
        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    for booking_id, invoice_id, invoice_comment in zip(verify_id, invoice_ids, invoice_comments):
                        print(booking_id)
                        cursor.callproc('correctionInvoiceRequestAdminFlightBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
                        emp = dictfetchall(cursor)
                        print(emp)
                    cursor.close()

                    data = {'success': 1, 'message': "invoice Revise Successfully"}
                    return JsonResponse(data)
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                    data = {'success': 0, 'error': getattr(e, 'message', str(e))}
                    return JsonResponse(data)
            else:
                data = {'success': 0, 'error': "User Information Not Found"}
                return JsonResponse(data)
        else:
            data = {'success': 0, 'Corporates': "Token Not Found"}
            return JsonResponse(data)
    else:
        data = {'success': 0, 'error': "Missing Parameter Value Try Again..."}

        return JsonResponse(data)
