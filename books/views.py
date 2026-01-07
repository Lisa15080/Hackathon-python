# books/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, ReadingStatus
from .forms import BookForm


def book_list(request):
    books = Book.objects.select_related('added_by').prefetch_related('reading_statuses__user').all()

    user_status_map = {}
    if request.user.is_authenticated:
        user_status_map = {
            rs.book_id: rs.status
            for rs in ReadingStatus.objects.filter(user=request.user, book__in=books)
        }

    return render(request, 'books/book_list.html', {
        'books': books,
        'user_status_map': user_status_map,
        'status_choices': ReadingStatus.STATUS_CHOICES,
    })


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Добавить книгу'})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Редактировать книгу'})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


@login_required
def update_reading_status(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    status = request.POST.get('status')
    if status in dict(ReadingStatus.STATUS_CHOICES):
        ReadingStatus.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={'status': status}
        )
    return redirect('book_list')