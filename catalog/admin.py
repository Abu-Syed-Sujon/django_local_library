from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance

#admin.site.register(Author)
#admin.site.register(Genre)
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Language)

# ============================
# AUTHOR ADMIN
# ============================
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Show these fields in list view
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    # Add filter sidebar
    list_filter = ('date_of_birth', 'date_of_death')

    # Default ordering
    ordering = ('last_name', 'first_name')


# ============================
# GENRE ADMIN
# ============================
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


# ============================
# BOOK ADMIN
# ============================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')

    # Helps search quickly
    search_fields = ('title', 'author__last_name')


# ============================
# BOOK INSTANCE ADMIN (IMPORTANT)
# ============================
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    # Show important fields in list page
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    # Filters in sidebar
    list_filter = ('status', 'due_back')

    # Organize fields in edit page
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
