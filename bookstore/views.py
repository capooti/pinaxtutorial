#from django
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#from bookstore
from bookstore.models import Book
from bookstore.forms import BookForm

def books(request):
    """ Return the all books list, ordered by added date. """
    books = Book.objects.all().order_by("-added")
    return render_to_response("bookstore/books.html", {
        "books": books,
        "list": 'all',
    }, context_instance=RequestContext(request))
    
def user_books(request, username):
    """ Return an user books list. """
    user = get_object_or_404(User, username=username)
    userbooks = Book.objects.filter(adder=user).order_by("-added")
    return render_to_response("bookstore/books.html", {
        "books": userbooks,
        "list": 'user',
        "username": username,
    }, context_instance=RequestContext(request))
    
def book(request, book_id):
    """ Return a book given its id. """
    isyours = False
    book = Book.objects.get(id=book_id)
    if request.user == book.adder:
        isyours = True
    return render_to_response("bookstore/book.html", {
        "book": book,
        "isyours": isyours,
    }, context_instance=RequestContext(request))
    
@login_required
def your_books(request):
    """ Return the logged user books list. """
    yourbooks = Book.objects.filter(adder=request.user).order_by("-added")
    return render_to_response("bookstore/books.html", {
        "books": yourbooks,
        "list": 'yours',
    }, context_instance=RequestContext(request))

@login_required
def add_book(request):
    """ Add a book to the bookstore. """
    # POST request
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            # from ipdb import set_trace; set_trace()
            new_book = book_form.save(commit=False)
            new_book.adder = request.user
            new_book.save()
            request.user.message_set.create(message=_("You have saved book '%(title)s'") %  {'title': new_book.title})
            return HttpResponseRedirect(reverse("bookstore.views.books"))            
    # GET request
    else:
        book_form = BookForm()
        return render_to_response("bookstore/add.html", {
            "book_form": book_form,
            }, context_instance=RequestContext(request))
    # generic case
    return render_to_response("bookstore/add.html", {
        "book_form": book_form,
    }, context_instance=RequestContext(request)) 
    
@login_required
def update_book(request, book_id):
    """ Update a book given its id. """
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES, instance=book)
        book_form.is_update = True
        if request.user == book.adder:
            #from ipdb import set_trace; set_trace()
            if book_form.is_valid():
                book_form.save()
                request.user.message_set.create(message=_("You have updated book '%(title)s'") %  {'title': book.title})
                return HttpResponseRedirect(reverse("bookstore.views.books"))            
    else:
        book_form = BookForm(instance=book)
        return render_to_response("bookstore/update.html", {
            "book_form": book_form,
            "book": book,
            }, context_instance=RequestContext(request))  
              
@login_required
def delete_book(request, book_id):
    """ Delete a book given its id. """
    book = get_object_or_404(Book, id=book_id)
    if request.user == book.adder:
        book.delete()
        request.user.message_set.create(message="Book Deleted")
    
    return HttpResponseRedirect(reverse("bookstore.views.books"))

