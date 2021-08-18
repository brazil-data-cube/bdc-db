#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Database management extension configuration.

You can customize any BDC-DB config variable exposing the environment variables::

    export SQLALCHEMY_DATABASE_URI="postgresql://user:pass@locahost/bdc"
    export JSONSCHEMAS_HOST=myhost.org
"""

import os

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                    'postgresql://postgres:postgres@localhost:5432/bdc')
"""The database URI that should be used for the database connection. 

Defaults to ``'postgresql://postgres:postgres@localhost:5432/bdc'``."""

SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
"""Enable (True) or disable (False) signals before and after changes are committed to the database. 

Defaults to ``False``."""

SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', False)
"""Enables or disable debug output of statements to ``stderr``.

Defaults to ``False``."""

JSONSCHEMAS_HOST = os.getenv('JSONSCHEMAS_HOST', 'brazildatacube.org')
"""Define the hostname for any JSONSchemas supported by Brazil Data Cube."""
