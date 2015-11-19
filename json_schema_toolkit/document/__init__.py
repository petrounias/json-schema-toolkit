# -*- coding: utf-8 -*-
#
# This document is free and open-source software, subject to the OSI-approved
# BSD license below.
#
# Copyright (c) 2013 - 2015 by Alexis Petrounias <www.petrounias.org>,
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

__status__ = "beta"
__version__ = "1.0.0b1"
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

    def __init__(self, value, validator = None):
        # set _fields before __getattribute__ is processed
        self._fields = {}
        super(JSONDocument, self).__init__(value,  self._generate_schema(),
            validator = validator)

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

    def __getattribute__(self, name):
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
        optional = False, null = False, pattern = None, content = None, 
        enum = None, implementation = None):
        super(JSONDocumentField, self).__init__()
        self.title = title
        self.description = description
        self.default = default
        self.optional = optional
        self.null = null
        self.pattern = pattern if pattern is not None else ''
        self.content = content
        self.enum = enum
        self.implementation = implementation or JSONDocumentFragment

    def _generate_schema(self):
        SCHEMA = {
            'type' : self.TYPE if not self.null else [ self.TYPE, 'null', ],
            'title' : self.title,
            'description' : self.description,
            'default' : self.default,
            'optional' : self.optional,
            'null' : self.null,
            'pattern' : self.pattern,
            'properties' : {},
            '__field' : self,
            '__fragment_cls' : self.implementation,
        }
        if self.enum is not None:
            SCHEMA['enum']=self.enum
        return SCHEMA


class JSONBooleanField(JSONDocumentField):
    """
    """

    TYPE = 'boolean'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONBooleanField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)


class JSONIntegerField(JSONDocumentField):
    """
    """

    TYPE = 'integer'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None, max_value = None, min_value = None):
        super(JSONIntegerField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)
        self.minimum = min_value
        self.maximum = max_value

    def _generate_schema(self):
        schema = super(JSONIntegerField, self)._generate_schema()
        if self.minimum is not None: schema['minimum'] = self.minimum
        if self.maximum is not None: schema['maximum'] = self.maximum
        return schema


class JSONDecimalField(JSONDocumentField):
    """
    """

    TYPE = 'number'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None, max_value = None, min_value = None):
        super(JSONDecimalField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)
        self.minimum = min_value
        self.maximum = max_value

    def _generate_schema(self):
        schema = super(JSONDecimalField, self)._generate_schema()
        if self.minimum is not None: schema['minimum'] = self.minimum
        if self.maximum is not None: schema['maximum'] = self.maximum
        return schema


class JSONStringField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None, min_length = None,
        max_length = None):
        super(JSONStringField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)
        self.minLength = min_length
        self.maxLength = max_length

    def _generate_schema(self):
        schema = super(JSONStringField, self)._generate_schema()
        if self.minLength is not None: schema['minLength'] = self.minLength
        if self.maxLength is not None: schema['maxLength'] = self.maxLength
        return schema


class JSONDateTimeField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONDateTimeField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)

    def _generate_schema(self):
        schema = super(JSONDateTimeField, self)._generate_schema()
        schema['format'] = 'date-time'
        return schema


class JSONDateField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    # PATTERN matching the following date formats:
    # - YYYY-MM-DD
    # - MM/DD/YYYY
    # - MM/DD/YY

    PATTERN = (r"^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$|"
                "^(0[1-9]|1[012])[/](0[1-9]|[12][0-9]|3[01])[/](19|20)\d\d$|"
                "^(0[1-9]|1[012])[/](0[1-9]|[12][0-9]|3[01])[/]\d\d$")

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONDateField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern or self.PATTERN, content = content,
            enum = enum, implementation = implementation)


class JSONTimeField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    # PATTERN matching the following time formats:
    # - HH:MM:SS
    # - HH:MM
    
    PATTERN = (r"^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$|"
                "^([0-1]?[0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$")

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONTimeField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern or self.PATTERN, content = content,
            enum = enum, implementation = implementation)


class JSONTimeDeltaField(JSONDocumentField):
    """
    """

    TYPE = 'string'

    PATTERN = r"^(\d+)d (\d+)s (\d+)us$"

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONTimeDeltaField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern or self.PATTERN, content = content,
            enum = enum, implementation = implementation)


class JSONObjectField(JSONDocumentField):
    """
    """

    TYPE = 'object'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONObjectField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)

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
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None):
        super(JSONListField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)

    def _generate_schema(self):
        schema = super(JSONListField, self)._generate_schema()
        if not self.content is None:
            schema['items'] = [value._generate_schema() for value in
                self.content]
        return schema


class JSONEmailField(JSONStringField):
    """
    """

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None, min_length = None,
        max_length = None):
        super(JSONEmailField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation, min_length = min_length, 
            max_length = max_length)

    def _generate_schema(self):
        schema = super(JSONEmailField, self)._generate_schema()
        schema['format'] = 'email'
        return schema


class JSONIPAddressField(JSONStringField):
    """
    """

    DEFAULT_PROTOCOL = 'ipv4'

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, protocol=None, implementation = None):
        super(JSONIPAddressField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern, content = content, enum = enum,
            implementation = implementation)
        self.protocol = protocol if protocol is not None else \
            self.DEFAULT_PROTOCOL

    def _generate_schema(self):
        schema = super(JSONIPAddressField, self)._generate_schema()
        schema['format'] = self.protocol
        return schema


class JSONSlugField(JSONStringField):
    """
    """
    
    PATTERN = r"^[a-z0-9-]+$"

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None, min_length = None,  max_length = None):
        super(JSONSlugField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern or self.PATTERN, content = content,
            enum = enum, implementation = implementation, min_length = min_length,
            max_length = max_length)


class JSONURLField(JSONStringField):
    """
    """

    # Pattern based on django's URLValidator regex pattern
    PATTERN = (r"^(http|ftp)s?://(([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)"
                "+([A-Za-z]{2,6}\.?|[A-Za-z0-9-]{2,}\.?)|localhost|\d{1,3}\."
                "\d{1,3}\.\d{1,3}\.\d{1,3}|\[?[a-fA-F0-9]*:[A-Fa-f0-9:]+\]?)"
                "(:\d+)?(/?|[/?]\S+)$")

    def __init__(self, title = None, description = None, default = None,
        optional = False, null = False, pattern = None, content = None,
        enum = None, implementation = None, min_length = None,  max_length = None):
        super(JSONURLField, self).__init__(title = title,
            description = description, default = default, optional = optional,
            null = null, pattern = pattern or self.PATTERN, content = content,
            enum = enum, implementation = implementation,
            min_length = min_length,  max_length = max_length)

