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


"""Represent the custom data types for BDC-Catalog."""

from typing import Any

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB as _JSONB

from .utils import validate_schema


class JSONB(TypeDecorator):
    """Represent a Custom Data Type for dealing with JSONB and JSONSchemas on SQLAlchemy.

    The :class:`bdc_db.sqltypes.JSONB` type includes the fully support of
    `sqlalchemy.dialects.postgresql.JSONB <https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB>`_,
    including the JSONSchema validator.

    .. versionadded:: 0.6.0

    Examples:
        This examples describes a minimal way to use :class:`bdc_db.sqltypes.JSONB`.
        It expects you have module structure like described in :doc:`usage`, and the
        ``myapp/myschema.json`` is defined as::

            {
                "$schema": "http://json-schema.org/draft-07/schema",
                "$id": "myapp.json",
                "type": "object",
                "title": "Teste",
                "required": [
                    "mykey"
                ],
                "properties": {
                    "mykey": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    }
                }
            }

        In the JSONSchema above, it contains the key ``mykey`` defined, which has the constraint that the
        value ``MUST`` be between ``0`` and ``100``. The following section describes a minimal way to
        insert your model into database:

        .. doctest::
            :skipIf: True

            >>> from bdc_db.db import db
            >>> from bdc_db.sqltypes import JSONB
            >>> class Collection(db.Model):
            ...      # Define a simple table to store collections.
            ...      __table_name__ = 'collections'
            ...      id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            ...      name = db.Column(db.String, nullable=False)
            ...      properties = db.Column(JSONB('myapp/myschema.json'))
            >>> c = Collection()
            >>> c.name = 'Teste'
            >>> c.properties = {"mykey": 10}
            >>> db.session.add(c)
            >>> db.session.commit()
            >>> c.properties = {"mykey": 102}
            >>> db.session.commit()  # Error

    .. seealso::

        `sqlalchemy.dialects.postgresql.JSONB <https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB>`_
    """

    _schema_key: str
    """Keep the JSONSchema relative file path."""
    _draft_checker: Any
    """The JSONSchema draft checker model version."""
    impl = _JSONB
    """Set the SQLAlchemy Data Type to manage this custom type."""
    cache_ok = True
    """Enable cache context for JSONB type. It also removes SQLAlchemy Warnings."""

    def __init__(self, schema: str, draft_checker=None, *args, **kwargs):
        """Build a new data type."""
        self._schema_key = schema
        self._draft_checker = draft_checker
        super().__init__(*args, **kwargs)

    def coerce_compared_value(self, op, value):
        """Define a 'coerced' Python value in an expression.

        Note:
            Implements native SQLAlchemy :class:`~sqlalchemy.dialects.postgresql.JSONB`.
        """
        return self.impl.coerce_compared_value(op, value)

    def process_bind_param(self, value, dialect):
        """Apply JSONSchema validation and bind the JSON value to the SQLAlchemy Engine execution.

        TODO: Use native SQLAlchemy ValidatorError when an error occurs.
        """
        options = dict()
        if self._draft_checker:
            options['draft_checker'] = self._draft_checker
        if value is not None:
            validate_schema(self._schema_key, value, **options)

        return value
