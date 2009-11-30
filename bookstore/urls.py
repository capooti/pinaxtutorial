#from django
from django.conf.urls.defaults import *

# from bookstore
from bookstore.models import Book

urlpatterns = patterns('',
        url(r'^$', 'bookstore.views.books', name="all_books"),
        url(r'^(\d+)/book/$', 'bookstore.views.book', name="describe_book"),
        url(r'^your_books/$', 'bookstore.views.your_books', name="your_books"),
        url(r'^user_books/(?P<username>\w+)/$', 'bookstore.views.user_books', name="user_books"),
        # CRUD urls
        url(r'^add/$', 'bookstore.views.add_book', name="add_book"),
        url(r'^(\d+)/update/$', 'bookstore.views.update_book', name="update_book"),
        url(r'^(\d+)/delete/$', 'bookstore.views.delete_book', name="delete_book"),
    )

