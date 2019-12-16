
from django.urls import path
from . import views


urlpatterns = [

path('',views.index_cs, name="index_cs"),

path('index',views.index, name="index"),

path('about',views.about, name="about"),

path('cotrav/login',views.login, name="login"),

path('signup',views.signup, name="signup"),

path('contact',views.contact, name="contact"),

path('support',views.support, name="support"),

path('testsignup',views.testsignup, name="testsignup"),

path('testemail',views.testsignup, name="testsignup"),

path('voucher',views.voucher, name="voucher"),

path('export',views.export_movies_to_xlsx, name="export"),

path('create_token',views.Create_Token, name="create_token"),




    ]