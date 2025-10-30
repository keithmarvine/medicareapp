from django.contrib import admin
from careapp.models import *

# Register your models here.

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(appointment)
admin.site.register(contact_view)