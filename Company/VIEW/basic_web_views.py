from django.shortcuts import render, redirect
from datetime import datetime
from django_global_request.middleware import get_request
from django.contrib.auth import authenticate, login as auth_login, logout
from Company.forms import Corporate_Login_Form
from Company.models import Corporate_Login_Access_Token
from Company.models import Corporate_Spoc_Login_Access_Token
from Company.models import Corporate_Approves_1_Login_Access_Token
from Company.models import Corporate_Approves_2_Login_Access_Token
from Company.models import Corporate_Agent_Login_Access_Token
from django.db import connection


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
        user_type = corporate_login_type;
        user = authenticate(username=username, post_password=password, login_type=corporate_login_type)

        if user is not None:
            if user:
                request.session.set_expiry(86400)  # sets the exp. value of the session
                print("without login")
                user_info = {}
                cursor = connection.cursor()

                if user_type == '1':
                    cursor.callproc('getAllCorporateAdminsDetails', [user.corporate_id])
                    user_info = dictfetchall(cursor)
                    auth_login(request, user, backend='Company.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Corporate/home")
                else:
                    print("User Info Not Found")

                if user_type == '2':
                    cursor.callproc('getAllCorporateSubgroupsDetails', [user.corporate_id])
                    user_info = dictfetchall(cursor)
                    auth_login(request, user, backend='Company.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Approves_1/home")
                else:
                    print("User Info Not Found")

                if user_type == '3':
                    cursor.callproc('getAllCorporateGroupsDetails', [user.corporate_id])
                    user_info = dictfetchall(cursor)
                    auth_login(request, user, backend='Company.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Approves_2/home")
                else:
                    print("User Info Not Found")

                if user_type == '4':
                    cursor.callproc('getAllCorporateSpocsDetails', [user.corporate_id])
                    user_info = dictfetchall(cursor)
                    print(user_info)
                    auth_login(request, user, backend='Company.backends.CustomCompanyUserAuth')  # the user is now logged in
                    return redirect("Spoc/home")
                else:
                    print("User Info Not Found")

        else:
            context['error'] = "Invalid Email Or Password"
            return render(request,'corporate_login.html',context)
    else:
        # the login is a  GET request, so just show the user the login form.
        form = Corporate_Login_Form()
        return render(request,'corporate_login.html',{'form':form})


def logout_action(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']

    if login_type == '1':
        user = Corporate_Login_Access_Token.objects.get(access_token=access_token)
    elif login_type == '2':
        user = Corporate_Approves_1_Login_Access_Token.objects.get(access_token=access_token)
    elif login_type == '3':
        user = Corporate_Approves_2_Login_Access_Token.objects.get(access_token=access_token)
    elif login_type == '4':
        user = Corporate_Spoc_Login_Access_Token.objects.get(access_token=access_token)
    elif login_type == 'agent':
        user = Corporate_Agent_Login_Access_Token.objects.get(access_token=access_token)
    else:
        return None

    user.expiry_date = datetime.now()  # change field
    user.save()  # this will update only
    logout(request)  # the user is now LogOut
    return redirect("/login")


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]