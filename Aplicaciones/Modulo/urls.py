from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name='modulo'
urlpatterns = [
    path('', login_required(booksPage), name='BooksPage'),
    path('BookDetail/<id>',bookDetail, name='BookDetail'),
    path('BookRequest/<id>', bookRequest, name='BookRequest'),
    path('AdminBooksPage/', login_required(adminView), name='AdminBooksPage'),
    path('AdminBookDetail/<id>/', adminBookDetail, name='AdminBookDetail'),
    path('AdminDeleteBook/<id>/',adminDeleteBook, name='AdminDeleteBook'),
    path('AdminAddBook/', adminAddBook, name='AdminAddBook'),
    path('AdminRequestList/', adminRequestList, name='AdminRequestList'),
] 