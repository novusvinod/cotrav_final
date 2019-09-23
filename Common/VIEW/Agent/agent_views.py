from django.conf import settings
from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django_global_request.middleware import get_request
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from Common.models import Corporate_Agent_Login_Access_Token
from django.http import HttpResponseRedirect


@login_required()
def agent_homepage(request):
    return render(request,'Agent/agent_home_page.html',{'user': request.user})


def agent_login_action(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, post_password=password, login_type="10")
        print(user)
        if user is not None:
            if user:
                request.session.set_expiry(7200)  # sets the exp. value of the session
                auth_login(request, user, backend='Common.backends.CustomCompanyUserAuth')  # the user is now logged in
                return redirect("/agents/agent_home")
        else:
            context['error'] = "Invalid Email Or Password"
            return render(request,'Agent/corporate_agent_login.html',context)
    else:
        return render(request,'Agent/corporate_agent_login.html',{})


def agent_logout_action(request):
    request = get_request()
    access_token = request.session['access_token']
    user = Corporate_Agent_Login_Access_Token.objects.get(access_token=access_token)
    user.expiry_date = datetime.now()  # change field
    user.save()  # this will update only
    logout(request)  # the user is now LogOut
    return redirect("/agents/login")


@login_required(login_url='/login')
def taxi_types(request):
    if request.method == "POST":
        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            type_name = request.POST.get('type_name', '')

            taxitype_id = request.POST.get('taxitype_id', '')
            user_id = request.POST.get('user_id', '')
            delete_id = request.POST.get('delete_id', '')
            print(delete_id)
            url = ""
            payload = {}
            if taxitype_id:
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_taxi_type"
                    payload = {'taxitype_id':taxitype_id,'user_id':user_id,'user_type':user_type}
                else:
                    url = settings.API_BASE_URL + "update_taxi_type"
                    payload = {'type_name':type_name,'taxitype_id':taxitype_id,'user_id':user_id,'user_type':user_type}
            else:
                url = settings.API_BASE_URL + "add_taxi_type"
                payload = {'type_name':type_name,'user_id':user_id,'user_type':user_type}

            taxi = getDataFromAPI(user_type, access_token, url, payload)

            if taxi['success'] == 1:
                return HttpResponseRedirect("agents/taxi-types", {'message': "Operation Successfully"})

        else:
            return HttpResponseRedirect("/agents/login")

    else:
        user_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "taxi_types"
        payload = {'': ''}
        taxi = getDataFromAPI(user_type, access_token, url, payload)

        if taxi['success'] == 1:
            taxi_data = taxi['taxi_types']

            return render(request, "Agent/taxitypes.html", {'types': taxi_data})
        else:
            return render(request, "Agent/taxitypes.html", {'Types': {}})


