from django import forms
from Company.models import Corporate_Login

from Company.models import Corporate_Agent
from Company.models import Corporate

class Corporate_Login_Form(forms.ModelForm):
    class Meta:
        model = Corporate_Login
        fields = "__all__"
        #fields = ['email','password','corporate_id','name']

        # if specific fileds then fields = ['field_1','field_2',...,'field_n' ]


class Corporate_Agent_Login_Form(forms.ModelForm):
    class Meta:
        model = Corporate_Agent
        fields = ['email','password','status','username']


class Corporate_Form(forms.ModelForm):
    class Meta:
        model = Corporate
        fields = "__all__"
        #fields = ['corporate_name', 'corporate_code', 'contact_person_name', 'contact_person_no','contact_person_email','is_radio','is_local','is_outstation','is_bus','is_train','is_flight','is_hotel','is_meal','is_water_bottles','is_reverse_logistics']
