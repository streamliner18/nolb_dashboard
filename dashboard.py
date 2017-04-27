import ui
import console

from car import car


def log_item(view, item):
    view['txt_log'].text += '\n' + str(item)

def redraw_status(v):
	v['lbl_speed'].text = str(car.speed)
	v['lbl_steps'].text = str(car.steps)
	if car.obstacle == 0:
		v['img_tcas_normal'].alpha = 1
		v['img_tcas_triggered'].alpha = 0
	else:
		v['img_tcas_normal'].alpha = 0
		v['img_tcas_triggered'].alpha = 1
	if car.state == '':
		v['lbl_state'].border_color = 'blue'
		v['lbl_state'].text = 'NOMINAL'
	elif car.state == 'data':
		v['lbl_state'].border_color = 'red'
		v['lbl_state'].text = 'DATA_CORRUPT'
	else:
		v['lbl_state'].border_color = 'yellow'
		v['lbl_state'].text = car.state

@ui.in_background
def sw_connect_action(sender):
	global_activity.start()
	try:
		log_item(sender.superview, 'Connecting')
		car.connect(ip_addr=sender.superview['txt_ip_addr'].text,really=sender.value)
		console.hud_alert('Connection '+('Established' if sender.value else 'Ended'), 'success',0.25)
		redraw_status(sender.superview)
		log_item(sender.superview, 'Connected' if sender.value else 'Disconnected')
	except Exception as e:
		console.hud_alert('Could not '+('establish ' if sender.value else 'terminate ')+'connection: '+str(e),'error',0.25)
		log_item(sender.superview, e);
		sender.value = not sender.value
		car.state = 'Connection Failed'
	global_activity.stop()
	redraw_status(sender.superview)


@ui.in_background
def sw_turn_action(sender):
	global_activity.start()
	try:
		log_item(sender.superview, 'heading/set-relative?value={}'.format(sender.angle))
		r = car.exec_function('heading/set-relative', value=sender.angle)
		log_item(sender.superview, r)
	except Exception as e:
		console.hud_alert(e.__repr__(),'error',0.25)
		car.state = 'Exception'
	global_activity.stop()
	redraw_status(sender.superview)

@ui.in_background
def sw_steer_action(sender):
	global_activity.start()
	try:
		# speed = sender.superview['slide_speed'].value
		speed = int(sender.superview['lbl_speed_f'].text)
		car.speed = speed
		log_item(sender.superview, 'speed/set-absolute?value={}'.format(speed))
		r = car.exec_function('speed/set-absolute', value=str(speed))
		log_item(sender.superview, r)
	except Exception as e:
		console.hud_alert(e.__repr__()+': '+e.__str__(),'error',0.25)
		car.state = 'Exception'
	global_activity.stop()
	redraw_status(sender.superview)

@ui.in_background
def sw_stop_action(sender):
	global_activity.start()
	try:
		log_item(sender.superview, 'speed/set-absolute?value=0')
		car.speed = 0
		r = car.exec_function('speed/set-absolute', value='0')
		log_item(sender.superview, r)
	except Exception as e:
		console.hud_alert(e.__repr__(),'error',0.25)
		car.state = 'Exception'
	global_activity.stop()
	redraw_status(sender.superview)

def sw_clear_log_action(sender):
	sender.superview['txt_log'].text = ''
	
@ui.in_background
def sw_update_action(sender):
	global_activity.start()
	try:
		log_item(sender.superview, '/status'+('-nc' if sender.nc else ''))
		r = car.reload_status(nc=sender.nc)
		log_item(sender.superview, r)
		redraw_status(sender.superview)
		car.reload_speed()
	except Exception as e:
		console.hud_alert(e.__repr__(),'error',0.25)
		car.state = 'Exception'
	redraw_status(sender.superview)
	global_activity.stop()
	
@ui.in_background
def sl_speed_action(sender):
	v = int(sender.value * 10)
	sender.superview['lbl_speed_f'].text = str([-8,-7,-6,-5,-4,0,4,5,6,7,8][v])
	
@ui.in_background
def sw_general_action(sender):
	global_activity.start()
	try:
		log_item(sender.superview, sender.endpoint)
		r = car.exec_function(sender.endpoint)
		log_item(sender.superview, r)
	except Exception as e:
		log_item(sender.superview, e)
		car.state = 'Exception'
	global_activity.stop()
	redraw_status(sender.superview)

v = ui.load_view()
global_activity = ui.ActivityIndicator()
global_activity.hides_when_stopped = True
global_activity.style = ui.ACTIVITY_INDICATOR_STYLE_GRAY
global_activity.center = v.width - 90, 80
v.add_subview(global_activity)
v.present('full_screen', orientations=["landscape-right"])


