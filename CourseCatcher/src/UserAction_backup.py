import pycurl 
import StringIO 
import os
import urllib
import certifi
from Main.models import User
from Main.models import VerificationCodeList
from Main.models import Task
from hashlib import md5
from django.db.models import Q  
import datetime

class UserAction:
	def __init__(self, id):
		self.id = id
		self.user = self.__get_user(id)
		self.cookie_path = './datas/cookies/cookie' + str(self.id) + '.txt'
	
	def __get_code(self, is_login):
		code = ""
		for i in range(10):
			if (is_login == True):
				os.system("curl -b " + self.cookie_path + " http://zhjwxkyw.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1 > static/temp/" + str(self.id) + "/temp_login.jpg  2>static/temp/" + str(self.id) + "/system_output_temp");
			else:
				os.system("curl -b " + self.cookie_path + " http://zhjwxkyw.cic.tsinghua.edu.cn/login-jcaptcah.jpg > static/temp/" + str(self.id) + "/temp_login.jpg  2>static/temp/" + str(self.id) + "/system_output_temp");
			md5_ = UserAction.md5_file("static/temp/" + str(self.id) + "/temp_login.jpg")
			if (len(VerificationCodeList.objects.filter(md5 = md5_).filter(~Q(code = ''))) > 0):
				code = VerificationCodeList.objects.get(md5 = md5_).code
				break
		return code
		
	
	def login(self):
		code = self.__get_code(True);
		if code == '':
			return False
		os.system("curl -b " + self.cookie_path + " http://zhjwxkyw.cic.tsinghua.edu.cn/xklogin.do > static/temp/" + str(self.id) + "/res.html 2>static/temp/" + str(self.id) + "/system_output_temp");
		b = StringIO.StringIO() 
		c = pycurl.Curl() 
		
		url = "https://zhjwxkyw.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do"
		filds = {"_login_image_":code,"captchaflag":"login1","j_password":self.user.password,"j_username":self.user.username}
		#print urllib.urlencode(filds)
		c.setopt(pycurl.URL, url) 
		c.setopt(pycurl.CUSTOMREQUEST, "POST")
		c.setopt(pycurl.POSTFIELDS, urllib.urlencode(filds)) 
		c.setopt(pycurl.COOKIEFILE, self.cookie_path)
		c.setopt(pycurl.SSL_VERIFYPEER, 0)   
		c.setopt(pycurl.SSL_VERIFYHOST, 0)

		c.setopt(pycurl.WRITEFUNCTION, b.write) 
		c.setopt(pycurl.FOLLOWLOCATION, 1) 
		c.setopt(pycurl.MAXREDIRS, 5) 
		c.perform() 
		status = c.getinfo(c.HTTP_CODE) 
		#print b.getvalue() 
		b.close() 
		c.close()
		
		b = StringIO.StringIO() 
		c = pycurl.Curl() 
		c.setopt(pycurl.URL, "http://zhjwxkyw.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=tySearch&p_xnxq=2016-2017-2&tokenPriFlag=ty")
		c.setopt(pycurl.COOKIEFILE, self.cookie_path)
		c.setopt(pycurl.WRITEFUNCTION, b.write) 
		c.setopt(pycurl.FOLLOWLOCATION, 1) 
		c.setopt(pycurl.MAXREDIRS, 5) 
		c.perform() 
		status = c.getinfo(c.HTTP_CODE) 
		#print b.getvalue() 
		b.close() 
		c.close()
		return True
	
	def get_cookie(self):
		c = pycurl.Curl() 
	
		b = StringIO.StringIO() 
		c.setopt(pycurl.URL, "http://zhjwxkyw.cic.tsinghua.edu.cn/xsxk_index.jsp") 
		c.setopt(pycurl.COOKIEJAR, self.cookie_path)
		c.setopt(pycurl.HTTPHEADER, ["Accept:"]) 
		c.setopt(pycurl.FOLLOWLOCATION, 1) 
		c.setopt(pycurl.MAXREDIRS, 5) 
		c.setopt(pycurl.WRITEFUNCTION, b.write) 
		c.perform() 
		
		c.close()
		
	def select_course(self, code):		
		b = StringIO.StringIO() 
		c = pycurl.Curl() 
		c.setopt(pycurl.URL, "http://zhjwxkyw.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=rxSearch&p_xnxq=2016-2017-2&tokenPriFlag=rx&is_zyrxk=1")
		c.setopt(pycurl.COOKIEFILE, self.cookie_path)
		c.setopt(pycurl.WRITEFUNCTION, b.write) 
		c.setopt(pycurl.FOLLOWLOCATION, 1) 
		c.setopt(pycurl.MAXREDIRS, 5) 
		c.perform() 
		status = c.getinfo(c.HTTP_CODE) 
		res = b.getvalue()
		posi = res.find('token" value="')
		
		if (posi == -1):
			return False
		
		token = res[posi + 14 : posi + 46]
		b.close() 
		c.close()
		tasks = User.objects.get(id = self.id).task_set.all()
		b = StringIO.StringIO() 
		c = pycurl.Curl() 
		c.setopt(pycurl.URL, "http://zhjwxkyw.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do")
		c.setopt(pycurl.COOKIEFILE, self.cookie_path)
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1) 
		c.setopt(pycurl.MAXREDIRS, 5)
		
		query = "m=saveRxKc&page=&token=" + token + "&p_sort.p1=&p_sort.p2=&p_sort.asc1=true&p_sort.asc2=true&p_xnxq=2016-2017-2&is_zyrxk=&tokenPriFlag=rx&p_kch=" + tasks[0].course_id + "&p_kcm=&p_kkdwnm=&p_kctsm=&p_rxklxm=";
		for task in tasks:
			task.try_times = task.try_times + 1
			task.save()
			query += "&p_rx_id=2016-2017-2;" + task.course_id + ";" + task.course_id2 + ";"
			#!!!!vvvv
			#query += "&p_rx_xkzy=3"
		query += "&goPageNumber=1";
		if code != "":
			query += "&j_captcha_bks_xk=" + code
			
		#print query
		c.setopt(pycurl.POSTFIELDS, query) 
		c.perform() 
		status = c.getinfo(c.HTTP_CODE) 
		res = b.getvalue()
		b.close() 
		c.close()
		if res.find("j_captcha_bks_xk") != -1:
			print '[need code]'
			if code != "":
				return False
			code = self.__get_code(False);
			if code == '':
				return False
			return self.select_course(code)
			
		
		return True
	
	def check_course(self):
		b = StringIO.StringIO() 
		c = pycurl.Curl() 
		url = "http://zhjwxkyw.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=kbSearch&p_xnxq=2016-2017-2&pathContent=Registered%20primary%20course%20schedule"
		c.setopt(pycurl.URL, url) 
		c.setopt(pycurl.CUSTOMREQUEST, "GET")
		c.setopt(pycurl.COOKIEFILE, self.cookie_path)

		c.setopt(pycurl.WRITEFUNCTION, b.write) 
		c.setopt(pycurl.FOLLOWLOCATION, 1) 
		c.setopt(pycurl.MAXREDIRS, 5) 
		c.perform() 
		res = b.getvalue() 
		b.close() 
		c.close()
		
		if res.find('<table') == -1:
			return False
		else:
			tasks = User.objects.get(id = self.id).task_set.all()
			for task in tasks:
				task.selected = not (res.find(str(task.course_id)) == -1)
				task.save()
			return True
	
	def __get_user(self, id_):
		return User.objects.get(id = id_) 

	@staticmethod
	def md5_file(name):
		m = md5()
		a_file = open(name, 'rb')   
		m.update(a_file.read())
		a_file.close()
		return m.hexdigest()