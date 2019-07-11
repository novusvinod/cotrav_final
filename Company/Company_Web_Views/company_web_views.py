from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
    return render(request,'Company/home_page.html',{'user': request.user})


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
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")

                if user_type == '2':
                    cursor.callproc('getAllCorporateSubgroupsDetails', [user.corporate_id])
                    user_info = dictfetchall(cursor)
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")

                if user_type == '3':
                    cursor.callproc('getAllCorporateGroupsDetails', [user.corporate_id])
                    user_info = dictfetchall(cursor)
                    print("Found User Info")
                    print(user_info)
                else:
                    print("User Info Not Found")

                if user_type == '4':
                    cursor.callproc('getAllCorporateSpocsDetails', [user.corporate_id])
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
        return render(request, "Company/company_admins.html", {'admins': admins})
    else:
        return render(request, "Company/company_admins.html", {'admins': {}})


@login_required(login_url='/login')
def company_billing_entities(request,id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "billing_entities"
    payload = {'corporate_id': id}

    company = getDataFromAPI(login_type,access_token,url,payload)
    url_city = settings.API_BASE_URL + "cities"
    cities = getDataFromAPI(login_type,access_token,url_city,payload)

    if company['success'] == 1:
        entities = company['Entitys']
        cities = cities["Cities"]
        return render(request, "Company/billing_entities.html", {'billing_entities': entities,"cities":cities,})
    else:
        return render(request, "Company/billing_entities.html", {'entities': {}})





@login_required(login_url='/login')
def company_rates(request,id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "company_rates"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        company_rates = company['Corporate_Retes']
        return render(request, "Company/company_rates.html", {'corporate_rates': company_rates})
    else:
        return render(request, "Company/company_rates.html", {'entities': {}})


@login_required(login_url='/login')
def company_groups(request,id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "groups"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        groups = company['Groups']
        return render(request, "Company/groups.html", {'groups': groups})
    else:
        return render(request, "Company/groups.html", {'groups': {}})

@login_required(login_url='/login')
def company_subgroups(request,id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "subgroups"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        subgroups = company['Subgroups']
        return render(request, "Company/subgroups.html", {'subgroups': subgroups})
    else:
        return render(request, "Company/subgroups.html", {'subgroups': {}})


@login_required(login_url='/login')
def company_spocs(request,id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "spocs"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        spocs = company['Spocs']
        return render(request, "Company/spocs.html", {'subgroups': spocs})
    else:
        return render(request, "Company/spocs.html", {'spocs': {}})


@login_required(login_url='/login')
def company_employees(request,id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "employees"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        employees = company['Employees']
        return render(request, "Company/employees.html", {'employees': employees})
    else:
        return render(request, "Company/employees.html", {'employees': {}})


@login_required(login_url='/login')
def add_company_rate(request,id):
    if request.method == 'POST':
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        url = settings.API_BASE_URL + "company_rates"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)
        if company['success'] == 1:
            company_rates = company['Corporate_Retes']
            return render(request, "Company/company_rates.html", {'corporate_rates': company_rates})
        else:
            return render(request, "Company/company_rates.html", {'entities': {}})
    else:
        return render(request, "Company/company_rate_add.html", {'entities': {}})
        pass


@login_required(login_url='/login')
def add_company_entity(request,id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        entity_name = request.POST.get('entity_name', '')
        billing_city_id = request.POST.get('billing_city_id')
        contact_person_name = request.POST.get('contact_person_name', '')
        contact_person_email = request.POST.get('contact_person_email', '')
        contact_person_no = request.POST.get('contact_person_no', '')
        address_line_1 = request.POST.get('address_line_1', '')
        address_line_2 = request.POST.get('address_line_2', '')
        address_line_3 = request.POST.get('address_line_3', '')
        gst_id = request.POST.get('gst_id', '')
        pan_no = request.POST.get('pan_no', '')

        entity_id = request.POST.get('entity_id')

        delete_id = request.POST.get('delete_id')

        payload = {'corporate_id': corporate_id,'user_id':user_id,'login_type':login_type,'access_token':access_token,
                   'entity_name':entity_name,'billing_city_id':billing_city_id,'contact_person_name':contact_person_name,'contact_person_email':contact_person_email,
                   'contact_person_no':contact_person_no,'address_line_1':address_line_1,'address_line_2':address_line_2,
                   'address_line_3':address_line_3,'gst_id':gst_id,'pan_no':pan_no,'entity_id':entity_id,'is_delete':delete_id,}

        url = settings.API_BASE_URL + "add_billing_entity"
        company = getDataFromAPI(login_type,access_token,url,payload)

        if company['success'] == 1:
            return HttpResponseRedirect("/company-billing_entities/"+corporate_id,{'message':"Added Successfully"})
        else:
            return HttpResponseRedirect("/company-billing_entities/"+corporate_id,{'message':"Record Not Added"})


def getDataFromAPI(login_type,access_token,url,payload):
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    api_response = json.loads(r.text)
    return api_response


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]