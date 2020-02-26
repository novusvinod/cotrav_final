from pyfcm import FCMNotification
import requests
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

COTRAV_EMAILS = "cotrav@taxivaxi.in"
COTRAV_NUMBERS = "9579477262,"
API_ACCESS_KEY_EMPLOYEE = 'AAAAE7JHFiU:APA91bH8hJWfLlFEjL9TiSKIT0so-HL1PXqDXgKWtU_19W-3ViuJHZC8Iswkq3eXl-Tjd8jKBm7X9UxCFMKpJaBQt5Ar-9qJeAB07R753hpmamQXW6lP917Fa0S6w02qzi6tNai3Kmsh'
API_ACCESS_KEY_SPOC = ''


class SignIn_OTP:
    def send_email(self, email_to, email_subject, email_body):
        #email_subject = "Cotrav - Verify Your Email"
        #email_body = "Dear User,<br><br>"+generate_otp+" is your verification code to access your profile and bookings on Cotrav app, you need to verify your email first. <br><br>Rgrds,<br>CoTrav."
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [email_to])
        msg.content_subtype = "html"
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        res = 1
        return (res)


class AddBooking_Email:
    def send_taxi_email(self, booking, approvers, booking_type):
        global booking_tempalte
        global email_body
        global email_subject
        global email_content
        global email_title

        if booking_type == "Taxi":
            booking_tempalte = "Email_Templates/taxi_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Taxi Booking Received"
            email_content = "New booking request for Taxi received. Details as below,"
            email_title = "New Taxi Booking Received"

        elif booking_type == "Bus":
            print("in bus booking")
            booking_tempalte = "Email_Templates/bus_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Bus Booking Received"
            email_content = "New booking request for Bus received. Details as below,"
            email_title = "New Bus Booking Received"

        elif booking_type == "Train":
            booking_tempalte = "Email_Templates/train_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Train Booking Received"
            email_content = "New booking request for Train received. Details as below,"
            email_title = "New Train Booking Received"

        elif booking_type == "Flight":
            booking_tempalte = "Email_Templates/flight_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Flight Booking Received"
            email_content = "New booking request for Flight received. Details as below,"
            email_title = "New Flight Booking Received"

        else:
            print("in hotel booking")
            booking_tempalte = "Email_Templates/hotel_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Hotel Booking Received"
            email_content = "New booking request for Hotel received. Details as below,"
            email_title = "New Hotel Booking Received"

        employee_name = ''
        employee_emails = ''
        name_approver_1 = ''
        name_approver_2 = ''
        email_approver_1 = ''
        email_approver_2 = ''
        is_send_email_approver_1 = ''
        is_send_sms_approver_1 = ''
        is_send_email_approver_2 = ''
        is_send_sms_approver_2 = ''

        spoc_email = booking[0]['user_email']
        print("spoc email")
        print(spoc_email)

        for passangerss in booking[0]['Passangers']:
            employee_emails = "".join(map(str, passangerss['employee_email']))
            employee_name = "".join(map(str, passangerss['employee_name']))

        if approvers:
            for approver in approvers:
                if approver['email_approver_1']:
                    name_approver_1 = "".join(map(str, approver['approver_1']))
                    email_approver_1 = "".join(map(str, approver['email_approver_1']))
                    is_send_email_approver_1 = "".join(map(str, approver['is_send_email_approver_1']))

                if approver['email_approver_2']:
                    name_approver_2 = "".join(map(str, approver['approver_2']))
                    email_approver_2 = "".join(map(str, approver['email_approver_2']))
                    is_send_email_approver_2 = "".join(map(str, approver['is_send_email_approver_2']))

        self.send_mail_to_cotrav_agent(booking, COTRAV_EMAILS, "Team", email_subject, email_body,booking_tempalte, email_content, email_title)
        print("email_send")
        self.send_mail_to_employee(booking, employee_emails, employee_name, email_subject, email_body, booking_tempalte, email_content, email_title)

        if booking[0]['spoc_is_send_email'] == '1':
            self.send_mail_to_spoc(booking, spoc_email, booking[0]['user_name'], email_subject, email_body,booking_tempalte, email_content, email_title)

        if email_approver_1:
            if booking_type == "Taxi":
                email_content = "Booking request for Taxi is pending for approval. Details as below,"
            elif booking_type == "Bus":
                email_content = "Booking request for Bus is pending for approval. Details as below,"
            elif booking_type == "Train":
                email_content = "Booking request for Train is pending for approval. Details as below,"
            elif booking_type == "Hotel":
                email_content = "Booking request for Hotel is pending for approval. Details as below,"
            elif booking_type == "Flight":
                email_content = "Booking request for Flight is pending for approval. Details as below,"
            if is_send_email_approver_1:
                self.send_mail_to_approvel(booking, email_approver_1, name_approver_1, email_subject, email_body,booking_tempalte, email_content, email_title)
        if email_approver_2:
            if booking_type == "Taxi":
                email_content = "Booking request for Taxi is pending for approval. Details as below,"
            elif booking_type == "Bus":
                email_content = "Booking request for Bus is pending for approval. Details as below,"
            elif booking_type == "Train":
                email_content = "Booking request for Train is pending for approval. Details as below,"
            elif booking_type == "Hotel":
                email_content = "Booking request for Hotel is pending for approval. Details as below,"
            elif booking_type == "Flight":
                email_content = "Booking request for Flight is pending for approval. Details as below,"
            if is_send_email_approver_2:
                self.send_mail_to_approvel2(booking, email_approver_2, name_approver_2, email_subject, email_body,booking_tempalte, email_content, email_title)

        return 1

    def send_mail_to_cotrav_agent(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_employee(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name, 'email_content':email_content, 'email_title':email_title})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_spoc(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name, 'email_content':email_content, 'email_title':email_title})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_approvel(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name, 'email_content':email_content, 'email_title':email_title})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_approvel2(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name, 'email_content':email_content, 'email_title':email_title})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1


    def send_taxi_msg(self, booking, approvers,booking_type):
        employee_numbers = ''
        employee_name = ''
        name_approver_1 = ''
        name_approver_2 = ''
        contact_approver_1 = ''
        contact_approver_2 = ''
        is_send_sms_approver_1 = ''
        is_send_sms_approver_2 = ''
        for passangerss in booking[0]['Passangers']:
            employee_numbers = "".join(map(str, passangerss['employee_contact']))
            employee_name = "".join(map(str, passangerss['employee_name']))

        if approvers:
            for approver in approvers:
                if approver['email_approver_1']:
                    name_approver_1 = "".join(map(str, approver['approver_1']))
                    is_send_sms_approver_1 = "".join(map(str, approver['is_send_sms_approver_1']))
                if approver['email_approver_2']:
                    is_send_sms_approver_2 = "".join(map(str, approver['is_send_sms_approver_2']))
                    name_approver_2 = "".join(map(str, approver['approver_2']))
                if approver['contact_approver_1']:
                    contact_approver_1 = "".join(map(str, approver['contact_approver_1']))
                if approver['contact_approver_2']:
                    contact_approver_2 = "".join(map(str, approver['contact_approver_2']))
            if contact_approver_1 and is_send_sms_approver_1:
                self.send_sms_to_taxi_for_approve(booking, contact_approver_1, name_approver_1, booking_type)
            if contact_approver_2 and is_send_sms_approver_2:
                self.send_sms_to_taxi_for_approve(booking, contact_approver_2, name_approver_2, booking_type)
            if employee_numbers:
                self.send_sms_to_taxi_for_approve(booking, employee_numbers, employee_name,booking_type)
            if booking[0]['user_contact']:
                self.send_sms_to_taxi_for_approve(booking, employee_numbers, employee_name,booking_type)
            self.send_sms_to_taxi_for_approve(booking, COTRAV_NUMBERS, "Team", booking_type)
        else:
            # if No Approvels
            if employee_numbers:
                self.send_sms_to_taxi(booking, employee_numbers, employee_name,booking_type)
            if booking[0]['user_contact']:
                self.send_sms_to_taxi(booking, employee_numbers, employee_name,booking_type)
            self.send_sms_to_taxi(booking, COTRAV_NUMBERS, "Team" ,booking_type)

        return 1

    def send_sms_to_taxi_for_approve(self,booking, phone_number, name, booking_type):
        sender_id = 'COTRAV'
        exotel_sid = "novuslogic1"
        exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
        exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"

        global sms_body

        if booking_type == "Taxi":
            tour_type = str(booking[0]['tour_type'])
            if tour_type == '1':
                tour_type = "Radio"
            if tour_type == '2':
                tour_type = "Local"
            if tour_type == '3':
                tour_type = "Outstation"
            sms_body = "Dear " + name + ",\n\nYour Taxi Booking is created and sent for approval. " + booking[0]['reference_no'] + ".\n\nPickup from " + \
                booking[0]['pickup_location'] + " on " + booking[0]['pickup_datetime'] + ".\nDrop: " + booking[0]['drop_location'] + "\nTrip Type: " + \
                str(tour_type) + ".\nTaxi Type: " + str(booking[0]['taxi_type_request']) + ".\n\nPlease call at " + COTRAV_NUMBERS + \
                            " for any query.\n\nRgrds,\nTaxiVaxi.";
        elif booking_type == "Bus":
            sms_body = "Dear "+name+",\n\nYour Bus Booking is created and sent for approval.\n\nID: "+booking[0]['reference_no']+"\n\nFrom: "+\
                       booking[0]['pickup_location']+"\nTo: "+booking[0]['drop_location']+"\nJourney Date: "+booking[0]['pickup_from_datetime']+"\nBus Type: "+\
                       booking[0]['bus_type_priority_1']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi.";

        elif booking_type == "Train":
            sms_body = "Dear "+name+",\n\nYour Train Booking is created and sent for approval.\n\nID: "+\
                       booking[0]['reference_no']+"\nFrom: "+booking[0]['pickup_location']+"\nTo: "+booking[0]['drop_location']+"\nJourney Date: "+\
                       booking[0]['pickup_from_datetime']+"\nCoach Type: "+booking[0]['train_type_priority_1']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi";
        elif booking_type == "Flight":
            sms_body = "Dear "+name+",\n\nYour Flight Booking is created and sent for approval.\n\nID: "+booking[0]['reference_no']+"\nFrom: "+booking[0]['from_location']+\
                       "\nTo: "+booking[0]['to_location']+"\nJourney Date: "+booking[0]['departure_datetime']+"\nTrip Type: "+\
                       booking[0]['usage_type']+"\nSeat Type: "+booking[0]['journey_type']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi";
        else:
            sms_body =  "Dear "+name+",\n\nYour Hotel Booking is created and sent for approval.\n\nID: "+booking[0]['reference_no']+"\nArea: "+\
                        str(booking[0]['from_area_id_name'])+"\nCheck-In Date: "+booking[0]['checkin_datetime']+"\nRoom Type: "+str(booking[0]['bucket_priority_1'])+\
                        "\nRoom Occupancy: "+str(booking[0]['room_type_id'])+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi.";

        requests.post(
            'https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
            auth=(exotel_key, exotel_token),
            data={
                'From': sender_id,
                'To': phone_number,
                'Body': sms_body
            })
        return 1

    def send_sms_to_taxi(self,booking, phone_number, name, booking_type):
        sender_id = 'COTRAV'
        exotel_sid = "novuslogic1"
        exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
        exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"

        global sms_body

        if booking_type == "Taxi":
            tour_type = str(booking[0]['tour_type'])
            if tour_type == '1':
                tour_type = "Radio"
            if tour_type == '2':
                tour_type = "Local"
            if tour_type == '3':
                tour_type = "Outstation"
            sms_body = "Dear " + name + ",\n\nYour Bus Booking is created.\n\nID: " + booking[0]['reference_no'] + ".\n\nPickup from " + \
                booking[0]['pickup_location'] + " on " + booking[0]['pickup_datetime'] + ".\nDrop: " + booking[0]['drop_location'] + "\nTrip Type: " + \
                str(tour_type) + ".\nTaxi Type: " + str(booking[0]['taxi_type_request']) + ".\n\nPlease call at " + COTRAV_NUMBERS + \
                            " for any query.\n\nRgrds,\nTaxiVaxi.";
        elif booking_type == "Bus":
            sms_body = "Dear "+name+",\n\nYour Bus Booking is created.\n\nID: "+booking[0]['reference_no']+"\n\nFrom: "+\
                       booking[0]['pickup_location']+"\nTo: "+booking[0]['drop_location']+"\nJourney Date: "+booking[0]['pickup_from_datetime']+"\nBus Type: "+\
                       booking[0]['bus_type_priority_1']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi.";

        elif booking_type == "Train":
            sms_body = "Dear "+name+",\n\nYour Train Booking is created.\n\nID: "+\
                       booking[0]['reference_no']+"\nFrom: "+booking[0]['pickup_location']+"\nTo: "+booking[0]['drop_location']+"\nJourney Date: "+\
                       booking[0]['pickup_from_datetime']+"\nCoach Type: "+booking[0]['train_type_priority_1']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi";
        elif booking_type == "Flight":
            sms_body = "Dear "+name+",\n\nYour Flight Booking is created.\n\nID: "+booking[0]['reference_no']+"\nFrom: "+booking[0]['from_location']+\
                       "\nTo: "+booking[0]['to_location']+"\nJourney Date: "+booking[0]['departure_datetime']+"\nTrip Type: "+\
                       booking[0]['usage_type']+"\nSeat Type: "+booking[0]['journey_type']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi";
        else:
            sms_body =  "Dear "+name+",\n\nYour Hotel Booking is created \n\nID: "+booking[0]['reference_no']+"\nArea: "+\
                        str(booking[0]['from_area_id_name'])+"\nCheck-In Date: "+booking[0]['checkin_datetime']+"\nRoom Type: "+str(booking[0]['bucket_priority_1'])+\
                        "\nRoom Occupancy: "+str(booking[0]['room_type_id'])+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi.";

        requests.post(
            'https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
            auth=(exotel_key, exotel_token),
            data={
                'From': sender_id,
                'To': phone_number,
                'Body': sms_body
            })
        return 1

    def new_user_send_email(self, username, password, user_type):
        email_subject = "CoTrav New User Login Credentials"
        email_body = "Dear " + username + ",<br> Url: cotrav.co/login <br> Email:" + username + "<br> Password:" + password + "<br> UserType:" + user_type + \
                     "<br> Thank you for Signup. <br><br>Please call at  for any query. <br><br>Rgrds,<br>CoTrav."
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [username])
        msg.content_subtype = "html"
        res = msg.send(fail_silently=True)
        return 1

    def send_sms(self):
        sender_id = 'COTRAV'
        exotel_sid = "novuslogic1"
        exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
        exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"
        sms_body = "New Taxi Booking - " + "TV132131" + ".<br><br>Pickup from: " + "Pune" + "<br>Pickup Time: " + "10-10-2019 12:12 AM" + ".<br>Trip Type: " + "Local" + ".<br>Taxi Type: " + "N/A" + ".<br><br>Regards,<br>TaxiVaxi";

        requests.post('https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
                      auth=(exotel_key, exotel_token),
                      data={
                          'From': sender_id,
                          'To': COTRAV_NUMBERS,
                          'Body': sms_body
                      })
        return 1


