from django.db import models


class Corporate_Login(models.Model):
    name = models.CharField(default=True,max_length=200)
    email = models.CharField(default=True,max_length=200)
    password = models.CharField(max_length=100)
    contact_no = models.CharField(default=True,max_length=100)
    corporate_id = models.CharField(default=True,max_length=10)
    last_login = models.DateTimeField(default=True,max_length=100)
    is_radio = models.BooleanField()
    is_local = models.BooleanField()
    is_outstation = models.BooleanField()
    is_bus = models.BooleanField()
    is_train = models.BooleanField()
    is_hotel = models.BooleanField()
    is_meal = models.BooleanField()
    is_flight = models.BooleanField()
    is_water_bottles = models.BooleanField()
    is_reverse_logistics = models.BooleanField()
    class Meta:
        db_table = "corporate_logins"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Corporate_Agent(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    last_login = models.DateTimeField(max_length=100)
    class Meta:
        db_table = "corporate_agents"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Corporate_Spoc_Login(models.Model):
    user_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(max_length=100)
    spoc_id = models.CharField(max_length=10)
    is_radio = models.BooleanField()
    is_local = models.BooleanField()
    is_outstation = models.BooleanField()
    is_bus = models.BooleanField()
    is_train = models.BooleanField()
    is_hotel = models.BooleanField()
    is_meal = models.BooleanField()
    is_flight = models.BooleanField()
    is_water_bottles = models.BooleanField()
    is_reverse_logistics = models.BooleanField()
    class Meta:
        db_table = "corporate_spocs"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Corporate_Approves_1_Login(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(max_length=100)
    subgroup_id = models.CharField(max_length=10)
    is_radio = models.BooleanField()
    is_local = models.BooleanField()
    is_outstation = models.BooleanField()
    is_bus = models.BooleanField()
    is_train = models.BooleanField()
    is_hotel = models.BooleanField()
    is_meal = models.BooleanField()
    is_flight = models.BooleanField()
    is_water_bottles = models.BooleanField()
    is_reverse_logistics = models.BooleanField()
    class Meta:
        db_table = "corporate_subgroup_authenticater"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Corporate_Approves_2_Login(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(max_length=100)
    group_id = models.CharField(max_length=10)
    is_radio = models.BooleanField()
    is_local = models.BooleanField()
    is_outstation = models.BooleanField()
    is_bus = models.BooleanField()
    is_train = models.BooleanField()
    is_hotel = models.BooleanField()
    is_meal = models.BooleanField()
    is_flight = models.BooleanField()
    is_water_bottles = models.BooleanField()
    is_reverse_logistics = models.BooleanField()

    class Meta:
        db_table = "corporate_group_authenticator"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Corporate(models.Model):
    corporate_name = models.CharField(max_length=100)
    corporate_code = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    contact_person_no = models.CharField(max_length=100)
    contact_person_email = models.EmailField(max_length=100)
    has_auth_level = models.BooleanField()
    has_assessment_codes = models.BooleanField()
    is_radio = models.BooleanField()
    is_local = models.BooleanField()
    is_outstation = models.BooleanField()
    is_bus = models.BooleanField()
    is_train = models.BooleanField()
    is_hotel = models.BooleanField()
    is_meal = models.BooleanField()
    is_flight = models.BooleanField()
    is_water_bottles = models.BooleanField()
    is_reverse_logistics = models.BooleanField()

    class Meta:
        db_table = "corporates"


class Corporate_Login_Access_Token(models.Model):
    corporate_login_id = models.CharField(default=True, max_length=10)
    access_token = models.CharField(default=True,max_length=200)
    expiry_date = models.DateTimeField(max_length=100)
    user_agent = models.CharField(default=True, max_length=200)

    class Meta:
        db_table = "corporate_login_access_tokens"

class Corporate_Spoc_Login_Access_Token(models.Model):
    spoc_id = models.CharField(default=True, max_length=10)
    access_token = models.CharField(default=True,max_length=200)
    expiry_date = models.DateTimeField(max_length=100)
    user_agent = models.CharField(default=True, max_length=200)

    class Meta:
        db_table = "corporate_spoc_access_tokens"


class Corporate_Approves_1_Login_Access_Token(models.Model):
    subgroup_authenticater_id = models.CharField(default=True, max_length=10)
    access_token = models.CharField(default=True,max_length=200)
    expiry_date = models.DateTimeField(max_length=100)
    user_agent = models.CharField(default=True, max_length=200)

    class Meta:
        db_table = "corporate_subgroup_authenticater_access_tokens"


class Corporate_Approves_2_Login_Access_Token(models.Model):
    group_authenticater_id = models.CharField(default=True, max_length=10)
    access_token = models.CharField(default=True,max_length=200)
    expiry_date = models.DateTimeField(max_length=100)
    user_agent = models.CharField(default=True, max_length=200)

    class Meta:
        db_table = "corporate_group_authenticater_access_tokens"


class Corporate_Agent_Login_Access_Token(models.Model):
    agent_id = models.CharField(default=True, max_length=10)
    access_token = models.CharField(default=True,max_length=200)
    expiry_date = models.DateTimeField(max_length=100)
    user_agent = models.CharField(default=True, max_length=200)

    class Meta:
        db_table = "corporate_agent_access_tokens"