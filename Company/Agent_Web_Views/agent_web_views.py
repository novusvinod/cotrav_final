from django.conf import settings
from django.shortcuts import render, redirect
import traceback
import requests
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django_global_request.middleware import get_request
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout
from Company.forms import Corporate_Login_Form
from django.contrib.auth.decorators import login_required

from Company.forms import Corporate_Agent_Login_Form
from Company.forms import Corporate_Form
from Company.models import Corporate
from django.contrib.auth.hashers import make_password
from Company.models import Corporate_Login_Access_Token
from Company.models import Corporate_Spoc_Login_Access_Token
from Company.models import Corporate_Approves_1_Login_Access_Token
from Company.models import Corporate_Approves_2_Login_Access_Token
from Company.models import Corporate_Agent_Login_Access_Token
from django.db import connection

@login_required(login_url='/login')
def homepage(request):
    return render(request,'home_page.html',{'user': request.user})


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
                    cursor.callproc('getAllCorporateAdminsDetails', [])
                    user_info = dictfetchall(cursor)
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")

                if user_type == '2':
                    cursor.callproc('getAllCorporateSubgroupsDetails', [])
                    user_info = dictfetchall(cursor)
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")

                if user_type == '3':
                    cursor.callproc('getAllCorporateGroupsDetails', [])
                    user_info = dictfetchall(cursor)
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")

                if user_type == '4':
                    cursor.callproc('getAllCorporateSpocsDetails', [])
                    user_info = dictfetchall(cursor)
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")
                print(user_info)
                auth_login(request, user, backend='Company.backends.CustomCompanyUserAuth')  # the user is now logged in
                print("with login")


                return redirect("/home")
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




@login_required()
def agent_homepage(request):
    return render(request,'Agent/agent_home_page.html',{'user': request.user})

def agent_login(request):
    form = Corporate_Agent_Login_Form()
    return render(request, 'Agent/corporate_agent_login.html', {'form': form})

def agent_login_action(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, post_password=password, login_type="agent")
        print(user)
        if user is not None:
            if user:
                request.session.set_expiry(86400)  # sets the exp. value of the session
                auth_login(request, user, backend='Company.backends.CustomCompanyUserAuth')  # the user is now logged in
                return redirect("/agents/agent_home")
        else:
            context['error'] = "Invalid Email Or Password"
            return render(request,'Agent/corporate_agent_login.html',context)
    else:
        # the login is a  GET request, so just show the user the login form.
        form = Corporate_Agent_Login_Form()
        return render(request,'Agent/corporate_agent_login.html',{'form':form})

def agent_logout_action(request):
    request = get_request()
    access_token = request.session['access_token']
    user = Corporate_Agent_Login_Access_Token.objects.get(access_token=access_token)
    user.expiry_date = datetime.now()  # change field
    user.save()  # this will update only
    logout(request)  # the user is now LogOut
    return redirect("/agents/login")

