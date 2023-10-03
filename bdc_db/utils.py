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

"""Utility for Image Catalog Extension."""

import typing as t
from dataclasses import dataclass

import jsonschema
from flask import current_app
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def validate_schema(schema_key: str, value: t.Any, draft_checker=None) -> t.Any:
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

    draft_checker = draft_checker or jsonschema.FormatChecker()
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


def list_triggers(engine: Engine) -> t.List[TriggerResult]:
    """List all the available triggers on current engine.

    Args:
        engine (Engine): The activate SQLAlchemy database connector.
    """
    query_result = execute(
        "SELECT event_object_schema as schema,"
        "       event_object_table as table_name,"
        "       trigger_schema,"
        "       trigger_name,"
        "       action_statement as definition, "
        "       string_agg(event_manipulation, ',') as trigger_event "
        "  FROM information_schema.triggers "
        "GROUP BY schema,table_name,trigger_schema,trigger_name,definition "
        "ORDER BY schema, table_name",
        engine
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

    execute(f'DROP TRIGGER IF EXISTS {name} ON {schema}.{table}', engine)


def execute(statement: t.Union[str, t.Any], executor: t.Union[Engine, t.Any], *args, **kwargs):
    """Execute a query statement in SQLAlchemy database engine.

    Args:
        statement: Query or SQLAlchemy query expression to execute
        executor: The database engine to create connections
    """
    if isinstance(statement, str):
        statement = text(statement)

    if isinstance(executor, Engine):
        with executor.connect() as conn:
            result = conn.execute(statement, *args, **kwargs)
    else:
        result = executor.execute(statement, *args, **kwargs)

    return result


def has_schema(engine: Engine, schema: str, **kwargs) -> bool:
    """Check if the database schema (namespace) exists.

    Args:
        engine: The SQLAlchemy engine object.
        schema: Database schema (namespace).
    Keyword Args:
        ** Any extra parameter supported by Engine dialect.
    """
    inspector = inspect(engine)
    return inspector.has_schema(schema, **kwargs)
