from urllib.parse import urlencode

import requests
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

COTRAV_EMAILS = "cotrav@taxivaxi.in"
COTRAV_NUMBERS = "9579477262,"


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

        if booking_type == "Taxi":
            booking_tempalte = "Email_Templates/taxi_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Taxi Booking Received"

        elif booking_type == "Bus":
            print("in bus booking")
            booking_tempalte = "Email_Templates/bus_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Bus Booking Received"

        elif booking_type == "Train":
            booking_tempalte = "Email_Templates/train_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Train Booking Received"

        elif booking_type == "Flight":
            booking_tempalte = "Email_Templates/flight_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Flight Booking Received"

        else:
            print("in hotel booking")
            booking_tempalte = "Email_Templates/hotel_email_template.html"
            email_body = ""
            email_subject = "" + booking[0]['reference_no'] + "- Hotel Booking Received"

        employee_name = ''
        employee_emails = ''
        name_approver_1 = ''
        name_approver_2 = ''
        email_approver_1 = ''
        email_approver_2 = ''

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
                if approver['email_approver_2']:
                    name_approver_2 = "".join(map(str, approver['approver_2']))
                    email_approver_2 = "".join(map(str, approver['email_approver_2']))


        self.send_mail_to_cotrav_agent(booking, COTRAV_EMAILS, "Team", email_subject, email_body,booking_tempalte)
        print("email_send")
        self.send_mail_to_employee(booking, employee_emails, employee_name, email_subject, email_body, booking_tempalte)
        self.send_mail_to_spoc(booking, spoc_email, booking[0]['user_name'], email_subject, email_body,booking_tempalte)

        if email_approver_1:
            self.send_mail_to_approvel(booking, email_approver_1, name_approver_1, email_subject, email_body,booking_tempalte)
        if email_approver_2:
            self.send_mail_to_approvel2(booking, email_approver_2, name_approver_2, email_subject, email_body,booking_tempalte)

        return 1

    def send_mail_to_cotrav_agent(self, booking, emails, name, email_subject, email_body, booking_tempalte):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_employee(self, booking, emails, name, email_subject, email_body, booking_tempalte):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_spoc(self, booking, emails, name, email_subject, email_body, booking_tempalte):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_approvel(self, booking, emails, name, email_subject, email_body, booking_tempalte):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
        msg = EmailMultiAlternatives(email_subject, email_body, 'cotrav@taxivaxi.in', [emails])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1
        return 1

    def send_mail_to_approvel2(self, booking, emails, name, email_subject, email_body, booking_tempalte):
        connection = get_connection()  # uses SMTP server specified in settings.py
        connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        html_content = render_to_string(booking_tempalte, {'bookings': booking, 'user_name': name})
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
        for passangerss in booking[0]['Passangers']:
            employee_numbers = "".join(map(str, passangerss['employee_contact']))
            employee_name = "".join(map(str, passangerss['employee_name']))

        if approvers:
            for approver in approvers:
                if approver['email_approver_1']:
                    name_approver_1 = "".join(map(str, approver['approver_1']))
                if approver['email_approver_2']:
                    name_approver_2 = "".join(map(str, approver['approver_2']))
                if approver['contact_approver_1']:
                    contact_approver_1 = "".join(map(str, approver['contact_approver_1']))
                if approver['contact_approver_2']:
                    contact_approver_2 = "".join(map(str, approver['contact_approver_2']))
        else:
            # if No Approvels
            if employee_numbers:
                self.send_sms_to_taxi(booking, employee_numbers, employee_name,booking_type)
        if contact_approver_1:
            self.send_sms_to_taxi(booking, contact_approver_1, name_approver_1,booking_type)
        if contact_approver_2:
            self.send_sms_to_taxi(booking, contact_approver_2, name_approver_2,booking_type)

        self.send_sms_to_taxi(booking, COTRAV_NUMBERS, "Team" ,booking_type)

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
            sms_body = "Dear " + name + ",\n\nBooking successfully registered with id " + booking[0]['reference_no'] + ".\n\nPickup from " + \
                booking[0]['pickup_location'] + " on " + booking[0]['pickup_datetime'] + ".\nDrop: " + booking[0]['drop_location'] + "\nTrip Type: " + \
                str(tour_type) + ".\nTaxi Type: " + str(booking[0]['taxi_type_request']) + ".\n\nPlease call at " + COTRAV_NUMBERS + \
                            " for any query.\n\nRgrds,\nTaxiVaxi.";
        elif booking_type == "Bus":
            sms_body = "Dear "+name+",\n\nYour Bus Booking is created.\n\nID: "+booking[0]['reference_no']+"\n\nFrom: "+\
                       booking[0]['pickup_location']+"\nTo: "+booking[0]['drop_location']+"\nJourney Date: "+booking[0]['pickup_from_datetime']+"\nBus Type: "+\
                       booking[0]['bus_type_priority_1']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi.";

        elif booking_type == "Train":
            sms_body = "Dear "+name+",\n\nYour Train Booking is created and sent for approval.\n\nID: "+\
                       booking[0]['reference_no']+"\nFrom: "+booking[0]['pickup_location']+"\nTo: "+booking[0]['drop_location']+"\nJourney Date: "+\
                       booking[0]['pickup_from_datetime']+"\nCoach Type: "+booking[0]['train_type_priority_1']+"\n\nPlease call at "+COTRAV_NUMBERS+" for any query.\n\nRgrds,\nTaxiVaxi";
        elif booking_type == "Flight":
            sms_body = "Dear "+name+",\n\nYour Flight Booking is created.\n\nID: "+booking[0]['reference_no']+"\nFrom: "+booking[0]['from_location']+\
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