class newUserAdd_Email:
    def new_user_send_email(self, name, username_email, password, user_type):
        email_subject = "CoTrav New User Login Credentials"
        tempalte = "Email_Templates/New_User_Add/add_new_user_email_template.html"
        email_body = ""
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(tempalte, {'password':password, 'user_name': name,'user_type':user_type, 'username_email':username_email })
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [username_email])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1


class Assign_Booking_Email:
    def is_client_email(self,booking, booking_type, gen_voucher_path):
        global booking_tempalte
        global email_body

        if booking_type == "Taxi":
            booking_tempalte = "Email_Templates/Assign_Booking/taxi_email_template.html"
        elif booking_type == "Bus":
            print("in bus booking")
            booking_tempalte = "Email_Templates/Assign_Booking/bus_email_template.html"

        elif booking_type == "Train":
            booking_tempalte = "Email_Templates/Assign_Booking/train_email_template.html"

        elif booking_type == "Flight":
            booking_tempalte = "Email_Templates/Assign_Booking/flight_email_template.html"
        else:
            print("in hotel booking")
            booking_tempalte = "Email_Templates/Assign_Booking/hotel_email_template.html"

        employee_name = ''
        employee_emails = ''
        email_body = ''

        spoc_email = booking[0]['user_email']
        print("spoc email")
        print(spoc_email)

        for passangerss in booking[0]['Passangers']:
            employee_emails = "".join(map(str, passangerss['employee_email']))
            employee_name = "".join(map(str, passangerss['employee_name']))

        email_subject = "" + booking[0]['reference_no'] + "- Ride Details Confirmed"

        self.send_mail_to_cotrav_agent(booking, COTRAV_EMAILS, "Team", email_subject, email_body, booking_tempalte, gen_voucher_path)
        print("email_send")
        self.send_mail_to_employee(booking, employee_emails, employee_name, email_subject, email_body, booking_tempalte, gen_voucher_path)
        if booking[0]['spoc_is_send_email'] == '1':
            self.send_mail_to_spoc(booking, spoc_email, booking[0]['user_name'], email_subject, email_body,booking_tempalte, gen_voucher_path)

    def send_mail_to_cotrav_agent(self, booking, emails, name, email_subject, email_body, booking_tempalte, gen_voucher_path):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        if gen_voucher_path:
            msg.attach_file(gen_voucher_path)
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_employee(self, booking, emails, name, email_subject, email_body, booking_tempalte, gen_voucher_path):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        if gen_voucher_path:
            msg.attach_file(gen_voucher_path)
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_spoc(self, booking, emails, name, email_subject, email_body, booking_tempalte, gen_voucher_path):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        if gen_voucher_path:
            msg.attach_file(gen_voucher_path)
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1


    def send_client_sms(self,booking, booking_type):
        employee_numbers = ''
        employee_name = ''
        for passangerss in booking[0]['Passangers']:
            employee_numbers = "".join(map(str, passangerss['employee_contact']))
            employee_name = "".join(map(str, passangerss['employee_name']))
        if employee_numbers:
            self.send_sms_to_employee(booking, employee_numbers, employee_name, booking_type)


    def send_sms_to_employee(self,booking, phone_number, name, booking_type):
        sender_id = 'COTRAV'
        exotel_sid = "novuslogic1"
        exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
        exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"

        global sms_body

        if booking_type == "Taxi":
            sms_body = "Dear "+name+"\n\nYour Booking ID " +booking[0]['reference_no']+" is confirmed.\n\nPickup From: "+booking[0]['pickup_location']+\
                       "\nPickup on: "+booking[0]['drop_location']+"\nCar: "+booking[0]["model_name"]+" ("+booking[0]["taxi_reg_no"]+")\nDriver: "+\
                       booking[0]["driver_name"]+ " (" +booking[0]["driver_contact"]+")\nPassenger: " +name+ "\n\nFor any assistance, please call us at " +\
                       COTRAV_NUMBERS+ "\n\n$sms_sender_name";
        elif booking_type == "Bus":
            sms_body = "Dear "+name+"\n\nYour Booking ID "+booking[0]['reference_no']+" is assigned.\n\nOperator: "+booking[0]['operator_name']+\
                       "\nPNR No: "+booking[0]['pnr_no']+"\nTicket No: "+booking[0]['ticket_no']+"\nSeat No:"+booking[0]['seat_no']+"\nBus Type: "+\
                       booking[0]['assign_bus_type_id']+"\nBoarding Time: "+booking[0]['boarding_datetime']+"\nBoarding Point: "+booking[0]['boarding_point']+\
                       "\n\nIn case of any query, please call at "+COTRAV_NUMBERS+".\n\nRgrds,\nTaxiVaxi";

        elif booking_type == "Train":
            sms_body = "Dear "+name+",\n\nYour Booking ID "+booking[0]['reference_no']+" assigned by TaxiVaxi.\n\nTrain: "+booking[0]['train_name']+\
                       "\nTrain No.:"+booking[0]['train_name']+"\nPNR No.: "+booking[0]['pnr_no']+"\nCoach No.:"+booking[0]['seat_no']+"\nSeat No.: "+\
                       booking[0]['seat_no']+"\nCoach Type: "+booking[0]['assign_bus_type_id']+"\nBoarding Time: "+booking[0]['boarding_datetime']+\
                       "\nBoarding Station: "+booking[0]['boarding_point']+"\n\nIn case of any query, please call at "+COTRAV_NUMBERS+\
                       ".\n\nRegards,\nTaxiVaxi";

        elif booking_type == "Flight":
            sms_body =  "Dear "+name+",\n\nYour Booking ID "+booking[0]['reference_no']+" assigned by TaxiVaxi.\n\nFlight: "+booking[0]['Flights'][0]['flight_name']+\
                        " ("+booking[0]['Flights'][0]['flight_no']+")\nPNR No.: "+booking[0]['Flights'][0]['pnr_no']+"\nFlight Type: "+booking[0]['journey_type']+"\nSeat Type: "+\
                        booking[0]['flight_class']+"\nTrip Type: "+booking[0]['usage_type']+"\nBoarding Time: "+str(booking[0]['Flights'][0]['departure_datetime'])+\
                        "\nBoarding at:"+booking[0]['from_location']+"\n\nIn case of any query, please call at "+COTRAV_NUMBERS+".\n\nRegards,\nTaxiVaxi";

        else:
            sms_body = "Dear "+name+",\n\nYour Booking ID "+booking[0]['reference_no']+" assigned by TaxiVaxi.\n\nHotel: "+booking[0]['operator_name']+\
                       "\nHotel Address: "+booking[0]['operator_contact']+"\nHotel Contact: "+booking[0]['operator_contact']+"\nVoucher No.: "+\
                       booking[0]['reference_no']+"\nRoom Type: "+booking[0]['hotel_type_name']+"\nCheck-In Date: "+booking[0]['checkin_datetime']+\
                       "\n\nIn case of any query, please call at "+COTRAV_NUMBERS+"\n\nRegards,\nTaxiVaxi";


        requests.post(
            'https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
            auth=(exotel_key, exotel_token),
            data={
                'From': sender_id,
                'To': phone_number,
                'Body': sms_body
            })
        return 1


