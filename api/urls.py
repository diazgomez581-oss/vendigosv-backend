# Ubicación: api/api/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 👇 Esto envía todo lo de "/api/" al archivo de tu app (donde sí está el router)
    path('api/', include('myapp.urls')), 
]

# Configuración para imágenes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)