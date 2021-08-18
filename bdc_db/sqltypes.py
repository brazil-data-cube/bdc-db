#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


"""Represent the custom data types for BDC-Catalog."""

from typing import Any

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB as _JSONB

from .utils import validate_schema


class JSONB(TypeDecorator):
    """Represent a Custom Data Type for dealing with JSONB and JSONSchemas on SQLAlchemy.

    The :class:`bdc_db.sqltypes.JSONSchemaType` type includes the fully support of
    `sqlalchemy.dialects.postgresql.JSONB <https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB>`_,
    including the JSONSchema validator.

    .. versionadded:: 0.6.0

    .. seealso::

        `sqlalchemy.dialects.postgresql.JSONB <https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB>`_
    """

    _schema_key: str
    """Keep the JSONSchema relative file path."""
    _draft_checker: Any
    """The JSONSchema draft checker model version."""
    impl = _JSONB
    """Set the SQLAlchemy Data Type to manage this custom type."""

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