@login_required(login_url='/login')
def taxi_models(request):
    if request.method == "POST":
        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            brand_name = request.POST.get('brand_name', '')
            model_name = request.POST.get('model_name', '')
            taxitype_id = request.POST.get('taxitype_id', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            user_id = request.POST.get('user_id', '')
            delete_id = request.POST.get('delete_id', '')
            model_id = request.POST.get('model_id', '')

            url = ""
            payload = {}
            if model_id:
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_taxi_model"
                    payload = {'model_id':model_id,'user_id':user_id,'user_type':user_type}
                else:
                    url = settings.API_BASE_URL + "update_taxi_model"
                    payload = {'brand_name':brand_name,'model_name':model_name,'taxitype_id':taxitype_id,'no_of_seats':no_of_seats,'model_id':model_id,'user_id':user_id,'user_type':user_type}
            else:
                url = settings.API_BASE_URL + "add_taxi_model"
                payload = {'brand_name':brand_name,'model_name':model_name,'taxitype_id':taxitype_id,'no_of_seats':no_of_seats,'user_id':user_id,'user_type':user_type}

            taxi = getDataFromAPI(user_type, access_token, url, payload)

            if taxi['success'] == 1:
                return HttpResponseRedirect("agents/taxi-models", {'message': "Operation Successfully"})

        else:
            return HttpResponseRedirect("/agents/login")

    else:
        user_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "taxi_types"
        payload = {'': ''}
        taxi = getDataFromAPI(user_type, access_token, url, payload)

        url_m = settings.API_BASE_URL + "taxi_models"
        payload = {'': ''}
        taxi_model = getDataFromAPI(user_type, access_token, url_m, payload)

        if taxi['success'] == 1:
            taxi_data = taxi['taxi_types']
            taxi_model = taxi_model['Models']
            return render(request, "Agent/taxi_models.html", {'types': taxi_data, 'taxi_models': taxi_model})
        else:
            return render(request, "Agent/taxi_models.html", {'Types': {}})


@login_required(login_url='/login')
def taxis(request):
    if request.method == "POST":
        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            model_id = request.POST.get('model_id', '')
            taxi_reg_no = request.POST.get('taxi_reg_no', '')
            make_year = request.POST.get('make_year', '')
            garage_location = request.POST.get('garage_location', '')
            garage_distance = request.POST.get('garage_distance', '')

            user_id = request.POST.get('user_id', '')
            delete_id = request.POST.get('delete_id', '')
            taxi_id = request.POST.get('taxi_id', '')

            print(taxi_id)
            print(delete_id)

            url = ""
            payload = {}
            if taxi_id:
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_taxi"
                    payload = {'taxi_id':taxi_id,'user_id':user_id,'user_type':user_type}
                else:
                    url = settings.API_BASE_URL + "update_taxi"
                    payload = {'model_id':model_id,'taxi_reg_no':taxi_reg_no,'make_year':make_year,'garage_location':garage_location,'garage_distance':garage_distance,'taxi_id':taxi_id,'user_id':user_id,'user_type':user_type}
            else:
                url = settings.API_BASE_URL + "add_taxi"
                payload = {'model_id':model_id,'taxi_reg_no':taxi_reg_no,'make_year':make_year,'garage_location':garage_location,'garage_distance':garage_distance,'user_id':user_id,'user_type':user_type}

            taxi = getDataFromAPI(user_type, access_token, url, payload)

            if taxi['success'] == 1:
                return HttpResponseRedirect("agents/taxis", {'message': "Operation Successfully"})

        else:
            return HttpResponseRedirect("/agents/login")

    else:
        user_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "taxis"
        payload = {'': ''}
        taxi = getDataFromAPI(user_type, access_token, url, payload)

        url_m = settings.API_BASE_URL + "taxi_models"
        payload = {'': ''}
        taxi_model = getDataFromAPI(user_type, access_token, url_m, payload)

        if taxi['success'] == 1:
            taxi = taxi['Taxis']
            taxi_model = taxi_model['Models']
            return render(request, "Agent/taxis.html", {'taxis': taxi, 'taxi_models': taxi_model})
        else:
            return render(request, "Agent/taxis.html", {'Types': {}})


@login_required(login_url='/login')
def add_company(request):
    if request.method == "POST":
        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

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

            user_id = request.POST.get('cotrav_agent_id', '')


            corporate_id = request.POST.get('corporate_id')
            delete_id = request.POST.get('delete_id')

            if corporate_id:
                password = ''
            else:
                password = make_password("taxi123")
                corporate_id = 0

            payload = {'corporate_name':corporate_name,'corporate_code':corporate_code,'contact_person_name':contact_person_name,'contact_person_no':contact_person_no,
                     'contact_person_email': contact_person_email,'bill_corporate_name':bill_corporate_name,'address_line_1':address_line_1,
                      'address_line_2': address_line_2,'address_line_3': address_line_3, 'gst_id': gst_id,'has_billing_spoc_level':has_billing_spoc_level,
                      'has_auth_level': has_auth_level,'no_of_auth_level':no_of_auth_level,'has_assessment_codes':
                      has_assessment_codes,'is_radio': is_radio, 'is_local': is_local, 'is_outstation': is_outstation, 'is_bus': is_bus,
                       'is_train': is_train, 'is_hotel': is_hotel, 'is_meal': is_meal, 'is_flight': is_flight,
                       'is_water_bottles': is_water_bottles, 'is_reverse_logistics': is_reverse_logistics,'is_spoc':is_spoc,'password':password,'cotrav_agent_id':user_id,
                       'user_type':user_type}

            url = settings.API_BASE_URL + "add_company"
            company = getDataFromAPI(user_type, access_token, url, payload)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/companies", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/companies", {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")
    else:
        request = get_request()

        if id:
            return render(request, 'Agent/add_company.html',{})
        else:
            return render(request, 'Agent/add_company.html', {})


@csrf_exempt
@login_required(login_url='/login')
def companies(request):
    request = get_request()
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        url = settings.API_BASE_URL+"companies"
        payload = {'some': 'data'}
        company = getDataFromAPI(login_type, access_token, url, payload)
        if company['success'] == 1:
            corporates_data = company['Corporates']
            return render(request,"Agent/companies.html",{'companies':corporates_data})
        else:
            return render(request,"Agent/companies.html",{'companies':{}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def edit_company(request, id):
    if request.method == "POST":
        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            corporate_name = request.POST.get('corporate_name', '')
            corporate_code = request.POST.get('corporate_code', '')
            contact_person_name = request.POST.get('contact_person_name', '')
            contact_person_no = request.POST.get('contact_person_no', '')
            contact_person_email = request.POST.get('contact_person_email', '')
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

            user_id = request.POST.get('user_id', '')

            corporate_id = request.POST.get('corporate_id', '')

            url = settings.API_BASE_URL + "update_company"
            payload = {'corporate_name':corporate_name,'corporate_code':corporate_code,'contact_person_name':contact_person_name,'contact_person_no':contact_person_no,
                     'contact_person_email': contact_person_email,'has_billing_spoc_level':has_billing_spoc_level,
                      'has_auth_level': has_auth_level,'no_of_auth_level':no_of_auth_level,'has_assessment_codes':
                      has_assessment_codes,'is_radio': is_radio, 'is_local': is_local, 'is_outstation': is_outstation, 'is_bus': is_bus,
                       'is_train': is_train, 'is_hotel': is_hotel, 'is_meal': is_meal, 'is_flight': is_flight,
                       'is_water_bottles': is_water_bottles, 'is_reverse_logistics': is_reverse_logistics,'corporate_id': corporate_id,'user_id':user_id,'user_type':user_type}
            print(payload)
            company = getDataFromAPI(user_type, access_token, url, payload)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/companies", {'message': "Updated Successfully"})
            else:
                return HttpResponseRedirect("/agents/companies", {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")
    else:
        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "view_company"
            payload = {'corporate_id': id}
            company = getDataFromAPI(user_type, access_token, url, payload)
            companys = company['Corporates']
            return render(request, 'Agent/edit_company.html', {'companys': companys})
        else:
            return HttpResponseRedirect("/agents/login")


def delete_company(request,id):
    request = get_request()
    if 'login_type' in request.session:
        user_type = request.session['login_type']
        access_token = request.session['access_token']

        corporate_id = request.POST.get('corporate_id', '')
        user_id = request.POST.get('user_id', '')

        url = settings.API_BASE_URL+"delete_company"
        payload = {'corporate_id': corporate_id,'user_id':user_id}
        company = getDataFromAPI(user_type, access_token, url, payload)
        if company['success'] == 1:
            return HttpResponseRedirect("/agents/companies", {'message': "Deleted Successfully"})
        else:
            return HttpResponseRedirect("/agents/companies", {'message': "Fail"})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def company_admins(request, id):
    request = get_request()
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "admins"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)

        url_companies = settings.API_BASE_URL + "companies"
        companies = getDataFromAPI(login_type, access_token, url_companies, payload)
        companies = companies['Corporates']

        if company['success'] == 1:
            admins = company['Admins']
            return render(request, "Agent/company_admins.html", {'admins': admins,'companies':companies})
        else:
            return render(request, "Agent/company_admins.html", {'admins': {}})
    else:
        return HttpResponseRedirect("/agents/login")

    
@login_required(login_url='/login')
def company_billing_entities(request, id):
    request = get_request()
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "billing_entities"
        payload = {'corporate_id': id}

        company = getDataFromAPI(login_type, access_token, url, payload)
        url_city = settings.API_BASE_URL + "cities"
        cities = getDataFromAPI(login_type, access_token, url_city, payload)

        url_companies = settings.API_BASE_URL + "companies"
        companies = getDataFromAPI(login_type, access_token, url_companies, payload)
        companies = companies['Corporates']

        if company['success'] == 1:
            entities = company['Entitys']
            cities = cities["Cities"]
            return render(request, "Agent/billing_entities.html",{'billing_entities': entities,"cities": cities,'companies': companies})
        else:
            return render(request, "Agent/billing_entities.html", {'entities': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def company_rates(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "company_rates"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)

        url_companies = settings.API_BASE_URL + "companies"
        companies = getDataFromAPI(login_type, access_token, url_companies, payload)
        companies = companies['Corporates']
        url_city = settings.API_BASE_URL + "cities"
        cities = getDataFromAPI(login_type, access_token, url_city, payload)
        url_taxi_type = settings.API_BASE_URL + "taxi_types"
        taxi_type = getDataFromAPI(login_type, access_token, url_taxi_type, payload)

        if company['success'] == 1:
            company_rates = company['Corporate_Retes']
            cities = cities["Cities"]
            taxi_type = taxi_type['taxi_types']
            return render(request, "Agent/company_rates.html", {'corporate_rates': company_rates,'companies':companies,'cities':cities,'taxi_types':taxi_type})
        else:
            return render(request, "Agent/company_rates.html", {'entities': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def company_groups(request, id):
    request = get_request()
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "groups"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)

        url_companies = settings.API_BASE_URL + "companies"
        companies = getDataFromAPI(login_type, access_token, url_companies, payload)
        companies = companies['Corporates']

        if company['success'] == 1:
            groups = company['Groups']
            return render(request, "Agent/groups.html", {'groups': groups,'companies':companies})
        else:
            return render(request, "Agent/groups.html", {'groups': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def company_subgroups(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "subgroups"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)

        url_companies = settings.API_BASE_URL + "companies"
        companies = getDataFromAPI(login_type, access_token, url_companies, payload)
        companies = companies['Corporates']

        if company['success'] == 1:
            url2 = settings.API_BASE_URL + "groups"
            subgroups = company['Subgroups']
            r = requests.post(url2, data=payload, headers=headers)
            gr = json.loads(r.text)
            groups = gr['Groups']
            return render(request, "Agent/subgroups.html", {'subgroups': subgroups, 'groups': groups,'companies':companies})
        else:
            return render(request, "Agent/subgroups.html", {'subgroups': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def company_spocs(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "spocs"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)
        if company['success'] == 1:
            spocs = company['Spocs']
            return render(request, "Agent/spocs.html", {'spocs': spocs})
        else:
            return render(request, "Agent/spocs.html", {'spocs': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def company_employees(request, id):
    request = get_request()
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "employees"
        payload = {'corporate_id': id}
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)
        if company['success'] == 1:
            employees = company['Employees']
            return render(request, "Agent/employees.html", {'employees': employees})
        else:
            return render(request, "Agent/employees.html", {'employees': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def assessment_cities(request,id):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id;

        if request.method == 'POST':
            corporate_id = request.POST.get('corporate_id', '')
            city_name = request.POST.get('city_name', '')

            city_id = request.POST.get('city_id', '')

            payload = {'corporate_id':corporate_id,'city_name':city_name,'city_id':city_id,'login_type':login_type,'user_id':user_id}

            if city_id:
                url = settings.API_BASE_URL + "update_assessment_cities"
            else:
                url = settings.API_BASE_URL + "add_assessment_cities"

            company = getDataFromAPI(login_type, access_token, url, payload)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/assessment_cities/0", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/assessment_cities/0", {'message': "Record Not Added"})

        else:
            url = settings.API_BASE_URL + "assessment_cities"
            payload = {'corporate_id':id}
            headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
            r = requests.post(url, data=payload, headers=headers)
            company = json.loads(r.text)

            url_comp = settings.API_BASE_URL + "companies"
            company1 = getDataFromAPI(login_type, access_token, url_comp, payload)


            if company['success'] == 1:
                cities = company['Cities']
                companies = company1['Corporates']
                return render(request, "Agent/assessment_cities.html", {'cities': cities,'companies':companies})
            else:
                return render(request, "Agent/assessment_cities.html", {'employees': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def assessment_codes(request,id):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        user_id = request.user.id;
        if request.method == 'POST':

            corporate_id = request.POST.get('corporate_id', '')
            assessment_code = request.POST.get('assessment_code', '')
            code_desc = request.POST.get('code_desc', '')
            from_date = request.POST.get('from_date', '')
            to_date = request.POST.get('to_date', '')
            service_from = request.POST.get('service_from', '')
            service_to = request.POST.get('service_to', '')

            city_id = request.POST.get('city_id', '')

            payload = {'corporate_id': corporate_id, 'assessment_code': assessment_code, 'code_desc': code_desc,'from_date':from_date,'to_date':to_date,
                       'login_type': login_type, 'user_id': user_id,'service_from':service_from,'service_to':service_to}

            if city_id:
                url = settings.API_BASE_URL + "update_assessment_codes"
            else:
                url = settings.API_BASE_URL + "add_assessment_codes"

            company = getDataFromAPI(login_type, access_token, url, payload)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/assessment_codes/0", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/assessment_codes/0", {'message': "Record Not Added"})

        else:
            url = settings.API_BASE_URL + "assessment_codes"
            payload = {'corporate_id':id}
            headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
            r = requests.post(url, data=payload, headers=headers)
            company = json.loads(r.text)

            url_comp = settings.API_BASE_URL + "companies"
            company1 = getDataFromAPI(login_type, access_token, url_comp, payload)

            if company['success'] == 1:
                codes = company['Codes']
                companies = company1['Corporates']
                return render(request, "Agent/assessment_codes.html", {'codes': codes,'companies':companies})
            else:
                return render(request, "Agent/assessment_codes.html", {'codes': {}})
    else:
        return HttpResponseRedirect("/agents/login")

@login_required(login_url='/login')
def delete_assessment_codes(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        code_id = request.POST.get('code_id')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            payload = {'code_id': code_id, 'user_id': user_id, 'login_type': login_type}
            url = settings.API_BASE_URL + "delete_assessment_codes"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/assessment_codes/0", {'message': "Deleted Successfully"})
            else:
                return HttpResponseRedirect("/agents/assessment_codes/0", {'message': "Fails"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def delete_assessment_cities(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        city_id = request.POST.get('city_id')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            payload = {'city_id': city_id, 'user_id': user_id, 'login_type': login_type}
            url = settings.API_BASE_URL + "delete_assessment_cities"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/assessment_cities/0", {'message': "Deleted Successfully"})
            else:
                return HttpResponseRedirect("/agents/assessment_cities/0", {'message': "Fails"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_rate(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')

        if 'login_type' in request.session:
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            package_name = request.POST.get('package_name', '')
            city_id = request.POST.get('city_id')
            taxi_type = request.POST.get('taxi_type', '')
            tour_type = request.POST.get('tour_type', '')
            kms = request.POST.get('kms', '')
            hours = request.POST.get('hours', '')
            km_rate = request.POST.get('km_rate', '')
            hour_rate = request.POST.get('hour_rate', '')
            base_rate = request.POST.get('base_rate', '')
            night_rate = request.POST.get('night_rate', '')

            delete_id = request.POST.get('delete_id')
            rate_id = request.POST.get('rate_id')

            payload = {'corporate_id': corporate_id,'package_name':package_name,'city_id':city_id,'taxi_type':taxi_type,
            'tour_type':tour_type,'kms':kms,'hours':hours,'km_rate':km_rate,'hour_rate':hour_rate,'base_rate':base_rate,'night_rate':night_rate,
            'user_id': user_id, 'user_type': user_type,'rate_id':rate_id,'is_delete': delete_id, }

            if rate_id:
                url = settings.API_BASE_URL + "update_company_rates"

                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_company_rates"

            else:
                url = settings.API_BASE_URL + "add_company_rates"

            company = getDataFromAPI(user_type, access_token, url, payload)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/rates/0", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/rates/0", {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_entity(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')


        if 'login_type' in request.session:
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

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token,
                       'entity_name': entity_name, 'billing_city_id': billing_city_id,
                       'contact_person_name': contact_person_name, 'contact_person_email': contact_person_email,
                       'contact_person_no': contact_person_no, 'address_line_1': address_line_1,
                       'address_line_2': address_line_2,
                       'address_line_3': address_line_3, 'gst_id': gst_id, 'pan_no': pan_no, 'entity_id': entity_id,
                       'is_delete': delete_id, }

            url = ""
            if entity_id:
                url = settings.API_BASE_URL + "update_billing_entity"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_billing_entity"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_billing_entity"

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/billing_entities/0", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/billing_entities//0", {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_group(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            group_name = request.POST.get('group_name', '')
            zone_name = request.POST.get('zone_name')

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'group_name': group_name, 'zone_name': zone_name}

            url = settings.API_BASE_URL + "add_group"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/groups/" + str(id), {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/groups/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_subgroup(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            subgroup_name = request.POST.get('group_name', '')
            group_id = request.POST.get('group_id', '')

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'subgroup_name': subgroup_name, 'group_id': group_id}

            print(payload)
            url = settings.API_BASE_URL + "add_subgroup"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/subgroups/" + str(id), {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/subgroups/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def update_company_group(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        group_id = request.POST.get('group_id', '')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            group_name = request.POST.get('group_name', '')
            zone_name = request.POST.get('zone_name')

            payload = {'group_id': group_id, 'access_token': access_token, 'group_name': group_name, 'zone_name': zone_name,
                       'user_id': user_id, 'login_type': login_type}

            print(payload)
            url = settings.API_BASE_URL + "update_group"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/view-company-group/" + group_id, {'message': "Update Successfully"})
            else:
                return HttpResponseRedirect("/agents/view-company-group/" + group_id, {'message': "Record Not Updated"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def update_company_subgroup(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            group_name = request.POST.get('group_name', '')

            payload = {'subgroup_id': subgroup_id, 'access_token': access_token, 'group_name': group_name,
                       'user_id': user_id, 'login_type': login_type}

            print(payload)
            url = settings.API_BASE_URL + "update_subgroup"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/view-company-subgroup/" + str(id),{'message': "Update Successfully"})
            else:
                return HttpResponseRedirect("/agents/view-company-subgroup/" + str(id),{'message': "Record Not Updated"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def delete_company_group(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        group_id = request.POST.get('group_id')

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            access_token_auth = request.session['access_token']

            payload = {'group_id': group_id, 'user_id': user_id, 'login_type': login_type, 'access_token': access_token,
                       'access_token_auth': access_token_auth}
            url = settings.API_BASE_URL + "delete_group"
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/groups/" + str(id), {'message': "Delete Successfully"})
            else:
                return HttpResponseRedirect("/agents/groups/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def delete_company_subgroup(request, id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            user_id = request.POST.get('user_id', '')
            subgroup_id = request.POST.get('subgroup_id')
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            access_token_auth = request.session['access_token']

            payload = {'subgroup_id': subgroup_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'access_token_auth': access_token_auth}
            url = settings.API_BASE_URL + "delete_subgroup"
            company = getDataFromAPI(login_type, access_token, url, payload)
            print(payload)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/subgroups/" + str(id), {'message': "Delete Successfully"})
            else:
                return HttpResponseRedirect("/agents/subgroups/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_group_auth(request, id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            user_id = request.POST.get('user_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            access_token_auth = request.session['access_token']

            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            cid = request.POST.get('cid', '')
            contact_no = request.POST.get('contact_no', '')

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

            group_id = request.POST.get('group_id')
            group_auth_id = request.POST.get('group_auth_id')
            delete_id = request.POST.get('delete_id')

            if group_id:
                group_auth_id = group_auth_id
                password = make_password("taxi123")

            if group_auth_id:
                group_auth_id = group_auth_id
            else:
                group_auth_id = 0

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'name': name, 'email': email, 'cid': cid, 'contact_no': contact_no,
                       'is_radio': is_radio, 'is_local': is_local, 'is_outstation': is_outstation, 'is_bus': is_bus,
                       'is_train': is_train, 'is_hotel': is_hotel, 'is_meal': is_meal, 'is_flight': is_flight,
                       'is_water_bottles': is_water_bottles, 'is_reverse_logistics': is_reverse_logistics,
                       'group_id': group_id, 'delete_id': delete_id, 'password': password, 'group_auth_id': group_auth_id,
                       'access_token_auth': access_token_auth}

            url = ""
            if group_auth_id:
                url = settings.API_BASE_URL + "update_group_auth"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_group_auth"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_group_auth"

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/view-company-group/" + group_id, {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/view-company-group/" + group_id, {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_subgroup_auth(request, id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            user_id = request.POST.get('user_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            access_token_auth = request.session['access_token']

            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            cid = request.POST.get('cid', '')
            contact_no = request.POST.get('contact_no', '')

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

            subgroup_id = request.POST.get('subgroup_id')
            subgroup_auth_id = request.POST.get('subgroup_auth_id')
            delete_id = request.POST.get('delete_id')

            if subgroup_id:
                subgroup_auth_id = subgroup_auth_id
                password = make_password("taxi123")

            if subgroup_auth_id:
                subgroup_auth_id = subgroup_auth_id
            else:
                subgroup_auth_id = 0

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'name': name, 'email': email, 'cid': cid, 'contact_no': contact_no,
                       'is_radio': is_radio, 'is_local': is_local, 'is_outstation': is_outstation, 'is_bus': is_bus,
                       'is_train': is_train, 'is_hotel': is_hotel, 'is_meal': is_meal, 'is_flight': is_flight,
                       'is_water_bottles': is_water_bottles, 'is_reverse_logistics': is_reverse_logistics,
                       'subgroup_id': subgroup_id, 'delete_id': delete_id, 'password': password,
                       'subgroup_auth_id': subgroup_auth_id, 'access_token_auth': access_token_auth}

            url = ""
            if subgroup_auth_id:
                url = settings.API_BASE_URL + "update_subgroup_auth"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_subgroup_auth"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_subgroup_auth"

            company = getDataFromAPI(login_type, access_token, url, payload)
            print(url)
            print(company)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/view-company-subgroup/" + subgroup_id,{'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/view-company-subgroup/" + subgroup_id, {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_company_admins(request, id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            user_id = request.POST.get('user_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            access_token_auth = request.session['access_token']

            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            cid = request.POST.get('cid', '')
            contact_no = request.POST.get('contact_no', '')

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

            admin_id = request.POST.get('admin_id')

            delete_id = request.POST.get('delete_id')

            if admin_id:
                password = ''
            else:
                password = make_password("taxi123")

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'name': name, 'email': email, 'cid': cid, 'contact_no': contact_no,
                       'is_radio': is_radio, 'is_local': is_local, 'is_outstation': is_outstation, 'is_bus': is_bus,
                       'is_train': is_train, 'is_hotel': is_hotel, 'is_meal': is_meal, 'is_flight': is_flight,
                       'is_water_bottles': is_water_bottles, 'is_reverse_logistics': is_reverse_logistics,
                       'admin_id': admin_id, 'delete_id': delete_id, 'password': password,
                       'access_token_auth': access_token_auth}

            url = ""
            if admin_id:
                url = settings.API_BASE_URL + "update_admin"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_admin"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_admin"

            company = getDataFromAPI(login_type, access_token, url, payload)
            print(url)
            print(company)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/admins/" + str(id), {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/admins/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_spocs(request, id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            user_id = request.POST.get('user_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            group_id = request.POST.get('group_id', '')
            subgroup_id = request.POST.get('subgroup_id', '')
            user_cid = request.POST.get('user_cid', '')

            user_name = request.POST.get('user_name', '')
            user_contact = request.POST.get('user_contact', '')
            email = request.POST.get('email', '')
            username = request.POST.get('username', '')
            budget = request.POST.get('budget', '')
            expense = request.POST.get('expense', '')

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

            spoc_id = request.POST.get('spoc_id')

            delete_id = request.POST.get('delete_id')

            if spoc_id:
                password = ''
            else:
                password = make_password("taxi123")
                spoc_id =0

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                       'access_token': access_token, 'group_id': group_id, 'subgroup_id': subgroup_id, 'user_cid': user_cid, 'user_name': user_name,
                       'user_contact':user_contact,'email':email,'username':username,'budget':budget,'expense':expense,
                       'is_radio': is_radio, 'is_local': is_local, 'is_outstation': is_outstation, 'is_bus': is_bus,
                       'is_train': is_train, 'is_hotel': is_hotel, 'is_meal': is_meal, 'is_flight': is_flight,
                       'is_water_bottles': is_water_bottles, 'is_reverse_logistics': is_reverse_logistics,
                       'spoc_id': spoc_id, 'delete_id': delete_id, 'password': password}

            url = ""
            print(payload)
            if spoc_id:
                url = settings.API_BASE_URL + "update_spoc"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_spoc"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_spoc"

            company = getDataFromAPI(login_type, access_token, url, payload)
            print(url)
            print(company)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/spocs/" + str(id), {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/spocs/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")
    else:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
        if 'login_type' in request.session:
            url_spoc = settings.API_BASE_URL + "view_spoc"
            payload = {'spoc_id': id}
            r = requests.post(url_spoc, data=payload, headers=headers)
            company_spoc = json.loads(r.text)
            spocs = company_spoc['Spoc']

            for spoc in spocs:
                corporate_id = spoc['corporate_id']

            url = settings.API_BASE_URL + "groups"
            payload = {'corporate_id': 0}

            r = requests.post(url, data=payload, headers=headers)
            company = json.loads(r.text)
            groups = company['Groups']
            url_subgroup = settings.API_BASE_URL + "subgroups"
            r = requests.post(url_subgroup, data=payload, headers=headers)
            company_sub = json.loads(r.text)
            subgroups = company_sub['Subgroups']

            url_companies = settings.API_BASE_URL + "companies"
            companies = getDataFromAPI(login_type, access_token, url_companies, payload)
            companies = companies['Corporates']

            if id:
                return render(request, 'Agent/add_spoc.html', {'groups': groups, 'subgroups': subgroups, 'spoc':spocs, 'companies':companies})
            else:
                return render(request, 'Agent/add_spoc.html', {'groups': groups, 'subgroups': subgroups,'companies':companies})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_employee(request, id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            user_id = request.POST.get('user_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            spoc_id = request.POST.get('spoc_id', '')
            billing_entity_id = request.POST.get('billing_entity_id', '')
            core_employee_id = request.POST.get('core_employee_id', '')
            employee_cid = request.POST.get('employee_cid', '')

            employee_name = request.POST.get('employee_name', '')
            employee_email = request.POST.get('employee_email', '')
            employee_contact = request.POST.get('employee_contact', '')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            id_proof_type = request.POST.get('id_proof_type')

            id_proof_no = request.POST.get('id_proof_no', '')
            is_active = request.POST.get('is_active','')
            has_dummy_email = request.POST.get('has_dummy_email')
            fcm_regid = request.POST.get('fcm_regid')
            is_cxo = request.POST.get('is_cxo')
            designation = request.POST.get('designation', '')
            home_city = request.POST.get('home_city', '')
            home_address = request.POST.get('home_address', '')
            assistant_id = request.POST.get('assistant_id', '')
            date_of_birth = request.POST.get('date_of_birth', '')

            employee_id = request.POST.get('employee_id')

            delete_id = request.POST.get('delete_id')

            if employee_id:
                password = ''
            else:
                password = make_password("taxi123")
                employee_id =0

            payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,'spoc_id':spoc_id,'core_employee_id':core_employee_id,
                       'access_token': access_token,'employee_cid':employee_cid,'employee_name':employee_name,'employee_email':employee_email,
                       'employee_contact':employee_contact,'age':age,'gender':gender,'id_proof_type':id_proof_type,'id_proof_no':id_proof_no,
                       'is_active':is_active,'has_dummy_email':has_dummy_email,'fcm_regid':fcm_regid,'is_cxo':is_cxo,'employee_id': employee_id,
                       'designation':designation,'home_city':home_city,'home_address':home_address,'assistant_id':assistant_id,'date_of_birth':date_of_birth,
                       'delete_id': delete_id, 'password': password,'billing_entity_id':billing_entity_id}

            url = ""
            print(payload)
            if employee_id:
                url = settings.API_BASE_URL + "update_employee"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_employee"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_employee"

            company = getDataFromAPI(login_type, access_token, url, payload)
            print(url)
            print(company)
            if company['success'] == 1:
                return HttpResponseRedirect("/agents/employees/" + str(id), {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/employees/" + str(id), {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")
    else:
        request = get_request()

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url_emp = settings.API_BASE_URL + "view_employee"
            payload = {'employee_id': id}
            company_emp = getDataFromAPI(login_type, access_token, url_emp, payload)
            employees = company_emp['Employee']

            url_companies = settings.API_BASE_URL + "companies"
            companies = getDataFromAPI(login_type, access_token, url_companies, payload)
            companies = companies['Corporates']

            url_spoc = settings.API_BASE_URL + "spocs"
            payload_spoc = {'corporate_id': 0}
            company_spoc = getDataFromAPI(login_type, access_token, url_spoc, payload_spoc)
            spocs = company_spoc['Spocs']

            url_entity = settings.API_BASE_URL + "billing_entities"
            payload_entity = {'corporate_id': 0}
            company_entity = getDataFromAPI(login_type, access_token, url_entity, payload_entity)
            entitys = company_entity['Entitys']

            if id:
                return render(request, 'Agent/add_employee.html', {'employee':employees,'spocs':spocs,'entitys':entitys,'companies':companies})
            else:
                return render(request, 'Agent/add_employee.html', {'spocs':spocs,'entitys':entitys,'companies':companies})
        else:
            return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def add_agent(request,id):
    if request.method == 'POST':
        request = get_request()

        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('user_id', '')

            emp_id = request.POST.get('emp_id', '')
            username = request.POST.get('username', '')
            contact_no = request.POST.get('contact_no', '')
            email = request.POST.get('email', '')

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

            has_billing_access = request.POST.get('has_billing_access', '')
            has_voucher_payment_access = request.POST.get('has_voucher_payment_access', '')
            has_voucher_approval_access = request.POST.get('has_voucher_approval_access', '')
            is_super_admin = request.POST.get('is_super_admin', '')

            agent_id = request.POST.get('agents_id','')

            delete_id = request.POST.get('delete_id')

            if agent_id:
                password = ''
            else:
                password = make_password("taxi123")
                agent_id =0

            payload = {'emp_id': emp_id,'username': username,'contact_no': contact_no,'email': email,'is_radio': is_radio,'is_local': is_local,
                  'is_outstation': is_outstation,'is_bus': is_bus,'is_train': is_train,'is_hotel': is_hotel,'is_meal':is_meal,'is_flight':is_flight,
                     'is_water_bottles':  is_water_bottles,'is_reverse_logistics':
            is_reverse_logistics,'has_billing_access':has_billing_access,'has_voucher_payment_access':has_voucher_payment_access,
                      'has_voucher_approval_access': has_voucher_approval_access,'is_super_admin':is_super_admin,'password':password,'user_id':user_id,'user_type':login_type,'agent_id':agent_id}

            url = ""
            print(payload)
            if agent_id:
                url = settings.API_BASE_URL + "update_agent"
                print("in auth id")
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_agent"
                    print(url)

            else:
                url = settings.API_BASE_URL + "add_agent"

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/agents", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/agents", {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if id:

            if 'login_type' in request.session:
                login_type = request.session['login_type']
                access_token = request.session['access_token']

                url_agent = settings.API_BASE_URL + "view_agent"
                payload = {'agent_id': id}
                agent = getDataFromAPI(login_type, access_token, url_agent, payload)
                agents = agent['Agent']
                return render(request, 'Agent/add_agent.html', {'agent':agents})
            else:
                return HttpResponseRedirect("/agents/login")
        else:
            return render(request, 'Agent/add_agent.html', {})


@login_required(login_url='/login')
def view_company_group(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_group"
        payload = {'group_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        url = settings.API_BASE_URL + "view_group_auth"
        grp_auths = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            groups = company['Groups']
            grp_auths = grp_auths['Groups']
            return render(request, "Agent/view_groups.html", {'group': groups, 'grp_auths': grp_auths})
        else:
            return render(request, "Agent/view_groups.html", {'group': {}})
    else:
        return HttpResponseRedirect("/agents/login")


@login_required(login_url='/login')
def view_company_subgroup(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_subgroup"
        payload = {'subgroup_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        url = settings.API_BASE_URL + "view_subgroup_auth"
        subgrp_auths = getDataFromAPI(login_type, access_token, url, payload)
        print(subgrp_auths)
        if company['success'] == 1:
            subgroups = company['SubGroups']
            subgrp_auths = subgrp_auths['SubGroups']
            return render(request, "Agent/view_subgroups.html",{'subgroup': subgroups, 'subgrp_auths': subgrp_auths})
        else:
            return render(request, "Agent/view_subgroups.html", {'group': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def view_agents(request):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL+"agents"
        payload = {'some': 'data'}
        agents = getDataFromAPI(login_type, access_token, url, payload)
        if agents['success'] == 1:
            agents = agents['Agents']
            return render(request,"Agent/agents.html",{'agents':agents})
        else:
            return render(request,"Agent/agents.html",{'agents':{}})
    else:
        return HttpResponseRedirect("/agents/login")


def operators(request):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL+"operators"
        payload = {}
        operators = getDataFromAPI(login_type, access_token, url, payload)
        if operators['success'] == 1:
            operators = operators['Operators']
            return render(request,"Agent/operators.html",{'operators':operators})
        else:
            return render(request,"Agent/operators.html",{'operators':{}})
    else:
        return HttpResponseRedirect("/agents/login")


def operator_contacts(request, id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            operator_id = request.POST.get('operator_id', '')
            operator_address = request.POST.get('operator_address', '')
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            contact_no = request.POST.get('contact_no', '')

            contact_id = request.POST.get('contact_id', '')
            user_id = request.POST.get('user_id', '')
            delete_id = request.POST.get('delete_id', '')
            url = ""
            payload = {}

            if contact_id:
                if delete_id == '1':
                    print("in delete")
                    url = settings.API_BASE_URL + "delete_operator_contact"
                    payload = {'contact_id':contact_id,'user_id':user_id,'user_type':user_type}
                else:
                    print("in edit")
                    url = settings.API_BASE_URL + "update_operator_contact"
                    payload = {'contact_id':contact_id,'operator_id':operator_id,'operator_address':operator_address,'contact_name':contact_name,'contact_email':contact_email,
                               'contact_no':contact_no,'user_id':user_id,'user_type':user_type}
            else:
                url = settings.API_BASE_URL + "add_operator_contact"
                payload = {'operator_id':operator_id,'operator_address':operator_address,'contact_name':contact_name,'contact_email':contact_email,
                               'contact_no':contact_no,'user_id':user_id,'user_type':user_type}

            taxi = getDataFromAPI(user_type, access_token, url, payload)

            if taxi['success'] == 1:
                return HttpResponseRedirect("/agents/operator_contacts/"+str(id), {'message': "Added Successfully"})
        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL+"operator_contacts"
            payload = {'operator_id':id}
            operator_contacts = getDataFromAPI(login_type, access_token, url, payload)

            if operator_contacts['success'] == 1:
                operator_contacts = operator_contacts['OperatorContacts']
                return render(request,"Agent/operator_contacts.html",{'operator_contacts':operator_contacts,'operator_id':id})
            else:
                return render(request,"Agent/operator_contacts.html",{'operator_contacts':{}})
    else:
        return HttpResponseRedirect("/agents/login")


def operator_banks(request,id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            user_type = request.session['login_type']
            access_token = request.session['access_token']

            operator_id = request.POST.get('operator_id', '')
            beneficiary_name = request.POST.get('beneficiary_name', '')
            beneficiary_account_no = request.POST.get('beneficiary_account_no', '')
            bank_name = request.POST.get('bank_name', '')
            ifsc_code = request.POST.get('ifsc_code', '')

            bank_id = request.POST.get('bank_id', '')
            user_id = request.POST.get('user_id', '')
            delete_id = request.POST.get('delete_id', '')

            url = ""
            payload = {}

            if bank_id:
                if delete_id == '1':
                    print("in delete")
                    url = settings.API_BASE_URL + "delete_operator_bank"
                    payload = {'bank_id': bank_id, 'user_id': user_id, 'user_type': user_type}
                else:
                    print("in edit")
                    url = settings.API_BASE_URL + "update_operator_bank"
                    payload = {'bank_id': bank_id, 'operator_id': operator_id,'beneficiary_name':beneficiary_name,
                               'beneficiary_account_no':beneficiary_account_no,'bank_name':bank_name,'ifsc_code':ifsc_code,
                               'user_id': user_id, 'user_type': user_type}
            else:
                url = settings.API_BASE_URL + "add_operator_bank"
                payload = {'operator_id': operator_id,'beneficiary_name':beneficiary_name,'beneficiary_account_no':beneficiary_account_no,'bank_name':bank_name,'ifsc_code':ifsc_code,
                           'user_id': user_id, 'user_type': user_type}

            taxi = getDataFromAPI(user_type, access_token, url, payload)

            if taxi['success'] == 1:
                return HttpResponseRedirect("/agents/operator_banks/"+id, {'message': "Added Successfully"})

        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "operator_banks"
            payload = {'operator_id': id}
            operator_banks = getDataFromAPI(login_type, access_token, url, payload)
            if operator_banks['success'] == 1:
                operator_banks = operator_banks['OperatorBanks']
                return render(request, "Agent/operator_banks.html", {'operator_banks': operator_banks,'operator_id':id})
            else:
                return render(request, "Agent/operator_banks.html", {'operator_contacts': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def delete_operator(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        operator_id = request.POST.get('operator_id', '')
        user_id = request.POST.get('user_id', '')

        url = settings.API_BASE_URL+"delete_operator"
        payload = {'operator_id': operator_id,'user_id':user_id,'user_type':login_type}
        operators = getDataFromAPI(login_type, access_token, url, payload)
        if operators['success'] == 1:
            return HttpResponseRedirect("/agents/operators", {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/agents/operators", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/agents/login")




def add_operator(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            cotrav_agent_id = request.POST.get('cotrav_agent_id', '')

            type = request.POST.get('type', '')
            username = request.POST.get('username', '')
            operator_name = request.POST.get('operator_name', '')
            operator_email = request.POST.get('operator_email', '')

            operator_contact = request.POST.get('operator_contact', '')
            website = request.POST.get('website', '')

            is_service_tax_applicable = request.POST.get('is_service_tax_applicable', '')
            service_tax_number = request.POST.get('service_tax_number', '')
            night_start_time = request.POST.get('night_start_time', '')
            night_end_time = request.POST.get('night_end_time', '')
            tds_rate = request.POST.get('tds_rate', '')
            gst_id = request.POST.get('gst_id', '')
            pan_no = request.POST.get('pan_no', '')

            operator_id = request.POST.get('operator_id', '')
            delete_id = request.POST.get('delete_id')

            if operator_id:
                password = ''
            else:
                password = make_password("taxi123")
                operator_id = 0

            payload = {'type':type,'username':username,'password':password,'operator_name':operator_name,'operator_email':operator_email,'operator_contact':operator_contact,
                       'website':website,
                       'is_service_tax_applicable':is_service_tax_applicable,'service_tax_number':service_tax_number,'night_start_time':night_start_time,
                       'night_end_time':night_end_time,'tds_rate':tds_rate,'gst_id':gst_id,'pan_no':pan_no,'operator_id':operator_id,'user_id':cotrav_agent_id,'user_type':login_type}

            url = ""

            if operator_id:
                url = settings.API_BASE_URL + "update_operator"
                if delete_id == '1':
                    url = settings.API_BASE_URL + "delete_operator"
            else:
                url = settings.API_BASE_URL + "add_operator"

            operator = getDataFromAPI(login_type, access_token, url, payload)

            if operator['success'] == 1:
                return HttpResponseRedirect("/agents/operators", {'message': "Added Successfully"})
            else:
                return HttpResponseRedirect("/agents/operators", {'message': "Record Not Added"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            if id:
                login_type = request.session['login_type']
                access_token = request.session['access_token']
                payload = {'operator_id':id}
                url = settings.API_BASE_URL + "view_operator"
                operator = getDataFromAPI(login_type, access_token, url, payload)
                operator = operator['Operator']
                return render(request, 'Agent/add_operator.html', {'operators':operator})
            else:
                return render(request, 'Agent/add_operator.html', {})
        else:
            return HttpResponseRedirect("/agents/login")



def operator_rates(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "operator_rates"
        payload = {}
        op_rates = getDataFromAPI(login_type, access_token, url, payload)
        if op_rates['success'] == 1:
            op_rates = op_rates['Rates']
            return render(request, "Agent/operator_rates.html", {'op_rates': op_rates})
        else:
            return render(request, "Agent/operator_rates.html", {'op_rates': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def add_operator_rate(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            user_id = request.POST.get('cotrav_agent_id', '')

            operator_id = request.POST.get('operator_id', '')
            city_id = request.POST.get('city_id', '')
            taxi_type_id = request.POST.get('taxi_type_id', '')
            package_name = request.POST.get('package_name', '')
            tour_type = request.POST.get('tour_type', '')
            kms = request.POST.get('kms', '')
            hours = request.POST.get('hours', '')
            km_rate = request.POST.get('km_rate', '')
            hour_rate = request.POST.get('hour_rate', '')
            base_rate = request.POST.get('base_rate', '')
            night_rate = request.POST.get('night_rate', '')
            fuel_rate = request.POST.get('fuel_rate', '')

            rate_id = request.POST.get('rate_id', '')

            payload = {'operator_id':operator_id,'city_id':city_id,'taxi_type_id':taxi_type_id,'package_name':package_name,'tour_type':tour_type,
                       'kms':kms,'hours':hours,'km_rate':km_rate,'hour_rate':hour_rate,'base_rate':base_rate,'night_rate':night_rate,'fuel_rate':fuel_rate,
                       'rate_id':rate_id,'user_id':user_id,'login_type':login_type}

            url = ""

            if rate_id:
                url = settings.API_BASE_URL + "update_operator_rate"
            else:
                url = settings.API_BASE_URL + "add_operator_rate"

            operator = getDataFromAPI(login_type, access_token, url, payload)

            if operator['success'] == 1:
                return HttpResponseRedirect("/agents/operator-rates", {'message': "Operation Successfully"})
            else:
                payload = {'operator_id': id}
                url = settings.API_BASE_URL + "operator_rate"
                operators = getDataFromAPI(login_type, access_token, url, payload)
                operators = operators['Rates']

                url_cities = settings.API_BASE_URL + "cities"
                cities = getDataFromAPI(login_type, access_token, url_cities, payload)
                cities = cities['Cities']

                url_taxi_type = settings.API_BASE_URL + "taxi_types"
                taxi_types = getDataFromAPI(login_type, access_token, url_taxi_type, payload)
                taxi_types = taxi_types['taxi_types']

                return render(request, 'Agent/add_operator_rate.html', {'operators':operators,'cities':cities,'taxi_types':taxi_types})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            if id:
                if 'login_type' in request.session:
                    login_type = request.session['login_type']
                    access_token = request.session['access_token']
                    payload = {'rate_id': id}
                    url = settings.API_BASE_URL + "view_operator_rate"
                    op_rates = getDataFromAPI(login_type, access_token, url, payload)
                    op_rates = op_rates['Rate']

                    url = settings.API_BASE_URL + "operators"
                    operators = getDataFromAPI(login_type, access_token, url, payload)
                    operators = operators['Operators']

                    url_cities = settings.API_BASE_URL + "cities"
                    cities = getDataFromAPI(login_type, access_token, url_cities, payload)
                    cities = cities['Cities']

                    url_taxi_type = settings.API_BASE_URL + "taxi_types"
                    taxi_types = getDataFromAPI(login_type, access_token, url_taxi_type, payload)
                    taxi_types = taxi_types['taxi_types']

                    return render(request, 'Agent/add_operator_rate.html', {'operator_rates': op_rates,'operators':operators,'cities':cities,'taxi_types':taxi_types})
                else:
                    return HttpResponseRedirect("/agents/login")
            else:
                if 'login_type' in request.session:
                    login_type = request.session['login_type']
                    access_token = request.session['access_token']

                    payload = {'operator_id': id}
                    url = settings.API_BASE_URL + "operators"
                    operators = getDataFromAPI(login_type, access_token, url, payload)
                    operators = operators['Operators']

                    url_cities = settings.API_BASE_URL + "cities"
                    cities = getDataFromAPI(login_type, access_token, url_cities, payload)
                    cities = cities['Cities']

                    url_taxi_type = settings.API_BASE_URL + "taxi_types"
                    taxi_types = getDataFromAPI(login_type, access_token, url_taxi_type, payload)
                    taxi_types = taxi_types['taxi_types']

                    return render(request, 'Agent/add_operator_rate.html', {'operators':operators,'cities':cities,'taxi_types':taxi_types})
                else:
                    return HttpResponseRedirect("/agents/login")
        else:
            return HttpResponseRedirect("/agents/login")


def delete_operator_rate(request,id):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        rate_id = request.POST.get('rate_id', '')
        user_id = request.POST.get('user_id', '')

        url = settings.API_BASE_URL+"delete_operator_rate"
        payload = {'rate_id': rate_id,'user_id':user_id,'user_type':login_type}
        operators = getDataFromAPI(login_type, access_token, url, payload)
        if operators['success'] == 1:
            return HttpResponseRedirect("/agents/operator-rates", {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/agents/operator-rates", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/agents/login")


def operator_drivers(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "operator_drivers"
        payload = {}
        op_drivers = getDataFromAPI(login_type, access_token, url, payload)
        if op_drivers['success'] == 1:
            drivers = op_drivers['Drivers']
            return render(request, "Agent/operator_drivers.html", {'op_drivers': drivers})
        else:
            return render(request, "Agent/operator_drivers.html", {'op_drivers': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def add_operator_driver(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            user_id = request.POST.get('cotrav_agent_id', '')

            operator_id = request.POST.get('operator_id', '')
            driver_name = request.POST.get('driver_name', '')
            driver_contact = request.POST.get('driver_contact', '')
            driver_email = request.POST.get('driver_email', '')
            licence_no = request.POST.get('licence_no', '')
            fcm_regid = request.POST.get('fcm_regid', '')

            driver_id = request.POST.get('driver_id', '')
            if driver_id:
                password = ''
            else:
                password = make_password("taxi123")
                driver_id = 0

            payload = {'operator_id':operator_id,'driver_name':driver_name,'driver_contact':driver_contact,'driver_email':driver_email,'licence_no':licence_no,
                          'fcm_regid':fcm_regid,'password':password,'driver_id':driver_id,'user_id':user_id,'login_type':login_type}

            url = ""

            if driver_id:
                url = settings.API_BASE_URL + "update_operator_driver"
            else:
                url = settings.API_BASE_URL + "add_operator_driver"

            op_drivers = getDataFromAPI(login_type, access_token, url, payload)

            if op_drivers['success'] == 1:
                return HttpResponseRedirect("/agents/operator-drivers", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/operator-drivers", {'message': "Operation Fails"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            if id:
                if 'login_type' in request.session:
                    login_type = request.session['login_type']
                    access_token = request.session['access_token']
                    payload = {'driver_id': id}
                    url = settings.API_BASE_URL + "view_operator_driver"
                    op_drivers = getDataFromAPI(login_type, access_token, url, payload)
                    op_drivers = op_drivers['Drivers']

                    url = settings.API_BASE_URL + "operators"
                    operators = getDataFromAPI(login_type, access_token, url, payload)
                    operators = operators['Operators']

                    return render(request, 'Agent/add_operator_driver.html', {'operator_drivers': op_drivers,'operators':operators})
                else:
                    return HttpResponseRedirect("/agents/login")
            else:
                if 'login_type' in request.session:
                    login_type = request.session['login_type']
                    access_token = request.session['access_token']

                    payload = {'operator_id': id}
                    url = settings.API_BASE_URL + "operators"
                    operators = getDataFromAPI(login_type, access_token, url, payload)
                    operators = operators['Operators']

                    return render(request, 'Agent/add_operator_driver.html', {'operators':operators})
                else:
                    return HttpResponseRedirect("/agents/login")
        else:
            return HttpResponseRedirect("/agents/login")


def delete_operator_driver(request,id):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        driver_id = request.POST.get('driver_id', '')
        user_id = request.POST.get('user_id', '')

        url = settings.API_BASE_URL+"delete_operator_driver"
        payload = {'driver_id': driver_id,'user_id':user_id,'user_type':login_type}
        operators = getDataFromAPI(login_type, access_token, url, payload)

        if operators['success'] == 1:
            return HttpResponseRedirect("/agents/operator-drivers", {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/agents/operator-drivers", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/agents/login")


def taxi_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "agent_taxi_bookings"
        payload = {'booking_type': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/taxi_bookings.html",{'bookings': booking})
        else:
            return render(request, "Agent/taxi_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def view_taxi_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_taxi_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/view_taxi_booking.html",{'bookings': booking})
        else:
            return render(request, "Agent/view_taxi_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def add_taxi_booking(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('user_id', '')

            corporate_id = request.POST.get('corporate_id', '')
            entity_id = request.POST.get('entity_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            spoc_details = [x.strip() for x in spoc_id.split(',')]

            spoc_id = spoc_details[0]
            group_id = spoc_details[1]
            subgroup_id = spoc_details[2]

            tour_type = request.POST.get('tour_type', '')
            pickup_city = request.POST.get('pickup_city', '')
            pickup_location = request.POST.get('pickup_location', '')
            drop_location = request.POST.get('drop_location', '')
            pickup_datetime = request.POST.get('pickup_datetime', '')
            taxi_type = request.POST.get('taxi_type', '')
            package_id = request.POST.get('package_id', '')
            no_of_days = request.POST.get('no_of_days', '')

            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            pickup_details = [x.strip() for x in pickup_city.split(',')]
            city_data = {'login_type': login_type, 'access_token': access_token, 'city_country': pickup_details[2]}

            url_add_city = settings.API_BASE_URL + "add_city_name"
            url_add_state = settings.API_BASE_URL + "add_state_name"
            url_add_country = settings.API_BASE_URL + "add_country_name"

            country_id = getDataFromAPI(login_type, access_token, url_add_country, city_data)
            for conty_id in country_id['id']:
                actual_country_id = conty_id['id']

            city_data = {'login_type': login_type, 'access_token': access_token, 'city_state': pickup_details[1], 'country_id': actual_country_id}
            state_id = getDataFromAPI(login_type, access_token, url_add_state, city_data)

            for conty_id in state_id['id']:
                actual_state_id = conty_id['id']

            city_data = {'login_type': login_type, 'access_token': access_token, 'city_name': pickup_details[0],
                         'state_id': actual_state_id}
            city_id = getDataFromAPI(login_type, access_token, url_add_city, city_data)

            for conty_id in city_id['id']:
                actual_city_id = conty_id['id']

            payload = {'login_type':login_type,'user_id':user_id,'access_token':access_token,'entity_id':entity_id,'corporate_id': corporate_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'tour_type':tour_type,'pickup_city':actual_city_id,
                       'pickup_location':pickup_location,'drop_location':drop_location,'pickup_datetime':pickup_datetime,'taxi_type':taxi_type,
                       'package_id':package_id,'no_of_days':no_of_days,'reason_booking':reason_booking,'no_of_seats':no_of_seats,'employees':employees}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "add_taxi_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)

            if booking['success'] == 1:
                return HttpResponseRedirect("/agents/taxi-bookings/1", {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "companies"
            payload = {'some': 'data'}
            company = getDataFromAPI(login_type, access_token, url, payload)
            companies = company['Corporates']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            url_taxi = settings.API_BASE_URL + "taxi_types"
            taxies = getDataFromAPI(login_type, access_token, url_taxi, payload)
            taxies = taxies['taxi_types']

            if id:
                return render(request, 'Agent/add_taxi_booking.html', {'companies':companies,'cities':cities,'taxies':taxies})
            else:
                return render(request, 'Agent/add_taxi_booking.html', {'companies':companies,'cities':cities,'taxies':taxies})
        else:
            return HttpResponseRedirect("/agents/login")


def accept_taxi_booking(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        booking_id = request.POST.get('booking_id', '')
        user_id = request.POST.get('user_id', '')
        accept_id = request.POST.get('accept_id', '')
        reject_id = request.POST.get('reject_id', '')

        url = ""
        if accept_id:
            url = settings.API_BASE_URL + "accept_taxi_booking"

        if reject_id:
            url = settings.API_BASE_URL + "reject_taxi_booking"

        payload = {'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            return HttpResponseRedirect("/agents/taxi-bookings/1", {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/agents/taxi-bookings/1", {'message': "Operation Fails"})
    else:
        return HttpResponseRedirect("/agents/login")


def assign_taxi_booking(request,id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')

            vendor_booking_id = request.POST.get('vendor_booking_id', '')
            operator_id = request.POST.get('operator_id', '')
            driver_id = request.POST.get('driver_id', '')
            taxi_id= request.POST.get('taxi_id', '')

            is_client_sms = request.POST.get('is_client_sms', '')
            is_client_email = request.POST.get('is_client_email', '')
            is_driver_sms = request.POST.get('is_driver_sms', '')

            url = settings.API_BASE_URL + "assign_taxi_booking"
            payload = {'vendor_booking_id':vendor_booking_id,'operator_id':operator_id,'driver_id':driver_id,'taxi_id':taxi_id,'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/taxi-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/taxi-bookings/1", {'message': "Operation Fails"})
        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            payload = {'booking_id': id}
            opr_url = settings.API_BASE_URL + "operators"
            operators = getDataFromAPI(login_type, access_token, opr_url, payload)
            operators = operators['Operators']

            drivers_url = settings.API_BASE_URL + "operator_drivers"
            operator_drivers = getDataFromAPI(login_type, access_token, drivers_url, payload)
            operator_drivers = operator_drivers['Drivers']

            url_taxi = settings.API_BASE_URL + "taxi_models"
            taxis = getDataFromAPI(login_type, access_token, url_taxi, payload)
            models = taxis['Models']

            url_taxi_types = settings.API_BASE_URL + "taxi_types"
            url_taxi_types = getDataFromAPI(login_type, access_token, url_taxi_types, payload)
            taxi_types = url_taxi_types['taxi_types']

            url_taxis = settings.API_BASE_URL + "taxis"
            url_taxis = getDataFromAPI(login_type, access_token, url_taxis, payload)
            taxis = url_taxis['Taxis']

            url = settings.API_BASE_URL + "view_taxi_booking"
            payload = {'booking_id': id}
            booking = getDataFromAPI(login_type, access_token, url, payload)
            booking = booking['Bookings']

            return render(request, 'Agent/assign_taxi_booking.html',
                          {'bookings': booking, 'operators': operators, 'operator_drivers': operator_drivers,
                           'models': models,'taxi_types':taxi_types,'taxis':taxis})

    else:
        return HttpResponseRedirect("/agents/login")

############################## BUS  ######################################

def bus_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "agent_bus_bookings"
        payload = {'booking_type': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/bus_bookings.html",{'bookings': booking})
        else:
            return render(request, "Agent/bus_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def view_bus_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_bus_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/view_bus_booking.html",{'bookings': booking})
        else:
            return render(request, "Agent/view_bus_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def add_bus_booking(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('user_id', '')

            corporate_id = request.POST.get('corporate_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            spoc_details = [x.strip() for x in spoc_id.split(',')]

            spoc_id = spoc_details[0]
            group_id = spoc_details[1]
            subgroup_id = spoc_details[2]

            from_location = request.POST.get('from', '')
            to_location = request.POST.get('to', '')
            bus_type = request.POST.get('bus_type', '')
            booking_datetime = request.POST.get('booking_datetime', '')
            journey_datetime = request.POST.get('journey_datetime', '')
            entity_id = request.POST.get('entity_id', '')
            preferred_bus = request.POST.get('preferred_bus', '')

            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            payload = {'login_type':login_type,'user_id':user_id,'access_token':access_token,'corporate_id': corporate_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'from':from_location,'to':to_location,'bus_type':bus_type,'booking_datetime':booking_datetime,
            'journey_datetime':journey_datetime,'entity_id':entity_id,'reason_booking':reason_booking,'no_of_seats':no_of_seats,'preferred_bus':preferred_bus,'employees':employees}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "add_bus_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)
            print(booking)
            if booking['success'] == 1:
                return HttpResponseRedirect("/agents/bus-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/bus-bookings/1", {'message': "Operation Fails"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "companies"
            payload = {'some': 'data'}
            company = getDataFromAPI(login_type, access_token, url, payload)
            companies = company['Corporates']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            if id:
                return render(request, 'Agent/add_bus_booking.html', {'companies':companies,'cities':cities})
            else:
                return render(request, 'Agent/add_bus_booking.html', {'companies':companies,'cities':cities})
        else:
            return HttpResponseRedirect("/agents/login")


def accept_bus_booking(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        if request.method == 'POST':
            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')
            accept_id = request.POST.get('accept_id', '')
            reject_id = request.POST.get('reject_id', '')

            print(accept_id)
            print(reject_id)

            url = ""
            if accept_id == '1':
                url = settings.API_BASE_URL + "accept_bus_booking"
                print("in accept")

            if reject_id == '1':
                url = settings.API_BASE_URL + "reject_bus_booking"
                print('In reject')

            payload = {'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/bus-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/bus-bookings/1", {'message': "Operation Fails"})
        else:
            return render(request, "Agent/bus_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def assign_bus_booking(request,id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')

            ticket_no = request.POST.get('ticket_no', '')
            pnr_no = request.POST.get('pnr_no', '')
            assign_bus_type_id = request.POST.get('assign_bus_type_id', '')
            seat_no= request.POST.get('seat_no', '')
            portal_used = request.POST.get('portal_used', '')
            operator_name = request.POST.get('operator_name', '')
            operator_contact = request.POST.get('operator_contact', '')
            boarding_point = request.POST.get('boarding_point', '')
            boarding_datetime = request.POST.get('boarding_datetime', '')
            boarding_datetime = datetime.strptime(boarding_datetime, '%d/%m/%Y %H:%M:%S')

            is_client_sms = request.POST.get('is_client_sms', '')
            is_client_email = request.POST.get('is_client_email', '')
            is_driver_sms = request.POST.get('is_driver_sms', '')

            url = settings.API_BASE_URL + "assign_bus_booking"
            payload = {'ticket_no':ticket_no,'pnr_no':pnr_no,'assign_bus_type_id':assign_bus_type_id,'seat_no':seat_no,'portal_used':portal_used
                ,'operator_name':operator_name,'operator_contact':operator_contact,'boarding_point':boarding_point,'boarding_datetime':boarding_datetime,
                       'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/bus-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/bus-bookings/1", {'message': "Operation Fails"})
        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            payload = {'booking_id': id}

            url = settings.API_BASE_URL + "view_bus_booking"
            payload = {'booking_id': id}
            booking = getDataFromAPI(login_type, access_token, url, payload)
            booking = booking['Bookings']

            return render(request, 'Agent/assign_bus_booking.html',
                          {'bookings': booking,})

    else:
        return HttpResponseRedirect("/agents/login")


############################## TRAIN  ######################################

def train_bookings(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "agent_train_bookings"
        payload = {'booking_type': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/train_bookings.html",{'bookings': booking})
        else:
            return render(request, "Agent/train_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def view_train_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_train_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/view_train_booking.html",{'bookings': booking})
        else:
            return render(request, "Agent/view_train_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def add_train_booking(request,id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('user_id', '')

            corporate_id = request.POST.get('corporate_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            spoc_details = [x.strip() for x in spoc_id.split(',')]

            spoc_id = spoc_details[0]
            group_id = spoc_details[1]
            subgroup_id = spoc_details[2]

            from_location = request.POST.get('from', '')
            to_location = request.POST.get('to', '')
            train_type = request.POST.get('train_type', '')
            booking_datetime = request.POST.get('booking_datetime', '')
            journey_datetime = request.POST.get('journey_datetime', '')
            entity_id = request.POST.get('entity_id', '')
            preferred_train = request.POST.get('preferred_train', '')

            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            payload = {'login_type':login_type,'user_id':user_id,'access_token':access_token,'corporate_id': corporate_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'from':from_location,'to':to_location,'train_type':train_type,'booking_datetime':booking_datetime,
            'journey_datetime':journey_datetime,'entity_id':entity_id,'reason_booking':reason_booking,'no_of_seats':no_of_seats,'preferred_train':preferred_train,'employees':employees}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "add_train_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)
            print(booking)
            if booking['success'] == 1:
                return HttpResponseRedirect("/agents/train-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/train-bookings/1", {'message': "Operation Fails"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "companies"
            payload = {'some': 'data'}
            company = getDataFromAPI(login_type, access_token, url, payload)
            companies = company['Corporates']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            url_train = settings.API_BASE_URL + "train_types"
            trains = getDataFromAPI(login_type, access_token, url_train, payload)
            types = trains['Types']

            if id:
                return render(request, 'Agent/add_train_booking.html', {'companies':companies,'cities':cities,'types':types})
            else:
                return render(request, 'Agent/add_train_booking.html', {'companies':companies,'cities':cities,'types':types})
        else:
            return HttpResponseRedirect("/agents/login")


def accept_train_booking(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        if request.method == 'POST':
            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')
            accept_id = request.POST.get('accept_id', '')
            reject_id = request.POST.get('reject_id', '')

            url = ""
            if accept_id == '1':
                url = settings.API_BASE_URL + "accept_train_booking"

            if reject_id == '1':
                url = settings.API_BASE_URL + "reject_train_booking"

            payload = {'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/train-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/train-bookings/1", {'message': "Operation Fails"})
        else:
            return render(request, "Agent/train_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def assign_train_booking(request,id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')

            ticket_no = request.POST.get('ticket_no', '')
            pnr_no = request.POST.get('pnr_no', '')
            assign_bus_type_id = request.POST.get('assign_bus_type_id', '')
            seat_no= request.POST.get('seat_no', '')
            portal_used = request.POST.get('portal_used', '')
            operator_name = request.POST.get('operator_name', '')
            operator_contact = request.POST.get('operator_contact', '')
            boarding_point = request.POST.get('boarding_point', '')
            boarding_datetime = request.POST.get('boarding_datetime', '')
            boarding_datetime = datetime.strptime(boarding_datetime, '%d/%m/%Y %H:%M:%S')

            is_client_sms = request.POST.get('is_client_sms', '')
            is_client_email = request.POST.get('is_client_email', '')
            is_driver_sms = request.POST.get('is_driver_sms', '')

            url = settings.API_BASE_URL + "assign_train_booking"
            payload = {'ticket_no':ticket_no,'pnr_no':pnr_no,'assign_bus_type_id':assign_bus_type_id,'seat_no':seat_no,'portal_used':portal_used
                ,'operator_name':operator_name,'operator_contact':operator_contact,'boarding_point':boarding_point,'boarding_datetime':boarding_datetime,
                       'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/train-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/train-bookings/1", {'message': "Operation Fails"})
        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            payload = {'booking_id': id}

            url = settings.API_BASE_URL + "view_train_booking"
            payload = {'booking_id': id}
            booking = getDataFromAPI(login_type, access_token, url, payload)
            booking = booking['Bookings']

            url_train = settings.API_BASE_URL + "train_types"
            trains = getDataFromAPI(login_type, access_token, url_train, payload)
            types = trains['Types']

            return render(request, 'Agent/assign_train_booking.html',
                          {'bookings': booking,'types':types})

    else:
        return HttpResponseRedirect("/agents/login")

############################## HOTELS  ######################################


def add_hotel_booking(request, id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            user_id = request.POST.get('user_id', '')
            corporate_id = request.POST.get('corporate_id', '')
            # spoc_id = request.POST.get('spoc_id', '')

            spoc_id = request.POST.get('spoc_id', '')
            spoc_details = [x.strip() for x in spoc_id.split(',')]

            spoc_id = spoc_details[0]
            group_id = spoc_details[1]
            subgroup_id = spoc_details[2]

            corporate_id = request.POST.get('corporate_id')
            booking_email_copy = request.POST.get('booking_email_copy')
            from_city = request.POST.get('from_city')
            city_area = request.POST.get('city_area')
            preferred_hotel_area = request.POST.get('preferred_hotel_area')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            room_type_priority1 = request.POST.get('room_type_priority1')
            room_type_priority2 = request.POST.get('room_type_priority2')
            room_occupancy = request.POST.get('room_occupancy')
            preferred_hotel = request.POST.get('preferred_hotel')
            booking_date = request.POST.get('booking_datetime')

            assessment_code = request.POST.get('assessment_code')

            assessment_city = request.POST.get('assessment_city')
            billing_entity = request.POST.get('billing_entity')
            reason_for_booking = request.POST.get('reason_for_booking')
            send_sms = request.POST.get('send_sms')
            send_email = request.POST.get('send_email')
            no_of_seats = request.POST.get('no_of_seats')

            # post variables end

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1, no_of_emp):
                employees.append(request.POST.get('employee_id_' + str(i), ''))
                print(employees)

            payload = {'login_type': login_type, 'user_id': user_id, 'access_token': access_token,
                       'corporate_id': corporate_id, 'spoc_id': spoc_id, 'group_id': group_id,
                       'subgroup_id': subgroup_id, 'from_city_id': from_city, 'from_area_id': city_area,
                       'preferred_area': preferred_hotel_area, 'checkin_datetime': check_in_date,
                       'checkout_datetime': check_out_date, 'bucket_priority_1': room_type_priority1,
                       'bucket_priority_2': room_type_priority2, 'room_type_id': room_occupancy,
                       'preferred_hotel': preferred_hotel, 'booking_datetime': booking_date,
                       'assessment_code': assessment_code, 'assessment_city_id': assessment_city,
                       'billing_entity_id': billing_entity, 'employees': employees,'reason_booking':reason_for_booking,'no_of_seats':no_of_seats}

            print(payload)
            url_taxi_booking = settings.API_BASE_URL + "add_hotel_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)
            if booking['success'] == 1:
                 return HttpResponseRedirect("/agents/hotel-bookings/1", {'message': "Operation Successfully"})
            else:
                 return HttpResponseRedirect("/agents/hotel-bookings/1", {'message': "Operation Fails"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "companies"
            payload = {'some': 'data'}
            company = getDataFromAPI(login_type, access_token, url, payload)
            companies = company['Corporates']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            if id:
                return render(request, 'Agent/add_hotel_booking.html', {'companies': companies, 'cities': cities, })
            else:
                return render(request, 'Agent/add_hotel_booking.html', {'companies': companies, 'cities': cities, })
        else:
            return HttpResponseRedirect("/agents/login")


def hotel_bookings(request, id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "agent_hotel_bookings"
        payload = {'booking_type': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/hotel_bookings.html", {'bookings': booking})
        else:
            return render(request, "Agent/hotel_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def view_hotel_booking(request,id):
    request = get_request()

    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_hotel_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/view_hotel_booking.html",{'bookings': booking})
        else:
            return render(request, "Agent/view_hotel_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def accept_hotel_booking(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        if request.method == 'POST':
            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')
            accept_id = request.POST.get('accept_id', '')
            reject_id = request.POST.get('reject_id', '')

            url = ""
            if accept_id == '1':
                url = settings.API_BASE_URL + "accept_hotel_booking"

            if reject_id == '1':
                url = settings.API_BASE_URL + "reject_hotel_booking"

            payload = {'booking_id': booking_id, 'user_id': user_id, 'user_type': login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/hotel-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/hotel-bookings/1", {'message': "Operation Fails"})
        else:
            return render(request, "Agent/hotel_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def assign_hotel_booking(request, id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            assign_hotel_id = request.POST.get('assign_hotel_id', '')

            assign_room_type = request.POST.get('room_type', '')
            is_ac_room = request.POST.get('is_ac_room', '')
            daily_brakefast = request.POST.get('daily_brakefast', '')
            is_prepaid = request.POST.get('is_prepaid', '')
            agent_booking_id = request.POST.get('agent_booking_id', '')
            comment = request.POST.get('comment', '')

            total_room_price = request.POST.get('total_room_price', '')
            voucher_number = request.POST.get('voucher_number', '')
            portal_used = request.POST.get('portal_used', '')
            commission_earned = request.POST.get('commission_earned', '')



            user_id = request.POST.get('user_id')
            booking_id = request.POST.get('booking_id')

            url = settings.API_BASE_URL + "assign_hotel_booking"

            payload = {'assign_hotel_id': assign_hotel_id,'assign_room_type':assign_room_type,'is_ac_room':is_ac_room,'daily_brakefast':daily_brakefast,
            'is_prepaid':is_prepaid,'agent_booking_id':agent_booking_id,'comment':comment,'user_id':user_id,'user_type': login_type,'total_room_price':total_room_price,
            'voucher_number':voucher_number,'portal_used':portal_used,'commission_earned':commission_earned,'booking_id':booking_id}

            company = getDataFromAPI(login_type, access_token, url, payload)

            print(company)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/hotel-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/hotel-bookings/1", {'message': "Operation Fails"})
        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            payload = {'booking_id': id}

            url = settings.API_BASE_URL + "view_hotel_booking"
            payload = {'booking_id': id}
            booking = getDataFromAPI(login_type, access_token, url, payload)
            booking = booking['Bookings']

            url_hotels = settings.API_BASE_URL + "operators"
            payload = {'booking_id': id}
            hotels = getDataFromAPI(login_type, access_token, url_hotels, payload)
            hotels = hotels['Operators']

            url_room_types = settings.API_BASE_URL + "hotel_types"
            payload = {'booking_id': id}
            room_types = getDataFromAPI(login_type, access_token, url_room_types, payload)
            room_types = room_types['Types']

            url_room_types = settings.API_BASE_URL + "hotel_booking_portals"
            payload = {'booking_id': id}
            portals = getDataFromAPI(login_type, access_token, url_room_types, payload)
            portals = portals['Portals']

            return render(request, 'Agent/assign_hotel_booking.html',{'bookings': booking, 'hotels': hotels,'portals':portals,'room_types':room_types})

    else:
        return HttpResponseRedirect("/agents/login")


############################## FLIGHT  ######################################

def flight_bookings(request,id):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "agent_flight_bookings"
        payload = {'booking_type': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/flight_bookings.html",{'bookings': booking})
        else:
            return render(request, "Agent/flight_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def view_flight_booking(request,id):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        url = settings.API_BASE_URL + "view_flight_booking"
        payload = {'booking_id': id}
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            booking = company['Bookings']
            return render(request, "Agent/view_flight_booking.html",{'bookings': booking})
        else:
            return render(request, "Agent/view_flight_booking.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")


def add_flight_booking(request, id):
    if request.method == 'POST':
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            user_id = request.POST.get('user_id', '')

            corporate_id = request.POST.get('corporate_id', '')
            entity_id = request.POST.get('entity_id', '')
            spoc_id = request.POST.get('spoc_id', '')
            spoc_details = [x.strip() for x in spoc_id.split(',')]

            spoc_id = spoc_details[0]
            group_id = spoc_details[1]
            subgroup_id = spoc_details[2]

            usage_type = request.POST.get('usage_type', '')
            trip_type = request.POST.get('trip_type', '')
            seat_type = request.POST.get('seat_type', '')
            from_city = request.POST.get('from_city', '')
            to_city = request.POST.get('to_city', '')
            booking_datetime = request.POST.get('booking_datetime', '')
            departure_date = request.POST.get('departure_date', '')
            preferred_flight = request.POST.get('preferred_flight', '')
            assessment_code = request.POST.get('assessment_code', '')
            billing_entity_id = request.POST.get('billing_entity_id', '')
            reason_booking = request.POST.get('reason_booking', '')
            no_of_seats = request.POST.get('no_of_seats', '')

            employees = []
            no_of_emp = int(no_of_seats) + 1
            for i in range(1,no_of_emp):
                employees.append(request.POST.get('employee_id_'+str(i), ''))
                print(employees)

            payload = {'user_id':user_id,'user_type':login_type,'corporate_id':corporate_id,'entity_id':entity_id,'spoc_id':spoc_id,'group_id':group_id,
                       'subgroup_id':subgroup_id,'usage_type':usage_type,'trip_type':trip_type,'seat_type':seat_type,'from_city':from_city,'to_city':to_city,
                       'booking_datetime':booking_datetime,'departure_date':departure_date,'preferred_flight':preferred_flight,'assessment_code':assessment_code,
                       'reason_booking':reason_booking,'no_of_seats':no_of_seats,'employees':employees,'billing_entity_id':billing_entity_id}
            print(payload)

            url_taxi_booking = settings.API_BASE_URL + "add_flight_booking"
            booking = getDataFromAPI(login_type, access_token, url_taxi_booking, payload)

            if booking['success'] == 1:
                return HttpResponseRedirect("/agents/flight-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/flight-bookings/1", {'message': "Operation Successfully"})
        else:
            return HttpResponseRedirect("/agents/login")

    else:
        request = get_request()
        if 'login_type' in request.session:
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            url = settings.API_BASE_URL + "companies"
            payload = {'some': 'data'}
            company = getDataFromAPI(login_type, access_token, url, payload)
            companies = company['Corporates']

            url_city = settings.API_BASE_URL + "cities"
            cities = getDataFromAPI(login_type, access_token, url_city, payload)
            cities = cities['Cities']

            if id:
                return render(request, 'Agent/add_flight_booking.html', {'companies':companies,'cities':cities,})
            else:
                return render(request, 'Agent/add_flight_booking.html', {'companies':companies,'cities':cities,})
        else:
            return HttpResponseRedirect("/agents/login")


def assign_flight_booking(request,id):
    if 'login_type' in request.session:
        if request.method == 'POST':
            login_type = request.session['login_type']
            access_token = request.session['access_token']

            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')
            no_of_passanger = request.POST.get('no_of_passanger', '')

            meal_is_include = request.POST.get('meal_is_include', '')
            fare_type = request.POST.get('fare_type', '')
            trip_type = request.POST.get('trip_type', '')
            flight_type = request.POST.get('flight_type', '')
            seat_type = request.POST.get('seat_type', '')
            no_of_stops = request.POST.get('no_of_stops', '')

            ticket_number = request.POST.getlist('ticket_number', '')
            employee_booking_id = request.POST.getlist('employee_booking_id', '')

            flight_from = request.POST.getlist('from', '')
            flight_to = request.POST.getlist('to', '')
            departure_time = request.POST.getlist('departure_time', '')
            arrival_time = request.POST.getlist('arival_time', '')
            flight_name = request.POST.getlist('flight_name', '')
            flight_no = request.POST.getlist('flight_no', '')
            pnr_no = request.POST.getlist('pnr_number', '')

            portal_used = request.POST.get('portal_used', '')

            is_client_sms = request.POST.get('is_client_sms', '')
            is_client_email = request.POST.get('is_client_email', '')
            is_driver_sms = request.POST.get('is_driver_sms', '')

            url = settings.API_BASE_URL + "assign_flight_booking"
            payload = {'ticket_no':ticket_number,'pnr_no':pnr_no,'portal_used':portal_used
                ,'booking_id': booking_id,'user_id':user_id,'user_type':login_type,'flight_no':flight_no,'flight_name':flight_name,'arrival_time':arrival_time,
                       'departure_time':departure_time,'flight_to':flight_to,'flight_from':flight_from,'no_of_stops':no_of_stops,'seat_type':seat_type,'flight_type':flight_type,
                       'trip_type':trip_type,'fare_type':fare_type,'meal_is_include':meal_is_include,'no_of_passanger':no_of_passanger,'employee_booking_id':employee_booking_id}
            print(payload)
            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/flight-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/flight-bookings/1", {'message': "Operation Fails"})
        else:
            login_type = request.session['login_type']
            access_token = request.session['access_token']
            payload = {'booking_id': id}

            url = settings.API_BASE_URL + "view_flight_booking"
            payload = {'booking_id': id}
            booking = getDataFromAPI(login_type, access_token, url, payload)
            booking = booking['Bookings']

            return render(request, 'Agent/assign_flight_booking.html',{'bookings': booking,})

    else:
        return HttpResponseRedirect("/agents/login")


def accept_flight_booking(request):
    if 'login_type' in request.session:
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        if request.method == 'POST':
            booking_id = request.POST.get('booking_id', '')
            user_id = request.POST.get('user_id', '')
            accept_id = request.POST.get('accept_id', '')
            reject_id = request.POST.get('reject_id', '')

            url = ""
            if accept_id == '1':
                url = settings.API_BASE_URL + "accept_flight_booking"

            if reject_id == '1':
                url = settings.API_BASE_URL + "reject_flight_booking"

            payload = {'booking_id': booking_id,'user_id':user_id,'user_type':login_type}

            company = getDataFromAPI(login_type, access_token, url, payload)

            if company['success'] == 1:
                return HttpResponseRedirect("/agents/flight-bookings/1", {'message': "Operation Successfully"})
            else:
                return HttpResponseRedirect("/agents/flight-bookings/1", {'message': "Operation Fails"})
        else:
            return render(request, "Agent/train_bookings.html", {'': {}})
    else:
        return HttpResponseRedirect("/agents/login")
























def getDataFromAPI(login_type, access_token, url, payload):
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