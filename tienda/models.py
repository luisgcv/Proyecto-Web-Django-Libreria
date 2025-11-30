from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone



class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True,verbose_name="Rol")

    def __str__(self):
        return self.nombre
    
     #para el panel de administracion
    class Meta:
        verbose_name= "Rol"
        verbose_name_plural="Roles"
        #ordene los ariculos por id
        ordering = ['id']


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=110,unique=True, verbose_name="Nombre_Usuario")
    correo_electronico = models.CharField(max_length=110, verbose_name="Correo Electroncio ")
    password = models.CharField(max_length=110, verbose_name="Contraseña")


    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)


     #para el panel de administracion
    class Meta:
        verbose_name= "Usuario"
        verbose_name_plural="Usuarios"
        #ordene los ariculos por id
        ordering = ['id']

    def __str__(self):
        return f"{self.username} - {self.rol.nombre if self.rol else 'Sin rol'}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True,verbose_name="Categoria")
    descripcion = models.CharField(max_length=300,verbose_name="Descripcion")

    def __str__(self):
        return self.nombre
    
         #para el panel de administracion
    class Meta:
        verbose_name= "Categoria"
        verbose_name_plural="Categorias"
        #ordene los ariculos por id
        ordering = ['id']

class Producto(models.Model):
    nombre = models.CharField(max_length=150,verbose_name="Nombre")
    precio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Precio") 
    cantidad_stock = models.PositiveIntegerField(default=0,verbose_name="Cantidad en Stock")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos',verbose_name="Categoria")
    autor = models.CharField(max_length=150,verbose_name='Autor',default='Sin autor')
    descripcion = models.TextField(max_length=500,verbose_name='Descripcion',default='Sin descripcion')
    fecha_publicacion = models.DateField(default='2000-01-01')
    imagen = models.ImageField(default='null',verbose_name="Imagen",upload_to='productos') 

    
    class Meta:
        verbose_name= "Producto"
        verbose_name_plural="Productos"
        #ordene los ariculos por id
        ordering = ['id']

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model): 

    nombre = models.CharField(max_length=150,verbose_name="Nombre")
    correo_electronico = models.CharField(max_length=110, verbose_name="Correo Electroncio ")
    telefono = PhoneNumberField(verbose_name="Teléfono", region='CR') 
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name= "Cliente"
        verbose_name_plural="Clientes"
        #ordene los ariculos por id
        ordering = ['id']


class Tipo_Venta(models.Model): 
    nombre = models.CharField(max_length=100, unique=True,verbose_name="Categoria")
    descripcion = models.CharField(max_length=300,verbose_name="Descripcion")

    def __str__(self):
        return self.nombre
    
         #para el panel de administracion
    class Meta:
        verbose_name= "Tipo Venta"
        verbose_name_plural="Tipos de Ventas"
        #ordene los ariculos por id
        ordering = ['id']



class Venta(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, verbose_name="Cliente")
    tipo_venta = models.ForeignKey('Tipo_Venta', on_delete=models.PROTECT, verbose_name="Tipo de Venta")
    fecha = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Venta")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']    


class DetalleVenta(models.Model):
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE, verbose_name="Venta")
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")


    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en venta #{self.venta.id}"

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        ordering = ['venta']

    

