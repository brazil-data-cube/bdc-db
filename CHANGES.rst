..
    This file is part of BDC-DB.
    Copyright (C) 2020 INPE.

    BDC-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


================
BDC-DB - Changes
================


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
