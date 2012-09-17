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

If this is the first time you are configuring this environment, perform the
steps outlined below. Else, just restart the ``fastcgi`` process::

    sudo /etc/init.d/php-fastcgi restart

Additional first-time setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^
These steps only need to be performed once when configuring a new environment.

Create an empty file called ``settings_production.py`` to indicate that this is
a production environment::

    touch /var/www/flosstalks.org/flosstalks/settings_production.py

Create the following symlinks::

    sudo ln -s /var/www/flosstalks.org/config/flosstalks.org.nginx /etc/nginx/sites-available/flosstalks.org
    sudo ln -s /etc/nginx/sites-available/flosstalks.org /etc/nginx/sites-enabled/flosstalks.org
    sudo ln -s /var/www/flosstalks.org/config/django-fastcgi /etc/init.d/php-fastcgi

Start nginx and fastcgi up::

    sudo /etc/init.d/nginx start
    sudo /etc/init.d/php-fastcgi start

.. _1: https://www.djangoproject.com/download/
.. _2: https://docs.djangoproject.com/en/dev/intro/install/
.. _nginx and python-flup: https://code.djangoproject.com/wiki/DjangoAndNginx
