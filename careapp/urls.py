
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('starter', views.starter, name= 'starter'),
    path('about', views.about, name = 'about'),
    path('services', views.services, name = 'services'),
    path('departments', views.departments, name = 'departments'),
    path('appointments', views.appointments, name = 'appointments'),
    path('doctors', views.doctors, name = 'doctors'),
    path('contact', views.contact, name = 'contact'),
    path('show', views.show, name = 'show'),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>', views.edit)


]
