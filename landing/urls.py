
from django.urls import path
from . import views
from . import Cotrav_InsertData_Scripts


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
path('get_flights',views.get_flights, name="get_flights"),
path('get_pnr',views.get_pnr, name="get_pnr"),


path('script/add_taxi',Cotrav_InsertData_Scripts.add_taxi),

path('script/add_bus',Cotrav_InsertData_Scripts.add_bus),

path('script/add_train',Cotrav_InsertData_Scripts.add_train),

path('script/add_flight',Cotrav_InsertData_Scripts.add_flight),

path('script/add_hotel',Cotrav_InsertData_Scripts.add_hotel),




    ]