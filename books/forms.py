from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Форма для создания и редактирования экземпляров модели Book.

    Поля:
    - title (str): Название книги.
    - author (str): Автор книги.
    - year (int): Год издания (ограничен диапазоном от 1 до 2026).
    - genre (str): Жанр книги.
    - description (str): Описание книги (многострочное поле).

    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'genre', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 2026
            }),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'title': 'Название',
            'author': 'Автор',
            'year': 'Год издания',
            'genre': 'Жанр',
            'description': 'Описание',
        }
