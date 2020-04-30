import json
import socket

from django.db import connection
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils.timesince import timesince

from Common.VIEW.Agent.agent_views import dictfetchall, getDataFromAPI
from Common.models import Corporate, Corporate_Agent

from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from datetime import timedelta
import requests
from landing.forms import LeadGenerationModelForm
from landing.models import Leadgeneration, LeadComments, LeadLog
from django.contrib import messages
from landing.utils import render_to_pdf
from Common.email_settings import SignIn_OTP

from threading import Thread, activeCount
COTRAV_EMAILS = list(Corporate_Agent.objects.filter(is_super_admin=1).exclude(email='').values_list('email', flat=True))
COTRAV_NUMBERS = Corporate_Agent.objects.filter(is_super_admin=1).exclude(contact_no='').values_list('contact_no', flat=True)


# Create your views here.
def index_cs(request):
    return render(request,'comingsoon.html')


def index(request):
    return render(request,'cotrav_index.html')


def about(request):
    return render(request,'cotrav_about.html')


def login(request):
    return render(request,'cotrav_login.html')


def signup(request):
    if request.method == 'POST':

        corporate_name = request.POST.get('corporate_name')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_no = request.POST.get('contact_person_no')
        contact_person_email = request.POST.get('contact_person_email')
        corporate_location = request.POST.get('corporate_location')
        Lead_Source = request.POST.get('Lead_Source')
        Hear_About_Us = request.POST.get('Hear_About_Us')
        if Hear_About_Us == 'other':
            Hear_About_Us = request.POST.get('input_Hear_About_Us')
        message = request.POST.get('message')

        Newcompany = Leadgeneration()

        Newcompany.Company_Name = corporate_name
        Newcompany.Company_Location = corporate_location
        Newcompany.Contact_Name = contact_person_name
        Newcompany.Contact_Number = contact_person_no
        Newcompany.Contact_Email = contact_person_email
        Newcompany.Company_Website = ''
        Newcompany.Message = message
        Newcompany.Assigned_Sales_Person = 0
        Newcompany.Status = 'Lead Created'
        Newcompany.Lead_Source = Lead_Source
        Newcompany.Hear_About_Us = Hear_About_Us
        Newcompany.Attachments = ''
        Newcompany.Lead_Communication = ''
        Newcompany.Comments = ''

        try:
            ref = Leadgeneration.objects.get(Company_Name=corporate_name)
            print("Company with same name allready exist")
            # return redirect('signup')
            err_msg = "Company with same name allready exist"
            return render(request, 'cotrav_signup.html',
                          {'company': corporate_name, 'name': contact_person_name, 'number': contact_person_no,
                           'email': contact_person_email, 'city': corporate_location, 'message': message,
                           'err_msg': err_msg})
        except ObjectDoesNotExist:
            Newcompany.save()
            messages.success(request, "A Cotrav Official would be contacting you in 24 hours to discuss business solutions for your team...!")
        return redirect('signup')

    else:
        return render(request, 'cotrav_signup.html')



def contact(request):
    if request.method == 'POST':
        corporate_name = request.POST.get('corporate_name')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_no = request.POST.get('contact_person_no')
        contact_person_email = request.POST.get('contact_person_email')
        corporate_location = ''
        Lead_Source = 'Contact Us'
        message = request.POST.get('message')

        Newcompany = Leadgeneration()

        Newcompany.Company_Name = corporate_name
        Newcompany.Company_Location = corporate_location
        Newcompany.Contact_Name = contact_person_name
        Newcompany.Contact_Number = contact_person_no
        Newcompany.Contact_Email = contact_person_email
        Newcompany.Company_Website = ''
        Newcompany.Message = message
        Newcompany.Assigned_Sales_Person = 0
        Newcompany.Status = 'Lead Created'
        Newcompany.Lead_Source = Lead_Source
        Newcompany.Attachments = ''
        Newcompany.Lead_Communication = ''
        Newcompany.Comments = ''

        Newcompany.save()
        messages.success(request,
                         "A Cotrav Official would be contacting you in 24 hours to discuss business solutions for your team..!")
        return redirect('contact')

    else:

        return render(request, 'cotrav_contact.html')


def support(request):
        return render(request,'cotrav_support.html')

