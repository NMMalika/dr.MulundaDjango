from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views import View
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'index.html'

class AppointmentTemplateView(TemplateView):
    template_name = 'index.html'
    
    def post(self,request):
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        date=request.POST.get('date')
        message=request.POST.get('note')
        
        appointment= Appointment.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            message=message
        )
        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {name} for your appointment request. We will get back to you soon.")
        return redirect ('booking-section')

class ContactTemplateView(TemplateView):
    template_name = 'index.html'

    def post(self,request):
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        location=request.POST.get('location')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
                # Render HTML email content
        context = {
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'location': location,
            'subject': subject,
            'message': message,
        }
        html_content = render_to_string("email.html", context)

        # Fallback plain text
        text_content = f"""
        Name: {name}
        Email: {email}
        Phone_number: {phone_number}
        Location: {location}
        Subject: {subject}
        Message: {message}
        """

        # Construct and send email
        email_message = EmailMultiAlternatives(
            subject=f"{subject} - {name} from Jackie WEBSITE enquiry",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return HttpResponse("Email sent successfully!")
    
class ManageAppointmentView(View):
    template_name = 'manage_appointment.html'

    def get(self, request):
        appointments = Appointment.objects.all().order_by('-created_at')
        paginator = Paginator(appointments, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'appointments': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
            'title': 'Manage Appointments',
            'description': 'View and manage all appointments.',
        })

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action_type')
        appointment_id = request.POST.get('appointment_id')
        message = request.POST.get('message')
        
        # handle your message sending or appointment updating here
        return redirect(request,'admin/doctor/manage_appointments.html')
    

@method_decorator(staff_member_required, name='dispatch')
class ManageAppointmentView(View):
    template_name = 'manage_appointment.html'

    def get(self, request):
        appointments = Appointment.objects.all().order_by('-created_at')
        # Your pagination logic is correct
        paginator = Paginator(appointments, 3) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'appointments': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
            'title': 'Manage Appointments',
        })

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action_type')
        appointment_id = request.POST.get('appointment_id')
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if action == 'accept':
                appointment.status = 'Accepted' # Assumes you have a 'status' field in your model
                messages.success(request, f"Appointment for {appointment.name} was accepted.")
            elif action == 'reject':
                appointment.status = 'Rejected'
                messages.error(request, f"Appointment for {appointment.name} was rejected.")
            appointment.save()
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
            
        # Redirect back to the same management page
        return redirect('admin:doctor_appointment_changelist')
      
    
   