
from django.contrib import admin
from django.urls import path, include
from doctor import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("doctor.urls")),
    path("export/pdf/", views.export_appointments_pdf, name="export_appointments_pdf"),
    path("export/excel/", views.export_appointments_excel, name="export_appointments_excel"),
]
