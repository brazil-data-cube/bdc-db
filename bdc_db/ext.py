#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Database management extension for Brazil Data Cube applications and services."""

import os

import pkg_resources
from flask import current_app
from flask_alembic import Alembic
from sqlalchemy.orm import configure_mappers


def alembic_include_object(object, name, type_, reflected, compare_to):
    """Ignores the tables in 'exclude_tables'.

    For more information, please, refer to the
    `Runtime Objects section <https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object>`_
    in the Alembic documentation.

    Args:
        object: A SchemaItem object ( Table, Column, Index UniqueConstraint, or ForeignKeyConstraint object).
        name: The name of the object.
        type\_: A string describing the type of object ("table", "column", "index", "unique_constraint", or "foreign_key_constraint").
        reflected: True if the given object was produced based on table reflection, False if it’s from a local MetaData object.
        compare_to: The object being compared against, if available, else None.

    Returns:
        True if the given object should be considered in the autogenerate sweep, otherwise, returns False.
    """
    exclude_tables = current_app.config.get('ALEMBIC_EXCLUDE_TABLES', [])

    return not ((type_ == 'table') and (name in exclude_tables))


class BrazilDataCubeDB:
    """Database management extension for Brazil Data Cube applications and services.

    Attributes:
        alembic: A Flask-Alembic instance used to prepare migration environment.
    """

    def __init__(self, app=None, **kwargs):
        """Initialize the database management extension.

        Args:
            app: Flask application
            kwargs: Optional arguments to Flask-SQLAlchemy.
        """
        self.alembic = Alembic(run_mkdir=False, command_name='alembic')

        if app:
            self.init_app(app, **kwargs)


    def init_app(self, app, **kwargs):
        """Initialize Flask application instance.

        This method prepares the Alembic configuration for multiple named
        branches according to each package entry point.

        Args:
            app: Flask application
            kwargs: Optional arguments to Flask-SQLAlchemy.
        """
        self.init_db(app, **kwargs)

        # prepare the configuration for multiple named branches
        # according to each package entry point
        script_location = pkg_resources.resource_filename('bdc_bdc', 'alembic')

        version_locations = [
            (base_entry.name, pkg_resources.resource_filename(
                base_entry.module_name, os.path.join(*base_entry.attrs, )
            )) for base_entry in pkg_resources.iter_entry_points('bdc_db.alembic'
            )
        ]

        if ('bdc_db', script_location) in version_locations:
            version_locations.remove(('bdc_db', script_location))

        app.config.setdefault('ALEMBIC', {
            'script_location': script_location,
            'version_locations': version_locations,
        })

        # Exclude PostGIS tables from migration
        exclude_tables = [
            'spatial_ref_sys',
        ]

        app.config.setdefault('ALEMBIC_EXCLUDE_TABLES', exclude_tables)

        # Use a default callable function or one provided
        # in kwargs in order to give the chance to consider
        # an object in the autogenerate sweep.
        handler_include_table = kwargs.get('include_object', alembic_include_object)

        # Set the Alembic environment context
        app.config.setdefault('ALEMBIC_CONTEXT', {
            'compare_type': True,
            'include_schemas': True,
            'include_object': handler_include_table,

        })

        # Initialize Flask-Alembic extension
        self.alembic.init_app(app)

        # Add BDC-DB extension to Flask extension list
        app.extensions['bdc-db'] = self


    def init_db(self, app, entry_point_group = 'bdc_db.models', **kwargs):
        """Initialize Flask-SQLAlchemy extension.

        Args:
            app: Flask application
            entry_point_group: Entrypoint definition to load models
            kwargs: optional Arguments to Flask-SQLAlchemy.
        """
        # Setup SQLAlchemy
        app.config.setdefault(
            'SQLALCHEMY_DATABASE_URI',
            os.environ.get('SQLALCHEMY_DATABASE_URI')
        )

        app.config.setdefault(
            'SQLALCHEMY_TRACK_MODIFICATIONS',
            os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        )

        app.config.setdefault('SQLALCHEMY_ECHO', False)

        # Initialize Flask-SQLAlchemy extension.
        database = kwargs.get('db', db)
        database.init_app(app)

        # Loads all models
        if entry_point_group:
            for base_entry in pkg_resources.iter_entry_points(entry_point_group):
                base_entry.load()

        # All models should be loaded by now.
        # Initialize the inter-mapper relationships of all loaded mappers.
        configure_mappers()