class SignupEmail():

    def __init__(self, company, company_location, cp_name, cp_no, cp_email, message):
        self.company = company
        self.company_location = company_location
        self.cp_name = cp_name
        self.cp_no = cp_no
        self.cp_email = cp_email
        self.message = message
        self.send_to = cp_email

    def send_email(self):
        email_subject=''
        tempalte= ''
        email_body=''
        if self.company_location == 'contactus':
            email_subject = "Thanks for contact us"
            tempalte = "contact_welcome.html"
            email_body = 'Thank You For Showing Interest. We will Contact You Soon'
        else:
            email_subject = "Thanks for joining us"
            tempalte = "signup_welcome.html"
            email_body = 'Thank You For Showing Interest. We will Contact You Soon'
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(tempalte, {'company': self.company, 'location': self.company_location,
                                                   'user_name': self.cp_name, 'cp_no': self.cp_no,
                                                   'cp_email': self.cp_email, 'message': self.message})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [self.send_to,"cotrav@taxivaxi.in"])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1

        return (res)


    def reminder_email(self):
        email_subject = "Lead Generation Reminder"
        tempalte = "signup_welcome.html"
        email_body = 'Lead With Following Company Details Contacted US Again..!'
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(tempalte, {'company': self.company, 'location': self.company_location,
                                                   'cp_name': self.cp_name, 'cp_no': self.cp_no,
                                                   'cp_email': self.cp_email, 'message': self.message})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [self.cp_email])
        msg.attach_alternative(html_content, "text/html")

        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1

        return (res)


