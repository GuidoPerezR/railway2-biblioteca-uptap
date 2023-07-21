from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.postgres.fields import ArrayField
from django.db import models

class Carrera(models.Model):
    id_carrera = models.BigAutoField(primary_key=True)
    nom_carrera = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nom_carrera)
    
class Cargo (models.Model):
    id_cargo= models.BigAutoField(primary_key=True)
    nombre= models.CharField(max_length=20)
    def __str__(self):
        return str(self.nombre)
    
class Turno(models.Model):
    id_turno = models.BigAutoField(primary_key=True)
    nom_turno = models.CharField(max_length=30)
    def __str__(self):
        return str(self.nom_turno)

class Libro(models.Model):
    codigo_interno = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    disponibles = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    estado_libro = models.CharField(max_length=50)
    idioma = models.CharField(max_length=30)
    editorial = models.CharField(max_length=50)
    paginas = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3000)])
    imagen = models.ImageField(upload_to='media/booksImages/')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.titulo}'
    
    class Meta:
        ordering = ['codigo_interno']

class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    id_cargo= models.ForeignKey(Cargo, on_delete=models.CASCADE)
    id_turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre_completo} - {self.id_cargo.nombre}'

class Prestamo(models.Model):
    id_prestamo = models.BigAutoField(primary_key=True)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id_usuario.nombre_completo} - {self.id_prestamo}'

class Det_Prestamo(models.Model):
    id_det_prestamo = models.BigAutoField(primary_key=True)
    cant_libros = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    estatus = models.CharField(max_length=50)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True)
    id_prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id_prestamo.id_usuario.nombre_completo} - {self.id_prestamo.id_prestamo}'

""" class Librero(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    activo = models.BooleanField(default=False)

    def get_librero_total(self):
        libros = self.librero_items.all()
        print(libros)

class Det_Librero(models.Model):
    librero = models.ForeignKey(Librero, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE) """