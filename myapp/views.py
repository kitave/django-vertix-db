

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404

from myapp.models import Book
from myapp.my_forms import BookForm, RegisterForm


# Create your views here.
@login_required
def show_books(request):
    books = Book.objects.all() #select * from books
    return render(request, 'show_books.html',{'books':books})


# def add_book(request):
#     return render(request, 'add_book.html')

@login_required
@permission_required('myapp')
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("show_books")
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

#django models

# Book.objects.create(title = 'A Little LIfe',
#                         year =2019,
#                         cost= 450,
#                         category ='Slice of LIfe',
#                         isbn ='0123456789',
#                         published = True)
#     Book.objects.create(title = 'White NIghts',
#                         year =1967,
#                         cost=900,
#                         category ='Romance',
#                         isbn ='754983229',
#                         published = True)

@login_required()
def delete_book(request, id):
    book = Book.objects.get(id=id) #select * from books
    book.delete() #delete the book
    messages.error(request, "Book has been deleted")
    return redirect("show_books")

@login_required()
def edit_book(request ,id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book Updated Successfully')
            return redirect("show_books")
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("show_books")

    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin  ")

    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required()
def signout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')