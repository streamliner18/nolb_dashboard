import ui
import console

from car import car


@ui.in_background
def sw_connect_action(sender):
	global_activity.start()
	try:
		car.connect(ip_addr=sender.superview['txt_ip_addr'].text,really=sender.value)
		console.hud_alert('Connection '+('Established' if sender.value else 'Ended'))
	except Exception as e:
		console.hud_alert('Could not '+('establish ' if sender.value else 'terminate ')+'connection: '+str(e))
		sender.value = not sender.value
	global_activity.stop()

def sw_turn_action(sender):
	global_activity.start()
	try:
		car.exec_function('heading/set-relative', value=sender.angle)
	except Exception as e:
		console.hud_alert(str(e))
	global_activity.stop()

v = ui.load_view()
global_activity = ui.ActivityIndicator()
global_activity.hides_when_stopped = True
global_activity.style = ui.ACTIVITY_INDICATOR_STYLE_GRAY
global_activity.center = v.width - 90, 80
v.add_subview(global_activity)
v.present('full_screen', orientations=["landscape-right"])


