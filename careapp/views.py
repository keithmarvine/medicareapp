from django.shortcuts import render, redirect, get_object_or_404
from careapp.models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def departments(request):
    return render(request, 'departments.html')

def appointments(request):
    if request.method == 'POST':
         myappointment = appointment(
            name = request.POST ['name'],
            email = request.POST ['email'],
            phone = request.POST ['phone'],
            date = request.POST ['date'],
            department = request.POST ['department'],
            doctor = request.POST ['doctor'],
            message = request.POST ['message']
        )
         myappointment.save()
         messages.success(request, 'Your appointment has been booked successfully!')

         return redirect('/show')
    else:
        return render(request, 'appointments.html')
def doctors(request):
    return render(request, 'doctors.html')

def contact(request):
    if request.method == 'POST':
        mycontact = contact_view(
            name = request.POST ['name'],
            email = request.POST ['email'],
            subject = request.POST ['subject'],
            message = request.POST ['message']
        )

        mycontact.save()
        messages.success(request, 'Your contact has been saved successfully!')
        return redirect('/contact')


    else:

        return render(request, 'contact.html')
        messages.error(request, 'Unable to book your contact!')


def show(request):
    allappointments = appointment.objects.all()
    return render(request, 'show.html', {'allappointments': allappointments})

def delete(request,id):
    myappoint =get_object_or_404(appointment, id = id)
    myappoint.delete()
    messages.success(request, 'Your message has been deleted!')

    return redirect('/show')

def edit(request, id):
    editappoint = get_object_or_404(appointment, id = id)

    if request.method == "POST":
        editappoint.name = request.POST.get('name')
        editappoint.email = request.POST.get('email')
        editappoint.phone = request.POST.get('phone')
        editappoint.date = request.POST.get('date')
        editappoint.department = request.POST.get('department')
        editappoint.doctor = request.POST.get('doctor')
        editappoint.message = request.POST.get('message')

        editappoint.save()
        messages.success(request, 'Your request has been updated')

        return redirect('/show')

    else:
        return render(request, 'edit.html', {'editappoint': editappoint})

