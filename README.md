JSON Schema Toolkit
===================

Programmatic building of JSON schemas (recursive field mappings) with
validation, a Django JSON Field, and native PostgreSQL JSON type constraints.

Documentation https://json-schema-toolkit.readthedocs.org

Overview
========

Built on top of https://github.com/zyga/json-document/ and
https://github.com/zyga/json-schema-validator/, with
powerful support for building and validating JSON documents. Can be used to
programmatically build JSON schemas by mapping fields to a document or
recursively to other fields, as well as used for validating a Django JSON field
during save operations. If PostgreSQL >= 9.2 is used, supports the native JSON
data type. If PostgreSQL >= 9.3 is used, supports custom JSON SQL constraint
generation for the Django Model.

Extends json_document to provide nullable fields (in additional to optional
fields), deletion of members (through del), a Pythonic API for dot notation
member access, as well as convenience input transformations for data such as
dates and times, time deltas, and others.

* JSON Schema: < http://json-schema.org/ >
* Django: < http://www.djangoproject.com/ >
* PostgreSQL JSON Functions and Operators
  < http://www.postgresql.org/docs/9.3/static/functions-json.html >


Prerequisites
=============

Core:

- Python >= 2.6
- json_document >= 0.8
- json_schema_validator >= 2.3


Optionally, for the Django field:

- Django >= 1.4


Optionally, for PostgreSQL native JSON data type:

- PostgreSQL >= 9.2
- psycopg2 >= 2.4


Optionally, for JSON SQL constraints:

- PostgreSQL >= 9.3


Optionally, for testing:

- unittest2 >= 0.5.1


Obtaining
=========

- Author's website for the project: http://www.petrounias.org/software/json-schema-toolkit/

- Git repository on GitHub: https://github.com/petrounias/json-schema-toolkit/

- Mercurial repository on BitBucket: http://www.bitbucket.org/petrounias/json-schema-toolkit/


Installation
============

Ensure the required packages json_document and json_schema_validator are
installed, and then install json_schema_toolkit:

Via setup tools::

    python setup.py install

Via pip and pypi::

    pip install json-schema-toolkit


Release Notes
=============

v1.0.0 alpha, 16 June 2013 -- Initial public release.


Development Status
==================

Actively developed and maintained. Currently used in production in proprietary
projects by the author and his team.


Future Work
===========

- ?


Contributors
============

Written and maintained by Alexis Petrounias < http://www.petrounias.org/ >

Based on work and feedback by Zygmunt Krynicki < http://www.suxx.pl/ >


License
=======

Released under the OSI-approved BSD license. Please note that json_document and
json_schema_validator are LGPLv3 and not copyleft-free, so this may affect your
ability to include this software's requirements in proprietary software. This
software only links against the aforementioned libraries in accordance with
their license.

Copyright (c) 2013 Alexis Petrounias < www.petrounias.org >,
all rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

Neither the name of the author nor the names of its contributors may be used to
endorse or promote products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

