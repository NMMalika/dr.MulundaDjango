from django.contrib import admin
from django.urls import path
from .views import ContactTemplateView, HomeTemplateView, AppointmentTemplateView, blogdetail,blog
from doctor.views import ManageAppointmentView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("booking-section/", AppointmentTemplateView.as_view(), name="booking-section"),
    path("contact/", ContactTemplateView.as_view(), name="contact"),
    path("manage-appointment/", ManageAppointmentView.as_view(), name="manage_appointment"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("blog/", blog, name="blog"),
    path("blogdetail/<blog_id>", blogdetail, name="blogdetail"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
