from django.contrib import admin

from .models import MyUser, Query, OfficeHour, TimeSlot, Appointment, Feedback

admin.site.register(MyUser)
admin.site.register(Query)
admin.site.register(OfficeHour)
admin.site.register(TimeSlot)
admin.site.register(Appointment)
admin.site.register(Feedback)
