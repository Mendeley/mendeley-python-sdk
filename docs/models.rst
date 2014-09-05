Models
======

This page details the various model objects in the Mendeley Python SDK.

User documents
--------------

Documents
^^^^^^^^^

.. autoclass:: mendeley.models.documents.UserDocument()
    :members:
    :inherited-members:

.. autoclass:: mendeley.models.documents.TrashDocument()
    :members:
    :inherited-members:

Views
^^^^^

The following views are available on :class:`UserDocuments <mendeley.models.documents.UserDocument>` and
:class:`TrashDocuments <mendeley.models.documents.TrashDocument>`.

.. autoclass:: mendeley.models.documents.UserBibView()
    :members:
    :inherited-members:

.. autoclass:: mendeley.models.documents.UserClientView()
    :members:
    :inherited-members:

.. autoclass:: mendeley.models.documents.UserTagsView()
    :members:
    :inherited-members:

Catalog documents
-----------------

Documents
^^^^^^^^^

.. autoclass:: mendeley.models.catalog.CatalogDocument()
    :members:
    :inherited-members:

Views
^^^^^

The following views are available on :class:`CatalogDocuments <mendeley.models.documents.CatalogDocument>`.

.. autoclass:: mendeley.models.catalog.CatalogBibView()
    :members:
    :inherited-members:

.. autoclass:: mendeley.models.catalog.CatalogClientView()
    :members:
    :inherited-members:

.. autoclass:: mendeley.models.catalog.CatalogStatsView()
    :members:
    :inherited-members:

Profiles
--------

.. autoclass:: mendeley.models.profiles.Profile()
    :members:

Groups
------

.. autoclass:: mendeley.models.groups.Group()
    :members:

.. autoclass:: mendeley.models.groups.GroupMember()
    :members:
    :inherited-members:

Files
-----

.. autoclass:: mendeley.models.files.File()
    :members:

Common objects
--------------

.. autoclass:: mendeley.models.common.Discipline()
    :members:

.. autoclass:: mendeley.models.common.Education()
    :members:

.. autoclass:: mendeley.models.common.Employment()
    :members:

.. autoclass:: mendeley.models.common.Location()
    :members:

.. autoclass:: mendeley.models.common.Person()
    :members:

.. autoclass:: mendeley.models.common.Photo()
    :members:
