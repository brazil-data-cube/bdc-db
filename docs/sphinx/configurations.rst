..
    This file is part of BDC-DB.
    Copyright (C) 2020 INPE.

    BDC-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Extension Configuration
=======================


.. data:: SQLALCHEMY_DATABASE_URI

   The database URI that should be used for the database connection. Defaults to ``'postgresql://postgres:postgres@localhost:5432/bdc'``.


.. data:: SQLALCHEMY_TRACK_MODIFICATIONS

    Enable (True) or disable (False) signals before and after changes are committed to the database. Defaults to ``False``.


.. data:: SQLALCHEMY_ECHO

   Enables or disable debug output of statements to ``stderr``. Defaults to ``False``.
