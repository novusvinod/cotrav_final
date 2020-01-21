from datetime import datetime
import sys
from django.http import JsonResponse
from django.db import connection
from Common.VIEW.Api.api_views import getUserinfoFromAccessToken, dictfetchall


def spoc_taxi_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':

            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllSPOCTaxiBookings', [spoc_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
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


def spoc_bus_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllSPOCBusBookings', [spoc_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
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


def spoc_train_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllSPOCTrainBookings', [spoc_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
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


def spoc_hotel_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllSPOCHotelBookings', [spoc_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
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


def spoc_flight_bookings(request):
    if 'AUTHORIZATION' in request.headers and 'USERTYPE' in request.headers:
        req_token = request.META['HTTP_AUTHORIZATION']
        user_type = request.META['HTTP_USERTYPE']
        spoc_id = request.POST.get('spoc_id', '')
        user = {}
        booking_type = request.POST.get('booking_type', '')

        user_token = req_token.split()
        if user_token[0] == 'Token':
            user = getUserinfoFromAccessToken(user_token[1], user_type)
            if user:
                try:
                    cursor = connection.cursor()
                    cursor.callproc('getAllSPOCFlightBookings', [spoc_id,booking_type])
                    emp = dictfetchall(cursor)
                    cursor.close()
                    for e in emp:
                        cursor1 = connection.cursor()
                        booking_id = e['id']
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


def spoc_reject_taxi_bookings(request):
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
                    cursor.callproc('rejectSpocTaxiBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
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


def spoc_reject_bus_bookings(request):
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
                    cursor.callproc('rejectSpocBusBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    print(emp)
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
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


def spoc_reject_train_bookings(request):
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
                    cursor.callproc('rejectSpocTrainBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
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


def spoc_reject_flight_bookings(request):
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
                    cursor.callproc('rejectSpocFlightBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
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


def spoc_reject_hotel_bookings(request):
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
                    cursor.callproc('rejectSpocHotelBookings', [user_id,user_type,booking_id])
                    emp = dictfetchall(cursor)
                    data = {'success': 1, 'message': "Booking Reject Successfully"}
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


def spoc_verify_taxi_bookings(request):
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
                    for booking_id, corporate_id, invoice_id in zip(verify_id, corporate_ids, invoice_ids):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('verifyInvoiceSpocTaxiBookings', [booking_id,user_id,user_type,corporate_id,invoice_id])
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


def spoc_revise_taxi_bookings(request):
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
                    for booking_id, corporate_id, invoice_id, invoice_comment in zip(verify_id, corporate_ids, invoice_ids, invoice_comments):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('correctionInvoiceRequestSpocTaxiBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
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


def spoc_verify_bus_bookings(request):
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
                    for booking_id, corporate_id, invoice_id in zip(verify_id, corporate_ids, invoice_ids):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('verifyInvoiceSpocBusBookings', [booking_id,user_id,user_type,corporate_id,invoice_id])
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


def spoc_revise_bus_bookings(request):
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
                    for booking_id, corporate_id, invoice_id, invoice_comment in zip(verify_id, corporate_ids, invoice_ids, invoice_comments):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('correctionInvoiceRequestSpocBusBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
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


def spoc_verify_train_bookings(request):
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
                    for booking_id, corporate_id, invoice_id in zip(verify_id, corporate_ids, invoice_ids):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('verifyInvoiceSpocTrainBookings', [booking_id,user_id,user_type,corporate_id,invoice_id])
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


def spoc_revise_train_bookings(request):
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
                    for booking_id, corporate_id, invoice_id, invoice_comment in zip(verify_id, corporate_ids, invoice_ids, invoice_comments):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('correctionInvoiceRequestSpocTrainBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
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


def spoc_verify_hotel_bookings(request):
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
                    for booking_id, corporate_id, invoice_id in zip(verify_id, corporate_ids, invoice_ids):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('verifyInvoiceSpocHotelBookings', [booking_id,user_id,user_type,corporate_id,invoice_id])
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


def spoc_revise_hotel_bookings(request):
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
                    for booking_id, corporate_id, invoice_id, invoice_comment in zip(verify_id, corporate_ids, invoice_ids, invoice_comments):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('correctionInvoiceRequestSpocHotelBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
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


def spoc_verify_flight_bookings(request):
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
                    for booking_id, corporate_id, invoice_id in zip(verify_id, corporate_ids, invoice_ids):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('verifyInvoiceSpocFlightBookings', [booking_id,user_id,user_type,corporate_id,invoice_id])
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


def spoc_revise_flight_bookings(request):
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
                    for booking_id, corporate_id, invoice_id, invoice_comment in zip(verify_id, corporate_ids, invoice_ids, invoice_comments):
                        print(booking_id)
                        print(corporate_id)
                        cursor.callproc('correctionInvoiceRequestSpocFlightBooking', [booking_id,user_id,user_type,invoice_id,invoice_comment])
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
