from rest_framework import serializers
from .models import Categoria, Producto, Imagen, Pedido, Detalle, ImagenProducto, Mensaje, UserProfile
from django.contrib.auth.models import User

# --- SERIALIZER SOLO LECTURA PARA USUARIO (solo los campos públicos necesarios) ---
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'address', 'member_since', 'rating', 'products_sold']


# ==========================================
# 0. SERIALIZER PARA REGISTRO DE USUARIOS
# ==========================================
class RegisterSerializer(serializers.Serializer):
    # Accept frontend field names: 'user' (email), 'user_name' (full name), 'password'
    user = serializers.EmailField(write_only=True)
    user_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_user(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo ya está registrado.")
        return value

    def create(self, validated_data):
        email = validated_data.get('user')
        full_name = validated_data.get('user_name', '')
        password = validated_data.get('password')

        # Create a username from email local part or from name
        username_base = email.split('@')[0]
        username = username_base
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{username_base}{counter}"
            counter += 1

        first_name = ''
        last_name = ''
        parts = full_name.strip().split()
        if len(parts) >= 1:
            first_name = parts[0]
        if len(parts) > 1:
            last_name = ' '.join(parts[1:])

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

# ==========================================
# 1. SERIALIZER DE CATEGORÍA (DEBE IR PRIMERO)
# ==========================================
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# ==========================================
# 2. SERIALIZER DE IMAGEN
# ==========================================
class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'

# ==========================================
# 3. SERIALIZER DE IMAGEN PRODUCTO (Galería)
# ==========================================
class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen']

# ==========================================
# 4. SERIALIZERS DE PRODUCTO
# ==========================================
# LECTURA: Usa CategoriaSerializer (que ya está definido arriba ✅)
class ProductoReadSerializer(serializers.ModelSerializer):
    category = CategoriaSerializer(read_only=True)
    imagenes_extra = ImagenProductoSerializer(many=True, read_only=True) 

    class Meta:
        model = Producto
        fields = '__all__'

# ESCRITURA
class ProductoWriteSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    delete_image_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['product_id']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        producto = Producto.objects.create(**validated_data)
        for img in uploaded_images:
            ImagenProducto.objects.create(producto=producto, imagen=img)
        return producto
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        delete_image_ids = validated_data.pop('delete_image_ids', [])
        
        instance = super().update(instance, validated_data)
        
        if delete_image_ids:
            ImagenProducto.objects.filter(id__in=delete_image_ids, producto=instance).delete()
            
        for img in uploaded_images:
            ImagenProducto.objects.create(producto=instance, imagen=img)
        return instance

# ==========================================
# 5. SERIALIZERS DE DETALLE (Mover arriba de Pedido)
# ==========================================
class DetalleReadSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.product_name', read_only=True)
    class Meta:
        model = Detalle
        fields = ['producto', 'producto_nombre', 'cantidad', 'precio_unidad']

class DetalleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle
        fields = '__all__'

# ==========================================
# 6. SERIALIZERS DE PEDIDO
# ==========================================
class PedidoReadSerializer(serializers.ModelSerializer):
    detalles = DetalleReadSerializer(many=True, read_only=True) 
    class Meta:
        model = Pedido
        fields = ['id', 'fecha_pedido', 'monto_total', 'estado', 'comentario', 'detalles']

class PedidoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'estado', 'comentario']
        read_only_fields = ['id']

# ==========================================
# 7. SERIALIZER DE MENSAJE
# ==========================================
class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'