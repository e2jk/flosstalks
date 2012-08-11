Altering the database to add a new field to a model
===================================================

Django does not alter existing tables when running ``python manage.py syncdb``,
so you will have to do that manually.

Adding a new field
------------------

In the ``flosstalks_app/models.py`` file, add a new class variable to the model
that you want to extend. Example if adding a new description_source field to
the Project model::

   description_source = models.URLField("Source of the description", null=True, blank=True)

Run ``python manage.py sql flosstalks_app`` and locate the line related to the
field you just added. Continuing with the previous example, the following line
in the ``flosstalks_app_project`` table is relevant::

   "description_source" varchar(200),

Start the sqlite command-line client by calling ``python manage.py dbshell``,
then execute the appropriate ``ALTER TABLE`` statement, example::

   ALTER TABLE flosstalks_app_project ADD COLUMN "description_source" varchar(200);

Your database now has a new field! You can confirm that by executing the
``.schema flosstalks_app_project`` command in the database client.

