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


@cli.command()
@with_appcontext
def init():
    """Create database repository."""
    click.secho('Creating database {0}...'.format(_db.engine.url),
                bold=True, fg='yellow')

    if not database_exists(str(_db.engine.url)):
        create_database(str(_db.engine.url))

    click.secho('Database created!', bold=True, fg='green')


@cli.command()
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


@cli.command()
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


@cli.command()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-f', '--force', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the database schema (all data will be lost)?')
@with_appcontext
def drop(verbose):
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