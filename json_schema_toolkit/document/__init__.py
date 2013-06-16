# -*- coding: utf-8 -*-
#
# This document is free and open-source software, subject to the OSI-approved
# BSD license below.
#
# Copyright (c) 2013 Alexis Petrounias <www.petrounias.org>,
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# * Neither the name of the author nor the names of its contributors may be used
# to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
"""

__status__ = "alpha"
__version__ = "1.0.0a1"
__maintainer__ = (u"Alexis Petrounias <www.petrounias.org>", )
__author__ = (u"Alexis Petrounias <www.petrounias.org>", )

# Python
import copy
import datetime

# JSON Document
from json_document.document import Document, DocumentFragment

# JSON Schema Validator
from json_schema_validator.extensions import datetime_extension, \
    timedelta_extension


class FragmentProxy(object):
    """
    """

    def __init__(self, fragment):
        super(FragmentProxy, self).__init__()
        self.__getattribute__('__dict__')['__fragment'] = fragment

    @property
    def _fragment(self) :
        return self.__getattribute__('__dict__')['__fragment']

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]

    def __getitem__(self, item):
        fragment = self._fragment[item]
        if fragment.schema.type in [ 'object', 'array', ]:
            return FragmentProxy(fragment)
        return fragment.value

    def __setitem__(self, key, value):
        self._fragment[key] = value

    def __delitem__(self, key):
        _value = copy.copy(self._fragment.value)
        del _value[key]
        self._fragment.value = _value


class JSONDocument(Document):
    """
    """

    def __init__(self, value):
        # set _fields before __getattribute__ is processed
        self._fields = {}
        super(JSONDocument, self).__init__(value, self._generate_schema())

    def _generate_schema(self):
        base = {
            'type' : 'object',
            'title' : self.Meta.title,
            'description' : self.Meta.description,
            'properties' : {},
        }
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, JSONDocumentField):
                base['properties'][name] = field._generate_schema()
                self._fields[name] = field
        return base

    def __getattribute__(self, name) :
        _fields = Document.__getattribute__(self, '_fields')
        if name in _fields:
            if isinstance(_fields[name], JSONObjectField) or \
                isinstance(_fields[name], JSONListField):
                return FragmentProxy(self[name])
            return self[name].value
        return Document.__getattribute__(self, name)

    def __setattr__(self, key, value):
        if hasattr(self, '_fields') and key in self._fields:
            self[key] = value
        else:
            return Document.__setattr__(self, key, value)

    def __delattr__(self, item):
        if hasattr(self, '_fields') and item in self._fields:
            del self[item]
        else:
            return Document.__delattr__(self, item)

    def __delitem__(self, key):
        # in order to bump the document revision, we must ensure
        # Document._set_value is invoked.
        _value = copy.copy(self.value)
        del _value[key]
        self.value = _value


class JSONDocumentFragment(DocumentFragment):
    """
    """

    def _get_value(self):
        return super(JSONDocumentFragment, self)._get_value()

    def _set_value(self, new_value):
        if isinstance(new_value, datetime.datetime):
            new_value = datetime_extension.to_json(new_value)
        if isinstance(new_value, datetime.timedelta):
            new_value = timedelta_extension.to_json(new_value)
        super(JSONDocumentFragment, self)._set_value(new_value)

    value = property(_get_value, _set_value)


class JSONDocumentField(object):
    """
    """

    TYPE = 'any'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONDocumentField, self).__init__()
        self.title = title
        self.description = description
        self.default = default
        self.optional = optional
        self.null = null
        self.content = content
        self.implementation = implementation or JSONDocumentFragment

    def _generate_schema(self) :
        return {
            'type' : self.TYPE if not self.null else [ self.TYPE, 'null', ],
            'title' : self.title,
            'description' : self.description,
            'default' : self.default,
            'optional' : self.optional,
            'null' : self.null,
            'properties' : {},
            '__field' : self,
            '__fragment_cls' : self.implementation,
        }


class JSONBooleanField(JSONDocumentField):
    """
    """

    TYPE = 'boolean'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONBooleanField, self).__init__(title, description, default,
            optional, null, content, implementation)


class JSONIntegerField(JSONDocumentField):
    """
    """

    TYPE = 'integer'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONIntegerField, self).__init__(title, description, default,
            optional, null, content, implementation)


class JSONDecimalField(JSONDocumentField):
    """
    """

    TYPE = 'number'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None) :
        super(JSONDecimalField, self).__init__(title, description, default,
            optional, null, content, implementation)


class JSONStringField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONStringField, self).__init__(title, description, default,
            optional, null, content, implementation)


class JSONDateTimeField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONDateTimeField, self).__init__(title, description, default,
            optional, null, content, implementation)

    def _generate_schema(self):
        schema = super(JSONDateTimeField, self)._generate_schema()
        schema['format'] = 'date-time'
        return schema


class JSONDateField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONDateField, self).__init__(title, description, default,
            optional, null, content, implementation)


class JSONTimeField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONTimeField, self).__init__(title, description, default,
            optional, null, content, implementation)


class JSONTimeDeltaField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    PATTERN = r"^(\d+)d (\d+)s (\d+)us$"

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONTimeDeltaField, self).__init__(title, description, default,
            optional, null, content, implementation)

    def _generate_schema(self) :
        schema = super(JSONTimeDeltaField, self)._generate_schema()
        schema['pattern'] = self.PATTERN
        return schema


class JSONObjectField(JSONDocumentField):
    """
    """

    TYPE = 'object'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONObjectField, self).__init__(title, description, default,
            optional, null, content, implementation)

    def _generate_schema(self):
        schema = super(JSONObjectField, self)._generate_schema()
        if not self.content is None:
            for key, value in self.content.items():
                schema['properties'][key] = value._generate_schema()
        return schema


class JSONListField(JSONDocumentField):
    """
    """

    TYPE = 'array'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, content = None, implementation = None):
        super(JSONListField, self).__init__(title, description, default,
            optional, null, content, implementation)

    def _generate_schema(self):
        schema = super(JSONListField, self)._generate_schema()
        if not self.content is None:
            schema['items'] = [value._generate_schema() for value in
                self.content]
        return schema

