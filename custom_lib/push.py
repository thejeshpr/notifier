from custom_lib import WirePusher

wp = WirePusher.WirePusher
notification = WirePusher.Notification

class Push(object):
    def __init__(self, id):
        self.id = id
        self.ref = wp(id)

    def push(self, title, message, notification_type="", action="", message_id=""):
        new = notification(
            title=title,
            message=message,
            notification_type=notification_type,
            action=action,
            message_id=message_id
        )
        self.ref.push(new)