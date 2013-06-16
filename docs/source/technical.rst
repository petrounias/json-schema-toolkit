.. technical:

Technical and Implementation Notes
============================================

Deleting a value is implemented through setting the value of a DocumentFragment.
This is done so the Document can keep track of fragments in its cache, as well
as bump its revision.


.. contents::
    :local:

