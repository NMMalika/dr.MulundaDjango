from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Appointment, Blogs,ContactMessage
from .forms import CommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
import io
from django.http import FileResponse, HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from openpyxl import Workbook
from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'index.html'

class AppointmentTemplateView(TemplateView):
    template_name = 'index.html'
    
    
    
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date = request.POST.get('date')
        message = request.POST.get('note')

        # Simple validation
        if not all([name, phone, email, date]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('booking-section')

        Appointment.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            message=message
        )

        messages.success(
            request,
            f"Thanks {name} for your appointment request. We will get back to you soon."
        )
        return redirect('booking-section')

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
        
        contact_message= ContactMessage.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            location=location,
            subject=subject,
            message=message,
        )

        return HttpResponse("Email sent successfully!")
    
@method_decorator(staff_member_required, name='dispatch')
class ManageAppointmentView(View):
    template_name = 'manage_appointment.html'

    def get(self, request):
        # Separate appointments by status
        pending_appointments = Appointment.objects.filter(status="Pending").order_by('-created_at')
        accepted_appointments = Appointment.objects.filter(status="Accepted").order_by('-created_at')
        rejected_appointments = Appointment.objects.filter(status="Rejected").order_by('-created_at')
        rescheduled_appointments = Appointment.objects.filter(status="Rescheduled").order_by('-created_at')

        # Paginate only pending ones (the active queue)
        paginator = Paginator(pending_appointments, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            "pending_appointments": page_obj,   # only pending paginated
            "accepted_appointments": accepted_appointments,
            "rejected_appointments": rejected_appointments,
            "rescheduled_appointments": rescheduled_appointments,
            "is_paginated": page_obj.has_other_pages(),
            "page_obj": page_obj,
            "title": "Manage Appointments",
        })

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action_type")
        appointment_id = request.POST.get("appointment_id")
        custom_message = request.POST.get("message")

        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Update status
        if action == "Accepted":
            appointment.status = "Accepted"
            subject = "Your Appointment is Accepted"
        elif action == "Rejected":
            appointment.status = "Rejected"
            subject = "Your Appointment is Rejected"
        elif action == "Rescheduled":
            appointment.status = "Rescheduled"
            subject = "Your Appointment is Rescheduled"
        else:
            subject = "Appointment Update"

        appointment.save()

        # Build email content
        email_message = (
            custom_message
            if custom_message
            else f"Dear {appointment.name}, your appointment on {appointment.date.strftime('%d %b %Y %H:%M')} has been {action.lower()}."
        )

        # Send email
        try:
            send_mail(
                subject=subject,
                message=email_message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[appointment.email],
                fail_silently=False,
            )
            messages.success(request, f"Email sent to {appointment.name}")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")

        return redirect("manage_appointment")  # Redirect back to same view

    
def blog(request):
    recent_blogs = Blogs.objects.all().order_by('-created_at')  # Get all blogs ordered by creation date
    paginator = Paginator(recent_blogs, 5)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "blog.html", {'page_obj': page_obj, 'recent_blogs': recent_blogs})


def blogdetail(request, blog_id):
    blog = Blogs.objects.get(id=blog_id)
    recent_blogs = Blogs.objects.all().exclude(id=blog_id).order_by('-created_at')[:4]  # Get the 4 most recent blogs
      # Previous post: blog with ID less than current (older)
    previous_blog = Blogs.objects.filter(id__lt=blog_id).order_by('-id').first()

    # Next post: blog with ID greater than current (newer)
    next_blog = Blogs.objects.filter(id__gt=blog_id).order_by('id').first()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog  # Link comment to this blog
            comment.save()
            return redirect('blogdetail', blog_id=blog.id)
    else:
        form = CommentForm()

    
    comments = blog.comments.filter(approved=True).order_by('-created_at')
    
    return render(request, "blogdetail.html", {
        'blog': blog,
        'recent_blogs': recent_blogs,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        'form': form,
        'comments': comments
    })

      




# --- PDF EXPORT ---
def export_appointments_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Appointments Report", styles['Heading1']))

    # Table data
    data = [["Name", "Email", "Phone", "Date", "Message"]]
    for appt in Appointment.objects.all():
        data.append([appt.name, appt.email, appt.phone,
                     appt.date.strftime("%d-%m-%Y"), appt.message])

    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="appointments.pdf")


# --- EXCEL EXPORT ---
def export_appointments_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Appointments"

    # Headers
    ws.append(["Name", "Email", "Phone", "Date", "Message"])

    # Data rows
    for appt in Appointment.objects.all():
        ws.append([appt.name, appt.email, appt.phone,
                   appt.date.strftime("%d-%m-%Y"), appt.message])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="appointments.xlsx"'
    wb.save(response)
    return response
  
   