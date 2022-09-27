#
# This file is part of BDC-DB.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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

SQLALCHEMY_ENGINE_OPTIONS = dict(
    pool_pre_ping=True
)
"""Set default engine options for SQLAlchemy instance.

See more in `EngineOptions <https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine.params.pool>`_.
"""
