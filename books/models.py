from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from users.models import User


class Book(models.Model):
    """
    Класс для представления книги в каталоге.
    """

    STATUS_NOT_STARTED = 'not_started'
    STATUS_READING = 'reading'
    STATUS_READ = 'read'

    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, 'Не начата'),
        (STATUS_READING, 'Читаю'),
        (STATUS_READ, 'Прочитана'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Обязательное поле. Не менее 1 символа."
    )
    author = models.CharField(
        max_length=150,
        verbose_name="Автор",
        help_text="Обязательное поле. Минимум 2 символа."
    )
    year = models.PositiveIntegerField(
        verbose_name="Год издания",
        help_text="Должен быть от 1 до текущего года."
    )
    genre = models.CharField(
        max_length=100,
        verbose_name="Жанр",
        help_text="Обязательное поле. Минимум 2 символа."
    )
    description = models.TextField(
        blank=True,
        verbose_name="Краткое описание"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
        verbose_name="Статус чтения"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Пользователь, добавивший книгу"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} — {self.author} ({self.year})"

    def clean(self):
        """Кастомная валидация полей."""
        if not self.title or len(self.title.strip()) < 1:
            raise ValidationError({'title': "Название книги не может быть пустым."})

        if not self.author or len(self.author.strip()) < 2:
            raise ValidationError({'author': "Имя автора должно содержать минимум 2 символа."})

        if not self.genre or len(self.genre.strip()) < 2:
            raise ValidationError({'genre': "Жанр должен содержать минимум 2 символа."})

        current_year = datetime.now().year
        if self.year < 1 or self.year > current_year:
            raise ValidationError({'year': f"Год издания должен быть от 1 до {current_year}."})

    def save(self, *args, **kwargs):
        """Автоматическая валидация при сохранении."""
        self.full_clean()
        super().save(*args, **kwargs)