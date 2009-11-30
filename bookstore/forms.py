#from django
from django import forms
from django.utils.translation import ugettext_lazy as _

#from bookstore
from bookstore.models import Book

class BookForm(forms.ModelForm):
    """
    Book Form: form associated to the Book model
    """
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.is_update = False
    
    def clean(self):
        """ Do validation stuff. """
        # title is mandatory
        if 'title' not in self.cleaned_data:
            return
        # if a book with that title already exists...
        if not self.is_update:
            if Book.objects.filter(title=self.cleaned_data['title']).count() > 0:
                raise forms.ValidationError(_("There is already this book in the library."))
        return self.cleaned_data
    
    class Meta:
        model = Book
        fields = ('coverart', 'publisher', 'author', 'description', 'title', 'tags')

