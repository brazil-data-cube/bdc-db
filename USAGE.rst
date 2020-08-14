..
    This file is part of BDC-DB.
    Copyright (C) 2020 INPE.

    BDC-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Usage
=====


Command-Line Interface (CLI)
----------------------------


The ``BDC-DB`` extension installs a command line toll named ``bdc-db`` that groups a set of database commands under the group ``db``:

- ``create-schema``: Create the database schema (tables, primary keys, foreign keys).

- ``drop-schema``: Drop the database schema (tables, primary keys, foreign keys).

- ``init``: Initialize a new database repository if it doesn't exist.

- ``destroy``: Drop the database repository.


Preparing a new Package with Alembic and BDC-DB
-----------------------------------------------


The Alembic commands are available trough the ``alembic`` command group. These are the the commands for managing upgrade recipes.

The ``BDC-DB`` follows the `Python Entry point specification <https://packaging.python.org/specifications/entry-points/>`_ to
discover and loads libraries dynamically.

Basically, the ``BDC-DB`` has two major entry point to deal with dynamic SQLAlchemy models:

    - ``bdc_db.alembic`` - The alembic migration folders.
    - ``bdc_db.models`` - The initialization of your own models.

Both of them must be defined in ``setup.py`` in your package if you would like to have database support.

The following code is an example of ``setup.py`` file:

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

        The package ``BDC-DB`` requires an instance of PostgreSQL listening up. You must set ``SQLALCHEMY_DATABASE_URI`` with your
        own instance.


.. warning::

        When the entry points ``bdc_db.models`` and ``bdc_db.alembic`` is set, make sure you have the target values in your file system.


To deal with migrations, you need to initialize the ``Alembic`` with the following command:

.. code-block:: shell

        FLASK_APP=myapp flask alembic mkdir

It will creates an folder named ``alembic`` inside ``myapp`` folder. This folder will store all the migration of your project.

You must follow the `SQLAlchemy Models <https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/>`_ in order to deal with models and generate migrations with ``BDC-DB``:

.. code-block:: python

        from bdc_db.db import db


        class Collection(db.Model):
            id = db.Column(db.Integer(), primary_key=True, nullable=False)
            name = db.Column(db.String(), nullable=False)
            title = db.Column(db.String(), nullable=False)
            version = db.Column(db.Integer())


Once model is set, you must generate a migration. To do that, use the command ``alembic revision``.


.. code-block:: shell

        FLASK_APP=myapp flask alembic revision "my app migration" --branch=myapp


The output will be something like:

.. code-block:: shell

        INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
        INFO  [alembic.runtime.migration] Will assume transactional DDL.
        INFO  [alembic.autogenerate.compare] Detected added table 'collection'


.. warning::

        Whenever you must to create a revision with ``alembic revision`` command, make sure you have set the parameter ``--branch``
        to ``BDC-DB`` put your migrations in the right place. Otherwise, it will move to ``site-packages/bdc_db/alembic``.
