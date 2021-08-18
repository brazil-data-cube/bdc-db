#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Utility for Image Catalog Extension."""

from typing import Any

import jsonschema
from flask import current_app


def validate_schema(schema_key: str, value: Any, draft_checker=jsonschema.draft7_format_checker) -> Any:
    """Validate a JSONSchema according a json model.

    .. versionadded:: 0.6.0

    Raises:
        jsonschema.ValidationError: When the current value does not match with expected schema.

    Note:
        This method works under a Flask Application Context since it seeks for JSONSchema
        loaded into :func:`~bdc_db.ext.BrazilDataCubeDB`

    Args:
        schema_key (str): The schema key path reference to the `jsonschemas` folder.
        value (Any): The model value to be validated.
        draft_checker (jsonschema.FormatChecker): The format checker validation for schemas.
    """
    extension = current_app.extensions['bdc-db']

    schema = extension.schemas.get_schema(schema_key)
    jsonschema.validate(instance=value, schema=schema, format_checker=draft_checker)

    return value
