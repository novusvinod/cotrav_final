from django.conf import settings
from django.shortcuts import render, redirect
import requests
import json
from django_global_request.middleware import get_request
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def homepage(request):
    return render(request, 'Company/Spoc/home_page.html', {'user': request.user})


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
        return render(request, "Company/Spoc/company_admins.html", {'admins': admins})
    else:
        return render(request, "Company/Spoc/company_admins.html", {'admins': {}})


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
        return render(request, "Company/Spoc/billing_entities.html",
                      {'billing_entities': entities, "cities": cities, })
    else:
        return render(request, "Company/Spoc/billing_entities.html", {'entities': {}})


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
        return render(request, "Company/Spoc/company_rates.html", {'corporate_rates': company_rates})
    else:
        return render(request, "Company/Spoc/company_rates.html", {'entities': {}})


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
        return render(request, "Company/Spoc/groups.html", {'groups': groups})
    else:
        return render(request, "Company/Spoc/groups.html", {'groups': {}})


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
        return render(request, "Company/Spoc/subgroups.html", {'subgroups': subgroups, 'groups': groups})
    else:
        return render(request, "Company/Spoc/subgroups.html", {'subgroups': {}})


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
        return render(request, "Company/Spoc/spocs.html", {'spocs': spocs})
    else:
        return render(request, "Company/Spoc/spocs.html", {'spocs': {}})


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
        return render(request, "Company/Spoc/employees.html", {'employees': employees})
    else:
        return render(request, "Company/Spoc/employees.html", {'employees': {}})


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
        return render(request, "Company/Spoc/view_groups.html", {'group': groups, 'grp_auths': grp_auths})
    else:
        return render(request, "Company/Spoc/view_groups.html", {'group': {}})


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
        return render(request, "Company/Spoc/view_subgroups.html",
                      {'subgroup': subgroups, 'subgrp_auths': subgrp_auths})
    else:
        return render(request, "Company/Spoc/view_subgroups.html", {'group': {}})


def add_taxi_booking(request,id):
    if request.method == 'POST':
        pass
    else:
        request = get_request()
        login_type = request.session['login_type']
        access_token = request.session['access_token']
        headers = {'Authorization': 'Token ' + access_token, 'usertype': login_type}

        url_emp = settings.API_BASE_URL + "employees"
        payload = {'corporate_id': id}
        r = requests.post(url_emp, data=payload, headers=headers)
        company_emp = json.loads(r.text)
        employees = company_emp['Employees']

        if id:
            return render(request, 'Company/Spoc/add-taxi-booking.html', {'employees':employees})
        else:
            return render(request, 'Company/Spoc/add-taxi-booking.html', {})


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
