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

"""Utility for Image Catalog Extension."""

from dataclasses import dataclass
from typing import Any, List

import jsonschema
from flask import current_app
from sqlalchemy.engine import Engine


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


@dataclass
class TriggerResult:
    """Represent a Queryable Trigger Result."""

    schema: str
    table_name: str
    trigger_schema: str
    trigger_name: str
    event: str
    definition: str


def list_triggers(engine: Engine) -> List[TriggerResult]:
    """List all the available triggers on current engine.

    Args:
        engine (Engine): The activate SQLAlchemy database connector.
    """
    query_result = engine.execute(
        "SELECT event_object_schema as schema,"
        "       event_object_table as table_name,"
        "       trigger_schema,"
        "       trigger_name,"
        "       action_statement as definition, "
        "       string_agg(event_manipulation, ',') as trigger_event "
        "  FROM information_schema.triggers "
        "GROUP BY schema,table_name,trigger_schema,trigger_name,definition "
        "ORDER BY schema, table_name"
    )

    return [
        TriggerResult(trigger.schema, trigger.table_name, trigger.trigger_schema,
                      trigger.trigger_name, trigger.trigger_event, trigger.definition)
        for trigger in query_result
    ]


def delete_trigger(name: str, engine: Engine, table: str, schema: str = None):
    """Delete a trigger context (if exists) on database.

    Args:
        name (str): The trigger name.
        engine (Engine): The SQLAlchemy active database engine.
        table (str): The table name.
        schema (str): The table schema that the trigger is attached.
    """
    schema = schema or 'public'

    engine.execute(f'DROP TRIGGER IF EXISTS {name} ON {schema}.{table}')
