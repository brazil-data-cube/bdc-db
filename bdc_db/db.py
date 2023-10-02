#
# This file is part of BDC-DB.
# Copyright (C) 202d INPE.
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

"""Database instance using Flask-SQLAlchemy extension."""

from sqlalchemy import MetaData as _MetaData

from ._compat import SQLAlchemyDB

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


db = SQLAlchemyDB(metadata=metadata)
"""Shared database instance using Flask-SQLAlchemy extension."""
