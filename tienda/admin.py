from django.contrib import admin
from tienda.models import Usuario, Producto, Categoria, Cliente, Tipo_Venta, DetalleVenta, Rol, Venta

#admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Tipo_Venta)
admin.site.register(DetalleVenta)
admin.site.register(Rol)
admin.site.register(Venta)

# Register your models here.
