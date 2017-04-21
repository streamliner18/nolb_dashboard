import requests as q
from requests import Session, get
from simplejson import loads

class Car():
	def __init__(self):
		self.connected = False
		self.executing = False
		self.speed = 0
		self.steps = 0
		self.obstacle = 0
	def connect(self,ip_addr='', really=False):
		if really and (not self.executing):
			self.session = Session()
			self.executing = True
			r = self.session.get('http://'+ip_addr+'/status')
			self.executing = False
			assert r.status_code == 200
			try:
				data = loads(r.content)
				self.steps = data['steps']
				self.obstacle	= data['obstacle']
			except: pass
			self.connected = True
			self.ip_addr = 'http://'+ip_addr+'/'
		else:
			self.session = None
			self.connected = False
			
	def exec_function(self, action, **kwargs):
		assert self.connected and not self.executing
		connection_string = self.ip_addr+action
		if len(kwargs) > 0:
			connection_string += '?' + ','.join([k+'='+v for k,v in kwargs.items()])
		try:
			self.executing = True
			r = self.session.get(connection_string);
			self.executing = False
		except Exception as e:
			self.executing = False
			raise(e)
		assert r.status_code == 200
		return loads(r.content)

	def reload_status(self, nc=False):
		action = 'status-nc' if nc else 'status'
		data = self.exec_function(action)
		self.steps = data['steps-traversed']
		self.obstacle	= data['obstacle']
		
	def reload_speed(self):
		data = self.exec_function('speed')
		self.speed = data['speed']
			
car = Car()
