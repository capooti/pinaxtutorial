Internationalization of the Bookstore application
=================================================

In this part of the tutorial I will show how easy it is to make your application internationalized with Pinax (Django).

You can find the code of this part of the tutorial here.

Introduction
------------
Enabling internationalization for a Pinax application is just the same procedure for enabling it for a Django application.

You can find a complete discussion about Django's internationalization mechanism `here <http://docs.djangoproject.com/en/dev/topics/i18n/>`_
Be sure to read this discussion before going on with this tutorial.

So you will need to complete three steps:

* use translation strings in Python code and templates
* create language files
* change settings

Let's see how to apply them to the Bookstore application.

Using translation strings in Python code and templates
------------------------------------------------------

In the Bookstore application we have already used translation strings in Python code and templates with the help of the django.utils.translation.ugettext_lazy() function and the {% trans %} (and {% blocktrans %}) template tag. For example:

In the model: PROJECT_ROOT/bookstore/models.py::

	...
	from django.utils.translation import ugettext_lazy as _

	class Book(models.Model):
		"""
		Book Model: title, publisher, author, description, coverart, adder, added
		"""
		title = models.CharField(_('title'), max_length=255)
		publisher = models.CharField(_('publisher'), max_length=255)
		author = models.CharField(_('author'), max_length=255)
		....

In the views: PROJECT_ROOT/bookstore/views.py::

	...
	from django.utils.translation import ugettext_lazy as _
	...
	@login_required
	def add_book(request):
		""" Add a book to the bookstore. """
		# POST request
		if request.method == "POST":
		    book_form = BookForm(request.POST, request.FILES)
		    if book_form.is_valid():
		        new_book = book_form.save(commit=False)
		        new_book.adder = request.user
		        new_book.save()
		        request.user.message_set.create(message=_("You have saved book '%(title)s'") %  {'title': new_book.title})
		        return HttpResponseRedirect(reverse("bookstore.views.books"))
		...
	...

In the templates: PROJECT_ROOT/templates/bookstore/base.html::

	{% extends "site_base.html" %}

	{% load i18n %}

	{% block rtab_id %}id="bookstore_tab"{% endblock %}

	{% block subnav %}
		<ul>
		    <li><a href="{% url all_books %}">{% trans "All books" %}</a></li>
		    <li><a href="{% url your_books %}">{% trans "Your books" %}</a></li>
		    <li><a href="{% url add_book %}">{% trans "Add a book" %}</a></li>
		</ul>
	{% endblock %}

Note that I did not use translation strings for everything in the last part, so if you have time try to cover the totality of the code (or download the source of this tutorial part at gitHub).

Creating language files
-----------------------

Once you have tagged your strings for being translated, you need to write the languages files for any language you wish the application needs to be translated.
For example create a message file for Italian by using the django-admin.py makemessages tool (note that we are creating the message file in the application directory, and that we need to create a locale directory before)::
	
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/bookstore$ django-admin.py makemessages -l it
	Error: This script should be run from the Django SVN tree or your project or app tree. If you did indeed run it from the SVN checkout or your project or application, maybe you are just missing the conf/locale (in the django tree) or locale (for project and application) directory? It is not created automatically, you have to create it by hand if you want to enable i18n for your project or application.
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/bookstore$ mkdir locale
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/bookstore$ django-admin.py makemessages -l it
	processing language it
	
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/templates/bookstore$ django-admin.py makemessages -l it
	Error: This script should be run from the Django SVN tree or your project or app tree. If you did indeed run it from the SVN checkout or your project or application, maybe you are just missing the conf/locale (in the django tree) or locale (for project and application) directory? It is not created automatically, you have to create it by hand if you want to enable i18n for your project or application.
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/templates/bookstore$ mkdir locale
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/templates/bookstore$ django-admin.py makemessages -l it
	processing language it
	
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial$ django-admin.py makemessages -l it
	Error: This script should be run from the Django SVN tree or your project or app tree. If you did indeed run it from the SVN checkout or your project or application, maybe you are just missing the conf/locale (in the django tree) or locale (for project and application) directory? It is not created automatically, you have to create it by hand if you want to enable i18n for your project or application.
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial$ mkdir locale
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial$ django-admin.py makemessages -l it
	processing language it

Open the django.po file that has been created, and change the msgstr for each msgid.

PROJECT_ROOT/bookstore/locale/it/LC_MESSAGES/django.po::

	...
	#: views.py:63
	#, python-format
	msgid "You have saved book '%(title)s'"
	msgstr "Hai aggiunto il libro '%(title)s'"

	#: views.py:87
	#, python-format
	msgid "You have updated book '%(title)s'"
	msgstr "Hai modificato il libro '%(title)s'"
	...

Now you need to compile the messages you modified in django.po by using the django-admin.py tool with the compilemessages option::

	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/bookstore$ django-admin.py compilemessages
	processing file django.po in /home/paolo/git/pinaxtutorial/bookstore/locale/it/LC_MESSAGES
	
	(pinax-env)paolo@paolo-laptop:~/virtualenv/pinax-env/pinaxtutorial/templates/bookstore$ django-admin.py compilemessages
	processing file django.po in /home/paolo/virtualenv/pinax-env/pinaxtutorial/templates/bookstore/locale/it/LC_MESSAGES


Now you should find a django.mo file in the PROJECT_ROOT/bookstore/locale/it/LC_MESSAGES directory.

Remember to restart the development server every time you compile the messages. 

Changing settings
-----------------

The bookstore application has now the Italian translation, but you need to make Django aware of the languages supported by the application.

Open your settings.py file and make sure you have the following settings::

	...
	# If you set this to False, Django will make some optimizations so as not
	# to load the internationalization machinery.
	USE_I18N = True
	...
	ugettext = lambda s: s
	LANGUAGES = (
		('en', u'English'),
		('it', u'Italiano'),
	)
	
Note by now only the bookstore application has been translated (in Italian). If you want to do the same for your project (the pinax project) you need to create and compile the messages file at the project level.

Now try your project (change the Pinax language by using the dropdown list in the upper right):

.. image:: images/internationalization/PinaxInternational.png
    :width: 600 px
    :alt: The Bookstore add book page
