from django.contrib import admin
from django.urls import path
from .views import ContactTemplateView, HomeTemplateView, AppointmentTemplateView
from doctor.views import ManageAppointmentView

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("booking-section/", AppointmentTemplateView.as_view(), name="booking-section"),
    path("contact/", ContactTemplateView.as_view(), name="contact"),
    path("manage-appointment/", ManageAppointmentView.as_view(), name="manage_appointment"),

]