class Lead_Status_Change_Email():
    def __init__(self, message,status,ag_email,ag_name):
        self.cp_email = "vinod@taxivaxi.com "
        self.message = message
        self.send_to = ag_email
        self.ag_name = ag_name
        self.status = status

    def send_email(self):
        email_subject = "Cotrav Lead Status Change"
        email_body = "Hi " + self.ag_name + ", <br><br> New Lead has been assigned to your queue <br><br> Details are as below,"+self.message+" <br><br> Please call at  for any query."+COTRAV_NUMBERS+" <br><br>Regards,<br>CoTrav."
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [self.send_to])
        msg.content_subtype = "html"
        res = msg.send(fail_silently=True)

        return (1)


class FCM:
    def send_notification(self, booking, approvers, booking_type):
        api_access_key = API_ACCESS_KEY_EMPLOYEE
        push_service = FCMNotification(api_key=api_access_key)

        registration_id = []
        registration_id.append(booking[0]['spoc_fcm_reg_id'])
        for passangerss in booking[0]['Passangers']:
            registration_id.append(passangerss['employee_fcm_regid'])
        if approvers:
            for approver in approvers:
                if approver['email_approver_1']:
                    registration_id.append(approver['approver1_regid'])
                if approver['email_approver_2']:
                    registration_id.append(approver['approver2_regid'])

        message_title = "CoTrav Notification"
        message_body = "Your new booking request has been received..!"

        if booking_type == "Taxi":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Taxi",
            }

        elif booking_type == "Bus":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_from_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Bus",
            }

        elif booking_type == "Train":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_from_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Train",
            }

        elif booking_type == "Flight":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['date_of_journey'],
                "pickup_from": booking[0]['from_location'],
                "drop_to": booking[0]['to_location'],
                "type": "Flight",
            }

        else:
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "Checkin": booking[0]['checkin_datetime'],
                "Checkout": booking[0]['checkin_datetime'],
                "pickup_from": booking[0]['from_area_id_name'],
                "type": "Hotel",
            }


        result = push_service.notify_multiple_devices(registration_ids=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
        print(result)
        return 1

    def send_custome_msg_notification(self, booking):
        api_access_key = API_ACCESS_KEY_EMPLOYEE
        push_service = FCMNotification(api_key=api_access_key)
        registration_id = ['cyaPMxbAwyQ:APA91bFKQgIHRSHYB-YjGYfX97EZhzXaa-vaRzrTmRxxqUOU3uSSB9Bf77DQgDSUjtotUb8nw8NooFIaxRMDY1HcO1Xg3vu3P5f8D6yKw4pZe1z72Utwtv0K_f61OBbbXhmZHl9hOK1v',
                           'eKbxdr2iCIc:APA91bGH7Go0qr_FMR5zC_46Yk3BYsvVuwaQfFgxbmm_BjtjJpfqjWS9zGPmmH59wn5mO4zKtx6_O1X6E8bl2EyCv3Z28cE1-o1LuZzKaYGaTqn4ZGuSmEnUzGkhHfdNR1n5yeC-3y1U',
                           'eUWpIIbiHdM:APA91bEvYbednDUHI1zNmpR2NWQvez9pJVGrR8WOUy3z0CjgtlurWBskK5goX6cMqExQaXM14zaqXkJOFB4hLXcq0cA0JK0fcHlxo0WFcPBkJUS7yHq9gqDmLZ3lK7HbeYh1ntMaL1ni',
                           'fTGSm3aO5mg:APA91bFiGt-ItCbxNPx7icpPzmWL61t75FDvZEOthGlYBz-J8gRWwU18T9dTdOl-92voJKl_aQTbXsX_sUq8fgeouWRROYmiKXDV1dKtY01r4moTLlU9QZB5KeIQucTzeEs-qkgxjjal']
        # #registration_id.append(booking[0]['spoc_fcm_reg_id'])
        data_message = {
            "reference_no": "CTTXI000001",
            "spoc_name": "Shreyash P",
            "pickup_time": "20-02-2020 03:20",
            "pickup_from": "Pune Railway Station, Sadhu Vaswani Road, Koregaon Park, Pune, Maharashtra, India",
            "drop_to": "Pimple Saudagar, Pimpri-Chinchwad, Maharashtra, India",
            "type": "Taxi"
        }
        result = push_service.multiple_devices_data_message(registration_ids=registration_id, data_message=data_message)
        print(result)
        return 1

    def send_custome_notification(self, booking):
        api_access_key = API_ACCESS_KEY_EMPLOYEE
        push_service = FCMNotification(api_key=api_access_key)
        registration_id = ''

        data_message = {
            "reference_no": "Balwant",
            "spoc_name": "Chauhan",
            "pickup_time": "Test Ok",
            "pickup_from": "Test Ok",
            "drop_to": "Test Ok",
            "type": "Test Ok",
        }

        result = push_service.multiple_devices_data_message(registration_ids=registration_id, data_message=data_message)
        print(result)
        return 1

    def send_broadcast_notification(self, msg_head, msg_title, msg_text):
        api_access_key = API_ACCESS_KEY_EMPLOYEE
        push_service = FCMNotification(api_key=api_access_key)

        data_message = {
            "ContentHead": ""+msg_head,
            "ContentTitle": ""+msg_title,
            "ContentText": ""+msg_text,
            "type": "broadcast",
            "image":"http://cotrav.co/static/email_template_images/bg_1.png",
        }
        result = push_service.notify_topic_subscribers(topic_name="news", data_message=data_message)
        return 1

    def send_message_to_moblies(self, mobile_nos, msg_text):
        sender_id = 'COTRAV'
        exotel_sid = "novuslogic1"
        exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
        exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"

        requests.post('https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
                      auth=(exotel_key, exotel_token),
                      data={
                          'From': sender_id,
                          'To': mobile_nos,
                          'Body': msg_text
                      })
        return 1

    def send_mail_to_user(self,email_subject, email_body, email_to):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [email_to])
        msg.content_subtype = "html"
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup

        return 1



