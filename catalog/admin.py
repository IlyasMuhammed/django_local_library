from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language


# Register your models here.


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookInline(admin.TabularInline):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


admin.site.register(Book, BookAdmin)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


admin.site.register(BookInstance, BookInstanceAdmin)


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


admin.site.register(Author, AuthorAdmin)


class LanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
