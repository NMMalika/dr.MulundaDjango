from django.contrib import admin
from django.urls import path, reverse
from .models import Appointment, Blogs, Comment, ContactMessage, FAQ, Testimonial, Service
from .views import ManageAppointmentView 
from .forms import ReplyForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from django.contrib import messages

class AppointmentAdmin(admin.ModelAdmin):
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # Use YourClass.as_view() to hook it into the URL
            path('', self.admin_site.admin_view(ManageAppointmentView.as_view()), name='doctor_appointment_changelist'),
        ]
        return custom_urls + urls

admin.site.register(Appointment, AppointmentAdmin)

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author']
    
    def view_link(self, obj):
        return f'<a href="{obj.get_absolute_url()}" target="_blank">View</a>'
    view_link.allow_tags = True
    view_link.short_description = "Preview"

    def view_on_site(self, obj):
        return obj.get_absolute_url()
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'blog', 'approved', 'created_at')
    list_filter = ('approved', 'created_at', 'blog')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "reply_button")
    search_fields = ("name", "email", "subject")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        if object_id:
            contact = ContactMessage.objects.get(pk=object_id)
            if contact.replied:
                extra_context["reply_button"] = '<span style="color: gray;">Already Replied</span>'
            else:
                url = reverse("admin:contactmessage-reply", args=[contact.pk])
                extra_context["reply_button"] = f'<a class="button" href="{url}">Reply</a>'

        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:message_id>/reply/",
                self.admin_site.admin_view(self.reply_view),
                name="contactmessage-reply",
            ),
        ]
        return custom_urls + urls

    def reply_view(self, request, message_id):
        contact = get_object_or_404(ContactMessage, pk=message_id)

        if request.method == "POST":
            form = ReplyForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data["subject"]
                body = form.cleaned_data["body"]

                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [contact.email],
                    fail_silently=False,
                )

                contact.replied = True
                contact.save(update_fields=["replied"])

                self.message_user(request, f"Reply sent to {contact.email}", messages.SUCCESS)
                app_label = self.model._meta.app_label
                return redirect(f"admin:{app_label}_contactmessage_changelist")
        else:
            form = ReplyForm(initial={"subject": f"Re: {contact.subject}"})

        context = {
            "form": form,
            "contact": contact,
            "title": "Reply to Message",
            "opts": self.model._meta,
        }
        return render(request, "admin/doctor/reply_form.html", context)

    def reply_button(self, obj):
        if getattr(obj, "replied", False):
            return format_html('<span style="color: gray;">Already Replied</span>')
        url = reverse("admin:contactmessage-reply", args=[obj.pk])
        return format_html('<a class="button" href="{}">Reply</a>', url)

    reply_button.short_description = "Action"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    ordering = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', 'order')
    ordering = ('order',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "created_at")
    search_fields = ("title", "description")