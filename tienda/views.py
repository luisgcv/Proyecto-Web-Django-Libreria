from django.shortcuts import render,redirect
from tienda.forms import LoginForm,Sign_up_Form,Crear_Producto,Crear_Categoria,Crear_Cliente, Crear_Tipo_Venta
from tienda.models import Usuario,Rol,Producto,Categoria,Cliente,Venta,DetalleVenta,Tipo_Venta
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.db.models.signals import post_migrate



# Create your views here.

def logout_view(request):
    request.session.flush()
    return redirect('login')    

def carga_inicio_sesion(request):
    formulario = LoginForm()
    return render(request,'inicio_sesion.html',{'formulario':formulario})

def login(request):
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password']

            try:
                # Verifica si existe el usuario
                usuario = Usuario.objects.get(nombre_usuario=username, password=password)

                # Guardar el usuario en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['rol'] = usuario.rol.nombre if usuario.rol else None

                return redirect('home')

            except Usuario.DoesNotExist:
                # Usuario no válido
                formulario.add_error(None, 'Usuario o contraseña incorrectos')
            except Exception as e:
                # Capturar errores inesperados (ej. problemas de conexión a BD) y mostrar mensaje genérico
                formulario.add_error(None, 'Error interno. Intente de nuevo más tarde.')
                print('Login error:', e)

    else:
        formulario = LoginForm()

    return render(request, 'inicio_sesion.html', {'formulario': formulario})

def carga_pagina_crear_cuenta(request): 
    formulario = Sign_up_Form()
    return render(request,'crear_cuenta.html',{'formulario':formulario})

def guardar_nuevo_usuario(request):
    # Intentamos obtener un rol por defecto; si no existe lo creamos
    rol_preterminado = None
    try:
        rol_preterminado = Rol.objects.filter(id=2).first()
        if not rol_preterminado:
            rol_preterminado, _ = Rol.objects.get_or_create(nombre='usuario')
    except Exception as e:
        # Si hay problemas con la BD, dejamos rol_preterminado en None y manejamos más abajo
        print('Error obteniendo rol por defecto:', e)

    if request.method == "POST":
        formulario = Sign_up_Form(request.POST)
        if formulario.is_valid():

            datos_form = formulario.cleaned_data
            nombre_usuario = datos_form.get('username')
            correo_electronico = datos_form['correo_Electronico']
            password = datos_form['password']

            if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                messages.error(request, "El nombre de usuario ya está en uso. Intente con otro.")
                return render(request, 'crear_cuenta.html', {'formulario': formulario})
            if Usuario.objects.filter(correo_electronico=correo_electronico).exists():
                messages.error(request, "Ya existe un usuario con ese correo electrónico.")
                return render(request, 'crear_cuenta.html', {'formulario': formulario})

            usuario = Usuario(
                nombre_usuario=nombre_usuario,
                correo_electronico=correo_electronico,
                password=password,
                rol=rol_preterminado
            )
            usuario.save()

                            # Guardar el usuario en la sesión
            request.session['usuario_id'] = usuario.id
        
            request.session['rol'] = usuario.rol.nombre
            return render(request, 'home.html')
        else:
            return render(request, 'crear_cuenta.html', {'formulario': formulario})
    else:
        formulario = Sign_up_Form()

    return render(request, 'crear_cuenta.html', {'formulario': formulario})


def home(request):
    usuario_id = request.session.get('usuario_id')

    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
    else:
        return redirect('inicio_sesion') 

    return render(request,'home.html',{'usuario': usuario}) 

def guardar_producto(request):
    if request.method == 'POST':
        form = Crear_Producto(request.POST, request.FILES)
        form.fields['categoria'].choices = [(c.id, c.nombre) for c in Categoria.objects.all()]

        if form.is_valid():
            data = form.cleaned_data
            producto = Producto(
                nombre=data['nombre'],
                precio=data['precio'],
                cantidad_stock=data['cantidad_stock'],
                categoria=Categoria.objects.get(id=data['categoria']),
                autor=data['autor'],
                descripcion=data['descripcion'],
                fecha_publicacion=data['fecha_publicacion'],
                imagen=data.get('imagen')
            )
            producto.save()
            return redirect('listar_productos')
        else:
            return render(request, 'crear_producto.html', {'formulario': form})

    return redirect('crear_producto')

def carga_pagina_crear_producto(request):
    formulario = Crear_Producto()
    formulario.fields['categoria'].choices = [(c.id, c.nombre) for c in Categoria.objects.all()]

    return render(request,'crear_producto.html',{'formulario': formulario}) 


def carga_pagina_ver_productos(request): 
    productos = Producto.objects.all().order_by('id')

    for producto in productos:
        # reemplazar coma por punto si es string
        if isinstance(producto.precio, str):
            producto.precio = producto.precio.replace(',', '.')
        else:
            # si es decimal, convertir a string con punto
            producto.precio = f"{producto.precio:.2f}"


    categorias = Categoria.objects.all().order_by('id')

    return render(request,'ver_producto.html',{'productos':productos, 'categorias':categorias})

