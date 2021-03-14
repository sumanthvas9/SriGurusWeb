from django.contrib.auth.base_user import BaseUserManager


# class UserManager(BaseUserManager):
#
#     def create_superuser(self, email, password, **extra_fields):
#         if password is None:
#             raise TypeError('Superusers must have a password.')
#
#         user = self.create_user(email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#
#         return user
