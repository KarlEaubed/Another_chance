from django.contrib.auth.backends import ModelBackend
from .models import User_Standard

class UserStandardBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User_Standard.objects.get(username=username)
            if user.check_password(password):
                return user
        except User_Standard.DoesNotExist:
            return None
