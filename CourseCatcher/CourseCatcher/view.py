from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from Main.models import User
from Main.models import VerificationCodeList
from Main.models import Task
from src.UserAction import UserAction
from django.db.models import F
import os
import django.utils.timezone as timezone
import pycurl 
import StringIO 

def index(request):
	context = get_default_context(request)
	return render(request, 'index.html', context)

def add_user(request):
	context = get_default_context(request)
	if 'info' in request.GET:
		if request.GET['info'] == '1':
			context['info'] = 'this account has already been registeied'
	return render(request, 'add_user.html', context)
	
def deal_add_user(request):
	context = get_default_context(request)
	if (len(User.objects.filter(username = request.POST['username'])) > 0) :
		response = HttpResponseRedirect('/add_user?info=1')
		return response
	else:
		user = User(username = request.POST['username'], password = request.POST['password'])
		user.save()
		act = UserAction(user.id)
		act.get_cookie()
		os.system("mkdir static/temp/" + str(user.id) + " 2>static/temp/system_output_temp");
			
		
		response = HttpResponseRedirect('/login')
		return response
	
def deal_login(request):
	user = User.objects.filter(username = request.POST['username']).filter(password = request.POST['password'])
	if (len(user) > 0) :
		response = HttpResponseRedirect('/')
		response.set_cookie('user_id', user[0].id)
		return response
	else:
		response = HttpResponseRedirect('/login?info=1')
		return response
		
def login(request):
	context = get_default_context(request)
	if 'info' in request.GET:
		if request.GET['info'] == '1':
			context['info'] = 'username/password error'
	return render(request, 'login.html', context)
		
def logout(request):
	response = HttpResponseRedirect('/')
	response.delete_cookie('user_id')
	return response
	
def user_info(request):
	if 'user_id' in request.COOKIES:
		context = get_default_context(request)
		user = User.objects.get(id = request.COOKIES['user_id'])
		context['tasks'] = user.task_set.all()
		context['add_code_times'] = user.add_code_times
		return render(request, 'user_info.html', context)
	else:
		response = HttpResponseRedirect('/login')
		return response
	
def add_task(request):
	if ('user_id' in request.COOKIES) and ('course_id' in request.POST):
		user_ = User.objects.get(id = request.COOKIES['user_id'])
		task = Task(course_id = request.POST['course_id'], course_id2 = request.POST['course_id2'], user = user_)
		task.save()
		response = HttpResponseRedirect('/user_info')
		return response
	else:
		response = HttpResponseRedirect('/login')
		return response
	
def add_code(request):
	context = get_default_context(request)
	
	codes = VerificationCodeList.objects.filter(code = "").filter(last_ask_time__lt = timezone.now() - timezone.timedelta(0, 30))
	if (len(codes) > 0):
		context['code_path'] = str(codes[0].id) + ".jpg"
		context['code_id'] = codes[0].id
		codes[0].last_ask_time = timezone.now()
		codes[0].save()
	else:
		has_code = False
		for i in range(5):
			os.system("curl http://zhjwxkyw.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1 > static/temp/temp.jpg  2>static/temp/system_output_temp");
			md5_ = UserAction.md5_file("static/temp/temp.jpg")
			if (len(VerificationCodeList.objects.filter(md5 = md5_)) == 0):
				has_code = True
				break
			print "233"
		if has_code:
			md5_ = UserAction.md5_file("static/temp/temp.jpg")
			code = VerificationCodeList(md5 = md5_, last_ask_time = timezone.now())
			code.save()
			context['code_path'] = str(code.id) + ".jpg"
			context['code_id'] = code.id
			os.system("cp static/temp/temp.jpg static/images/codes/" + str(code.id) + ".jpg  2>static/temp/system_output_temp")
		else:
			context['info'] = 'code is enough.'
					
	return render(request, 'add_code.html', context)

def deal_add_code(request):
	if 'code_id' in request.POST:
		code = VerificationCodeList.objects.get(id = request.POST['code_id'])
		code.code = request.POST['code']
		code.save()
		if 'user_id' in request.COOKIES:
			user = User.objects.get(id = request.COOKIES['user_id'])
			user.add_code_times = user.add_code_times + 1
			user.save()
	response = HttpResponseRedirect('/add_code')
	return response
		
def get_default_context(request):
	context = {}
	context['info'] = ''
	if 'user_id' in request.COOKIES:
		context['is_login'] = True
		context['user_id'] = request.COOKIES['user_id']
		context['username'] = User.objects.get(id = request.COOKIES['user_id']).username
	else:
		context['is_login'] = False
	return context

def remove_course(request):
	Task.objects.get(id = request.GET['id']).delete()
	response = HttpResponseRedirect('/user_info')
	return response
	
def test(request):
	action = UserAction(request.COOKIES['user_id'])
	
	b = StringIO.StringIO() 
	c = pycurl.Curl() 
	c.setopt(pycurl.URL, "http://zhjwxkyw.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=rxSearch&p_xnxq=2016-2017-2&tokenPriFlag=rx&is_zyrxk=1")
	c.setopt(pycurl.COOKIEFILE, action.cookie_path)
	c.setopt(pycurl.WRITEFUNCTION, b.write) 
	c.setopt(pycurl.FOLLOWLOCATION, 1) 
	c.setopt(pycurl.MAXREDIRS, 5) 
	c.perform() 
	status = c.getinfo(c.HTTP_CODE) 
	res = b.getvalue()
	posi = res.find('token" value="')

	token = res[posi + 14 : posi + 46]
	context = {}
	context['token'] = token
	return render(request, "test.html", context)

		
		
	