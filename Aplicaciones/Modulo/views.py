from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from datetime import date, timedelta
from .forms import *
from .models import *

def LogInUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('modulo:AdminBooksPage')
            else:
                login(request, user)
                return redirect('modulo:BooksPage')
        else:
            messages.success(request, 'Usuario o contraseña incorrectos')
    return render(request, "logIn.html")


def LogOutUser(request):
    logout(request)
    return redirect('modulo:logInUser')


def booksPage(request):
    libros = Libro.objects.all()
    carreras = Carrera.objects.all()
    user = request.user
    busqueda = request.GET.get("buscar")

    """Verificar si el usuario es administrador o alumno"""
    if user.is_staff:
        usuario = user
    else:
        usuario = get_object_or_404(Usuario, email = request.user.username)

    """Realizar busqueda de libro"""
    if busqueda:
        libros = Libro.objects.filter(
            Q(codigo_interno__icontains = busqueda) |
            Q(titulo__icontains = busqueda) |
            Q(autor__icontains = busqueda) |
            Q(idioma__icontains = busqueda)
        ).distinct()

        carreras = []
        for libro in libros:    
            carrera = libro.carrera
            if carrera is not None:
                carreras.append(carrera)

    data = {
        'libros': libros,
        'carreras': carreras,
        'usuario': usuario,
    }

    return render(request, "paginaLibros.html", data)


def bookDetail(request, id):
    book = get_object_or_404(Libro, codigo_interno = id)
    data = {
        'book': book
    }
    return render(request, "bookDetail.html", data)

def bookRequest(request, id):
    """Crear Prestamo"""
    request_date = date.today()
    return_request_date = request_date + timedelta(3)
    request_user = get_object_or_404(Usuario, email = request.user.username)
    book_request = Prestamo.objects.create(fecha_prestamo=request_date, fecha_devolucion=return_request_date, id_usuario=request_user)
    """Crear detalle Prestamo"""
    libro = Libro.objects.get(codigo_interno = id)
    det_prestamo = Det_Prestamo.objects.create(cant_libros = 1, estatus =  "Prestamo", libro = libro, id_prestamo = book_request)
    det_prestamo.save()
    data = {
        'book_request': book_request,
        'request_book_user': UserForm(instance=request_user)
    }

    return render(request, "bookRequest.html", data)

def adminView(request):
    libros = Libro.objects.all()
    carreras = Carrera.objects.all()

    data = {
        'libros': libros,
        'carreras': carreras,
        'user_form': UserForm(),
        'charge_form': ChargeForm(),
        'career_form': CareerForm(),
        'shift_form': ShiftForm()
    }

    """Registro de Usuario"""
    if request.method == 'POST':
        """Añadir Usuario"""
        user_form = UserForm(data=request.POST)
        username = request.POST.get('email')
        email = request.POST.get('email')
        password  = request.POST.get('contraseña')
        if user_form.is_valid():
            user_form.save()
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            messages.success(request, 'Usuario registrado correctamente')
        else:
            data['user_form'] = user_form

        """Añadir Carrera"""
        career_form = CareerForm(data=request.POST)
        if career_form.is_valid():
            career_form.save()
            messages.success(request, 'Carrera creada correctamente')
        else:
            data['career_form'] = career_form

        """Añadir Cargo"""
        charge_form = ChargeForm(data=request.POST)
        if charge_form.is_valid():
            charge_form.save()
            messages.success(request, 'Cargo creado correctamente')
        else:
            data['charge_form'] = charge_form

        """Añadir Turno"""
        shift_form = ShiftForm(data=request.POST)
        if shift_form.is_valid():
            shift_form.save()
            messages.success(request, 'Turno creado correctamente')
        else:
            data['shift_form'] = shift_form
        
    return render(request, "adminBooksPage.html", data)


def adminBookDetail(request, id):
    libro = get_object_or_404(Libro, codigo_interno = id)
    data = {
        'book_form': BookForm(instance=libro),
        'book': libro
    }
    if request.method == 'POST':
        book_form = BookForm(data=request.POST, instance=libro, files=request.FILES)
        if book_form.is_valid():
            book_form.save()
            messages.success(request, 'Libro guardado correctamente')
            return redirect("modulo:AdminBooksPage")
        else:
            data['book_form'] = book_form
    return render(request, "adminBookDetail.html", data)


def adminAddBook(request):
    data = {
        'book_form': BookForm()
    }
    if request.method == 'POST':
        book_form = BookForm(data=request.POST, files=request.FILES)
        if book_form.is_valid():
            book_form.save()
            messages.success(request, 'Libro agregado correctamente')
            return redirect("modulo:AdminBooksPage")
        else:
            data['book_form'] = book_form
    return render(request, "adminAddBook.html", data)


def adminDeleteBook(request, id):
    libro = get_object_or_404(Libro, codigo_interno = id)
    libro.delete()
    messages.success(request, 'Libro eliminado correctamente')
    return redirect(to="modulo:AdminBooksPage")


def adminRequestList(request):
    prestamos = Prestamo.objects.all()
    det_prestamos = Det_Prestamo.objects.all()
    busqueda = request.GET.get("buscar")

    """Realizar busqueda de prestamo"""
    if busqueda:
        prestamos = Prestamo.objects.filter(
            Q(id_prestamo__icontains = busqueda) |
            Q(id_usuario__nombre_completo__icontains = busqueda) 
        ).distinct()

    data = {
        "prestamos":prestamos,
        "det_prestamos": det_prestamos,
    }
    return render(request, "adminRequestList.html", data)

""" def addToBookCart(request, id):
    libro = Libro.objects.get(codigo_interno = id)
    user = get_object_or_404(Usuario, email = request.user.username)
    librero , _ = Librero.objects.get_or_create(id_usuario = user, activo = False)

    det_librero = Det_Librero.objects.create(librero = librero, libro = libro)
    det_librero.save()

    return redirect("modulo:BooksPage")

def deleteBookInBookCart(request, id):
    try:
        libro = Det_Librero.objects.get(libro = id)
        libro.delete()
    except Exception as e:
        print(e)


def BookCart(request):
    data = {
        'context': context
        }
    context = {'librero' : Librero.objects.filter(activo = False, id_usuario = request.user)} """