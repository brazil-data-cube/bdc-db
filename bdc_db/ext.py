#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Database management extension for Brazil Data Cube applications and services."""

import os
from pathlib import Path
from typing import Dict, Iterable, List

import pkg_resources
from flask import current_app
from flask_alembic import Alembic
from invenio_jsonschemas import InvenioJSONSchemas
from sqlalchemy.orm import configure_mappers

from . import config as _config
from .db import db as _db


def alembic_include_object(object, name, type_, reflected, compare_to):
    """Ignores the tables in 'exclude_tables'.

    For more information, please, refer to the
    `Runtime Objects section <https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object>`_
    in the Alembic documentation.

    Args:
        object: A SchemaItem object ( Table, Column, Index UniqueConstraint, or ForeignKeyConstraint object).
        name: The name of the object.
        type_: A string describing the type of object ("table", "column", "index", "unique_constraint", or "foreign_key_constraint").
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

    triggers: Dict[str, Dict[str, str]] = None
    scripts: Dict[str, Dict[str, str]] = None
    namespaces: List[str] = []
    schemas: InvenioJSONSchemas = None

    def __init__(self, app=None, **kwargs):
        """Initialize the database management extension.

        Args:
            app: Flask application
            kwargs: Optional arguments to Flask-SQLAlchemy.
        """
        self.triggers = dict()
        self.scripts = dict()
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

        Keyword Args:
            entry_point_group (str): Custom entry point group for SQLAlchemy database models.
            entry_point_jsonschemas (str): Custom entry point group for JSONSchemas
            engine_options (dict): Custom SQLAlchemy Engine Options for instance object.
        """
        self.init_db(app, **kwargs)

        # Load package namespaces
        self.load_namespaces()

        # Load package triggers
        self.load_triggers(**kwargs)

        # Load package SQL scripts
        self.load_scripts(**kwargs)

        # prepare the configuration for multiple named branches
        # according to each package entry point
        script_location = pkg_resources.resource_filename('bdc_db', 'alembic')

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

        self.schemas = InvenioJSONSchemas(app, entry_point_group=kwargs.get('entry_point_jsonschemas', 'bdc.schemas'))

        # Add BDC-DB extension to Flask extension list
        app.extensions['bdc-db'] = self

    def init_db(self, app, entry_point_group: str = 'bdc_db.models', engine_options=None, **kwargs):
        """Initialize Flask-SQLAlchemy extension.

        Args:
            app: Flask application
            entry_point_group: Entrypoint definition to load models
            engine_options: DB instance engine options
            kwargs: optional Arguments to Flask-SQLAlchemy.
        """
        # Setup SQLAlchemy
        app.config.setdefault('SQLALCHEMY_DATABASE_URI',
                              _config.SQLALCHEMY_DATABASE_URI)

        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS',
                              _config.SQLALCHEMY_TRACK_MODIFICATIONS)

        app.config.setdefault('SQLALCHEMY_ECHO',
                              _config.SQLALCHEMY_ECHO)

        app.config.setdefault('JSONSCHEMAS_HOST', _config.JSONSCHEMAS_HOST)

        app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', engine_options or _config.SQLALCHEMY_ENGINE_OPTIONS)

        # Initialize Flask-SQLAlchemy extension.
        database = kwargs.get('db', _db)
        database.init_app(app)

        # Loads all models
        if entry_point_group:
            for base_entry in pkg_resources.iter_entry_points(entry_point_group):
                base_entry.load()

        # All models should be loaded by now.
        # Initialize the inter-mapper relationships of all loaded mappers.
        configure_mappers()

    def load_namespaces(self, entry_point: str = 'bdc_db.namespaces'):
        """Load application namespaces dynamically using entry points.

        Args:
            entry_point - Pattern to search in the setup.py entry points.
        """
        for base_entry in pkg_resources.iter_entry_points(entry_point):
            namespace = base_entry.load()

            if not namespace:
                raise RuntimeError(f'Invalid namespace {namespace} in {base_entry.module_name}')

            if namespace in self.namespaces:
                current_app.logger.warning(f'Namespace {namespace} already loaded. Skipping')
                continue

            self.namespaces.append(namespace)

    def load_triggers(self, entry_point_group: str = 'bdc_db.triggers', **kwargs):
        """Load trigger files from packages to BDC-DB context.

        Seeks for .sql files in packages which set `bdc_db.triggers` entry point.

        Notes:
            It may throw exception when module is set, but does not exists in disk.

        Args:
            entry_point_group - Pattern to search in the setup.py entry points.
        """
        if entry_point_group:
            triggers = self._load_module(entry_point_group)

            for module, script in triggers.items():
                for trigger in script:
                    self.register_trigger(module, Path(trigger).stem, trigger)

    def _load_module(self, entry_point) -> Dict[str, Iterable[str]]:
        """Seek for files inside Python entry point."""
        modules = dict()

        if entry_point:
            for base_entry in pkg_resources.iter_entry_points(entry_point):
                package = base_entry.load()

                directory = package.__path__

                for path in directory._path:
                    modules.setdefault(package.__name__, list())
                    modules[package.__name__].extend(self._get_scripts(path))

        return modules

    def load_scripts(self, entry_point_group: str = 'bdc_db.scripts', **kwargs):
        """Load SQL files from packages to BDC-DB context."""
        scripts = self._load_module(entry_point_group)

        for module, script in scripts.items():
            for trigger in script:
                self.register_scripts(module, Path(trigger).stem, trigger)

    @staticmethod
    def _get_scripts(path: str) -> Iterable[str]:
        _path = Path(path)
        found_scripts = []

        for entry in _path.iterdir():
            if entry.is_file() and entry.suffix == '.sql':
                found_scripts.append(str(entry))

        return found_scripts

    def register_trigger(self, module_name: str, trigger_name: str, path: str):
        """Register trigger command to BDC-DB."""
        self.triggers.setdefault(module_name, dict())

        self.triggers[module_name][trigger_name] = path

    def register_scripts(self, module_name: str, trigger_name: str, path: str):
        """Register trigger command to BDC-DB."""
        self.scripts.setdefault(module_name, dict())

        self.scripts[module_name][trigger_name] = path