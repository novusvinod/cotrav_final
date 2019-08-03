from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import requests
import json
from django_global_request.middleware import get_request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


@login_required(login_url='/login')
def homepage(request):
    return render(request, 'Company/Admin/home_page.html', {'user': request.user})


@login_required(login_url='/login')
def company_admins(request, id):
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
        return render(request, "Company/Admin/company_admins.html", {'admins': admins})
    else:
        return render(request, "Company/Admin/company_admins.html", {'admins': {}})


@login_required(login_url='/login')
def company_billing_entities(request, id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "billing_entities"
    payload = {'corporate_id': id}

    company = getDataFromAPI(login_type, access_token, url, payload)
    url_city = settings.API_BASE_URL + "cities"
    cities = getDataFromAPI(login_type, access_token, url_city, payload)

    if company['success'] == 1:
        entities = company['Entitys']
        cities = cities["Cities"]
        return render(request, "Company/Admin/billing_entities.html",
                      {'billing_entities': entities, "cities": cities, })
    else:
        return render(request, "Company/Admin/billing_entities.html", {'entities': {}})


@login_required(login_url='/login')
def company_rates(request, id):
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
        return render(request, "Company/Admin/company_rates.html", {'corporate_rates': company_rates})
    else:
        return render(request, "Company/Admin/company_rates.html", {'entities': {}})


@login_required(login_url='/login')
def company_groups(request, id):
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
        return render(request, "Company/Admin/groups.html", {'groups': groups})
    else:
        return render(request, "Company/Admin/groups.html", {'groups': {}})


@login_required(login_url='/login')
def company_subgroups(request, id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']
    url = settings.API_BASE_URL + "subgroups"
    payload = {'corporate_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)
    if company['success'] == 1:
        url2 = settings.API_BASE_URL + "groups"
        subgroups = company['Subgroups']
        r = requests.post(url2, data=payload, headers=headers)
        gr = json.loads(r.text)
        groups = gr['Groups']
        return render(request, "Company/Admin/subgroups.html", {'subgroups': subgroups, 'groups': groups})
    else:
        return render(request, "Company/Admin/subgroups.html", {'subgroups': {}})


@login_required(login_url='/login')
def company_spocs(request, id):
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
        return render(request, "Company/Admin/spocs.html", {'spocs': spocs})
    else:
        return render(request, "Company/Admin/spocs.html", {'spocs': {}})


@login_required(login_url='/login')
def company_employees(request, id):
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
        return render(request, "Company/Admin/employees.html", {'employees': employees})
    else:
        return render(request, "Company/Admin/employees.html", {'employees': {}})


@login_required(login_url='/login')
def add_company_rate(request, id):
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
            return render(request, "Company/Admin/company_rates.html", {'corporate_rates': company_rates})
        else:
            return render(request, "Company/Admin/company_rates.html", {'entities': {}})
    else:
        return render(request, "Company/Admin/company_rate_add.html", {'entities': {}})
        pass


@login_required(login_url='/login')
def add_company_entity(request, id):
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

        payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                   'access_token': access_token,
                   'entity_name': entity_name, 'billing_city_id': billing_city_id,
                   'contact_person_name': contact_person_name, 'contact_person_email': contact_person_email,
                   'contact_person_no': contact_person_no, 'address_line_1': address_line_1,
                   'address_line_2': address_line_2,
                   'address_line_3': address_line_3, 'gst_id': gst_id, 'pan_no': pan_no, 'entity_id': entity_id,
                   'is_delete': delete_id, }

        url = settings.API_BASE_URL + "add_billing_entity"
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            return HttpResponseRedirect("/Corporate/Admin/company-billing_entities/" + corporate_id,
                                        {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/company-billing_entities/" + corporate_id,
                                        {'message': "Record Not Added"})


@login_required(login_url='/login')
def add_company_group(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = id
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        group_name = request.POST.get('group_name', '')
        zone_name = request.POST.get('zone_name')

        payload = {'corporate_id': corporate_id, 'user_id': user_id, 'login_type': login_type,
                   'access_token': access_token, 'group_name': group_name, 'zone_name': zone_name}

        print(payload)
        url = settings.API_BASE_URL + "add_group"
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            return HttpResponseRedirect("/Corporate/Admin/company-groups/" + str(id), {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/company-groups/" + str(id), {'message': "Record Not Added"})


@login_required(login_url='/login')
def add_company_subgroup(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')
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
            return HttpResponseRedirect("/Corporate/Admin/company-subgroups/" + str(id), {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/company-subgroups/" + str(id), {'message': "Record Not Added"})


@login_required(login_url='/login')
def update_company_group(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        group_id = request.POST.get('group_id', '')
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
            return HttpResponseRedirect("/Corporate/Admin/view-company-group/" + group_id, {'message': "Update Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/view-company-group/" + group_id, {'message': "Record Not Updated"})


@login_required(login_url='/login')
def update_company_subgroup(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        subgroup_id = request.POST.get('subgroup_id', '')
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        group_name = request.POST.get('group_name', '')

        payload = {'subgroup_id': subgroup_id, 'access_token': access_token, 'group_name': group_name,
                   'user_id': user_id, 'login_type': login_type}

        print(payload)
        url = settings.API_BASE_URL + "update_subgroup"
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            return HttpResponseRedirect("/Corporate/Admin/view-company-subgroup/" + str(id),
                                        {'message': "Update Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/view-company-subgroup/" + str(id),
                                        {'message': "Record Not Updated"})


@login_required(login_url='/login')
def delete_company_group(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        group_id = request.POST.get('group_id')
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        access_token_auth = request.session['access_token']
        payload = {'group_id': group_id, 'user_id': user_id, 'login_type': login_type, 'access_token': access_token,
                   'access_token_auth': access_token_auth}
        url = settings.API_BASE_URL + "delete_group"
        company = getDataFromAPI(login_type, access_token, url, payload)

        if company['success'] == 1:
            return HttpResponseRedirect("/Corporate/Admin/company-groups/" + str(id), {'message': "Delete Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/company-groups/" + str(id), {'message': "Record Not Added"})


@login_required(login_url='/login')
def delete_company_subgroup(request, id):
    if request.method == 'POST':
        request = get_request()
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
            return HttpResponseRedirect("/Corporate/Admin/company-subgroups/" + str(id), {'message': "Delete Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/company-subgroups/" + str(id), {'message': "Record Not Added"})


@login_required(login_url='/login')
def add_company_group_auth(request, id):
    if request.method == 'POST':
        request = get_request()
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
        print(url)
        print(delete_id)
        if company['success'] == 1:
            return HttpResponseRedirect("/Corporate/Admin/view-company-group/" + group_id, {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/view-company-group/" + group_id, {'message': "Record Not Added"})


@login_required(login_url='/login')
def add_company_subgroup_auth(request, id):
    if request.method == 'POST':
        request = get_request()
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
            return HttpResponseRedirect("/Corporate/Admin/view-company-subgroup/" + subgroup_id,
                                        {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/view-company-subgroup/" + subgroup_id,
                                        {'message': "Record Not Added"})


@login_required(login_url='/login')
def add_company_admins(request, id):
    if request.method == 'POST':
        request = get_request()
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
            return HttpResponseRedirect("/Corporate/Admin/company-admins/" + str(id), {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/Admin/company-admins/" + str(id), {'message': "Record Not Added"})


@login_required(login_url='/login')
def add_spocs(request, id):
    if request.method == 'POST':
        request = get_request()
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
            return HttpResponseRedirect("/Corporate/Admin/company-admins/" + str(id), {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/company-spocs/" + str(id), {'message': "Record Not Added"})
    else:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}

        url_spoc = settings.API_BASE_URL + "view_spoc"
        payload = {'spoc_id': id}
        r = requests.post(url_spoc, data=payload, headers=headers)
        company_spoc = json.loads(r.text)
        spocs = company_spoc['Spoc']

        for spoc in spocs:
            corporate_id = spoc['corporate_id']

        url = settings.API_BASE_URL + "groups"
        payload = {'corporate_id': corporate_id}

        r = requests.post(url, data=payload, headers=headers)
        company = json.loads(r.text)
        groups = company['Groups']
        url_subgroup = settings.API_BASE_URL + "subgroups"
        r = requests.post(url_subgroup, data=payload, headers=headers)
        company_sub = json.loads(r.text)
        subgroups = company_sub['Subgroups']

        if id:
            return render(request, 'Company/Admin/add-spoc.html', {'groups': groups, 'subgroups': subgroups, 'spoc':spocs})
        else:
            return render(request, 'Company/Admin/add-spoc.html', {'groups': groups, 'subgroups': subgroups})


@login_required(login_url='/login')
def add_employee(request, id):
    if request.method == 'POST':
        request = get_request()
        user_id = request.POST.get('user_id', '')
        corporate_id = request.POST.get('corporate_id', '')
        login_type = request.session['login_type']
        access_token = request.session['access_token']

        spoc_id = request.POST.get('spoc_id', '')
        core_employee_id = request.POST.get('core_employee_id', '')
        employee_cid = request.POST.get('employee_cid', '')

        employee_name = request.POST.get('employee_name', '')
        employee_email = request.POST.get('employee_email', '')
        employee_contact = request.POST.get('employee_contact', '')
        age = request.POST.get('age', '')
        gender = request.POST.get('gender')
        id_proof_type = request.POST.get('id_proof_type')

        id_proof_no = request.POST.get('id_proof_no', '')
        is_active = request.POST.get('is_active', '')
        has_dummy_email = request.POST.get('has_dummy_email', '')
        fcm_regid = request.POST.get('fcm_regid', '')
        is_cxo = request.POST.get('is_cxo', '')
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
                   'delete_id': delete_id, 'password': password}

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
            return HttpResponseRedirect("/Corporate/company-employees/" + str(id), {'message': "Added Successfully"})
        else:
            return HttpResponseRedirect("/Corporate/company-employees/" + str(id), {'message': "Record Not Added"})
    else:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}

        url_emp = settings.API_BASE_URL + "view_employee"
        payload = {'employee_id': id}
        r = requests.post(url_emp, data=payload, headers=headers)
        company_emp = json.loads(r.text)
        employees = company_emp['Employee']

        url_spoc = settings.API_BASE_URL + "spocs"
        payload_spoc = {'corporate_id': request.user.corporate_id}
        r2 = requests.post(url_spoc, data=payload_spoc, headers=headers)
        company_spoc = json.loads(r2.text)
        spocs = company_spoc['Spocs']

        if id:
            return render(request, 'Company/Admin/add-employee.html', {'employee':employees,'spocs':spocs})
        else:
            return render(request, 'Company/Admin/add-employee.html', {'spocs':spocs})


@login_required(login_url='/login')
def view_company_group(request, id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']

    url = settings.API_BASE_URL + "view_group"
    payload = {'group_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)

    url = settings.API_BASE_URL + "view_group_auth"
    r = requests.post(url, data=payload, headers=headers)
    grp_auths = json.loads(r.text)
    print(grp_auths)
    if company['success'] == 1:
        groups = company['Groups']
        grp_auths = grp_auths['Groups']
        return render(request, "Company/Admin/view_groups.html", {'group': groups, 'grp_auths': grp_auths})
    else:
        return render(request, "Company/Admin/view_groups.html", {'group': {}})


@login_required(login_url='/login')
def view_company_subgroup(request, id):
    request = get_request()
    login_type = request.session['login_type']
    access_token = request.session['access_token']

    url = settings.API_BASE_URL + "view_subgroup"
    payload = {'subgroup_id': id}
    headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}
    r = requests.post(url, data=payload, headers=headers)
    company = json.loads(r.text)

    url = settings.API_BASE_URL + "view_subgroup_auth"
    r = requests.post(url, data=payload, headers=headers)
    subgrp_auths = json.loads(r.text)
    print(subgrp_auths)
    if company['success'] == 1:
        subgroups = company['SubGroups']
        subgrp_auths = subgrp_auths['SubGroups']
        return render(request, "Company/Admin/view_subgroups.html",
                      {'subgroup': subgroups, 'subgrp_auths': subgrp_auths})
    else:
        return render(request, "Company/Admin/view_subgroups.html", {'group': {}})


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
