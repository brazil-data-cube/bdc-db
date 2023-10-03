#
# This file is part of BDC-DB.
# Copyright (C) 2023 INPE.
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

"""Define the compatibility for BDC-DB and theirs dependencies."""

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemyDB(_SQLAlchemy):
    """Represent the wrapper for ``Flask-SQLAlchemy`` to achieve compatibility for Alembic Extension module.

    Since the Flask-SQLAlchemy 3.0+, the property ``db`` used for ``Flask-Alembic`` is not supported.
    The change bellow ``db`` is just a wrapper to act like a connector flask alembic extension.
    It must be removed when the fix
    `flask-alembic#pr3 <https://github.com/davidism/flask-alembic/pull/3>`_ is merged and versioned.
    """

    @property
    def db(self) -> 'SQLAlchemyDB':
        """Wrap the ``db`` property to act like Flask SQLAlchemy instance."""
        return self
