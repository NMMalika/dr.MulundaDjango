from django.contrib import admin
from django.urls import path
from .models import Appointment, Blogs, Comment
from .views import ManageAppointmentView # <-- Import your CLASS

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