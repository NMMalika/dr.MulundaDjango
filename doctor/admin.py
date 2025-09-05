from django.contrib import admin
from django.urls import path
from .models import Appointment, Blogs, Comment, ContactMessage
from .views import ManageAppointmentView # <-- Import your CLASS
from .forms import ReplyForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings

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
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")

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

    def reply_view(self, request, message_id, *args, **kwargs):
        contact = ContactMessage.objects.get(pk=message_id)

        if request.method == "POST":
            form = ReplyForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data["subject"]
                body = form.cleaned_data["body"]

                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,  # sender
                    [contact.email],           # recipient
                    fail_silently=False,
                )

                self.message_user(request, f"Reply sent to {contact.email}", level=messages.SUCCESS)
                return redirect("admin:appname_contactmessage_changelist")  # 👈 replace `appname`
        else:
            form = ReplyForm(initial={"subject": f"Re: {contact.subject}"})

        return render(
            request,
            "admin/reply_form.html",
            {"form": form, "contact": contact},
        )

    # Add a "Reply" button in the change list
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().changelist_view(request, extra_context=extra_context)

# Add a "Reply" button on each detail page
    def change_view(self, request, object_id, form_url="", extra_context=None):
        contact = ContactMessage.objects.get(pk=object_id)
        extra_context = extra_context or {}
        extra_context["reply_link"] = f"{object_id}/reply/"
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