class AcceptBooking_Email():
    def send_email_sms_ntf(self, booking, booking_type):
        global booking_tempalte
        global email_body
        global email_subject
        registration_id = []
        global email_content
        global email_title
        email_title = "Approval confirmation"

        if booking_type == "Taxi":
            booking_tempalte = "Email_Templates/taxi_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Taxi Booking Approval confirmation"
            email_content = "Booking request for Taxi is Approved your Approver. Details as below,"

        elif booking_type == "Bus":
            print("in bus booking")
            booking_tempalte = "Email_Templates/bus_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Bus Booking Approval confirmation"
            email_content = "Booking request for Bus is Approved your Approver. Details as below,"

        elif booking_type == "Train":
            booking_tempalte = "Email_Templates/train_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Train Booking Approval confirmation"
            email_content = "Booking request for Train is Approved your Approver. Details as below,"

        elif booking_type == "Flight":
            booking_tempalte = "Email_Templates/flight_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Flight Booking Approval confirmation"
            email_content = "Booking request for Flight is Approved your Approver. Details as below,"

        else:
            print("in hotel booking")
            booking_tempalte = "Email_Templates/hotel_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Hotel Booking Approval confirmation"
            email_content = "Booking request for Hotel is Approved your Approver. Details as below,"

        employee_name = ''
        employee_emails = ''

        spoc_email = booking[0]['user_email']
        registration_id = registration_id.append(booking[0]['spoc_fcm_reg_id'])

        for passangerss in booking[0]['Passangers']:
            employee_emails = "".join(map(str, passangerss['employee_email']))
            employee_name = "".join(map(str, passangerss['employee_name']))
            registration_id = registration_id.append(passangerss['employee_fcm_regid'])

        self.send_mail(booking, COTRAV_EMAILS, "Team", email_subject, email_body, booking_tempalte, email_content, email_title)
        self.send_mail(booking, employee_emails, employee_name, email_subject, email_body, booking_tempalte, email_content, email_title)
        if booking[0]['spoc_is_send_email'] == '1':
            self.send_mail(booking, spoc_email, booking[0]['user_name'], email_subject, email_body,booking_tempalte, email_content, email_title)

        self.send_custome_notification(booking, registration_id, booking_type)
        return 1

    def send_mail(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name, 'email_content':email_content, 'email_title':email_title})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_custome_notification(self, booking, registration_id, booking_type):
        api_access_key = API_ACCESS_KEY_EMPLOYEE
        push_service = FCMNotification(api_key=api_access_key)
        registration_id = registration_id

        if booking_type == "Taxi":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Taxi",
                "ContentHead": "Taxi Booking Approved",
                "ContentTitle": "Taxi Booking "+booking[0]['reference_no']+" Approved",
                "ContentText": "'Taxi Hotel Booking "+booking[0]['reference_no']+" is Approved ",
            }

        elif booking_type == "Bus":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_from_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Bus",
                "ContentHead": "Bus Booking Approved",
                "ContentTitle": "Bus Booking " + booking[0]['reference_no'] + " Approved",
                "ContentText": "'Bus Hotel Booking " + booking[0]['reference_no'] + " is Approved ",
            }

        elif booking_type == "Train":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_from_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Train",
                "ContentHead": "Train Booking Approved",
                "ContentTitle": "Train Booking " + booking[0]['reference_no'] + " Approved",
                "ContentText": "'Train Hotel Booking " + booking[0]['reference_no'] + " is Approved ",
            }

        elif booking_type == "Flight":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['date_of_journey'],
                "pickup_from": booking[0]['from_location'],
                "drop_to": booking[0]['to_location'],
                "type": "Flight",
                "ContentHead": "Flight Booking Approved",
                "ContentTitle": "Flight Booking " + booking[0]['reference_no'] + " Approved",
                "ContentText": "'Flight Hotel Booking " + booking[0]['reference_no'] + " is Approved ",
            }

        else:
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "Checkin": booking[0]['checkin_datetime'],
                "Checkout": booking[0]['checkin_datetime'],
                "pickup_from": booking[0]['from_area_id_name'],
                "type": "Hotel",
                "ContentHead": "Hotel Booking Approved",
                "ContentTitle": "Hotel Booking " + booking[0]['reference_no'] + " Approved",
                "ContentText": "'Hotel Hotel Booking " + booking[0]['reference_no'] + " is Approved ",
            }
        result = push_service.multiple_devices_data_message(registration_ids=registration_id, data_message=data_message)
        print(result)


