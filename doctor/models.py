from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


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


class Blogs(models.Model):
    blog_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()  # Rich text + images
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-created_at']  
        indexes = [
            models.Index(fields=['title', 'author']),
        ]

class Comment(models.Model):
    
    blog = models.ForeignKey("Blogs", on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return f"{self.name} - {self.comment[:30]}"
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"