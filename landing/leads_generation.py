import random
import string

import requests
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render , redirect , get_object_or_404
from django_global_request.middleware import get_request


from Common.VIEW.Agent.agent_views import getDataFromAPI
from landing.forms import LeadGenerationModelForm , LeadUpdateForm

from django.views import generic

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.db.models.signals import post_save
from django.dispatch import receiver

from landing.models import Leadgeneration , LeadComments , LeadLog , Document
from Common.models import Corporate_Agent, Corporate
from landing.cotrav_messeging import LeadGenerationEmail

from django.contrib.auth.decorators import login_required

from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.views.generic.edit import ModelFormMixin

from django.contrib import messages

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

import os

from django.core.files.storage import default_storage


from landing.models import Document
from Common.email_settings import SignupEmail,Lead_Status_Change_Email


def lead_detail_view(request, pk):
    try:

        #lead = Leadgeneration.objects.raw('SELECT l.*,ca.user_name FROM cotrav_lead_generation_module l LEFT JOIN corporate_agents ca ON l.Assigned_Sales_Person = ca.id WHERE 1')
        lead = Leadgeneration.objects.get(id=pk)
        s_id = lead.Assigned_Sales_Person
        if s_id > 0:
            sales_person = Corporate_Agent.objects.get(id = s_id)
        else:
            sales_person = {'user_name':'not assigned'}


    except Leadgeneration.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'landing/lead_detail.html', context={'lead': lead , 'person':sales_person})


@receiver(post_save, sender=Leadgeneration)
def my_handler(sender, instance , created , **kwargs):
    corporate_name = instance.Company_Name
    corporate_location = instance.Company_Location
    contact_person_name = instance.Contact_Name
    contact_person_no = instance.Contact_Number
    contact_person_email = instance.Contact_Email

    if(created) :
        print ("create call")
    else:
        print("update call")
        print(instance.id)
        ag_id = instance.Assigned_Sales_Person
        ag_email = Corporate_Agent.objects.get(id=ag_id).email
        ag_name = Corporate_Agent.objects.get(id=ag_id).user_name
        message = ""
        if instance.Status == "Closed-Win":
            try:
                corporate_name = instance.Company_Name
                ref = Corporate.objects.get(corporate_name=corporate_name)
                print("company with same name allready exist")

            except ObjectDoesNotExist:
                corporate_name = instance.Company_Name
                corporate_city = instance.Company_Location
                corporate_code = instance.Company_Name
                contact_person_name = instance.Contact_Name
                contact_person_no = instance.Contact_Number
                contact_person_email = instance.Contact_Email

                company = Corporate()

                company.corporate_name = corporate_name
                company.corporate_city = corporate_city
                company.corporate_code = corporate_code
                company.contact_person_name = contact_person_name
                company.contact_person_no = contact_person_no
                company.contact_person_email = contact_person_email
                company.has_auth_level = 0
                company.no_of_auth_level = 0
                company.has_assessment_codes = 0
                company.is_radio = 0
                company.is_local = 1
                company.is_outstation = 1
                company.is_bus = 1
                company.is_train = 1
                company.is_hotel = 1
                company.is_meal = 0
                company.is_flight = 1
                company.is_water_bottles = 1
                company.is_reverse_logistics = 1
                company.is_deleted = 0

                company.save()
                request = get_request()
                login_type = request.session['agent_login_type']
                access_token = request.session['agent_access_token']
                access_token_auth = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(60))
                password = make_password("taxi123")
                payload = {'corporate_id': company.pk, 'user_id': request.user.id, 'login_type': login_type,
                           'access_token': access_token, 'name': contact_person_name, 'email': contact_person_email, 'cid': '',
                           'contact_no': contact_person_no,
                           'is_radio': 0, 'is_local': 1, 'is_outstation': 1, 'is_bus': 1,
                           'is_train': 1, 'is_hotel': 1, 'is_meal': 0, 'is_flight': 1,
                           'is_water_bottles': 1, 'is_reverse_logistics': 1,
                           'access_token_auth': access_token_auth,'password': password}
                url = settings.API_BASE_URL + "add_admin"
                company = getDataFromAPI(login_type, access_token, url, payload)

                print("Lead is converted to new company after closed-win status")

                message = "Lead with Company Name " + str(instance.Company_Name) + " is converted to new Corporate in Corporate database after Leads closed-win status"

        elif instance.Status == "Assigned":
            message = " <br> Company Name: " + str(instance.Company_Name) + "<br> Customer Name:  " + instance.Contact_Name + "<br> Contact Email : " + instance.Contact_Email + " <br>  Contact Number : " + instance.Contact_Number + " Kindly take it further. "
            # message = "Lead with id " + str(instance.id) + " is updated and assigned to agent " + ag_email
        else:
            message = ""
            message = " <br> Company Name: "+instance.Company_Name+"<br> Customer Name:  "+ instance.Contact_Name +"<br> Contact Email : "+ instance.Contact_Email +" <br>  Contact Number : "+ instance.Contact_Number +"<br><br> Kindly take it further. "
            status = instance.Status
            signup = Lead_Status_Change_Email(message,status,ag_email,ag_name)
            resp1 = signup.send_email()
            print("in mail send fun")
            print(resp1)


