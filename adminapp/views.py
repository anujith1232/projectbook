from idlelib.query import Query
from lib2to3.fixes.fix_input import context

from django.core.paginator import Paginator,EmptyPage
from django.shortcuts import render, redirect
from django.template.defaultfilters import title, register
from django.contrib.auth.models import User,auth
from django.contrib import messages

from .models import Book
from .forms import AuthorForm, BookForm
from django.db.models import Q
from django.shortcuts import render

def create_and_list_books(request):
    form = BookForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('adminapp:create_and_list_books')

    books = Book.objects.all()
    return render(request, 'admin/books.html', {'form': form, 'books': books})





def updatebook(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("adminapp:listbook")

    else:
        form = BookForm(instance=book)

    return render(request, 'admin/update.html', {'form': form})


def DeleteView(request, book_id):
    books = Book.objects.get(id=book_id)
    if request.method == "POST":
        books.delete()
        return redirect("adminapp:listbook")
    return render(request, 'admin/deleteview.html', {'books': books})

def listbook(request):
    books = Book.objects.all().order_by('title')
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_page)
    return render(request, 'admin/listbook.html', {'books': books , 'page':page})

def Create_author(request):
    if request.method == 'POST':

        form= AuthorForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect ('adminapp:create_and_list_books')
    else:
        form=AuthorForm()

    return render (request,'admin/author.html',{'form':form})

def detailsview(request,book_id):
    books = Book.objects.get(id=book_id)
    return render(request, 'admin/details.html', {'books': books})

def index(request):
    return render (request,'admin/base.html')

def search(request):
    query=None
    books=None

    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query))

    else:
        books=[]
    context = {'books': books, 'query': query}
    return render(request, 'admin/search.html', context)

def searchauthor (request):
    query=None
    author=None

    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(author__icontains=query))

    else:
        books=[]
        context={'books':books, 'query':query }

    return render (request,'admin/searchauthor.html',context)

def index(request):
    return render(request,'admin/base.html')