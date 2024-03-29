..
    This file is part of BDC-DB.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


Usage
=====


Command-Line Interface (CLI)
----------------------------


The ``BDC-DB`` extension installs a command line tool named ``bdc-db`` that groups a set of database commands under the group ``db``:

- ``init``: Initialize a new database repository if it doesn't exist.

- ``create-namespaces``: Create the table namespaces (schema) in database.

- ``create-extension-postgis``: Enables the PostGIS extenion in the database.

- ``create-schema``: Create the database schema (tables, primary keys, foreign keys).

- ``create-triggers``: Create in the database all triggers registered in the extension.

- ``load-scripts``: Load and execute database scripts.

- ``drop-schema``: Drop the database schema (tables, primary keys, foreign keys).

- ``destroy``: Drop the database repository.

- ``show-triggers``: List all registered triggers.

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

- ``bdc_db.namespaces``: Map of namespaces (table schema) to be created.

- ``bdc_db.schemas``: A folder with any JSONSchema files

- ``bdc_db.scripts``: A folder with SQL scripts to be loaded and executed in the database.

- ``bdc_db.triggers``: A folder with SQL scripts to create triggers.


These entry points may be defined in the ``setup.py`` of your package if you would like to have database support.


The following code is an example of an ``entry_points`` in ``setup.py`` file:


.. code-block:: python

    entry_points={
        'bdc_db.alembic': [
            'myapp = myapp:alembic'
        ],
        'bdc_db.models': [
            'myapp = myapp.models'
        ],
        'bdc_db.namespaces': [
            'myapp = myapp.config:SCHEMA'
        ]
    }


.. note::

    The package ``BDC-DB`` requires an instance of PostgreSQL listening up. You must set ``SQLALCHEMY_DATABASE_URI`` with your own instance.


.. warning::

    When the entry points ``bdc_db.models`` and ``bdc_db.alembic`` is set, make sure you have the target values in your file system.


To deal with migrations, you need to initialize the ``Alembic`` with the following command::

    FLASK_APP=myapp flask alembic mkdir


It will create a folder named ``alembic`` inside ``myapp`` folder. This folder will store all the migration of your project.


.. code-block:: python
    :caption: config.py

    SCHEMA = 'myapp'


You must follow the `SQLAlchemy Models <https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/>`_ in order to deal with models and generate migrations with ``BDC-DB``:


.. code-block:: python
    :caption: models.py

    from bdc_db.db import db


    class Collection(db.Model):
        id = db.Column(db.Integer(), primary_key=True, nullable=False)
        name = db.Column(db.String(), nullable=False)
        title = db.Column(db.String(), nullable=False)
        version = db.Column(db.Integer())


To create `myapp` namespace, use::

    FLASK_APP=myapp flask db create-namespaces


The output will be something like::

    Creating namespace myapp...
    Namespace created!


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


.. example_jsonb:

Using SQLAlchemy JSONB fields with JSONSchemas
----------------------------------------------

.. versionadded:: 0.6.0

We have created a new :class:`bdc_db.sqltypes.JSONB` to support the PostgreSQL JSONB fields with JSONSchema validation using `jsonschema <https://python-jsonschema.readthedocs.io/en/stable/>`_.

In order to do that, you must have to set the entrypoint `bdc.schemas` in `setup.py`:

.. code-block:: python

    entry_points={
        'bdc.schemas': [
            'myapp = myapp.jsonschemas'
        ],
        'bdc_db.models': [
            'myapp = myapp.models'
        ]
    }

After that, you must create a new folder `myapp.jsonschemas` with `__init__.py` inside. The `bdc-db` will be handle the entire folder
according your `myapp` and you must use relative files to refer the JSONSchemas. We recommend you to create `myapp` inside `jsonschemas` to add a prefix and place any JSONSchema in this directory like following::

    - myapp
      - myapp
        - __init__.py
        - jsonschemas
          - __init__.py
          - myapp
            - myschema.json
      - setup.py


And the create the ``models.py`` referring the `myapp/myschema.json`:

.. code-block:: python

    from bdc_db.db import db
    from bdc_db.sqltypes import JSONB


    class Collection(db.Model):
        """Define a simple table to store collections."""

        __table_name__ = 'collections'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String, nullable=False)
        properties = db.Column(JSONB('myapp/myschema.json'))

With ``myapp.models.Collection`` is created, the :class:`bdc_db.sqltypes.JSONB` will validate the field `properties` with the given schema when model is added in memory.

.. code-block:: python

    from bdc_db.db import db
    from flask import current_app
    from myapp.models import Collection

    with current_app.app_context():
        collection = Collection(name='S2_L1C')
        collection.properties = dict()

        db.session.add(collection) # apply validation here

