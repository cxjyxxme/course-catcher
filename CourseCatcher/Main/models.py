from django.db import models
import django.utils.timezone as timezone

class VerificationCodeList(models.Model):
	md5 = models.TextField()
	code = models.TextField(default = "")
	last_ask_time = models.DateTimeField()
	
class User(models.Model):
	username = models.TextField()
	password = models.TextField()
	add_code_times = models.IntegerField(default = 0)
	
class Task(models.Model):
	course_id = models.TextField()
	course_id2 = models.TextField()
	selected = models.BooleanField(default = False)
	try_times = models.IntegerField(default = 0)
	user = models.ForeignKey(User)