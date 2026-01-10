from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book  
from .forms import BookForm


@login_required
def book_list(request):
    """Список книг ТЕКУЩЕГО пользователя."""
    books = Book.objects.filter(user=request.user).order_by('title')
    return render(request, 'books/book_list.html', {
        'books': books,
        'status_choices': Book.STATUS_CHOICES,  
    })


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  
            book.save()
            messages.success(request, 'Книга добавлена!')
            return redirect('book_list')  
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Добавить книгу'
    })


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга обновлена!')
            return redirect('book_list')  
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Редактировать книгу'
    })


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книга удалена.')
        return redirect('book_list')  
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def update_book_status(request, pk, status):
    """Обновление статуса книги без полной формы."""
    book = get_object_or_404(Book, pk=pk, user=request.user)
    
    valid_statuses = dict(Book.STATUS_CHOICES).keys()
    if status in valid_statuses:
        book.status = status
        book.save()
        messages.success(request, f'Статус изменён на "{dict(Book.STATUS_CHOICES)[status]}".')
    else:
        messages.error(request, 'Недопустимый статус.')
    
    return redirect('book_list')
