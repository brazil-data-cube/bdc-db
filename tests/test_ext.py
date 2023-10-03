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
import importlib.resources
from importlib.metadata import EntryPoint
from unittest import mock

import pytest
from click.testing import CliRunner

import bdc_db.cli as bdc_cli
from bdc_db import BrazilDataCubeDB, db
from bdc_db.utils import list_triggers
from tests.utils import mock_entry_points


class FakeNamespaceEntryPoint(EntryPoint):
    """Mock an Python Entrypoint."""

    def load(self):
        """Overwrite a dynamic loading of Entry point."""
        return None


def mock_entry_point_invalid_namespace(group):
    data = {
        'bdc_db.namespaces': [
            FakeNamespaceEntryPoint(name='demo_app', group=None, value='demo_app',),
        ]
    }

    names = data.keys() if group is None else [group]
    for key in names:
        for entry_point in data.get(key, []):
            yield entry_point


class TestBDCExtension:
    """Test the BrazilDataCube Extension."""

    def _get_cli(self, app) -> CliRunner:
        """Define a helper to create a test client for click."""
        runner = app.test_cli_runner()
        return runner

    @mock.patch('bdc_db.ext.entry_points', mock_entry_points)
    @mock.patch('importlib_metadata.entry_points', mock_entry_points)
    def test_load_provider_through_entrypoint(self, app):
        """Test the dynamic entry point loading."""
        ext = BrazilDataCubeDB(app)

        db.create_all()

        assert len(ext.namespaces) == 1
        assert ext.namespaces[0] == 'myapp'
        # Assert JSONSchema loaded
        schema = ext.schemas.get_schema('dummy-jsonschema.json')
        assert schema

    @mock.patch('bdc_db.ext.entry_points', mock_entry_points)
    def test_create_schema_cli(self, app):
        ext = BrazilDataCubeDB(app)
        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_schema, ['--verbose'])
        assert result.exit_code == 0

    @mock.patch('bdc_db.ext.entry_points', mock_entry_points)
    def test_create_namespaces(self, app):
        """Test the creation of database namespaces (schemas) using command line."""
        ext = BrazilDataCubeDB(app)

        # Create namespace
        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_namespaces, [])
        assert result.exit_code == 0
        for namespace in ext.namespaces:
            assert f'Creating namespace {namespace}...' in result.stdout

        result = runner.invoke(bdc_cli.show_namespaces, [])
        assert result.exit_code == 0
        for namespace in ext.namespaces:
            assert f'\t-> {namespace}' in result.stdout

    @mock.patch('bdc_db.ext.entry_points', mock_entry_point_invalid_namespace)
    def test_invalid_namespace(self, app):
        """Test the dynamic entry point loading."""
        with pytest.raises(RuntimeError):
            _ = BrazilDataCubeDB(app)

    @mock.patch('bdc_db.ext.entry_points', mock_entry_points)
    def test_triggers_handler(self, app):
        """Test the creation of database triggers using command line."""
        _ = BrazilDataCubeDB(app)

        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_triggers, ['--verbose'])
        assert result.exit_code == 0

        result = runner.invoke(bdc_cli.show_triggers, [])
        assert result.exit_code == 0
        trigger_file = importlib.resources.path('demo_app.triggers', 'dummy.sql')
        assert str(trigger_file) in result.stdout

    def test_load_scripts(self, app):
        """Test the load of any database scripts using command line."""

        with mock.patch('bdc_db.ext.entry_points', mock_entry_points):
            ext = BrazilDataCubeDB(app)

        runner = self._get_cli(app)

        load_scripts_result = runner.invoke(bdc_cli.load_scripts, ['--verbose'])
        assert load_scripts_result.exit_code == 0
        assert f'Scripts from "demo_app.scripts" executed!' in load_scripts_result.stdout

        # load file manually
        sample_file = importlib.resources.path("demo_app.scripts", "dummy.sql")
        result = runner.invoke(bdc_cli.load_file, ['--file', sample_file, '--verbose'])

        assert result.exit_code == 0
        assert f'File {sample_file} loaded!' in result.stdout

        # Coverage test for empty scripts
        ext.scripts = {}
        result = runner.invoke(bdc_cli.load_scripts, ['--verbose'])
        assert result.exit_code == 0

    @mock.patch('bdc_db.ext.entry_points', mock_entry_points)
    def test_triggers_destroy(self, app):
        """Test destroy loaded triggers from database using command line."""
        dbext = BrazilDataCubeDB(app)

        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.drop_triggers, [])
        assert result.exit_code == 0

        # Code cov
        result = runner.invoke(bdc_cli.drop_triggers, [])
        assert result.exit_code == 0

        for trigger in list_triggers(db.engine):
            assert f'The trigger "{trigger.trigger_name}" was removed.' in result.stdout

        # Code cov when no trigger set
        dbext.triggers = {}
        result = runner.invoke(bdc_cli.drop_triggers, [])
        assert result.exit_code == 0

    def test_compatibility(self, app):
        _ = BrazilDataCubeDB(app)
        # Temporary Compatibility for Flask-Alembic and code coverage
        assert db == db.db
