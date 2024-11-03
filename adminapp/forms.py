from django import forms
from .models import Book, Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book name'}),
        'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book author'}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book price'})
    }
