import requests


class Notification(object):
    """
    Base class of notification type
    """
    def __init__(self, title, message, notification_type="", action="", message_id=""):
        """
        Init notification class
        :param title(*): the title that will be shown in the notification drawer
        :param message(*):  body or content of the notification
        :param notification_type: defines the ring tone, icon and vibration pattern for the notification, you can define
         the types on your mobile phone under "Types"
        :param action: what intent should be triggered when clicking the notification, in the form of URI
        :param message_id: (an integer) with this parameter you can overwrite a previous notification sent to your phone
         (if it's still showing in your notification drawer), if not specified then no notification will be overwritten
        """
        self.title = title
        self.message = message
        self.type = notification_type
        self.action = action
        self.message_id = message_id

    def __repr__(self):
        return [self.title, self.message, self.type, self.action, self.message_id]


class DefaultNotification(Notification):
    """
    Default type of notification
    """
    def __init__(self):
        super().__init__(title="Default title", message="Default message")


class WirePusher(object):
    def __init__(self, client_id):
        """
        :param client_id:
        """
        self.__id = client_id
        self.__notification = []
        self.__url = f'https://wirepusher.com/send?id={self.__id}'

    def __str__(self):
        return self.__url

    def load_notification(self, notification):
        """
        load notification without push it
        :param notification: class Notification
        :return: None
        """
        self.__url += f'&title={notification.title}'

    def push(self, notification=DefaultNotification()):
        """
        Used to send a notification to self.id
        :param notification: class Notification
        :return: None
        """
        params = {
            'title': notification.title,
            'message': notification.message,
            'type': notification.type,
            'action': notification.action,
            'message_id': notification.message,
        }
        try:
            req = requests.get(self.__url, params=params)
            print(req.text)
        except Exception as e:
            print(e)


r = WirePusher('mpgF5')

new = Notification('test title', 'test message')

r.push(new)