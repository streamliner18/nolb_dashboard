import requests as q
from requests import Session, get
from simplejson import loads

class Car():
	def __init__(self):
		self.connected = False
	def connect(self,ip_addr='', really=False):
		if really:
			self.session = Session()
			r = self.session.get('http://'+ip_addr+'/status')
			assert r.status_code == 200
			self.connected = True
			self.ip_addr = 'http://'+ip_addr+'/'
		else:
			self.session = None
			self.connected = False
	def exec_function(self, action, **kwargs):
		assert self.connected
		connection_string = self.ip_addr+action
		if len(kwargs) > 0:
			connection_string += '?' + ','.join([k+'='+v for k,v in kwargs.items()])
		r = self.session.get(connection_string);
		assert r.status_code == 200
		return loads(r.content)
		
			
car = Car()
