from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Libro)

@admin.register(Cargo)
class Cargo(admin.ModelAdmin):
    ordering = ('id_cargo',)
    #exclude = ('matricula',)

@admin.register(Turno)
class Turno(admin.ModelAdmin):
    ordering = ('id_turno',)
    #exclude = ('matricula',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    ordering = ('id_usuario',)
    #exclude = ('matricula',)


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    ordering = ('nom_carrera',)
    search_fields = ('nom_carrera',)
    
@admin.register(Prestamo)
class Prestamo(admin.ModelAdmin):
    ordering = ('id_prestamo',)
    search_fields = ('id_prestamo',)

@admin.register(Det_Prestamo)
class Detalle_Prestamo(admin.ModelAdmin):
    ordering = ('id_det_prestamo',)
    search_fields = ('id_det_prestamo',)