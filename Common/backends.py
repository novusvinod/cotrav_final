import string
import random

from Common.models import Corporate_Login
from Common.models import Corporate_Spoc_Login
from Common.models import Corporate_Approves_1_Login
from Common.models import Corporate_Approves_2_Login
from django.contrib.auth.hashers import check_password

from django_global_request.middleware import get_request

from Common.models import Corporate_Agent

from Common.models import Corporate_Login_Access_Token
from Common.models import Corporate_Spoc_Login_Access_Token
from Common.models import Corporate_Approves_1_Login_Access_Token
from Common.models import Corporate_Approves_2_Login_Access_Token
from Common.models import Corporate_Agent_Login_Access_Token


class CustomCompanyUserAuth(object):

    @staticmethod
    def authenticate(request, username=None, post_password=None, login_type=None):

        try:

            request = get_request()
            request.session['login_type'] = login_type

            user_info = request.META['HTTP_USER_AGENT']
            print("Browser Info")
            print(user_info)

            if login_type == '1':
                user = Corporate_Login.objects.get(email=username)
            elif login_type == '2':
                user = Corporate_Approves_1_Login.objects.get(email=username)
            elif login_type == '3':
                user = Corporate_Approves_2_Login.objects.get(email=username)
            elif login_type == '4':
                user = Corporate_Spoc_Login.objects.get(username=username)
            elif login_type == '10':
                user = Corporate_Agent.objects.get(email=username)
            else:
                return None

            if user:
                if check_password(post_password, user.password):
                    gen_access_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(60))

                    if login_type == '1':
                        insert_data = Corporate_Login_Access_Token.objects.create(corporate_login_id=user.corporate_id,access_token=gen_access_token,user_agent=user_info)
                    elif login_type == '2':
                        insert_data = Corporate_Approves_1_Login_Access_Token.objects.create(subgroup_authenticater_id=user.id,access_token=gen_access_token,user_agent=user_info)
                    elif login_type == '3':
                        insert_data = Corporate_Approves_2_Login_Access_Token.objects.create(group_authenticater_id=user.id, access_token=gen_access_token,user_agent=user_info)
                    elif login_type == '4':
                        insert_data = Corporate_Spoc_Login_Access_Token.objects.create(spoc_id=user.id,access_token=gen_access_token, user_agent=user_info)
                    elif login_type == '10':
                        insert_data = Corporate_Agent_Login_Access_Token.objects.create(agent_id=user.id, access_token=gen_access_token, user_agent=user_info)
                    request.session['access_token'] = insert_data.access_token

                    return user
                else:
                    print("IN : else")
                    return None
        except Corporate_Login.DoesNotExist:
            print("exception")
            return None

    @staticmethod
    def get_user(user_id):
        try:

            request = get_request()
            login_type = request.session['login_type']

            if login_type == '1':
                user = Corporate_Login.objects.get(pk=user_id)
            elif login_type == '2':
                user = Corporate_Approves_1_Login.objects.get(pk=user_id)
            elif login_type == '3':
                user = Corporate_Approves_2_Login.objects.get(pk=user_id)
            elif login_type == '4':
                user = Corporate_Spoc_Login.objects.get(pk=user_id)
            elif login_type == '10':
                user = Corporate_Agent.objects.get(pk=user_id)
            else:
                return None

            if user.is_active:
                return user
            return None
        except Corporate_Login.DoesNotExist:
            return None

