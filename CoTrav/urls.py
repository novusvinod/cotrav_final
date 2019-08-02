"""CoTrav URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Common.VIEW import basic_web_views



urlpatterns = [
    path('admin/', admin.site.urls),


######################### Comman urls ################
    path('login', basic_web_views.login_action),
    path('logout', basic_web_views.logout_action),
######################### END Commann urls ###############


######################### CORPORATE ADMIN URLS ############################
    path('', include('Common.URL.Admin.urls')),
    path('', include('Common.URL.Spoc.urls')),
    path('', include('Common.URL.Approves_1.urls')),
    path('', include('Common.URL.Approves_2.urls')),
######################### END CORPORATE URLS ####################


######################### AGENTS URLS ############################
    path('', include('Common.URL.Agent.urls')),
######################### END AGENTS URLS ################


######################### API URLS ############################
    path('', include('Common.URL.Api.urls')),
######################### END API URLS ####################







]
