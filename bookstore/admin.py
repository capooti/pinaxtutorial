from django.contrib import admin
from bookstore.models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'description', 'added', 'adder', 'coverart')

admin.site.register(Book, BookAdmin)


