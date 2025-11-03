from django.db import models

# Create your models here.
class Patient(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    idno = models.IntegerField()
    phonenumber = models.CharField(max_length=10)
    dob = models.DateField()
    age = models.IntegerField()
    admitteddatetime = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.fullname

class Doctor(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    idno = models.IntegerField()
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

class appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    date = models.DateTimeField()
    department = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name


class contact_view(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"

