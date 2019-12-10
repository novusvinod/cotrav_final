from django.shortcuts import render,redirect

from django.http import HttpResponse

from django.core.mail import EmailMultiAlternatives, get_connection

from django.core.mail import send_mail

from django.core import mail

from django.utils.html import strip_tags

from django.template.loader import render_to_string

from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook

from io import BytesIO

from django.template.loader import get_template

from xhtml2pdf import pisa

import os
from random import randint

from django.core.files import File

from threading import Thread, activeCount
from landing.utils import render_to_pdf


class BookingEmail:

    def __init__(self,booking_id,pickup_city,drop_city,preferred_train,pickup_time,drop_time):

        self.booking_id = booking_id
        self.pickup_city = pickup_city
        self.drop_city = drop_city
        self.preferred_train = preferred_train
        self.pickup_time = pickup_time
        self.drop_time = drop_time
        self.Passangers = [{'employee_name':'sannn','age':'12'}]
        self.send_to = "sanketongmel@gmail.com"

    def send_email (self,file: list):

        subject, from_email, to = 'hello', 'contact@cotrav.co', self.send_to
        text_content = 'This email message contain train booking details.'
        html_content = render_to_string("email_voucher_template/booking_email_template.html",{'booking_id':self.booking_id,'pickup_city':self.pickup_city,'Passangers':self.Passangers})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.content_subtype = "html"
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file(file[1])
        # msg.attach(attach.name, attach.read(), attach.content_type)
        #msg.send()
        res = msg.send()

        return (res)


    def send_sms (self):

        self.res = 1

        return self.res


class Bus():

    def __init__(self, params):
        self.params = params


    def get(self, request):
        params = self.params
        pdf = render_to_pdf('pdf_voucher_template/invoice2.html', params)
        file = Render.render_to_file('pdf_voucher_template/invoice2.html', params)

        return file


class Flight():

    def __init__(self, params):
        self.params = params

    def get(self, request):
        params = self.params
        pdf = render_to_pdf('pdf_voucher_template/flight_voucher.html', params)
        file = Render.render_to_file('pdf_voucher_template/flight_voucher.html', params)
        return file


class Hotel():
    def __init__(self, params):
        self.params = params

    def get(self, request):
        params = self.params
        pdf = render_to_pdf('pdf_voucher_template/hotel_voucher.html', params)
        file = Render.render_to_file('pdf_voucher_template/hotel_voucher.html', params)
        return file


class SignupEmail():

    def __init__(self,company,company_location,cp_name,cp_no,cp_email,message):
         self.company = company
         self.company_location = company_location
         self.cp_name = cp_name
         self.cp_no = cp_no
         self.cp_email = "vinod@taxivaxi.com "
         self.message = message
         self.send_to = cp_email

    def send_email(self):
         email_subject = "Thanks for joining us"
         tempalte = "signup_welcome.html"
         email_body = 'Thank You For Showing Interest. We will Contact You Soon'
         connection = get_connection()  # uses SMTP server specified in settings.py
         connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
         html_content = render_to_string(tempalte, {'company':self.company,'location':self.company_location,'cp_name':self.cp_name,'cp_no':self.cp_no,'cp_email':self.cp_email,'message':self.message})
         msg = EmailMultiAlternatives(email_subject, email_body, 'balwant@taxivaxi.in', [self.cp_email])
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
        msg = EmailMultiAlternatives(email_subject, email_body, 'balwant@taxivaxi.in', [self.cp_email])
        msg.attach_alternative(html_content, "text/html")

        res = msg.send(fail_silently=True)
        connection.close()  # Cleanup
        # res = 1

        return (res)

    

class LeadGenerationEmail():

    def __init__(self,company,company_location,cp_name,cp_no,cp_email,message,status):
         self.company = company
         self.company_location = company_location
         self.cp_name = cp_name
         self.cp_no = cp_no
         self.cp_email = cp_email
         self.message = message
         self.status = status
         self.send_to = "sanketongmel@gmail.com,vinod@taxivaxi.com,balwant@taxivaxi.in"


    def lead_create_send_email(self):
         subject, from_email, to = 'New Lead Is Generated', self.cp_email , self.send_to
         text_content = 'New Lead is generated..!!'
         html_content = render_to_string("landing/lead_generated_email_template.html", {'company':self.company,'location':self.company_location,'cp_name':self.cp_name,'cp_no':self.cp_no,'cp_email':self.cp_email,'message':self.message,'status':self.status})

         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
         msg.content_subtype = "html"
         msg.attach_alternative(html_content, "text/html")
         
         #msg.attach_file(file[1])
         res = msg.send(fail_silently=True)
         
         return 1 

    def lead_updated_send_email(self,agent):
         self.send_to = self.send_to + " , " + agent
         subject, from_email, to = 'Lead updated intimation', self.cp_email , self.send_to
         text_content = 'lead is updated and agent is assigned..!!'
         html_content = render_to_string("landing/lead_updated_email_template.html", {'company':self.company,'location':self.company_location,'cp_name':self.cp_name,'cp_no':self.cp_no,'cp_email':self.cp_email,'message':self.message,'status':self.status,'agent_assigned':agent})

         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
         msg.content_subtype = "html"
         msg.attach_alternative(html_content, "text/html")
         
         #msg.attach_file(file[1])
         res = msg.send(fail_silently=True)
         
         return 1      



class Excelexport():

    def __init__(self,ar):
        self.row = []
        self.keys = []
        self.value = []
        self.row_num = 1

        self.jsonar = ar

        self.columns = []


    def myexport(self):

        workbook = Workbook()
    
        # Get active worksheet/tab
        worksheet = workbook.active
        worksheet.title = 'Bookings'

        # get headings of coloumn from key

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
        #response = content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',

        response['Content-Disposition'] = 'attachment; filename={date}-movies.xlsx'.format(date=datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),)


        for keyval in self.jsonar:

            for key in keyval:

                self.keys.append(key)


        self.keys = list(dict.fromkeys(self.keys)) 

        self.columns = self.keys 

         # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(self.columns, 1):
            cell = worksheet.cell(row=self.row_num, column=col_num)
            cell.value = column_title
      

        # get each row values

        for book in self.jsonar:

            self.row_num += 1

            for key in book:

                if key == 'Passangers':

                    print("Passenger found")

                else:    
                    #print(key)
                    #print('##')
                    #keys.append(key)
                    val = book[key]
                    #print(val)
                    #print('####')
                    self.value.append(val)

            self.row = self.value

            for col_num, cell_value in enumerate(self.row, 1):
                cell = worksheet.cell(row=self.row_num, column=col_num)
                cell.value = cell_value

            self.value.clear()    

        workbook.save(response)  

        return response



class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        file = open("my.file.pdf", "wb")
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}{1}.pdf".format('Bus_Voucher_', randint(1, 1000000))
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "media//Email_Voucher_PDF", file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]








