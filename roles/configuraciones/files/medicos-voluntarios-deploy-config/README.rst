MEDICOS VOLUNTARIOS
===================


Dependencies
------------

At operating system, some packages need to be installed:

#. This project works with PostgreSQL and PostGIS, you can install it
   following this tutorial (for Debian 10 or Ubuntu 18):
   https://computingforgeeks.com/how-to-install-postgis-on-ubuntu-debian/

#. After creating the database, make sure to create the ``postgis``
   extension:

   .. code-block:: sql

      CREATE EXTENSION postgis;

   if the extension already exists and you want to update its version:

   .. code-block:: sql

      ALTER EXTENSION postgis UPDATE;


#. Install ``libgdal``: ``sudo apt-get install ligbdal20``

We use ``pip-tools`` (https://pypi.org/project/pip-tools/) to manage our
dependencies.

This project has 3 environments to use:

-  ``development``: To be run on development stage
-  ``production``: To be run in production stage
-  ``test``: To be run on CI automated tests or locally if desired

Shared dependencies go in ``base.in``

If you change any of the ``.in`` files, you must re-compile the ``.txt``
with ``requirements/compile-reqs.sh``

Setup
-----

#. Setup a virtual environment to use with this project.

#. Be sure to have ``pip`` updated and install ``pip-tools`` with:
   ``pip install -U pip pip-tools``.

#. This project is ready to be used in 3 different environments,
   *local development*, *deployed on production* and to *run tests*; you
   can install the dependencies for each environment as needed, for
   example:

   - To install dependencies for *local development* just run:
     ``pip install -U -r requirements/development.txt`` or even better
     use ``pip-sync requirements/development.txt``.
   - To install dependencies for a *deployed on production server* just
     run: ``pip install -U -r requirements/production.txt`` or even better
     use ``pip-sync requirements/production.txt``.

#. This project uses ``pip-tools`` so if you add a new dependency to
   use, you can add it to the correspondent `.in` file located in the
   ``requirements/`` folder, then run the ``./compile_reqs.sh`` script
   to update the requirements ``.txt`` files to later use it to install
   the dependencies.

#. Setup a ``.env`` file based on ``.env.sample`` file, configuring the
   environment variables according to the stage you're using/deploying
   the project.


Running
-------

The following are needed on a fresh install or if there are new packages
/ migrations:

#. Install the dependencies for this project according to the
   environment you're running it.

#. Run the migrations ``./manage.py migrate``.

#. ``./manage.py runserver``

#. Visit http://127.0.0.1:8000/ (or the corresponding URL) and
   celebrate!
