from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

# Obtenemos el modelo de usuario por defecto (auth_user)
User = get_user_model() 

class CustomHeaderAuthentication(BaseAuthentication):
    """
    Autenticación personalizada que revisa el header 'X-User-Id' para
    encontrar y autenticar a un usuario, permitiendo pasar el chequeo 
    de permisos de DRF.
    """
    def authenticate(self, request):
        user_id = request.headers.get('X-User-Id')

        if not user_id:
            # Si el header no existe, la autenticación falla (pasa al siguiente método)
            return None 

        try:
            # Intentamos convertir la ID a entero y buscar el usuario en auth_user
            user_id = int(user_id)
            user = User.objects.get(pk=user_id)
        except (ValueError, User.DoesNotExist):
            # Si la ID es inválida o el usuario no existe, lanzamos un error de autenticación
            raise AuthenticationFailed('Invalid user ID provided in X-User-Id header.')

        # Si encontramos al usuario, lo devolvemos junto con None (token/auth data)
        # Esto establece request.user = user para las vistas de DRF.
        return (user, None)
