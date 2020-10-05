import uuid
from datetime import date

from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a Book Genre (e.g Science, Fiction)')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300, help_text='Enter Title for the Book')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    summary = models.CharField(max_length=1000, help_text='Enter a brief description of the book')
    genre = models.ManyToManyField(Genre, help_text='select a genre for book')

    def __str__(self):
        return self.title

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique ID for this particular book')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True, help_text='Due back date')

    LOAN_STATUS = (('m', 'maintenance'), ('o', 'on loan'), ('a', 'Available'), ('r', 'Reserved'))
    status = models.CharField(max_length=1, blank=True, default='m', help_text='Book Availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name: CharField = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True, help_text='died')
    books = models.ManyToManyField(Book, related_name="%(class)s_book", help_text='select a book')

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Please enter Language')

    def __str__(self):
        return self.name
