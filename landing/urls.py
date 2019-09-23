
from django.urls import path
from . import views


urlpatterns = [

path('',views.index, name="index"),

path('about',views.about, name="about"),

path('cotrav/login',views.login, name="login"),

path('signup',views.signup, name="signup"),

path('contact',views.contact, name="contact"),

path('support',views.support, name="support"),


    ]

