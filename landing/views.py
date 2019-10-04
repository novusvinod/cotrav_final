from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):

    return render(request,'cotrav_index.html')

def about(request):

    return render(request,'cotrav_about.html')

def login(request):

    return render(request,'cotrav_login.html')

def signup(request):

    return render(request,'cotrav_signup.html')

def contact(request):

    return render(request,'cotrav_contact.html')

def support(request):

    return render(request,'cotrav_support.html')

def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, 'error_404.html', data)