# forms.py
from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from tienda.models import Cliente, Tipo_Venta, Producto, Usuario


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'required': True,
            'placeholder': 'Ingrese su usuario'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'required': True,
            'placeholder': 'Ingrese su contraseña'
        })
    )

class Sign_up_Form(forms.Form):
    username = forms.CharField(
        label="Usuario",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'required': True,
            'placeholder': 'Ingrese un usuario'
        })
    )

    correo_Electronico = forms.EmailField(
        label="Correo Electronico",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'required': True,
            'placeholder': 'Ingrese un correo'
        })
    )


    password = forms.CharField(
        label="Contraseña",
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'required': True,
            'placeholder': 'Ingrese una contraseña'
        }),
        validators=[
            MinLengthValidator(8, message='La contraseña debe tener al menos 8 caracteres.'),
            RegexValidator(
                regex=r'[A-Z]',
                message='La contraseña debe contener al menos una letra mayúscula.'
            ),
            RegexValidator(
                regex=r'[a-z]',
                message='La contraseña debe contener al menos una letra minúscula.'
            ),
            RegexValidator(
                regex=r'[0-9]',
                message='La contraseña debe contener al menos un número.'
            ),
        ]
    )

class Crear_Producto(forms.Form):
    nombre = forms.CharField(
        label="Nombre del producto",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nombre',
            'required': True,
            'placeholder': 'Ingrese el nombre del producto'
        })
    )

    precio = forms.DecimalField(
        label="Precio (₡)",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'precio',
            'required': True,
            'placeholder': 'Ingrese el precio'
        })
    )

    cantidad_stock = forms.IntegerField(
        label="Cantidad en stock",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'cantidad_stock',
            'required': True,
            'placeholder': 'Ingrese la cantidad'
        })
    )

    categoria = forms.ChoiceField(
        label="Categoría",
        choices=[],  # Se debe llenar dinámicamente en la vista
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'categoria',
            'required': True
        })
    )
    autor = forms.CharField(
        label="Autor", 
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el autor del Libro'
            }
        )
    )
    descripcion = forms.CharField(
        label="Descripción", 
        max_length=500, 
        required=True, 
        widget=forms.Textarea(
            attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el autor del Libro'           
            }
        )
    )
    fecha_publicacion = forms.DateField(
        label="Fecha de Publicación",
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',  
                'class': 'form-control' 
            }
        )
    )
    imagen = forms.ImageField(
        label="Imagen del producto",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'id': 'imagen'
        })
    )


class Crear_Categoria(forms.Form): 
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nombre',
            'required': True,
            'placeholder': 'Ingrese el nombre de la categoría'
        })
    )

    descripcion = forms.CharField(
        label="Descripción",
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'descripcion',
            'placeholder': 'Ingrese una descripción (opcional)',
            'rows': 3
        })
    )


class Crear_Cliente(forms.Form):
    
    nombre = forms.CharField(
        label="Nombre",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre',
            'required': True
        })
    )

    correo_electronico = forms.EmailField(
        label="Correo Electrónico",
        max_length=110,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el correo',
            'required': True
        })
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número de teléfono',
            'required': True,
            'pattern': '[0-9]+',
            'title': 'Solo se permiten números'
        })
    )

class Crear_Tipo_Venta(forms.ModelForm):
    class Meta:
        model = Tipo_Venta
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    

class UsuarioForm(forms.ModelForm):
    class Meta:
       model = Usuario
       fields = ['nombre_usuario', 'correo_electronico', 'password', 'rol']




