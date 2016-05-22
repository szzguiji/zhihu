from models import NewUser

class MyBackend:  
  
    def authenticate(self, email=None, password=None):
        try:
            user = NewUser.objects.get(email=email)
        except NewUser.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None
    def get_user(self, user_id):
        try:
            return NewUser.objects.get(pk=user_id)
        except NewUser.DoesNotExist:
            return None