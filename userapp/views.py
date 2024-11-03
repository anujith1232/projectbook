from django.urls import reverse
from itertools import product
from locale import currency
from wsgiref.util import request_uri
from django.conf import settings
from django.contrib.messages import success
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from urllib3 import request

from adminapp.models import Book
from adminapp.forms import AuthorForm, BookForm
from userapp.models import CartItem
from .models import Cart, CartItem
import stripe


def userlistbook(request):
    books = Book.objects.all()  # Ensure this retrieves the books
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(1)  # Default to the first page if the requested page does not exist

    return render(request, 'user/userlistbook.html', {'books': books, 'page': page})

def userdetailsview(request,book_id):
    books = Book.objects.get(id=book_id)
    return render(request, 'user/userdetails.html', {'books': books})


#def userindex(request):
    #return render(request, 'user/userbase.html')


def usersearch(request):
    query = None
    books = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query))
    else:
        books = []

    context = {'books': books, 'query': query}
    return render(request, 'user/usersearch.html', context)

def usersearchauthor(request):
    query = None
    books = []

    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(author__icontains=query))

    context = {'books': books, 'query': query}
    return render(request, 'user/userauthorsearch.html', context)


def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This email is already taken.')
            else:
                User.objects.create_user(username=username, first_name=first_name,
                                         last_name=last_name, email=email, password=password)
                return redirect('userapp:login')
        else:
            messages.info(request, 'Passwords do not match.')

    return render(request, 'user/userregister.html')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('userapp:home')
        else:
            messages.error(request, 'Please provide correct details.')
            return redirect('userapp:login')

    return render(request, 'user/userlogin.html')


def logout(request):
    auth.logout(request)
    return redirect('userapp:login')


def userHomepage(request):
    return render(request, 'user/userhome.html')

def add_to_cart(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'Book not found.')
        return redirect('userapp:listbook')

    if book.quantity > 0:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('userapp:viewcart')  # Redirect to the cart view

    messages.info(request, 'Sorry, this book is out of stock.')  # Message if the book is out of stock
    return redirect('userapp:listbook')  # Redirect to a list of books

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()  # Use related_name if defined, otherwise access with `cartitem_set`
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    }

    return render(request, 'user/cart.html', context)

def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('userapp:viewcart')

def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('userapp:viewcart')

def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('userapp:viewcart')

def create_checkout_session(request):
    cart_items = CartItem.objects.all()

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            line_items = []

            for cart_item in cart_items:
                if cart_item.book:
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            'unit_amount': int(cart_item.book.price * 100),
                            'product_data': {
                                'name': cart_item.book.title
                            },
                        },
                        'quantity': 1
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('userapp:success')),

                )

                return redirect(checkout_session.url, code=303)

def success(request):
    cart_items = CartItem.objects.all()

    for cart_item in cart_items:
        product = cart_item.book

        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()

    cart_items.delete()

    return render(request, 'user/success.html')


