from django.urls import path
from . import views

app_name = 'userapp'

urlpatterns = [
    path('', views.userRegister, name='reg'),
    path('login/', views.userlogin, name='login'),
path('home/', views.userHomepage, name='home'),
    path('login/', views.logout, name='logout'),
    path('list/', views.userlistbook, name='listbook'),
    path('detail/<int:book_id>/', views.userdetailsview, name='userdetails'),
    #path('index/', views.userindex),
path('usersearch/', views.usersearch, name='usersearch'),
path('add_to_cart/<int:book_id>/', views.add_to_cart, name='addtocart'),
path('view_cart/', views.view_cart, name='viewcart'),
path('search-author/',views.usersearchauthor, name='usersearchauthor'),
path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),
path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),

]