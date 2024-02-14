from pushbullet import Pushbullet

pb = Pushbullet("o.6czRw87kttwIY8d6z9jkKyb8ZYEcXX36")

def Send_Notif(title, message):
    # Iterate over all connected devices and send notifications if they're online
    for device in pb.devices:
        if device.is_online():
            device.push_note(title, message)
            # print(f"Notification sent to {device.name}")