class RejectBooking_Email():
    def send_email_sms_ntf(self, booking, booking_type):
        global booking_tempalte
        global email_body
        global email_subject
        registration_id = []
        global email_content
        global email_title
        if booking[0]['status_cotrav'] <= 2:
            email_title = "Booking "+ booking[0]['client_status']
        else:
            email_title = "Booking " + booking[0]['cotrav_status']+"by Agent"

        if booking_type == "Taxi":
            booking_tempalte = "Email_Templates/taxi_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Taxi Booking Cancelled"
            email_content = "Booking request for Taxi is Cancelled. Details as below,"

        elif booking_type == "Bus":
            print("in bus booking")
            booking_tempalte = "Email_Templates/bus_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Bus Booking Cancelled"
            email_content = "Booking request for Bus is Cancelled. Details as below,"

        elif booking_type == "Train":
            booking_tempalte = "Email_Templates/train_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Train Booking Cancelled"
            email_content = "Booking request for Train is Cancelled. Details as below,"

        elif booking_type == "Flight":
            booking_tempalte = "Email_Templates/flight_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Flight Booking Cancelled"
            email_content = "Booking request for Flight is Cancelled. Details as below,"

        else:
            print("in hotel booking")
            booking_tempalte = "Email_Templates/hotel_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Hotel Booking Approval confirmation"
            email_content = "Booking request for Hotel is Cancelled. Details as below,"

        employee_name = ''
        employee_emails = ''

        spoc_email = booking[0]['user_email']
        registration_id = registration_id.append(booking[0]['spoc_fcm_reg_id'])

        for passangerss in booking[0]['Passangers']:
            employee_emails = "".join(map(str, passangerss['employee_email']))
            employee_name = "".join(map(str, passangerss['employee_name']))
            registration_id = registration_id.append(passangerss['employee_fcm_regid'])

        self.send_mail(booking, COTRAV_EMAILS, "Team", email_subject, email_body, booking_tempalte, email_content, email_title)
        self.send_mail(booking, employee_emails, employee_name, email_subject, email_body, booking_tempalte, email_content, email_title)
        if booking[0]['spoc_is_send_email'] == '1':
            self.send_mail(booking, spoc_email, booking[0]['user_name'], email_subject, email_body,booking_tempalte, email_content, email_title)

        self.send_custome_notification(booking, registration_id, booking_type)
        return 1

    def send_mail(self, booking, emails, name, email_subject, email_body, booking_tempalte, email_content, email_title):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name, 'email_content':email_content, 'email_title':email_title})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_custome_notification(self, booking, registration_id, booking_type):
        api_access_key = API_ACCESS_KEY_EMPLOYEE
        push_service = FCMNotification(api_key=api_access_key)
        registration_id = registration_id

        if booking_type == "Taxi":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Taxi",
                "ContentHead": "Taxi Booking Cancelled",
                "ContentTitle": "Taxi Booking " + booking[0]['reference_no'] + " Cancelled",
                "ContentText": "'Taxi Hotel Booking " + booking[0]['reference_no'] + " is Cancelled ",
            }

        elif booking_type == "Bus":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_from_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Bus",
                "ContentHead": "Bus Booking Cancelled",
                "ContentTitle": "Bus Booking " + booking[0]['reference_no'] + " Cancelled",
                "ContentText": "'Bus Hotel Booking " + booking[0]['reference_no'] + " is Cancelled ",
            }

        elif booking_type == "Train":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['pickup_from_datetime'],
                "pickup_from": booking[0]['pickup_location'],
                "drop_to": booking[0]['drop_location'],
                "type": "Train",
                "ContentHead": "Train Booking Cancelled",
                "ContentTitle": "Train Booking " + booking[0]['reference_no'] + " Cancelled",
                "ContentText": "'Train Hotel Booking " + booking[0]['reference_no'] + " is Cancelled ",
            }

        elif booking_type == "Flight":
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "pickup_time": booking[0]['date_of_journey'],
                "pickup_from": booking[0]['from_location'],
                "drop_to": booking[0]['to_location'],
                "type": "Flight",
                "ContentHead": "Flight Booking Cancelled",
                "ContentTitle": "Flight Booking " + booking[0]['reference_no'] + " Cancelled",
                "ContentText": "'Flight Hotel Booking " + booking[0]['reference_no'] + " is Cancelled ",
            }

        else:
            data_message = {
                "reference_no": booking[0]['reference_no'],
                "spoc_name": booking[0]['user_name'],
                "Checkin": booking[0]['checkin_datetime'],
                "Checkout": booking[0]['checkin_datetime'],
                "pickup_from": booking[0]['from_area_id_name'],
                "type": "Hotel",
                "ContentHead": "Hotel Booking Cancelled",
                "ContentTitle": "Hotel Booking " + booking[0]['reference_no'] + " Cancelled",
                "ContentText": "'Hotel Hotel Booking " + booking[0]['reference_no'] + " is Cancelled ",
            }
        result = push_service.multiple_devices_data_message(registration_ids=registration_id, data_message=data_message)
        print(result)