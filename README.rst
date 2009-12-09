The Pinax Tutorial,
by Paolo Corti, 2009

Tutorial: writing Pinax's applications
======================================

1) Creating the basic application with CRUD methods and putting it in Pinax 
---------------------------------------------------------------------------
- create app
- menu
- localization
- messages bar
 
2) Using Pagination, Avatars and Profile
----------------------------------------
- add record in plugins table

3) Using the voting application (django_voting)
-----------------------------------------------
- tags to use: {% load voting_tags %}, {% load extra_voting_tags %}
- add a vote section in urls.py
- add the vote section in the html page
- add the javascript in the html page

4) Using the tagging application (django_tagging)
-------------------------------------------------
- insert the tags field in the model and get_tags method
- syncdb to update the database with the tags field
- add tags field in the form
- try to add some tags: note that both "Tagged Items" and "Tags" tables of Tagging app are updated
- call the get_tags method in the html pages
- insert booktags in the tag method in trunk/apps/tag_app/views 
- insert booktags section in the html of trunk/templates/tags/index.html

5) Using the feeds application
------------------------------
- not a Pinax but a Django's magic: http://docs.djangoproject.com/en/dev/ref/contrib/syndication/
- we use the django-atomformat library
- add feeds in url
- create a feeds.py file with the feed class
- add the feed link in the template

6) Adding comments
------------------
- comments framework is a django magic: http://docs.djangoproject.com/en/dev/ref/contrib/comments/
- many Pinax modules use the threadedcomments module, and here we go
- in book templates insert {% load comments_tag %} and then {% comments post %}
- in books template add {% load threadedcommentstags %} and then the comment section

7) Notifications
----------------
- add notification section in models
- create management.py and add notice types
- syncdb (new record in notice_types: bookstore_book_comment)
- note the new notice type in notice's profile: http://localhost:8000/notices/ (you may opt if receive emails or not)
- add the templates as suggested in the doc (templates/notification/bookstore_book_comment: full.html, full.txt, notice.html, short.txt)
- try adding a new comment on a book
- look at the pinax inbox/notices to find the new notification
- also examine the notices table: http://localhost:8000/admin/notification/notice/ (note the unseen and archived attributes)
- more info: http://pinaxproject.com/docs/dev/external/notification/index.html

8) Flagging contents
--------------------
- we will use the django-flags application, that lets users flag content as inappropriate or spam
- add {% load flagtags %} in the html template (book.html)
- add the flag section in book.html
- add the {% block extra_body %} with the javascript code (like in photos app) in book.html
- note the message in the message bar
- look in FlaggedConten table (http://localhost:8000/admin/flag/flaggedcontent/2/), your flagged book will be there

9) Deploymnet
-------------
- if you use webfaction, use this procedure: http://code.pinaxproject.com/wiki/DetailedPinaxWebfaction/








