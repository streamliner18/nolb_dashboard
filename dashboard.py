import ui
import console

from car import car


def log_item(view, item):
    view['txt_log'].text += '\n' + str(item)

@ui.in_background
def sw_connect_action(sender):
	global_activity.start()
	try:
        log_item(sender.superview, 'Connecting')
		car.connect(ip_addr=sender.superview['txt_ip_addr'].text,really=sender.value)
		console.hud_alert('Connection '+('Established' if sender.value else 'Ended'))
        log_item(sender.superview, 'Connected' if sender.value else 'Disconnected')
	except Exception as e:
		console.hud_alert('Could not '+('establish ' if sender.value else 'terminate ')+'connection: '+str(e),'error',0.25)
        log_item(sender.superview, e);
		sender.value = not sender.value
	global_activity.stop()


def sw_turn_action(sender):
	global_activity.start()
	try:
        log_item(sender.superview, 'heading/set-relative?value={}'.format(sender.angle))
		car.exec_function('heading/set-relative', value=sender.angle)
	except Exception as e:
		console.hud_alert(str(e),'error',0.25)
	global_activity.stop()

def sw_steer_action(sender):
    global_activity.start()
    try:
        speed = sender.superview['slide_speed'].value
        log_item(sender.superview, 'speed/set-absolute?value={}'.format(speed))
        car.exec_function('speed/set-absolute', speed=str(speed))
    except Exception as e:
        console.hud_alert(str(e),'error',0.25)
    global_activity.stop()

def sw_stop_action(sender):
    global_activity.start()
    try:
        log_item(sender.superview, 'speed/set-absolute?value=0')
        car.exec_function('speed/set-absolute', speed=0)
    except Exception as e:
        console.hud_alert(str(e),'error',0.25)
    global_activity.stop()

def sw_clear_log(sender):
    sender.superview['txt_log'].text = ''

v = ui.load_view()
global_activity = ui.ActivityIndicator()
global_activity.hides_when_stopped = True
global_activity.style = ui.ACTIVITY_INDICATOR_STYLE_GRAY
global_activity.center = v.width - 90, 80
v.add_subview(global_activity)
v.present('full_screen', orientations=["landscape-right"])


