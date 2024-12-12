from django.contrib import admin
from .models import Doctor, Client, Appointment

admin.site.register(Doctor)
admin.site.register(Client)
admin.site.register(Appointment)