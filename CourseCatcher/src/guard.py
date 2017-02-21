import time
import datetime
from Main.models import User
from Main.models import VerificationCodeList
from Main.models import Task
from src.UserAction import UserAction

users = User.objects.all()
for user in users:
	action = UserAction(user.id)
	action.get_cookie()

while True:
	users = User.objects.all()
	user_actions = []
	for user in users:
		user_actions.append(UserAction(user.id))
	
	times = 0
	for action in user_actions:
		print '[' + str(action.id) + ' : select course]'
		if not action.select_course(""):
			print '[' + str(action.id) + ' : login]'
			if not action.login():
				print "[not enough codes]"
		times += 1
		if times % 10 == 0:
			action.check_course()
	time.sleep(0.2)
	
	
	#t0 = datetime.datetime.now()
	#print ((datetime.datetime.now() - t0)).total_seconds()