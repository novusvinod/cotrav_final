import requests
from django.shortcuts import render, redirect
from datetime import datetime
from django_global_request.middleware import get_request
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import connection

from Common.forms import Corporate_Login_Form
from Common.models import Corporate_Login_Access_Token
from Common.models import Corporate_Spoc_Login_Access_Token
from Common.models import Corporate_Employee_Login_Access_Token
from Common.models import Corporate_Approves_1_Login_Access_Token
from Common.models import Corporate_Approves_2_Login_Access_Token
from Common.models import Corporate_Agent_Login_Access_Token
from Common.email_settings import SignIn_OTP,AddBooking_Email
COTRAV_NUMBERS = "8669152900"


def login(request):
    form = Corporate_Login_Form()
    return render(request, 'corporate_login.html', {'form': form})


def login_action(request):
    context = {}
    user_type = ''
    if request.method == 'POST':
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        corporate_login_type = request.POST.get('corporate_login_type', '')
        user_type = corporate_login_type
        user = authenticate(username=username, post_password=password, login_type=corporate_login_type)
        print(user)
        if user:
            if user:
                print("After Lagin")
                print(user.id)
                request.session.set_expiry(7200)  # sets the exp. value of the session
                print("without login")
                user_info = {}
                cursor = connection.cursor()

                if user_type == '1':
                    auth_login(request, user, backend='Common.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Corporate/Admin/home")
                else:
                    print("User Info Not Found")

                if user_type == '2':
                    auth_login(request, user, backend='Common.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Corporate/Approver_1/home")
                else:
                    print("User Info Not Found")

                if user_type == '3':
                    auth_login(request, user, backend='Common.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Corporate/Approver_2/home")
                else:
                    print("User Info Not Found")

                if user_type == '4':
                    auth_login(request, user, backend='Common.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Corporate/Spoc/home")
                else:
                    print("User Info Not Found")

                if user_type == '6':
                    auth_login(request, user, backend='Common.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Corporate/Employee/home")
                else:
                    print("User Info Not Found")

        else:
            messages.error(request, 'Invalid Email Or Password..!')
            return render(request,'corporate_login.html',context)
    else:
        # the login is a  GET request, so just show the user the login form.
        form = Corporate_Login_Form()
        return render(request,'corporate_login.html',{'form':form})


def logout_action(request):
    request = get_request()
    login_type = request.session['login_type']

    if login_type == '1':
        access_token = request.session['admin_access_token']
        user = Corporate_Login_Access_Token.objects.get(access_token=access_token)
        request.session['admin_login_type'] = ''
        request.session['admin_access_token'] = ''
    elif login_type == '2':
        access_token = request.session['approves_1_access_token']
        user = Corporate_Approves_1_Login_Access_Token.objects.get(access_token=access_token)
        request.session['approves_1_login_type'] = ''
        request.session['approves_1_access_token'] = ''
    elif login_type == '3':
        access_token = request.session['approves_2_access_token']
        user = Corporate_Approves_2_Login_Access_Token.objects.get(access_token=access_token)
        request.session['approves_2_login_type'] = ''
        request.session['approves_2_access_token'] = ''
    elif login_type == '4':
        access_token = request.session['spoc_access_token']
        user = Corporate_Spoc_Login_Access_Token.objects.get(access_token=access_token)
        request.session['spoc_login_type'] = ''
        request.session['spoc_token'] = ''
    elif login_type == '6':
        access_token = request.session['employee_access_token']
        user = Corporate_Employee_Login_Access_Token.objects.get(access_token=access_token)
        request.session['employee_login_type'] = ''
        request.session['employee_access_token'] = ''
    elif login_type == '10':
        access_token = request.session['agent_access_token']
        user = Corporate_Agent_Login_Access_Token.objects.get(access_token=access_token)
        request.session['agent_login_type'] = ''
        request.session['agent_access_token'] = ''
    else:
        return None

    user.expiry_date = datetime.now()  # change field
    user.save()  # this will update only
    #logout(request)  # the user is now LogOut
    return redirect("/login")


def change_password(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        user_type = request.POST.get('user_type', '')
        user_email = request.POST.get('user_email', '')
        user_password = request.POST.get('user_password', '')
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        conf_password = request.POST.get('conf_password', '')
        current_url = request.POST.get('current_url', '')

        if check_password(current_password, user_password) and new_password==conf_password:
            print("TRERERER")
            generate_password = make_password(new_password)
            cursor = connection.cursor()
            cursor.callproc('changeUserPassword', [user_id,user_type,generate_password])
            user_info = dictfetchall(cursor)
            if user_info:
                send_otp = SignIn_OTP()
                email_subject = "CoTrav Corporate - Password Change Successfully"
                email_body = "Dear " + user_email + ",<br><br>Welcome to CoTrav Corporate!!!<br><br>To access your profile and bookings on CoTrav Corporate app, you need to verify your Password.<br>Your Login Password is: <strong>" + new_password + "</strong><br><br>Regards,<br>CoTrav Team";
                resp1 = send_otp.send_email(user_email, email_subject, email_body)
                messages.error(request, 'Password Not Change Please Try Again..!')
                return HttpResponseRedirect(current_url, {})
            else:
                messages.success(request, 'Password Change Successfully..!')
            return HttpResponseRedirect(current_url, {})
        else:
            print("TRERERER")
            messages.error(request, 'Password Not Match Please Try Again..!')
            return HttpResponseRedirect(current_url,{})

    else:
        return None


def send_sms(request):
    sender_id = 'COTRAV'
    exotel_sid = "novuslogic1"
    exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
    exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"
    sms_body = "Dear "+"Balwant"+",\n\nBooking successfully registered with id "+"DFS3243423"+".\n\nPickup from "+"Pune"+" on "+"10-09-2019"+".\nDrop: " +"Mumbai"+ "\nTrip Type: " +"Local"+".\nTaxi Type: "+"SUV"+".\n\nPlease call at "+"9876543210"+" for any query.\n\nRgrds,\nTaxiVaxi.";

    requests.post('https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
                  auth=(exotel_key, exotel_token),
                  data={
                      'From': sender_id,
                      'To': COTRAV_NUMBERS,
                      'Body': sms_body
                  })
    return redirect("/login")


def send_email(request):
    add_booking_email = SignIn_OTP()
    to = "balwant@taxivaxi.in"
    subject = "Test Mail"
    body = "New Taxi Booking - "+'Balwant'+"<br><br> Pickup from: "+'Pune'+" <br> Pickup Time: "+'01-11-2019 12:12'+"<br>Trip Type: "+'Local'+"<br> Taxi Type: "+'Sedan'+"<br> Regards, <br> TaxiVaxi ";
    resp1 = add_booking_email.send_email(to,"123456")
    return redirect("/login")




def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]