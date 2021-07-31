import random
import string

# from authy.api import AuthyApiClient
from django.conf import settings
from django.http import HttpResponse

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from AuthApp.models import EmailDirectory
from AuthAppApi import tasks


# authy_api = AuthyApiClient(settings.TWILIO_AUTH_TOKEN)


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def get_random_numeric_string(length):
    letters = string.digits
    result_str = ''.join((random.choice(letters) for i in range(length)))
    return result_str


class EmailHandling:

    def send_email(self, email_type, user, domain, **kwargs):
        print("Email Handling")
        otp = get_random_numeric_string(4)
        self.store_email_entry(user=user, email_type=email_type, otp=otp)
        tasks.send_email_sub(user, 1, otp, domain)

    @staticmethod
    def store_email_entry(user, email_type, otp):
        if email_type is None:
            raise ValueError("Internal Server Error. Email Type passed is empty.")
        filter_dict = {'user': user,
                       'isActive': True,
                       # type: email_type
                       }
        EmailDirectory.objects.filter(**filter_dict).update(isActive=False)
        entry = EmailDirectory(user=user, type=email_type, otpCode=otp)
        entry.save()


class SmsHandling:
    def send_sms(self, email_type, user, domain):
        print("SMS Handling")
        r = MessagingResponse()
        r.message('Hello from your Django app!')
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            otp = get_random_numeric_string(4)
            EmailHandling.store_email_entry(user=user, email_type=email_type, otp=otp)
            print(user.phoneNumber)
            message = client.messages.create(from_=settings.TWILIO_NUMBER, to="+91" + user.phoneNumber,
                                             body="Please find otp for your request from {0} : {1}".format(*[domain, otp]))
            print(print(message.sid))
            return r
        except TwilioRestException as ex:
            print(ex)
            return HttpResponse(ex)

    def validate_otp(self, phone_number, otp):
        # authy_api.phones.verification_start(
        #     phone_number,
        #     "+91",
        #     via=otp
        # )
        return True
