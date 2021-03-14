import random
import string

from AuthApp.models import EmailDirectory
from AuthAppApi import tasks


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