def carga_pagina_crear_categoria(request):
    formulario = Crear_Categoria()
    return render(request,'crear_categoria.html',{'formulario':formulario})

def carga_pagina_listar_categorias(request): 
    categorias = Categoria.objects.all().order_by('id')
    return render(request,'listar_categorias.html',{'categorias':categorias})

def borrar_producto(request,id):
    try:
        producto = Producto.objects.get(pk=id )
        producto.delete()
        return redirect('listar_productos')
    except:
        return 
    

def editar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = Producto.objects.get(id=producto_id)

        form = Crear_Producto(request.POST, request.FILES)
        form.fields['categoria'].choices = [(c.id, c.nombre) for c in Categoria.objects.all()]

        if form.is_valid():
            data = form.cleaned_data
            producto.nombre = data['nombre']
            producto.precio = data['precio']
            producto.cantidad_stock = data['cantidad_stock']
            producto.categoria = Categoria.objects.get(id=data['categoria'])
            producto.descripcion = data['descripcion']
            producto.autor = data['autor']
            producto.fecha_publicacion = data['fecha_publicacion']
            
            # Solo actualiza la imagen si se subió una nueva
            if request.FILES.get('imagen'):
                producto.imagen = request.FILES['imagen']

            producto.save()
            return redirect('listar_productos') 

        return redirect('listar_productos')  

    return redirect('listar_productos')


