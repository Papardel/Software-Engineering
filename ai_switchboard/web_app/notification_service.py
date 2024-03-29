from pynotifier import Notification

Notification(
	title='Notification Title',
	description='Notification Description',
	icon_path='/absolute/path/to/image/icon.png', # On Windows .ico is required, on Linux - .png
	duration=5,                                   # Duration in seconds
	urgency='normal'
).send()