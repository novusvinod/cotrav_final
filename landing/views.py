from django.shortcuts import render , redirect
from django.http import HttpResponse
from Common.models import Corporate

from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from datetime import timedelta

from landing.forms import LeadGenerationModelForm
from landing.models import Leadgeneration, LeadComments, LeadLog
from django.contrib import messages
from landing.utils import render_to_pdf
from Common.email_settings import SignupEmail

# Create your views here.
def index_cs(request):
    return render(request,'comingsoon.html')


def index(request):
    return render(request,'cotrav_index.html')


def about(request):
    return render(request,'cotrav_about.html')


def login(request):
    return render(request,'cotrav_login.html')


def signup(request):
    if request.method == 'POST':

        corporate_name = request.POST.get('corporate_name')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_no = request.POST.get('contact_person_no')
        contact_person_email = request.POST.get('contact_person_email')
        corporate_location = request.POST.get('corporate_location')
        Lead_Source = request.POST.get('Lead_Source')
        Hear_About_Us = request.POST.get('Hear_About_Us')
        message = request.POST.get('message')

        Newcompany = Leadgeneration()

        Newcompany.Company_Name = corporate_name
        Newcompany.Company_Location = corporate_location
        Newcompany.Contact_Name = contact_person_name
        Newcompany.Contact_Number = contact_person_no
        Newcompany.Contact_Email = contact_person_email
        Newcompany.Company_Website = ''
        Newcompany.Message = message
        Newcompany.Assigned_Sales_Person = 0
        Newcompany.Status = 'Lead Created'
        Newcompany.Lead_Source = Lead_Source
        Newcompany.Hear_About_Us = Hear_About_Us
        Newcompany.Attachments = ''
        Newcompany.Lead_Communication = ''
        Newcompany.Comments = ''

        try:
            ref = Leadgeneration.objects.get(Company_Name=corporate_name)
            print("Company with same name allready exist")
            # return redirect('signup')
            err_msg = "Company with same name allready exist"
            return render(request, 'cotrav_signup.html',
                          {'company': corporate_name, 'name': contact_person_name, 'number': contact_person_no,
                           'email': contact_person_email, 'city': corporate_location, 'message': message,
                           'err_msg': err_msg})
        except ObjectDoesNotExist:
            Newcompany.save()
            messages.success(request, "A Cotrav Official would be contacting you in 24 hours to discuss business solutions for your team...!")
        return redirect('signup')

    else:
        return render(request, 'cotrav_signup.html')



def contact(request):
    if request.method == 'POST':
        corporate_name = request.POST.get('corporate_name')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_no = request.POST.get('contact_person_no')
        contact_person_email = request.POST.get('contact_person_email')
        corporate_location = 'contactus'
        Lead_Source = 'Contact Us'
        message = request.POST.get('message')

        Newcompany = Leadgeneration()

        Newcompany.Company_Name = corporate_name
        Newcompany.Company_Location = corporate_location
        Newcompany.Contact_Name = contact_person_name
        Newcompany.Contact_Number = contact_person_no
        Newcompany.Contact_Email = contact_person_email
        Newcompany.Company_Website = ''
        Newcompany.Message = message
        Newcompany.Assigned_Sales_Person = 0
        Newcompany.Status = 'Lead Created'
        Newcompany.Lead_Source = Lead_Source
        Newcompany.Attachments = ''
        Newcompany.Lead_Communication = ''
        Newcompany.Comments = ''

        Newcompany.save()
        messages.success(request,
                         "A Cotrav Official would be contacting you in 24 hours to discuss business solutions for your team..!")
        return redirect('contact')

    else:

        return render(request, 'cotrav_contact.html')


def support(request):
        return render(request,'cotrav_support.html')


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, 'error_404.html', data)


def testsignup(request):
    try:
        ref = Corporate.objects.get(corporate_name = "tcs")
    except ObjectDoesNotExist:
        print("duplicate entry")
    return HttpResponse("test")


def testemail(request):
    corporate_name = "taxivaxi"
    contact_person_name = "vinod"
    contact_person_no = "9876787676"
    contact_person_email = "vinod@gmail.com"
    corporate_location = "pune"
    message = "testing cotrav"
    signup = SignupEmail(corporate_name,corporate_location,contact_person_name,contact_person_no,contact_person_email,message)
    resp1 = signup.send_test_email()
    return HttpResponse(resp1)


def voucher(request):
    return render(request,'booking_email_voucher.html')



def export_movies_to_xlsx(request):
    """
    Downloads all movies as Excel file with a single worksheet
    """
    movie_queryset = Corporate.objects.all()

    print(movie_queryset)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-movies.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
    )

    return response


def pdf_render_test(request):
    voucher = {'name':'sanket'}
    pdf = render_to_pdf('filght_test_voucher.html', voucher)

    #return render(request,'train_email_temp.html')

    return HttpResponse(pdf, content_type='application/pdf')