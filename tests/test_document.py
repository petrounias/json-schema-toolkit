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

# Unittest2
from unittest2 import TestCase

# JSON Schema Toolkit
from json_schema_toolkit.document import JSONDocument, JSONIntegerField, \
    JSONStringField, JSONListField, JSONObjectField


class JSONDocumentTestCase(TestCase):

    def test_document_creation(self):

        class EmptyDocument(JSONDocument):

            class Meta(object):
                title = u'a title'
                description = u'a description'


        d1 = EmptyDocument({})
        self.assertEqual(d1.schema.title, u'a title')
        self.assertEqual(d1.schema.description, u'a description')


    def test_field_creation(self):

        class SimpleDocument(JSONDocument):

            answer = JSONIntegerField(title = u'the answer',
                description = u'answer mutually exclusive with question in each given universe')

            class Meta(object):
                title = u'a title'
                description = u'a description'

        d1 = SimpleDocument({ 'answer' : 42 })
        self.assertEquals(d1.answer, 42)
        self.assertEquals(d1.value['answer'], 42)


    def test_list_field_creation(self):

        class ListDocument(JSONDocument):

            events = JSONListField(title = u'events',
                description = u'important historical events', content = [
                    JSONStringField(title = u'event',
                        description = u'important historical event'),
                ])

            class Meta(object):
                title = u'history'
                description = u'a collection of historical events'

        d1 = ListDocument({ 'events' : [
            u'Sinking of Atlantis',
            u'Discovery of Atlantis',
            u'Colonization of Atlantis',
        ] })
        self.assertEquals(list(d1.events._fragment.value), d1.value['events'])


    def test_object_field_creation(self):

        class ObjectDocument(JSONDocument):

            events = JSONListField(title = u'events',
                description = u'important historical events', content = [
                    JSONObjectField(title = u'event',
                        description = u'important historical event', content = {
                            'title' : JSONStringField(title = u'event title'),
                            'importance' : JSONIntegerField(title = u'event importance'),
                        }),
                ])

            class Meta(object):
                title = u'history'
                description = u'a collection of historical events'

        d1 = ObjectDocument({ 'events' : [
            { 'title' : u'Sinking of Atlantis', 'importance' : 3 },
            { 'title' : u'Discovery of Atlantis', 'importance' : 7 },
            { 'title' : u'Colonization of Atlantis', 'importance' : 12 },
        ] })
        self.assertEquals(list(d1.events._fragment.value), d1.value['events'])



