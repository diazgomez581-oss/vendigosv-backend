# myapp/views.py (Código Final Corregido)

from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404 

from .models import Categoria, Producto, Imagen, Pedido, Detalle, UserProfile
from .serializers import (
    CategoriaSerializer,
    ProductoReadSerializer,
    ProductoWriteSerializer,
    ImagenSerializer,
    PedidoReadSerializer,  
    PedidoWriteSerializer,
    DetalleReadSerializer,
    DetalleWriteSerializer,
    RegisterSerializer,
    UserPublicSerializer,
    UserProfileSerializer
)
from rest_framework.permissions import IsAuthenticated

# ==========================================
# 0. VISTA SOLO LECTURA DE USUARIOS (PÚBLICA)
# ==========================================
from django.contrib.auth import get_user_model

class UserPublicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserPublicSerializer

# ==========================================
# 1. VISTA DE CATEGORÍAS 
# ==========================================
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ==========================
# 2. VISTA DE PRODUCTOS (CORRECCIÓN FINAL DE BÚSQUEDA)
# ==========================
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    
    filter_backends = [SearchFilter] 
    

    # 3. Define la búsqueda de texto SOLO en el nombre del producto
    search_fields = ['product_name']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductoReadSerializer
        return ProductoWriteSerializer
    
# ==========================
# 3. VISTA DE IMAGENES
# ==========================
class ImagenViewSet(viewsets.ModelViewSet):
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer

# ==========================
# 4. VISTA DE PEDIDOS
# ==========================
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PedidoReadSerializer 
        return PedidoWriteSerializer

# ==========================
# 5. VISTA DE DETALLES
# ==========================
class DetalleViewSet(viewsets.ModelViewSet):
    queryset = Detalle.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DetalleReadSerializer
        return DetalleWriteSerializer
    

    # ==========================
# 6. NUEVA VISTA: FILTRADO POR CATEGORÍA
# ==========================
class ProductosPorCategoriaAPIView(generics.ListAPIView):
    """
    Devuelve la lista de productos filtrados por una Category ID específica.
    Ruta de ejemplo: /api/productos/por_categoria/ID_DE_CATEGORIA/
    """
    serializer_class = ProductoReadSerializer

    def get_queryset(self):
        # 1. Obtiene el ID de la categoría de la URL
        category_id = self.kwargs['category_id']
        
        # 2. Filtra la tabla de Productos donde la clave foránea coincida
        # Esto evita que choquen los filtros de DRF y usa la consulta directa de Django
        queryset = Producto.objects.filter(category__category_id=category_id)
        
        return queryset


# ==========================================
# 7. VISTA PARA REGISTRO DE USUARIOS
# ==========================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegisterAPIView(APIView):
    """Permite crear un usuario nuevo vía POST.

    Espera: username, email, password, first_name (opcional), last_name (opcional)
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logging.getLogger('django.request').info(f"Registro request headers: {dict(request.headers)} from {request.META.get('REMOTE_ADDR')}")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado correctamente."}, status=status.HTTP_201_CREATED)

        # Normalizar errores a un único campo 'error' (el frontend actual lo espera así)
        errors = serializer.errors
        error_text = ''
        if isinstance(errors, dict):
            first = next(iter(errors.values()))
            if isinstance(first, list) and first:
                error_text = str(first[0])
            else:
                error_text = str(first)
        else:
            error_text = str(errors)

        return Response({"error": error_text}, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# 8. VISTA PARA LOGIN (TOKEN)
# ==========================================
class LoginAPIView(APIView):
    """Login que acepta 'user' (email o username) y 'password'.

    Devuelve token en caso de credenciales válidas y un mensaje de error en caso contrario.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logging.getLogger('django.request').info(f"Login request headers: {dict(request.headers)} from {request.META.get('REMOTE_ADDR')}; body: {request.data}")
        data = request.data
        user_input = data.get('user') or data.get('username')
        password = data.get('password')

        if not user_input or not password:
            return Response({"error": "Se requieren usuario y contraseña."}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        # Intentar primero por email
        user = User.objects.filter(email__iexact=user_input).first()
        if not user:
            # Intentar por username
            user = User.objects.filter(username__iexact=user_input).first()

        if not user or not user.check_password(password):
            return Response({"error": "Credenciales inválidas. Por favor verifica tu usuario/contraseña."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token, _ = Token.objects.get_or_create(user=user)
            token_key = token.key
        except Exception:
            # Si la tabla de tokens no existe (migrations pendientes), devolver sin token
            token_key = None

        resp = {
            "token": token_key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
        if token_key is None:
            resp["warning"] = "Token no disponible: ejecuta 'python manage.py migrate' para habilitar tokens."

        return Response(resp, status=status.HTTP_200_OK)


# ==========================================
# 9. VISTA DE PERFIL DE USUARIO
# ==========================================
from rest_framework.decorators import action
from rest_framework.response import Response

class UserProfileViewSet(viewsets.ViewSet):
    """ViewSet para gestionar el perfil del usuario autenticado.
    
    GET /api/user-profiles/me/ - Obtiene el perfil del usuario autenticado
    PATCH /api/user-profiles/me/ - Actualiza el perfil del usuario autenticado
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def get_or_update_profile(self, request):
        """Obtiene o actualiza el perfil del usuario autenticado."""
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
        except Exception as e:
            return Response(
                {"error": f"Error al obtener el perfil: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    