def cab(request):
    return render(request, 'cab_booking.html')

def hotel(request):
    return render(request, 'hotel_booking.html')

def mice(request):
    return render(request, 'mice.html')

def ticketing(request):
    return render(request, 'ticketing_booking.html')

def travel(request):
    return render(request, 'travel_reimbursement.html')

def visa(request):
    return render(request, 'visa_services.html')

def error_404_view(request, *args, **argv):
    data = {"name": "ThePythonDjango.com"}
    print(request.get_full_path())
    urlll = request.get_full_path()
    url = urlll.split("/")
    if url[1] == 'api':
        return JsonResponse({
            'success': 0,
            'message': 'api not found'
        })

    return render(request, 'error_404.html', data)


def error_500_view(request, *args, **arg):
    data = {"name": "ThePythonDjango.com"}
    print(request.get_full_path())
    urlll = request.get_full_path()
    url = urlll.split("/")
    if url[1] == 'api':
        return JsonResponse({
            'success': 0,
            'message': 'api not found'
        })

    return render(request, 'error_404.html', data)

def testsignup(request):
    try:
        ref = Corporate.objects.get(corporate_name = "tcs")
    except ObjectDoesNotExist:
        print("duplicate entry")
    return HttpResponse("test")


def testemail(request):
    email_to = "balwant@taxivaxi.in"
    subject = "Test"
    body = "Hiii"
    resp1 = 1
    try:
        signup = SignIn_OTP()
        print(COTRAV_EMAILS)
        print(type(COTRAV_EMAILS))
        resp1 = signup.send_email(COTRAV_EMAILS,subject,body)
        print(resp1)
    except Exception as e:
        print("exception")
        print(e)
        print("duplicate entry")
    return HttpResponse(resp1)


def voucher(request):
    return render(request,'booking_email_voucher.html')



def export_movies_to_xlsx(request):
    """
    Downloads all movies as Excel file with a single worksheet
    """
    movie_queryset = Corporate.objects.all()

    print(movie_queryset)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-movies.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
    )

    return response


def pdf_render_test(request):
    # payload = {'bill_id': 106}
    # url = settings.API_BASE_URL + "view_bill"
    # company = getDataFromAPI("10", "W6UC9UJJ63BT1XSQ9ZXSKEWVCF90WME8I9YWP9106V1688GZZ0ZINGQEY33C", url, payload)
    # print(company['Bill'][0])
    # voucher = {'bill_datas':company['Bill'][0]}
    # pdf = render_to_pdf('pdf_voucher_template/bill_template/bill_single_invoice.html', voucher)

    #return render(request,'train_email_temp.html')

    # cursor2 = connection.cursor()
    # cursor2.callproc('viewFlightBooking', [220])
    # emp = dictfetchall(cursor2)
    # cursor2.close()
    #
    # cursor1 = connection.cursor()
    # cursor1.callproc('getAllFlightBookingPassangers', [220])
    # passanger = dictfetchall(cursor1)
    # emp[0]['Passangers'] = passanger
    # cursor1.close()
    #
    # cursor3 = connection.cursor()
    # cursor3.callproc('getAllFlightBookingFlights', [220])
    # flights = dictfetchall(cursor3)
    # cursor3.close()
    #
    # emp[0]['Flights'] = flights
    #
    # DEP_DATE_0 = ''
    # for i, f in enumerate(flights):
    #     print(f)
    #
    #     ARRV_DATE_i = f['arrival_datetime']
    #     DEP_DATE_i = f['departure_datetime']
    #     adDate = datetime.strptime(str(DEP_DATE_i), "%d-%m-%Y %H:%M")
    #     ddDate = datetime.strptime(str(ARRV_DATE_i), "%d-%m-%Y %H:%M")
    #     dayHours_onword_i = timesince(adDate, ddDate)
    #     if i == 0:
    #         DEP_DATE_0 = f['arrival_datetime']
    #     if i == 1 or i == 2 or i == 3:
    #         ii = i - 1
    #         adDate = datetime.strptime(str(DEP_DATE_0), "%d-%m-%Y %H:%M")
    #         ddDate = datetime.strptime(str(DEP_DATE_i), "%d-%m-%Y %H:%M")
    #         emp[0]['DELAY_' + str(i)] = timesince(adDate, ddDate)
    #         DEP_DATE_0 = f['arrival_datetime']
    #     emp[0]['DURATION_' + str(i)] = dayHours_onword_i


    cursor2 = connection.cursor()
    cursor2.callproc('viewBusBooking', [120])
    emp = dictfetchall(cursor2)
    cursor2.close()

    cursor1 = connection.cursor()
    cursor1.callproc('getAllBusBookingPassangers', [120])
    passanger = dictfetchall(cursor1)
    emp[0]['Passangers'] = passanger
    cursor1.close()
    print(emp[0])
    #
    # cursor2 = connection.cursor()
    # cursor2.callproc('viewHotelBooking', [106])
    # emp = dictfetchall(cursor2)
    # cursor2.close()
    #
    # cursor1 = connection.cursor()
    # cursor1.callproc('getAllHotelBookingPassangers', [106])
    # passanger = dictfetchall(cursor1)
    # emp[0]['Passangers'] = passanger
    # cursor1.close()

    print(emp[0])

    pdf = render_to_pdf('pdf_voucher_template/bus_voucher.html', emp[0])
    return HttpResponse(pdf, content_type='application/pdf')


