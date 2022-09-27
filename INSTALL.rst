..
    This file is part of BDC-DB.
    Copyright (C) 2022 INPE.

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


Installation
============


Development Installation
------------------------


Pre-Requirements
++++++++++++++++

The Database Management Extension for Brazil Data Cube Applications and Services depends essentially on:

- `Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_: an extension for `Flask <http://flask.pocoo.org/>`_ that adds support for `SQLAlchemy <https://www.sqlalchemy.org/>`_ in applications.

- `Flask-Migrate <https://flask-migrate.readthedocs.io/en/latest/>`_: used to handle `SQLAlchemy <https://www.sqlalchemy.org/>`_ database migrations with `Alembic <https://alembic.sqlalchemy.org/en/latest/index.html>`_.

- `SQLAlchemy-Utils <https://sqlalchemy-utils.readthedocs.io/en/latest/index.html>`_: utility functions for SQLAlchemy such as database creation, database existence test, SQL script running.


Clone the software repository
+++++++++++++++++++++++++++++


Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/bdc-db.git


Install BDC-DB in Development Mode
++++++++++++++++++++++++++++++++++


Go to the source code folder::

    cd bdc-db


Install in development mode::

    pip3 install -e .[all]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.7::

        python3.7 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip setuptools wheel


Build the Documentation
+++++++++++++++++++++++


You can generate the documentation based on Sphinx with the following command::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html
