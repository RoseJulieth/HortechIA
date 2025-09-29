from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

class EmailBackend(BaseBackend):
    """
    Backend de autenticación personalizado que permite login con email
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # Buscar usuario por email o username
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
                
            # Verificar contraseña
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None