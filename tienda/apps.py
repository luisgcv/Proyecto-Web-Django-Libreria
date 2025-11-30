from django.apps import AppConfig


class TiendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tienda'
    verbose_name="Proyecto Web, Sitio de Libros"

    def ready(self):
        import tienda.signals