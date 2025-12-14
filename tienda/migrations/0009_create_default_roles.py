from django.db import migrations


def create_roles(apps, schema_editor):
    Rol = apps.get_model('tienda', 'Rol')
    # Crear roles en orden para intentar que 'usuario' quede con id=2
    Rol.objects.get_or_create(nombre='admin')
    Rol.objects.get_or_create(nombre='usuario')


def delete_roles(apps, schema_editor):
    Rol = apps.get_model('tienda', 'Rol')
    Rol.objects.filter(nombre__in=['admin', 'usuario']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0008_alter_producto_options_cliente_id_usuario'),
    ]

    operations = [
        migrations.RunPython(create_roles, delete_roles),
    ]
