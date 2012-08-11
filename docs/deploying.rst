Deploying FLOSS Weekly to a Nginx-powered server
================================================

First time installation
-----------------------
* Install Django (see `1`_ and `2`_)

* Install sqlite

* Install `nginx and python-flup`_

Updating the server
-------------------
Move the project's files to the server

Collect all the static files::

   python manage.py collectstatic

This will put all the files in ``flosstalks/static``. Move those files to the
server, but put them in the ``flosstalks_app/static`` folder. If you don't do
this, the admin site will not have any static resources.

Inside the project, start up fastcgi::

    python ./manage.py runfcgi host=127.0.0.1 port=8080

Set Debug to false in settings.py

Change path to database to be absolute

.. _1: https://www.djangoproject.com/download/
.. _2: https://docs.djangoproject.com/en/dev/intro/install/
.. _nginx and python-flup: https://code.djangoproject.com/wiki/DjangoAndNginx
