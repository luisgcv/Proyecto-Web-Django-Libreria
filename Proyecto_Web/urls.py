"""
URL configuration for Proyecto_Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tienda import views
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.carga_inicio_sesion,name='inicio_sesion'),
    path('login/',views.login,name='login'),
    path('crear-cuenta/',views.carga_pagina_crear_cuenta,name='registro'),
    path('guardar-usuario/',views.guardar_nuevo_usuario,name='guardar_usuario'),
    path('home/',views.home,name='home'),
    path('crear-producto/',views.carga_pagina_crear_producto,name='crear_producto'),
    path('listar-productos/',views.carga_pagina_ver_productos,name='listar_productos'), 
    path('crear-categoria/',views.carga_pagina_crear_categoria,name='crear_categoria'),
    path('listar-categorias/',views.carga_pagina_listar_categorias,name='listar_categorias'), 
    path('borrar-producto/<int:id>',views.borrar_producto,name='borrar_producto'),
    path('editar-producto/',views.editar_producto,name='editar_producto'),
    path('guardar-producto/',views.guardar_producto,name='guardar_producto'),
    path('editar-categoria/',views.editar_categoria,name="editar_categoria"),
    path('guardar-categoria/',views.guardar_categoria,name="guardar_categoria"),
    path('crear-cliente/',views.crear_cliente,name="crear_cliente"),
    path('listar-cliente/',views.listar_clientes,name="listar_clientes"), 
    path('ventas-asociadas-cliente/',views.ventas_asociadas_clientes,name="ventas_asociadas_cliente"), 
    path('guardar-cliente/',views.guardar_cliente,name="guardar_cliente"),
    path('editar-cliente/',views.editar_cliente,name='editar_cliente'),
    path('borrar-cliente/<int:id>',views.borrar_cliente,name="borrar_cliente"),
    path('crear-ventas/', views.crear_venta, name='crear_venta'),
    path('listar-ventas/',views.ver_ventas,name='listar_ventas'),
    path('guardar-venta/',views.guardar_venta,name='guardar_venta'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('ventas/factura/<int:venta_id>/', views.generar_factura, name='generar_factura'),
    path('crear_tipo_venta/', views.crear_tipo_venta, name='crear_tipo_venta'),
    path('listar_tipos_venta/', views.listar_tipos_venta, name='listar_tipos_venta'),
    path('ventas/editar_tipo_venta/', views.editar_tipo_venta, name='editar_tipo_venta'),
    path('logout/', views.logout_view, name='logout'),


]

#Configuración para cargar imagenes
#Hay que validar si el proyecto está en modo debug
#Si estuvieramos en producción funcionaria directamente
if settings.DEBUG:
    #vamos a importar solamente cuando lo necesitamos
    # para tener accesible la funcion static que permitira cargar 
    # la url a un archivo estatico que pueda leer el framework
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )


 
