#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Command-Line Interface for BDC database management."""

import click
from flask.cli import FlaskGroup, with_appcontext
from sqlalchemy_utils.functions import (create_database, database_exists,
                                        drop_database)

from . import create_app as _create_app
from .db import db as _db


def abort_if_false(ctx, param, value):
    """Callback that checks the user confirmation of a command."""
    if not value:
        ctx.abort()


@click.group(cls=FlaskGroup, create_app=_create_app)
def cli():
    """Database commands.

    .. note:: You can invoke more than one subcommand in one go.
    """


@cli.group()
def db():
    """More database commands.

    .. note:: You can invoke more than one subcommand in one go.
    """

@db.command()
@with_appcontext
def init():
    """Create database repository."""
    click.secho('Creating database {0}...'.format(_db.engine.url),
                bold=True, fg='yellow')

    if not database_exists(str(_db.engine.url)):
        create_database(str(_db.engine.url))

    click.secho('Database created!', bold=True, fg='green')


@db.command()
@click.option('-f', '--force', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
@with_appcontext
def destroy():
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

    if not database_exists(str(_db.engine.url)):
        click.secho('Database repository does not exist. '
                    'Use option \'--init\' before!',
                    bold=True, fg='red')
        return

    with click.progressbar(_db.metadata.sorted_tables) as bar:
        for table in bar:
            if verbose:
                click.echo(' Creating table {0}'.format(table))
            table.create(bind=_db.engine, checkfirst=True)

    click.secho('Database schema created!',
                bold=True, fg='green')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-f', '--force', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the database schema (all data will be lost)?')
@with_appcontext
def drop_schema(verbose):
    """Drop the database schema.

    The tables will be dropped in reverse sort order of
    the foreign key dependency.
    """
    click.secho('Dropping database schema...', bold=True, fg='yellow')

    with click.progressbar(reversed(_db.metadata.sorted_tables)) as bar:
        for table in bar:
            if verbose:
                click.echo(' Dropping table {0}'.format(table))
            table.drop(bind=_db.engine, checkfirst=True)

    click.secho('Database schema dropped!', bold=True, fg='green')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@with_appcontext
def create_namespace(verbose):
    """Create the table namespace (schema) in database."""
    schema = _db.metadata.schema

    if schema is None:
        return click.secho('No namespace configured in metadata.', bold=True, fg='red')

    click.secho(f'Creating namespace {schema}...', bold=True, fg='yellow')

    with _db.session.begin_nested():
        _db.session.execute(f'CREATE SCHEMA {schema}')
    _db.session.commit()

    click.secho('Namespace created!', bold=True, fg='green')


@db.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@with_appcontext
def create_extension_postgis(verbose):
    """Create extension PostGIS in database."""
    click.secho(f'Creating extension postgis...', bold=True, fg='yellow')

    with _db.session.begin_nested():
        _db.session.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    _db.session.commit()

    click.secho('Extension created!', bold=True, fg='green')
