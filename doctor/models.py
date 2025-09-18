from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Rescheduled', 'Rescheduled'),
    ]
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
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

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
        
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextUploadingField()
    order = models.PositiveIntegerField(default=0)  # to control the order of display

    class Meta:
        ordering = ['order']  # ensures FAQs display in correct order

    def __str__(self):
        return self.question

class Testimonial(models.Model):
    name = models.CharField(max_length=100)   # e.g. "C. K. O."
    content = RichTextUploadingField()             # the testimonial text
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)  
    stars = models.PositiveIntegerField(default=5)  # 1–5 stars rating
    order = models.PositiveIntegerField(default=0)  # for custom ordering

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextUploadingField()
    icon = models.CharField(
        max_length=50,
        help_text="Enter icon class e.g. 'bi bi-clipboard2-heart' or 'fas fa-baby'"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title