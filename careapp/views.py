
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from careapp.models import *
from django.contrib import messages

# Mpesa Imports
import requests
import json
from requests.auth import HTTPBasicAuth
from careapp.credentials import MpesaAccessToken, LipanaMpesaPpassword


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


# User Authentication

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request,user)
            messages.success(request, "You are now logged in!")
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')


# Mpesa Integration Views
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
     return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/callback",
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")

        if result_code == "0":
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Success"
            )
            transaction.save()
            
            context = {
                'success': True,
                'transaction_id': transaction_id,
                'amount': amount,
                'phone': phone
            }
            return render(request, 'payment_result.html', context)
        else:
            error_message = response_data.get("ResponseDescription", "Transaction failed")
            context = {
                'success': False,
                'error_message': error_message,
                'result_code': result_code,
                'amount': amount,
                'phone': phone
            }
            return render(request, 'payment_result.html', context)

    return HttpResponse("Invalid Request method")


def payment_result(request):
    return render(request, 'payment_result.html')


def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})