def Create_Token(request):
    if request.method == 'POST':
        try:
            url = "http://auth.ksofttechnology.com/API/AUTH"
            payload = {
                "TYPE": "AUTH",
                "NAME": "GET_AUTH_TOKEN",
                "STR": [
                    {
                        "A_ID": "79394396",
                        "U_ID": "Taxivaxi",
                        "PWD": "Taxi$Vaxi1234",
                        "MODULE": "B2B",
                        "HS": "D"
                    }
                ]
            }

            headers = {}
            r = requests.post(url, json=payload)
            print(r)
            api_response = r.json()
            print("response")
            print(socket.gethostname())
            messages.success(request, api_response)
            return render(request, 'api_call.html', {'response': api_response})
        except Exception as e:
            messages.error(request, e)
            return redirect('create_token')
    else:

        return render(request, 'api_call.html')


def get_flights(request):
    if request.method == 'POST':
        try:
            url = "http://mdt.ksofttechnology.com/API/FLIGHT"
            payload = {
                "TYPE": "AIR",
                "NAME": "GET_FLIGHT",
                "STR": [
                    {
                        "AUTH_TOKEN": "19d7c89d-41e2-4ddb-918f-b12a8f219686",
                        "SESSION_ID": "0vv5ycqeaxmndcdqhtatcscx",
                        "TRIP": "1",
                        "SECTOR": "D",
                        "SRC": "DEL",
                        "DES": "BOM",
                        "DEP_DATE": "2019-12-20",
                        "RET_DATE": "",
                        "ADT": "1",
                        "CHD": "0",
                        "INF": "1",
                        "PC": "",
                        "PF": "",
                        "HS": "D"
                    }
                ]
            }

            headers = {}
            r = requests.post(url, json=payload)
            print(r)
            api_response = r.json()
            print("response")
            print(socket.gethostname())
            messages.success(request, api_response)
            return render(request, 'api_call.html', {'response': api_response})
        except Exception as e:
            messages.error(request, e)
            return redirect('create_token')
    else:

        return render(request, 'api_call.html')


def get_pnr(request):
    if request.method == 'POST':
        try:
            url = "http://mdt.ksofttechnology.com/API/FLIGHT"
            payload = {
                    "NAME": "PNR_RETRIVE",
                    "STR": [
                        {
                            "BOOKINGID": "APIU637124397889286020Ua2e9",
                            "CLIENT_SESSIONID": "069764a1-8a35-42ff-baed-ab168d0b1341",
                            "HS": "D",
                            "MODULE": "B2B"
                        }
                    ],
                    "TYPE": "DC"
                }

            headers = {}
            r = requests.post(url, json=payload)
            print(r)
            api_response = r.json()
            print("response")
            print(socket.gethostname())
            messages.success(request, api_response)
            return render(request, 'api_call.html', {'response': api_response})
        except Exception as e:
            messages.error(request, e)
            return redirect('create_token')
    else:

        return render(request, 'api_call.html')


