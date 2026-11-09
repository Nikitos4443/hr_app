import yagmail

from hr_core.notifications.INotificationChannel import INotificationChannel


class EmailNotificationChannel(INotificationChannel):
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password

    def send(self, recipient: str, subject: str, body: str) -> None:
        with yagmail.SMTP(self.user, self.password) as smtp:
            smtp.send(to=recipient, subject=subject, contents=body)
