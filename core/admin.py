from django.contrib import admin
from core.models import Inventario,Carrera,Responsable,Ubicacion
# Register your models here.
class InventarioAdmin(admin.ModelAdmin):
    pass
class CarreraAdmin(admin.ModelAdmin):
    pass
class ResponsableAdmin(admin.ModelAdmin):
    pass
class UbicacionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ubicacion,UbicacionAdmin)
admin.site.register(Inventario,InventarioAdmin)
admin.site.register(Carrera,CarreraAdmin)
admin.site.register(Responsable,ResponsableAdmin)