from django.contrib import admin
from core.models import inventario,carreras,Responsables
# Register your models here.
class InventarioAdmin(admin.ModelAdmin):
    pass
class CarreraAdmin(admin.ModelAdmin):
    pass
class ResponsableAdmin(admin.ModelAdmin):
    pass
admin.site.register(inventario,InventarioAdmin)
admin.site.register(carreras,CarreraAdmin)
admin.site.register(Responsables,ResponsableAdmin)