from django.db import models

# Create your models here.
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    date = models.DateField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    rescheduled = models.BooleanField(default=False)
    rescheduled_date = models.DateField(blank=True, null=True)
    rescheduled_time = models.TimeField(blank=True, null=True)
    rescheduled_reason = models.TextField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Appointment by {self.name} on {self.date} at {self.appointment_time}"
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['date', 'appointment_time']),
        ]