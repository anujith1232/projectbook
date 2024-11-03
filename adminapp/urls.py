from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
path('create/', views.create_and_list_books, name='create_and_list_books'),
    path('listbook/', views.listbook, name='listbook'),
    path('delete/<int:book_id>/', views.DeleteView, name='deletebook'),
    path('update/<int:book_id>/', views.updatebook, name='updatebook'),
    path("author/", views.Create_author, name='author'),
path('details/<int:book_id>/', views.detailsview, name='details'),
path('index/', views.index),
    path('search/', views.search, name='search')]