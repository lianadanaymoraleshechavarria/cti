from django.contrib import admin
from plataforma.models import Usuario, NombreRol
# Register your models here.
admin.site.register(Usuario)


@admin.register(NombreRol)
class NombreRolAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_personalizado')
    search_fields = ('codigo', 'nombre_personalizado')
    list_editable = ('nombre_personalizado',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Limpiar cache al guardar cambios
        from django.core.cache import cache
        cache.delete('roles_personalizados_cache')