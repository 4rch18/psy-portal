from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class MyUser(models.Model):
	username=models.CharField(max_length=40)
	password=models.CharField(max_length=40)
	is_admin=models.BooleanField(default=False)
	sent_new_text=models.BooleanField(default=False)
	is_online=models.BooleanField(default=False)

	updated_office_hours=models.BooleanField(default=False)
	status_appointment_changed=models.BooleanField(default=False)
	updated_time_slots=models.BooleanField(default=False)



	def __str__(self):
		return self.username


class Query(models.Model):
	client=models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='client_text')
	admin=models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='admin_text')
	pub_date=models.DateTimeField('date published')
	text=models.CharField(max_length=200)
	by_admin=models.BooleanField(default=False)

	def __str__(self):
		return self.text


class OfficeHour(models.Model):
	admin=models.ForeignKey(MyUser, on_delete=models.CASCADE)
	start_time=models.CharField(max_length=10)
	end_time=models.CharField(max_length=10)
	display=models.CharField(max_length=20)

	def __str__(self):
		return self.display


class TimeSlot(models.Model):
	client=models.ForeignKey(MyUser, on_delete = models.CASCADE, related_name = 'client_slot', null = True)
	office_hours=models.ForeignKey(OfficeHour, on_delete=models.CASCADE, related_name = 'office_slot')
	display=models.CharField(max_length=40)
	is_free=models.BooleanField(default=True)		#if free then delete appoitment entry

	def __str__(self):
		return self.display

class Appointment(models.Model):
	client=models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='client_time')
	admin=models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='admin_time')
	slot=models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='slot_time')
	status=models.CharField(max_length=20, default='pending')		#if free then delete entry

	def __str__(self):
		return self.status
