from django.contrib import admin

from .models import User, Query, OfficeHour, TimeSlot, Appointment

admin.site.register(User)
admin.site.register(Query)
admin.site.register(OfficeHour)
admin.site.register(TimeSlot)
admin.site.register(Appointment)
