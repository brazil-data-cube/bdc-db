from unittest import mock

import pytest
from click.testing import CliRunner
from pkg_resources import EntryPoint, resource_filename

import bdc_db.cli as bdc_cli
from bdc_db import BrazilDataCubeDB, db
from tests.utils import mock_entry_points


class FakeNamespaceEntryPoint(EntryPoint):
    """Mock an Python Entrypoint."""

    def load(self):
        """Overwrite a dynamic loading of Entry point."""
        return None


def mock_entry_point_invalid_namespace(name):
    data = {
        'bdc_db.namespaces': [
            FakeNamespaceEntryPoint('demo_app', 'demo_app', attrs=()),
        ]
    }

    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data.get(key, []):
            yield entry_point


class TestBDCExtension:
    """Test the BrazilDataCube Extension."""

    def _get_cli(self, app) -> CliRunner:
        """Define a helper to create a test client for click."""
        runner = app.test_cli_runner()
        return runner

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_load_provider_through_entrypoint(self, app):
        """Test the dynamic entry point loading."""
        ext = BrazilDataCubeDB(app)

        db.create_all()

        assert len(ext.namespaces) == 1
        assert ext.namespaces[0] == 'myapp'
        # Assert JSONSchema loaded
        schema = ext.schemas.get_schema('dummy-jsonschema.json')
        assert schema

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_create_schema_cli(self, app):
        ext = BrazilDataCubeDB(app)
        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_schema, ['--verbose'])
        assert result.exit_code == 0

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
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

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_point_invalid_namespace)
    def test_invalid_namespace(self, app):
        """Test the dynamic entry point loading."""
        with pytest.raises(RuntimeError):
            _ = BrazilDataCubeDB(app)

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_triggers_handler(self, app):
        """Test the creation of database triggers using command line."""
        _ = BrazilDataCubeDB(app)

        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_triggers, ['--verbose'])
        assert result.exit_code == 0

        result = runner.invoke(bdc_cli.show_triggers, [])
        assert result.exit_code == 0
        trigger_file = resource_filename('demo_app', 'triggers/dummy.sql')
        assert trigger_file in result.stdout

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_load_scripts(self, app):
        """Test the load of any database scripts using command line."""
        _ = BrazilDataCubeDB(app)

        runner = self._get_cli(app)

        load_scripts_result = runner.invoke(bdc_cli.load_scripts, ['--verbose'])
        assert load_scripts_result.exit_code == 0
        assert f'Scripts from "demo_app.scripts" executed!' in load_scripts_result.stdout

        # load file manually
        sample_file = resource_filename('demo_app', 'scripts/dummy.sql')
        result = runner.invoke(bdc_cli.load_file, ['--file', sample_file, '--verbose'])

        assert result.exit_code == 0
        assert f'File {sample_file} loaded!' in result.stdout

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_triggers_destroy(self, app):
        """Test destroy loaded triggers from database using command line."""
        _ = BrazilDataCubeDB(app)

        runner = self._get_cli(app)

        result = runner.invoke(bdc_cli.drop_triggers, [])
        assert result.exit_code == 0

        # Code cov
        result = runner.invoke(bdc_cli.drop_triggers, [])
        assert result.exit_code == 0
        assert "No trigger available in db." in result.stdout