@login_required(login_url='/agents/login')
def leads(request):

    leads = Leadgeneration.objects.raw('SELECT l.*,ca.user_name FROM cotrav_lead_generation_module l LEFT JOIN corporate_agents ca ON l.Assigned_Sales_Person = ca.id WHERE 1')
    agents = Corporate_Agent.objects.all()
    return render(request,'landing/leadgeneration_list.html',{'leads':leads,'agents':agents})



@require_POST
def file_upload(request,lead_id):
    file_up = request.FILES['Attachments']
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', str(file_up))
    path = default_storage.save(save_path, request.FILES['Attachments'])
    doc_name = request.POST.get('doc_name', '')
    lead = Leadgeneration.objects.get(id=lead_id)
   #document = Document.objects.create(document=path, upload_by=lead, doc_name=doc_name)
    document = Document.objects.create(document=str(file_up), upload_by=lead, doc_name=doc_name)
    return JsonResponse({'document': document.id})




@login_required(login_url='/agents/login')
def lead_update(request, pk, template_name='landing/leadgeneration_form.html'):
    lead = get_object_or_404(Leadgeneration, pk=pk)
    comments = LeadComments.objects.filter(lead_id=pk)
    attachment = Document.objects.filter(upload_by=pk)
    if request.method == 'POST':

        form = LeadUpdateForm(request.POST or None,request.FILES, instance=lead , initial={'Comments': ''})
        print(form.is_valid())
        if form.is_valid():
            edit_lead = form.save()
            if request.FILES:
                print("i m gere")
                resp = file_upload(request, edit_lead.pk)
                print(resp)
            new_comment = form.cleaned_data['Comments']
            status_action = form.cleaned_data['Status']
            # print(new_lead.pk)
            # print(form.cleaned_data['Comments'])
            cmt = LeadComments()
            cmt.lead_id = edit_lead.pk
            cmt.comment = new_comment
            print(request.user.id)
            cmt.created_by = request.user
            cmt.created_at = timezone.now()
            cmt.save()
            log = LeadLog()
            log.lead_id = edit_lead.pk
            log.comment = new_comment
            log.status_action = status_action
            log.action_initiated_by = request.user.id
            log.save()

            messages.success(request, "Lead Status Updated Successfully..!")
            return redirect('lead-list')
        else:
            print(form.errors)
            messages.error(request, "Lead Status Not Updated ..!")
            form = LeadUpdateForm(request.POST or None, instance=lead , initial={'Comments': ''})
            return render(request, template_name, {'form': form, 'comments': comments, 'attachments': attachment, 'form_title': 'Update Lead'})
    else:

        form = LeadUpdateForm(request.POST or None, instance=lead , initial={'Comments': ''})

    return render(request, template_name, {'form':form,'comments':comments,'attachments':attachment, 'form_title': 'Update Lead'})



