.. examples:

Examples
========
All imports are from::

    from json_schema_toolkit.document import ...

.. contents::
    :local:


==============
Empty Document
==============
A document which is a simple object, with the 'any' JSON type::

    class EmptyDocument(JSONDocument):

        class Meta(object):
            title = u'a title'
            description = u'a description'

    d1 = EmptyDocument({})


===============
Simple Document
===============
A document which features a single field 'answer' of type 'integer'::

    class SimpleDocument(JSONDocument):

        answer = JSONIntegerField(title = u'the answer',
            description = u'answer mutually exclusive with question in each given universe')

        class Meta(object):
            title = u'oracle'
            description = u'a repository of truth'

    d1 = SimpleDocument({ 'answer' : 42 })


=============
List Document
=============
A document which contains a list 'events' of type 'string'::

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


==================
Composite Document
==================
A document which contains a list of objects, comprising a 'string' and an 'integer'::

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

