..
    This file is part of BDC-DB.
    Copyright (C) 2023 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


================
BDC-DB - Changes
================


Version 0.8.0 (2023-10-02)
--------------------------

- Upgrade libraries dependencies and support of SQLAlchemy 2x. (`#73 <https://github.com/brazil-data-cube/bdc-db/issues/73>`_).
- Improve documentation for setup and extension.
- Improve package Python version support: 3.8, 3.9, 3.10, 3.11+
- Review unittests for bdc-db


Version 0.6.3 (2022-09-22)
--------------------------

- Change LICENSE to GPL v3
- Set custom JSONB property `cache_ok=True` for performance and to avoid SQLAlchemy warnings (`#68 <https://github.com/brazil-data-cube/bdc-db/issues/68>`_).


Version 0.6.2 (2022-04-18)
--------------------------

- Fix extension initialization - variable not declared (`#66 <https://github.com/brazil-data-cube/bdc-db/issues/66>`_).


Version 0.6.1 (2022-01-05)
--------------------------

- Improve documentation how to use `JSONB` with JSONSchemas (`#63 <https://github.com/brazil-data-cube/bdc-db/issues/63>`_).
- Fix unittest with `JSONSchema` ref schema key (`#64 <https://github.com/brazil-data-cube/bdc-db/issues/64>`_).


Version 0.6.0 (2021-12-21)
--------------------------

- Add SQL Type for `JSONB` with JSONSchemas validator (`#52 <https://github.com/brazil-data-cube/bdc-db/issues/52>`_).
- Add new command line for `drop-triggers` (`#35 <https://github.com/brazil-data-cube/bdc-db/issues/35>`_).
- Add SQLAlchemy model representation for PostGIS `spatial_ref_sys` (`#41 <https://github.com/brazil-data-cube/bdc-db/issues/41>`_).
- Improve unittest and code coverage (`#26 <https://github.com/brazil-data-cube/bdc-db/issues/26>`_).
- Migrate repo build to Drone CI (`#45 <https://github.com/brazil-data-cube/bdc-db/issues/45>`_).


Version 0.4.3 (2021-03-17)
--------------------------


- Keep SQLAlchemy in version 1.3 until SQLAlchemyUtils is updated for SQLAlchemy 1.4. (`#48 <https://github.com/brazil-data-cube/bdc-db/issues/48>`_).


Version 0.4.2 (2020-12-08)
--------------------------


- New features:
  - add an entry point to manage registered namespaces (`#43 <https://github.com/brazil-data-cube/bdc-db/issues/43>`_).



Version 0.4.1 (2020-09-04)
--------------------------


- Bug fixes:
  - command ``load-file`` (`#37 <https://github.com/brazil-data-cube/bdc-db/issues/37>`_).


Version 0.4.0 (2020-08-31)
--------------------------


- New features:

  - dynamic handling of triggers and scripts.

  - new CLI commands: ``show-triggers``, ``create-triggers``, ``load-scripts``, and ``load-file``.


- Improved documentation.



Version 0.2.0 (2020-08-17)
--------------------------


- First experimental version.

- Command Line Interface (CLI).

- Alembic migration support.

- Documentation system based on Sphinx.

- Documentation integrated to ``Read the Docs``.

- Installation and build instructions.

- Package support through Setuptools.

- Installation and usage instructions.

- Travis CI support.

- Unit-test environment set.

- Source code versioning based on `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- License: `MIT <https://raw.githubusercontent.com/brazil-data-cube/bdc-db/master/LICENSE>`_.
