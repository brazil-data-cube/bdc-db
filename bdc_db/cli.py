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

"""Command-Line Interface for BDC database management."""

import click
from flask import current_app
from flask.cli import FlaskGroup, with_appcontext
from sqlalchemy.sql.ddl import CreateSchema
from sqlalchemy_utils.functions import (create_database, database_exists,
                                        drop_database)

from . import create_app as _create_app
from .db import db as _db
from .utils import delete_trigger, execute, has_schema, list_triggers


def abort_if_false(ctx, param, value):
    """Callback that checks the user confirmation of a command."""
    if not value:
        ctx.abort()


@click.group(cls=FlaskGroup, create_app=_create_app)
def cli():
    """Database commands.

    . note:: You can invoke more than one subcommand in one go.
    """


@cli.group()
def db():
    """More database commands.

    . note:: You can invoke more than one subcommand in one go.
    """


@db.command()
@with_appcontext
def init():
    """Create database repository."""
    click.secho('Creating database {0}...'.format(_db.engine.url),
                bold=True, fg='yellow')

    if not database_exists(_db.engine.url):
        create_database(_db.engine.url)

    click.secho('Database created!', bold=True, fg='green')


@db.command()
@click.option('-f', '--force', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
@with_appcontext
def destroy():  # pragma: no cover
    """Drop database repository."""
    click.secho('Dropping database {0}...'.format(_db.engine.url),
                bold=True, fg='yellow')

    drop_database(_db.engine.url)

    click.secho('Database dropped!', bold=True, fg='green')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@with_appcontext
def create_schema(verbose):
    """Create tables.

    The tables will be created in sorted order of
    the foreign key dependency.
    """
    click.secho('Creating database schema...', bold=True, fg='yellow')

    if not database_exists(_db.engine.url):
        click.secho('Database repository does not exist. '
                    'Use option \'--init\' before!',
                    bold=True, fg='red')
        return

    with click.progressbar(_db.metadata.sorted_tables) as bar:
        for table in bar:
            if verbose:
                click.echo('\tCreating table {0}'.format(table))
            table.create(bind=_db.engine, checkfirst=True)

    click.secho('Database schema created!',
                bold=True, fg='green')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-f', '--force', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the database schema (all data will be lost)?')
@with_appcontext
def drop_schema(verbose):  # pragma: no cover
    """Drop the database schema.

    The tables will be dropped in reverse sort order of
    the foreign key dependency.
    """
    click.secho('Dropping database schema...', bold=True, fg='yellow')

    with click.progressbar(reversed(_db.metadata.sorted_tables)) as bar:
        for table in bar:
            if verbose:
                click.echo('\tDropping table {0}'.format(table))
            table.drop(bind=_db.engine, checkfirst=True)

    click.secho('Database schema dropped!', bold=True, fg='green')


@db.command()
@with_appcontext
def create_namespaces():
    """Create the loaded table namespaces (schemas) in database."""
    ext = current_app.extensions['bdc-db']

    with _db.session.begin_nested():
        for namespace in ext.namespaces:
            click.secho(f'Creating namespace {namespace}...', bold=True, fg='yellow')
            if not has_schema(_db.engine, namespace):
                execute(CreateSchema(namespace), executor=_db.session)

    _db.session.commit()

    click.secho('Namespaces created!', bold=True, fg='green')


@db.command()
@with_appcontext
def show_namespaces():
    """List the supported namespaces by BDC-DB extension."""
    ext = current_app.extensions['bdc-db']

    click.secho(f'Available namespaces: ', bold=True, fg='green')
    for namespace in ext.namespaces:
        click.secho(f'\t-> {namespace}', bold=True, fg='green')


@db.command()
@with_appcontext
def create_extension_postgis():
    """Enables the PostGIS extenion in the database."""
    click.secho(f'Creating extension postgis...', bold=True, fg='yellow')

    with _db.session.begin_nested():
        execute('CREATE EXTENSION IF NOT EXISTS postgis', executor=_db.session)
    _db.session.commit()

    click.secho('Extension created!', bold=True, fg='green')