@login_required(login_url='/login')
def add_company(request):
    if request.method == "POST":
        form = Corporate_Form(request.POST)
        corporate_name = request.POST.get('corporate_name', '')
        corporate_code = request.POST.get('corporate_code', '')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        bill_corporate_name = request.POST.get('bill_corporate_name', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        gst_id = request.POST.get('gst_id', '')

        has_billing_spoc_level = request.POST.get('has_billing_spoc_level', '')
        has_auth_level = request.POST.get('has_auth_level', '')
        no_of_auth_level = request.POST.get('no_of_auth_level', '')
        has_assessment_codes = request.POST.get('has_assessment_codes', '')
        is_radio = request.POST.get('is_radio', '')
        is_local = request.POST.get('is_local', '')
        is_outstation = request.POST.get('is_outstation', '')
        is_bus = request.POST.get('is_bus', '')
        is_train = request.POST.get('is_train', '')
        is_hotel = request.POST.get('is_hotel', '')
        is_meal = request.POST.get('is_meal', '')
        is_flight = request.POST.get('is_flight', '')
        is_water_bottles = request.POST.get('is_water_bottles', '')
        is_reverse_logistics = request.POST.get('is_reverse_logistics', '')
        is_spoc = request.POST.get('is_spoc', '')
        password = make_password("taxi123")
        cotrav_agent_id = request.POST.get('cotrav_agent_id', '')

        if form.is_valid():
            print("Form Valide")
            try:
                cursor = connection.cursor()
                cursor.callproc('create_corporate_with_basic_details', [corporate_name,corporate_code,contact_person_name,contact_person_no,contact_person_email,bill_corporate_name,
                                                             address_line_1,address_line_2,address_line_3,gst_id,has_billing_spoc_level,has_auth_level,no_of_auth_level,
                                                             has_assessment_codes,is_radio,is_local,is_outstation,is_bus,is_train,is_hotel,is_meal,is_flight,
                                                             is_water_bottles,is_reverse_logistics,is_spoc,password,cotrav_agent_id,])
                cursor.close()

                return redirect('/agents/list_corporate')
            except:
                tb = traceback.format_exc()
                print(tb)
                pass
    else:
        form = Corporate_Form()
    return render(request,'Agent/add_company.html',{'form':form})


@csrf_exempt
@login_required(login_url='/login')
def companies(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL+"companies"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token '+access_token,'usertype':login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        corporates_data = company['Corporates']
        return render(request,"Agent/companies.html",{'companies':corporates_data})
    else:
        return render(request,"Agent/companies.html",{'companies':{}})


@login_required(login_url='/login')
def edit_company(request, id):
    if request.method == "POST":
        employee = Corporate.objects.get(id=id)
        form = Corporate_Form(request.POST, instance=employee)
        print("Form herer")
        if form.is_valid():
            print("Form Valide")
            try:
                form.save()
                return redirect('/agents/companies')
            except:
                tb = traceback.format_exc()
                print(tb)
                pass
    else:
        company = Corporate.objects.get(id=id)
        return render(request, 'Agent/edit_company.html', {'company': company})

@login_required(login_url='/login')
def company_rates(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "company_rates"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        corporate_rates = company['Corporate_Retes']
        return render(request, "Agent/company_rates.html", {'corporate_rates': corporate_rates})
    else:
        return render(request, "Agent/company_rates.html", {'corporate_rates': {}})


@login_required(login_url='/login')
def billing_entities(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "billing_entities"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        billing_entities = company['Entitys']
        return render(request, "Agent/billing_entities.html", {'billing_entities': billing_entities})
    else:
        return render(request, "Agent/billing_entities.html", {'billing_entities': {}})


@login_required(login_url='/login')
def admins(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "admins"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        admins = company['Admins']
        return render(request, "Agent/admins.html", {'admins': admins})
    else:
        return render(request, "Agent/admins.html", {'admins': {}})


@login_required(login_url='/login')
def groups(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "groups"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        groups = company['Groups']
        return render(request, "Agent/groups.html", {'groups': groups})
    else:
        return render(request, "Agent/groups.html", {'groups': {}})


@login_required(login_url='/login')
def subgroups(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "subgroups"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        subgroups = company['Subgroups']
        return render(request, "Agent/subgroups.html", {'subgroups': subgroups})
    else:
        return render(request, "Agent/subgroups.html", {'subgroups': {}})


@login_required(login_url='/login')
def spocs(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "spocs"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        spocs = company['Spocs']
        return render(request, "Agent/spocs.html", {'spocs': spocs})
    else:
        return render(request, "Agent/spocs.html", {'spocs': {}})


@login_required(login_url='/login')
def employees(request):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "employees"
    payload = {'some': 'data'}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        employees = company['Employees']
        return render(request, "Agent/employees.html", {'employees': employees})
    else:
        return render(request, "Agent/employees.html", {'employees': {}})


@login_required(login_url='/login')
def company_admins(request,id):
    print(id)
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "admins"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        admins = company['Admins']
        return render(request, "company_admins.html", {'admins': admins})
    else:
        return render(request, "company_admins.html", {'admins': {}})


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]