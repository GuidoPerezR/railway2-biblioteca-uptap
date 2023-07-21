from django import forms
from .models import Usuario, Libro, Prestamo, Cargo, Carrera, Turno

class ChargeForm(forms.ModelForm):
    
    class Meta:
        model = Cargo
        fields = '__all__'

class CareerForm(forms.ModelForm):
    
    class Meta:
        model = Carrera
        fields = '__all__'

class ShiftForm(forms.ModelForm):
    
    class Meta:
        model = Turno
        fields = '__all__'

class UserForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = '__all__'

class BookForm(forms.ModelForm):

    class Meta:
        model = Libro
        fields = '__all__'

class RequestForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = '__all__'