@db.command()
@with_appcontext
def show_triggers():
    """List the trigger definition files registered in ``BDC-DB`` extension."""
    ext = current_app.extensions['bdc-db']

    for module_name, entry in ext.triggers.items():
        click.secho(f'Available triggers in "{module_name}"', bold=True, fg='green')

        for file_name, script in entry.items():
            click.secho(f'\t-> {script}', bold=True, fg='green')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@with_appcontext
def create_triggers(verbose):
    """Create in the database the triggers registered in ``BDC-DB`` extension."""
    ext = current_app.extensions['bdc-db']

    with _db.session.begin_nested():
        if len(ext.triggers.keys()) == 0:
            click.secho(f'No trigger configured.', bold=True, fg='yellow')

        for module_name, entry in ext.triggers.items():
            click.secho(f'Registering triggers from "{module_name}"', bold=True, fg='yellow')

            for file_name, script in entry.items():
                with open(script) as f:
                    content = f.read()

                click.secho(f'\t-> {script}', bold=True, fg='green')

                if verbose:
                    click.secho(content)

                execute(content, executor=_db.session)

            click.secho(f'Triggers from "{module_name}" registered', bold=True, fg='green')

    _db.session.commit()


@db.command()
@click.option('-p', '--preview', help='Preview the affected triggers (Do not remove).',
              type=click.BOOL, is_flag=True, default=False)
@with_appcontext
def drop_triggers(preview: bool):
    """Delete the triggers on database that were loaded by BDC-DB Modules."""
    ext = current_app.extensions['bdc-db']
    if len(ext.triggers.keys()) == 0:
        click.secho(f'No trigger configured.', bold=True, fg='yellow')
        return

    db_triggers = list_triggers(_db.engine)

    triggers_to_remove = []
    for module_name, entry in ext.triggers.items():
        for file_name, script in entry.items():
            with open(script) as f:
                sql = f.read()

            for db_trigger in db_triggers:
                # TODO: Compare using schema and trigger name
                if db_trigger.trigger_name in sql:
                    triggers_to_remove.append((module_name, script, db_trigger))

    if triggers_to_remove:
        context_msg = 'will be' if preview else 'was'
        for (module_name, script_path, trigger) in triggers_to_remove:
            if not preview:
                delete_trigger(trigger.trigger_name, table=trigger.table_name, schema=trigger.schema, engine=_db.engine)
            click.secho(f'The trigger "{trigger.trigger_name}" '
                        f'{context_msg} removed. (from module {module_name})',
                        bold=True, fg='yellow' if preview else 'green')
        return

    click.secho(f'No trigger available in db.', bold=True, fg='yellow')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@with_appcontext
def load_scripts(verbose):
    """Load the database scripts registered in ``BDC-DB`` extension."""
    ext = current_app.extensions['bdc-db']

    with _db.session.begin_nested():
        if len(ext.scripts.keys()) == 0:
            click.secho(f'No scripts configured.', bold=True, fg='yellow')

        for module_name, entry in ext.scripts.items():
            click.secho(f'Executing scripts from "{module_name}"', bold=True, fg='yellow')

            for file_name, script in entry.items():
                with open(script) as f:
                    content = f.read()

                click.secho(f'\t-> {script}', bold=True, fg='yellow')

                if verbose:
                    click.secho(content)

                execute(content, executor=_db.session)

            click.secho(f'Scripts from "{module_name}" executed!', bold=True, fg='green')

    _db.session.commit()


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-f', '--file', type=click.File('r'),
              help='A SQL input file for insert.',
              required=True)
@with_appcontext
def load_file(verbose, file: click.File):
    """Load and execute a script file into database."""
    sql = file.read()

    click.secho(f'Loading file {file.name}...', bold=True, fg='yellow')

    if verbose:
        click.echo(sql)

    with _db.session.begin_nested():
        execute(sql, executor=_db.session)

    _db.session.commit()

    click.secho(f'File {file.name} loaded!', bold=True, fg='green')
