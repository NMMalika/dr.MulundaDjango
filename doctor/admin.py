from django.contrib import admin
from django.urls import path
from .models import Appointment
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