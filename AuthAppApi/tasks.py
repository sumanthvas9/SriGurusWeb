import smtplib
import threading
import time

from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


class RegistrationEmailThread(threading.Thread):
    def __init__(self, user, email_category, token, domain):
        self.user = user
        self.email_category = email_category
        self.token = token
        self.domain = domain
        threading.Thread.__init__(self)

    def run(self):
        if self.email_category == 1:
            mail_subject = 'OTP Verification'
            message = render_to_string('confirm_email_token.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
            message2 = render_to_string('confirm_email2.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
        elif self.email_category == 2:
            mail_subject = 'Confirmation Email'
            message = render_to_string('confirm_email_registration.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
            message2 = render_to_string('confirm_email2.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
        else:
            raise ValueError("Invalid email category passed")
        # email = EmailMessage(subject=mail_subject, body=message, to=[user if anonymous_user else user.email])
        print(self.user.email)
        email = EmailMultiAlternatives(subject=mail_subject, body=message2, to=[self.user.email])
        email.attach_alternative(message, "text/html")
        response = email.send()
        print(response)

    def run2(self):
        if self.email_category == 1:
            mail_subject = 'OTP Verification'
            message = render_to_string('confirm_email_token.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
            message2 = render_to_string('confirm_email2.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
        elif self.email_category == 2:
            mail_subject = 'Confirmation Email'
            message = render_to_string('confirm_email_registration.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
            message2 = render_to_string('confirm_email2.html', {
                'user': self.user,
                'domain': self.domain,
                'token': self.token,
            })
        else:
            raise ValueError("Invalid email category passed")

        msg = MIMEMultipart()
        msg.set_unixfrom('author')
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = [self.user.email]
        msg['Subject'] = mail_subject
        msg.attach(MIMEText(message))

        mail_server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail_server.ehlo()
        mail_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        response = mail_server.sendmail(msg['From'], msg['To'], msg.as_string())
        mail_server.quit()


def send_email_sub(user, email_category, token, domain):
    RegistrationEmailThread(user, email_category, token, domain).run()


class EmailThread(threading.Thread):
    def __init__(self, subject, recipients, email_template, body_content):
        self.subject = subject
        self.recipients = recipients
        self.email_template = email_template
        self.body_content = body_content
        threading.Thread.__init__(self)

    def run(self):
        message = render_to_string(self.email_template, {
            'name': self.body_content['name'], 'content': self.body_content['content']
        })
        email = EmailMultiAlternatives(subject=self.subject, body=message, to=self.recipients)
        email.attach_alternative(message, "text/html")
        email.send()


def send_email_sub2(mail_subject, main_content_body, to):
    EmailThread(mail_subject, to, 'confirm_email_contactus.html', body_content=main_content_body).start()
