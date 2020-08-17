..
    This file is part of BDC-DB.
    Copyright (C) 2020 INPE.

    BDC-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


============================================================================
Database Management Extension for Brazil Data Cube Applications and Services
============================================================================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/bdc-db/blob/master/LICENSE
        :alt: Software License


.. image:: https://travis-ci.org/brazil-data-cube/bdc-db.svg?branch=master
        :target: https://travis-ci.org/brazil-data-cube/bdc-db
        :alt: Build Status


.. image:: https://coveralls.io/repos/github/brazil-data-cube/bdc-db/badge.svg?branch=master
        :target: https://coveralls.io/github/brazil-data-cube/bdc-db?branch=master
        :alt: Code Coverage Test


.. image:: https://readthedocs.org/projects/bdc-db/badge/?version=latest
        :target: https://bdc-db.readthedocs.io/en/latest
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/brazil-data-cube/bdc-db.svg
        :target: https://github.com/brazil-data-cube/bdc-db/releases
        :alt: Release


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====


BDC-DB is a database management extension for Brazil Data Cube Applications and Services. It simplifies the work with `Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_ model classes and `Alembic <https://alembic.sqlalchemy.org/en/latest/index.html>`_ migration scripts.


Other packages, applications and services can register database objects through standard Python entry point in ``setup.py``. See the `USAGE.rst <./USAGE.rst>`_ documentation on how to take advantage of this package.


Installation
============


See `INSTALL.rst <./INSTALL.rst>`_.


Usage
=====


See `USAGE.rst <./USAGE.rst>`_.


Repository Organization
=======================


See `REPOSITORY.rst <REPOSITORY.rst>`_.


Developer Documentation
=======================


See https://bdc-db.readthedocs.io/en/latest.


Thanks
======

This module is based on `Invenio-DB <https://invenio-db.readthedocs.io/en/latest/>`_.
Thanks the Invenio Team for providing a scalable way to deal with dynamic database models with `Flask-SQLALchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_.


License
=======


.. admonition::
    Copyright (C) 2020 INPE.

    BDC-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
