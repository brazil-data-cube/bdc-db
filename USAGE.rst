..
    This file is part of BDC-DB.
    Copyright (C) 2020 INPE.

    BDC-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Usage
=====


Command-Line Interface (CLI)
----------------------------


The ``BDC-DB`` extension installs a command line tool named ``bdc-db`` that groups a set of database commands under the group ``db``:

- ``init``: Initialize a new database repository if it doesn't exist.

- ``create-namespace``: Create the table namespace (schema) in database.

- ``create-extension-postgis``: Enables the PostGIS extenion in the database.

- ``create-schema``: Create the database schema (tables, primary keys, foreign keys).

- ``create-triggers``: Create in the database all triggers registered in the extension.

- ``load-scripts``: Load and execute database scripts.

- ``drop-schema``: Drop the database schema (tables, primary keys, foreign keys).

- ``destroy``: Drop the database repository.

- ``show-triggers``: List all registred triggers.

- ``load-file``: Load and execute a script file into database.


Preparing a new Package with Alembic and BDC-DB
-----------------------------------------------


The Alembic commands are available trough the ``alembic`` command group. These are the commands for managing upgrade recipes:

- ``branches``: Show branch points.

- ``current``: Show current revision.

- ``downgrade``: Run downgrade migrations.

- ``heads``: Show latest revisions.

- ``log``: Show revision log.

- ``merge``: Create merge revision.

- ``mkdir``: Make migration directory.

- ``revision``: Create new migration.

- ``show``: Show the given revisions.

- ``stamp``: Set current revision.

- ``upgrade``: Run upgrade migrations.


.. note::

    For more information, type in the command line::

        bdc-db alembic --help


The ``BDC-DB`` follows the `Python Entry point specification <https://packaging.python.org/specifications/entry-points/>`_ to
discover and load libraries dynamically.


Basically, the ``BDC-DB`` has the following entry points to deal with dynamic SQLAlchemy models and daabase scripts:

- ``bdc_db.alembic``: The alembic migration folders.

- ``bdc_db.models``: The initialization of your own models.

- ``bdc_db.triggers``: A folder with SQL scripts to create triggers.

- ``bdc_db.scripts``: A folder with SQL scripts to be loaded and executed in the database.


These entry points may be defined in the ``setup.py`` of your package if you would like to have database support.


The following code is an example of an ``entry_points`` in ``setup.py`` file:


.. code-block:: python

    entry_points={
        'bdc_db.alembic': [
            'myapp = myapp:alembic'
        ],
        'bdc_db.models': [
            'myapp = myapp.models'
        ]
    }


.. note::

    The package ``BDC-DB`` requires an instance of PostgreSQL listening up. You must set ``SQLALCHEMY_DATABASE_URI`` with your own instance.


.. warning::

    When the entry points ``bdc_db.models`` and ``bdc_db.alembic`` is set, make sure you have the target values in your file system.


To deal with migrations, you need to initialize the ``Alembic`` with the following command::

    FLASK_APP=myapp flask alembic mkdir


It will create a folder named ``alembic`` inside ``myapp`` folder. This folder will store all the migration of your project.


You must follow the `SQLAlchemy Models <https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/>`_ in order to deal with models and generate migrations with ``BDC-DB``:


.. code-block:: python

    from bdc_db.db import db


    class Collection(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        name = db.Column(db.String(), nullable=False)
        title = db.Column(db.String(), nullable=False)
        version = db.Column(db.Integer())


Once the model is set, you must generate a migration. To do that, use the command ``alembic revision``::

    FLASK_APP=myapp flask alembic revision "my app migration" --branch=myapp


The output will be something like::

    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    INFO  [alembic.autogenerate.compare] Detected added table 'collection'


.. warning::

    Whenever you create a revision with ``alembic revision`` command, make sure you have set the parameter ``--branch`` to ``BDC-DB``. This will put your migrations in the right place. Otherwise, it will move to ``site-packages/bdc_db/alembic``.


Loading package SQL scripts SQLAlchemy and BDC-DB
-------------------------------------------------


The ``BDC-DB`` also supports to load files ``.sql`` dynamically using `Python Entry point specification <https://packaging.python.org/specifications/entry-points/>`_.


It is quite useful if you need to configure you environment, setting up `PostgreSQL PL/pgSQL Triggers <https://www.postgresql.org/docs/12/plpgsql-trigger.html>`_ and default script data.


To do that, you must define the entrypoint ``bdc_db.triggers`` in your application ``setup.py`` file as following:


.. code-block:: python

    entry_points={
        'bdc_db.triggers': [
            'myapp = myapp.triggers'
        ],
        'bdc_db.scripts': [
            'myapp = myapp.scripts'
        ]
    }


Once ``entrypoint`` is set, the ``BDC-DB`` will list entire directory for ``.sql`` files and map them to the application context.


You can show the triggers loaded (In-Memory) by ``BDC-DB`` command line::

    bdc-db db show-triggers


To register them into the database system, use the command::

    bdc-db db create-triggers


You can also load all data scripts with command::

    bdc-db db load-scripts


.. note::

    Make sure to have set ``SQLALCHEMY_DATABASE_URI``. Please refer to `Configurations <./configurations.html>`_ for further information.