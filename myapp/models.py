import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Perfil de usuario extendido (OneToOne con auth_user)
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    member_since = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, null=True, blank=True)
    products_sold = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'myapp_user_profile'

    def __str__(self):
        return f"Perfil de {self.user.username}"

# ==========================
# 1. MODELO CATEGORIA 
# ==========================
class Categoria(models.Model):
    category_id = models.CharField(
        primary_key=True, 
        max_length=36, 
        db_column='category_id' 
    )
    category_name = models.CharField(
        max_length=40, 
        db_column='category_name'
    )

    class Meta:
        managed = False       
        db_table = 'categoria' 
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.category_name

# ==========================
# 2. MODELO PRODUCTO
# ==========================
class Producto(models.Model):
    # CORRECCIÓN 1: Regresamos a CharField para el ID (Más rápido y seguro)
    product_id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4, 
        editable=False
    )
    
    image = models.ImageField(upload_to='productos/%Y/%m/%d/', blank=True, null=True)
    
    category = models.ForeignKey(
        Categoria, 
        models.DO_NOTHING, 
        db_column='category_id', 
        blank=True, 
        null=True
    )
    
    id_user = models.IntegerField(db_column='id_user', blank=True, null=True)
    
    product_name = models.CharField(max_length=50)

    # CORRECCIÓN 2: TextField SIN límite de longitud para textos largos
    description = models.TextField(blank=True, null=True)

    state = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True 
        db_table = 'myapp_producto' 

    def __str__(self):
        return self.product_name
# ==========================
# 2.1 NUEVO MODELO: Galería de Imágenes (Va DESPUÉS de Producto)
# ==========================
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes_extra', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/galeria/%Y/%m/%d/')

    class Meta:
        managed = True
        db_table = 'myapp_imagen_producto'

# ==========================
# 3. OTROS (Legacy)
# ==========================
class Imagen(models.Model):
    class Meta:
        managed = False
        db_table = 'imagen' 

# ==========================
# 4. MODELO PEDIDO
# ==========================
ESTADO_CHOICES = [
    ('Pendiente', 'Pendiente'),
    ('Completado', 'Completado'),
    ('Cancelado', 'Cancelado'),
]

class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Pendiente', choices=ESTADO_CHOICES)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'myapp_pedido' 
        managed = True 
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

# ==========================
# 5. MODELO DETALLE
# ==========================
class Detalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'myapp_detalle'
        managed = True 
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedido'
        unique_together = (('pedido', 'producto'),)
        
        
        # modelo mensajes   

# ... tus modelos anteriores (Pedido, Detalle, etc.) ...

# ... tus modelos anteriores (Pedido, Detalle, etc.) ...

# ✅ 1. AGREGAMOS EL MODELO VENDEDOR (Necesario para el chat)
class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='vendedores/', blank=True, null=True)
    # No ponemos usuario/password, es solo un perfil público
    
    class Meta:
        managed = True
        db_table = 'myapp_vendedor'
    
    def __str__(self):
        return self.nombre

# ✅ 2. EL MODELO MENSAJE (Ahora sí funcionará)
class Mensaje(models.Model):
    # Ahora Python ya conoce la clase 'Vendedor' de arriba
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='mensajes')
    cliente_id = models.IntegerField() # ID del usuario simulado
    
    # Opcional: Si quieres relacionarlo con un producto
    producto = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True)
    
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    es_vendedor = models.BooleanField(default=False) 

    class Meta:
        managed = True
        db_table = 'myapp_mensaje'