def editar_categoria(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Verifica que exista la categoría
        categoria = Categoria.objects.get(id=categoria_id)

        # Asigna los nuevos valores
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        categoria.save()

        return redirect('listar_categorias')  # O la vista que uses para verlas

    return redirect('listar_categorias')

def guardar_categoria(request): 
    if request.method == 'POST':
        form = Crear_Categoria(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            categoria = Categoria(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
            )
            categoria.save()
            return redirect('listar_categorias')
        else:
            return render(request, 'crear_categoria.html', {'formulario': form})

    return redirect('crear_categoria.html')  

def crear_cliente(request):
    
    formulario = Crear_Cliente() 
    return render(request,'crear_cliente.html',{'formulario': formulario})

def guardar_cliente(request):
    usuario_id = request.session.get('usuario_id')
    if request.method == 'POST':
        usuario = Usuario.objects.get(id=usuario_id)
        form = Crear_Cliente(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            cliente = Cliente(
                nombre=data['nombre'],
                correo_electronico=data['correo_electronico'], 
                telefono=data['telefono'],
                id_usuario = usuario
            )
            cliente.save()
            return redirect('listar_clientes')
        else:
            return render(request, 'crear_cliente.html', {'formulario': form})

    return redirect('crear_cliente')


def editar_cliente(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        cliente = Cliente.objects.get(id=cliente_id)

        form = Crear_Cliente(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            cliente.nombre = data['nombre']
            cliente.correo_electronico = data['correo_electronico']
            cliente.telefono = data['telefono']

            cliente.save()
            return redirect('listar_clientes')
        else:
            return redirect('listar_clientes')

    return redirect('listar_clientes')

def listar_clientes(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol')

    if not usuario_id:
        return redirect('inicio_sesion')

    if rol == 'admin':
        clientes = Cliente.objects.all().order_by('id')
    else:
        clientes = Cliente.objects.filter(id_usuario=usuario_id).order_by('id')

    return render(request, 'ver_clientes.html', {'clientes': clientes})


def borrar_cliente(request,id): 
    try:
        cliente = Cliente.objects.get(pk=id )
        cliente.delete()
        return redirect('listar_clientes')
    except:
        return HttpResponse('Error 404')
    

def ventas_asociadas_clientes(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol')

    if rol == 'admin':
        clientes = Cliente.objects.prefetch_related('venta_set__detalleventa_set__producto').all()
    else:
        clientes = Cliente.objects.filter(id_usuario=usuario_id).prefetch_related('venta_set__detalleventa_set__producto')

    return render(request, 'ventas_asociadas_cliente.html', {
        'clientes': clientes
    })




def crear_venta(request):
    producto = Producto.objects.all()
    tipo_venta = Tipo_Venta.objects.all()

    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol')

    if rol == 'admin':
        cliente = Cliente.objects.all()
    else:
        cliente = Cliente.objects.filter(id_usuario=usuario_id)

    mensaje = ""
    if not cliente.exists():
        mensaje = "Debe crear un cliente para continuar."

    return render(request, 'crear_ventas.html', {
        'producto': producto,
        'cliente': cliente,
        'tipo_venta': tipo_venta,
        'mensaje': mensaje
    })



import json
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone

def guardar_venta(request):
    if request.method == 'POST':

        try:
            cliente_id = request.POST.get('cliente')
            tipo_venta_id = request.POST.get('tipo_venta')
            productos_json = request.POST.get('productos')
            total = request.POST.get('total')
            observaciones = request.POST.get('observaciones')

            # Validaciones básicas
            if not cliente_id or not tipo_venta_id or not productos_json or not total:
                messages.error(request, "Faltan datos obligatorios para guardar la venta.")
                return redirect('crear_venta') 

            productos = json.loads(productos_json)
            if len(productos) == 0:
                messages.error(request, "Debe agregar al menos un producto a la venta.")
                return redirect('crear_venta')

            # Abrimos una transacción para asegurar atomicidad
            with transaction.atomic():
                # Crear la venta
                venta = Venta.objects.create(
                    cliente_id=cliente_id,
                    tipo_venta_id=tipo_venta_id,
                    fecha=timezone.now(),
                    total=total,
                    observaciones=observaciones
                )

                # Procesar cada detalle y actualizar stock
                for item in productos:
                    producto_id = item['id']
                    cantidad = item['cantidad']

                    # Obtener producto
                    producto = Producto.objects.select_for_update().get(id=producto_id)

                    # Verificar stock suficiente
                    if producto.cantidad_stock < cantidad:
                        raise ValueError(f"No hay suficiente stock para el producto {producto.nombre}.")

                    # Crear detalle
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad
                    )

                    # Actualizar stock
                    producto.cantidad_stock -= cantidad
                    producto.save()

            messages.success(request, f"Venta #{venta.id} guardada exitosamente.")
            return redirect('ventas_asociadas_cliente')  # o la página que quieras

        except Producto.DoesNotExist:
            messages.error(request, "Uno de los productos no existe.")
            return redirect('crear_venta')

        except ValueError as ve:
            messages.error(request, str(ve))
            return redirect('crear_venta')

        except Exception as e:
            messages.error(request, "Error al guardar la venta: " + str(e))
            return redirect('crear_venta')

def ver_ventas(request):
    # Traemos todas las ventas con sus detalles y relaciones cargadas
    ventas = Venta.objects.select_related('cliente', 'tipo_venta').prefetch_related('detalleventa_set__producto')

    return render(request, 'ver_ventas.html', {
        'ventas': ventas
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol, Venta
from .forms import UsuarioForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import base64
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Listar usuarios
def listar_usuarios(request):
    if 'rol' not in request.session or request.session['rol'] != 'admin':
        return HttpResponse("No tienes permisos para ver esta página.")
    
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})


# Crear usuario
def crear_usuario(request):
    if request.session['rol'] != 'admin':
        return HttpResponse("No tienes permisos para crear usuarios.")
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

# Eliminar usuario
def eliminar_usuario(request, usuario_id):
    if request.session['rol'] != 'admin':
        return HttpResponse("No tienes permisos para eliminar usuarios.")
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('listar_usuarios')

# Generar factura PDF instalar pip install xhtml2pdf
def generar_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalleventa_set.all()

    # Calculamos los subtotales de cada producto
    detalles_con_subtotal = []
    for detalle in detalles:
        subtotal = detalle.cantidad * detalle.producto.precio
        detalles_con_subtotal.append({
            'producto': detalle.producto,
            'cantidad': detalle.cantidad,
            'precio': detalle.producto.precio,
            'subtotal': subtotal
        })

    context = {
        'venta': venta,
        'detalles': detalles_con_subtotal
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_venta_{venta.id}.pdf"'

    template = get_template('factura.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Error al generar PDF: {pisa_status.err}')

    return response


# Estadísticas de ventas
def estadisticas(request):
    total_ventas = Venta.objects.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas = Venta.objects.count()

    ventas = Venta.objects.values('fecha').annotate(total=Sum('total')).order_by('fecha')

    fechas = [v['fecha'].strftime('%Y-%m-%d') for v in ventas]
    totales = [v['total'] for v in ventas]

    plt.figure(figsize=(10,5))
    plt.plot(fechas, totales, marker='o')
    plt.title('Ventas por Fecha')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'estadisticas.html', {'total_ventas': total_ventas, 'cantidad_ventas': cantidad_ventas, 'graphic': graphic})



def crear_tipo_venta(request):
    if request.method == 'POST':
        form = Crear_Tipo_Venta(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos_venta')  # Redirige inmediatamente después de crear
    else:
        form = Crear_Tipo_Venta()

    return render(request, 'crear_tipo_venta.html', {'formulario': form})


def listar_tipos_venta(request):
    tipos_venta = Tipo_Venta.objects.all().order_by('id')
    return render(request, 'listar_tipos_venta.html', {'tipos_venta': tipos_venta})

def editar_tipo_venta(request):
    if request.method == 'POST':
        tipo_id = request.POST.get('tipo_id')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        tipo = Tipo_Venta.objects.get(id=tipo_id)
        tipo.nombre = nombre
        tipo.descripcion = descripcion
        tipo.save()

        return redirect('listar_tipos_venta')

    return redirect('listar_tipos_venta')



