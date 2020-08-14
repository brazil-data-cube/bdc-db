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



