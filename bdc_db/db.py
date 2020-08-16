#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Database instance using Flask-SQLAlchemy extension."""

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import MetaData as _MetaData

# See more in https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
NAMING_CONVENTION = {
  "ix": 'idx_%(column_0_label)s',
  "uq": "%(table_name)s_%(column_0_name)s_key",
  "ck": "%(table_name)s_%(constraint_name)s_ckey",
  "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
  "pk": "%(table_name)s_pkey"
}
"""Naming convention for SQLAlchemy constraint keys"""

metadata = _MetaData(naming_convention=NAMING_CONVENTION)
"""Default database metadata object holding associated schema constructs."""


db = _SQLAlchemy(metadata=metadata)
"""Shared database instance using Flask-SQLAlchemy extension."""
