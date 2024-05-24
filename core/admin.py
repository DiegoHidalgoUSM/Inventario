from django.contrib import admin
from core.models import inventario,carreras
# Register your models here.
class InventarioAdmin(admin.ModelAdmin):
    pass
class CarreraAdmin(admin.ModelAdmin):
    pass

admin.site.register(inventario,InventarioAdmin)
admin.site.register(carreras,CarreraAdmin)