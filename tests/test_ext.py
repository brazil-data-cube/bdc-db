from typing import Tuple
from unittest import mock

import pytest
from click.testing import CliRunner
from flask.cli import ScriptInfo
from pkg_resources import EntryPoint, resource_filename

import bdc_db.cli as bdc_cli
from bdc_db import BrazilDataCubeDB
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

    def _get_cli(self, app) -> Tuple[CliRunner, ScriptInfo]:
        """Define a helper to create a test client for click."""
        script_info = ScriptInfo(create_app=lambda _: app)
        runner = CliRunner()
        return runner, script_info

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_load_provider_through_entrypoint(self, app):
        """Test the dynamic entry point loading."""
        ext = BrazilDataCubeDB(app)

        assert len(ext.namespaces) == 1
        assert ext.namespaces[0] == 'myapp'
        # Assert JSONSchema loaded
        schema = ext.schemas.get_schema('dummy-jsonschema.json')
        assert schema

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_create_namespaces(self, app):
        """Test the creation of database namespaces (schemas) using command line."""
        ext = BrazilDataCubeDB(app)

        # Create namespace
        runner, script_info = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_namespaces, [], obj=script_info)
        assert result.exit_code == 0
        for namespace in ext.namespaces:
            assert f'Creating namespace {namespace}...' in result.stdout

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_point_invalid_namespace)
    def test_invalid_namespace(self, app):
        """Test the dynamic entry point loading."""
        with pytest.raises(RuntimeError):
            _ = BrazilDataCubeDB(app)

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_triggers_handler(self, app):
        """Test the creation of database triggers using command line."""
        _ = BrazilDataCubeDB(app)

        runner, script_info = self._get_cli(app)

        result = runner.invoke(bdc_cli.create_triggers, ['--verbose'], obj=script_info)
        assert result.exit_code == 0

        result = runner.invoke(bdc_cli.show_triggers, [], obj=script_info)
        assert result.exit_code == 0
        trigger_file = resource_filename('demo_app', 'triggers/dummy.sql')
        assert trigger_file in result.stdout

    @mock.patch('pkg_resources.iter_entry_points', mock_entry_points)
    def test_load_scripts(self, app):
        """Test the load of any database scripts using command line."""
        _ = BrazilDataCubeDB(app)

        runner, script_info = self._get_cli(app)

        load_scripts_result = runner.invoke(bdc_cli.load_scripts, ['--verbose'], obj=script_info)
        assert load_scripts_result.exit_code == 0
        assert f'Scripts from "demo_app.scripts" executed!' in load_scripts_result.stdout

        # load file manually
        sample_file = resource_filename('demo_app', 'scripts/dummy.sql')
        result = runner.invoke(bdc_cli.load_file, ['--file', sample_file, '--verbose'], obj=script_info)

        assert result.exit_code == 0
        assert f'File {sample_file} loaded!' in result.stdout
