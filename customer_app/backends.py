from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):

    def authenticate(self,request,username=None,password=None):
        try:
            user=get_user_model().objects.get(email__iexact=username)
        except:
            return None
        else:
            if user.check_password(password) and user.is_active :
                return user
        return None