@login_required(login_url='/agents/login')
def lead_create(request, template_name='landing/leadgeneration_form.html'):
    if request.method == 'POST':
        form = LeadGenerationModelForm(request.POST or None , request.FILES)
        if form.is_valid():

            new_lead = form.save()
            if request.FILES:
                resp = file_upload(request, new_lead.pk)

            new_comment = form.cleaned_data['Comments']
            status_action = form.cleaned_data['Status']
            #print(new_lead.pk)
            #print(form.cleaned_data['Comments'])
            cmt = LeadComments()
            cmt.lead_id = new_lead.pk
            cmt.comment = new_comment
            cmt.created_by = request.user
            cmt.save()
            log = LeadLog()
            log.lead_id = new_lead.pk
            log.comment = new_comment
            log.status_action = status_action
            log.action_initiated_by = request.user.id
            log.save()
            print("Save Data")
            print(request.POST.get('is_email'))
            is_email = request.POST.get('is_email')
            is_sms = request.POST.get('is_sms')

            if is_email:
                print("in email")
                Contact_Name = request.POST.get('Contact_Name', '')
                Company_Name = request.POST.get('Company_Name', '')
                Contact_Number = request.POST.get('Contact_Number', '')
                Contact_Email = request.POST.get('Contact_Email', '')
                corporate_location = request.POST.get('Company_Location', '')
                message = "Thank you for contacting us, our sales person will get in touch with you as earliest as possible.<br><br>Regards,<br>CoTrav"
                signup = SignupEmail(Company_Name, corporate_location, Contact_Name, Contact_Number,
                                     Contact_Email, message)
                resp1 = signup.send_email()
                print(resp1)
            if is_sms:
                print("in smsm")
                sender_id = 'COTRAV'
                exotel_sid = "novuslogic1"
                exotel_key = "6ae4c99860c31346203da94dc98a4de7fd002addc5848182"
                exotel_token = "a2c78520d23942ad9ad457b81de2ee3f3be743a8188f8c39"
                Contact_no = request.POST.get('Contact_Number')
                sms_body = "Thank you for contacting us, our sales person will get in touch with you as earliest as possible.<br><br>Regards,<br>CoTrav";

                requests.post(
                    'https://twilix.exotel.in/v1/Accounts/{exotel_sid}/Sms/send.json'.format(exotel_sid=exotel_sid),
                    auth=(exotel_key, exotel_token),
                    data={
                        'From': sender_id,
                        'To': Contact_no,
                        'Body': sms_body
                    })

            messages.success(request, "Lead Created Successfully..!")
            return redirect('lead-list')
        else:
            messages.error(request, "Lead Status Not Updated ..!")
            return redirect('lead-list')
    else:
        form = LeadGenerationModelForm()

    return render(request, template_name, {'form':form , 'form_title': 'Create New Lead'})




@login_required(login_url='/agents/login')
def lead_delete(request, pk, template_name='landing/leadgeneration_confirm_delete.html'):
    lead = get_object_or_404(Leadgeneration, pk=pk)
    if request.method=='POST':
        lead.delete()
        return redirect('lead-list')
    return render(request, template_name, {'object':lead})


@login_required(login_url='/agents/login')
def lead_assigned(request, template_name='landing/leadgeneration_list.html'):
    if request.method=='POST':
        lead_id = request.POST.get('lead_id', '')
        agent_id = request.POST.get('agent_id', '')
        agent_email = request.POST.get('agent_email', '')
        Contact_Name = request.POST.get('Contact_Name', '')
        Company_Name = request.POST.get('Company_Name', '')
        Contact_Number = request.POST.get('Contact_Number', '')
        Contact_Email = request.POST.get('Contact_Email', '')
        message = " <br> Company Name: "+Company_Name+"<br> Customer Name:  "+Contact_Name+"<br> Contact Email : "+Contact_Number+" <br>  Contact Number : "+Contact_Email+"<br><br> Kindly take it further. "
        Leadgeneration.objects.filter(pk=lead_id).update(Assigned_Sales_Person=agent_id,Status='Assigned')
        signup = Lead_Status_Change_Email(message, 'Assigned', agent_email, "User")
        resp1 = signup.send_email()
        return redirect('lead-list')
    return render(request, template_name, {})


@login_required(login_url='/agents/login')
def lead_doc_delete(request, pk ):
    lead = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        lead.delete()

    return HttpResponse('deleted')





##########################


@login_required(login_url='/agents/login')
class LeadListView(generic.ListView):
    model = Leadgeneration
    queryset = Leadgeneration.objects.all()


class LeadCreate(SuccessMessageMixin , CreateView):
    model = Leadgeneration
    form_class = LeadGenerationModelForm
    #fields = '__all__'
    initial = {'Status': 'Lead Created'}
    success_message = "Lead Created Successfully"
    success_url = '/agents/lead/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.object)
        cmt = LeadComments()
        self.object = self.object.save()
        id = self.object.latest('id')
        cmt.lead_id = id
        cmt.comment = "testing comment"
        cmt.save()
        #LeadComments.objects.create(cotrav_lead_generation_module_id = self.object)
        #LeadComments.save()
        return redirect('/agents/lead/')


class LeadUpdate(SuccessMessageMixin , UpdateView):
    model = Leadgeneration
    form_class = LeadUpdateForm
    success_message = "Lead Updated Successfully"
    #fields = ['Contact_Name', 'Company_Name', 'Contact_Number', 'Contact_Email','Company_Location','Assigned_Sales_Person','Status','Comments']
    initial = {'Status': 'Assigned'}
    success_url = '/agents/lead/'

class LeadDelete(SuccessMessageMixin , DeleteView):
    model = Leadgeneration
    #messages.add_message(self.request, messages.INFO, 'Hello world.')
    success_message = "Lead Deleated Successfully"
    success_url = reverse_lazy('leads')
    #success_url = '/agents/lead/'
