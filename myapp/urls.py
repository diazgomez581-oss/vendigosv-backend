# Ubicación: api/myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ProductoViewSet,
    ImagenViewSet,
    PedidoViewSet,
    DetalleViewSet,
    ProductosPorCategoriaAPIView,
    RegisterAPIView,
    LoginAPIView,
    UserPublicViewSet,
    UserProfileViewSet
)

# ✅ AQUÍ SÍ CREAMOS EL ROUTER
router = DefaultRouter()

# Registramos las rutas
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'imagenes', ImagenViewSet, basename='imagen')
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'detalles', DetalleViewSet, basename='detalle')
router.register(r'users', UserPublicViewSet, basename='user-public')
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', RegisterAPIView.as_view(), name='registro'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('productos/por_categoria/<str:category_id>/', 
         ProductosPorCategoriaAPIView.as_view(), 
         name='productos-por-categoria'),
]