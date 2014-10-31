Using the SDK
=============

Authentication
--------------

There are three ways to authenticate with the Mendeley Python SDK.  Before you start, you'll need to have registered
your application at the `developer portal <http://dev.mendeley.com>`_.

Authorization code flow
^^^^^^^^^^^^^^^^^^^^^^^

This flow is recommended for applications that have access to secure, private storage, such as web applications deployed
on a server.

.. code-block:: python

    from mendeley import Mendeley

    # These values should match the ones supplied when registering your application.
    mendeley = Mendeley(client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    auth = mendeley.start_authorization_code_flow()

    # The user needs to visit this URL, and log in to Mendeley.
    login_url = auth.get_login_url()

    # After logging in, the user will be redirected to a URL, auth_response.
    session = auth.authenticate(auth_response)

Implicit grant flow
^^^^^^^^^^^^^^^^^^^

This flow is recommended for applications running in environments that do not provide secure storage.

.. code-block:: python

    from mendeley import Mendeley

    # These values should match the ones supplied when registering your application.
    mendeley = Mendeley(client_id, redirect_uri=redirect_uri)

    auth = mendeley.start_implicit_grant_flow()

    # The user needs to visit this URL, and log in to Mendeley.
    login_url = auth.get_login_url()

    # After logging in, the user will be redirected to a URL, auth_response.
    session = auth.authenticate(auth_response)

Client credentials flow
^^^^^^^^^^^^^^^^^^^^^^^

This flow does not require the user to log in.  However, it only provides access to a limited set of resources (the
read-only Mendeley Catalog of crowd sourced documents).

.. code-block:: python

    from mendeley import Mendeley

    # These values should match the ones supplied when registering your application.
    mendeley = Mendeley(client_id, client_secret=client_secret)

    auth = mendeley.start_client_credentials_flow()
    session = auth.authenticate()

Sessions
--------

After authentication, you will have a :class:`MendeleySession <mendeley.session.MendeleySession>`, which will allow you
to access the Mendeley API.  The linked resources describe the operations that you can perform, and the objects that you
can interact with.

.. autoclass:: mendeley.session.MendeleySession()
    :members:

Pagination
----------

Many collections in the API are spread over multiple pages.  Typically, the SDK provides two ways of navigating these
collections:

- an `iter` method, which provides the whole collection as an iterator.
- a `list` method, which returns the first page of results as a :class:`Page <mendeley.pagination.Page>`.  You can use
  this object to navigate through the other pages.

.. autoclass:: mendeley.pagination.Page()
    :members:

Examples
--------

To print the name of the logged-in user:

.. code-block:: python

    print session.profiles.me.display_name

To print the titles of all of the documents in the user's library:

.. code-block:: python

    for document in session.documents.iter():
        print document.title

To print the number of readers of a document by DOI:

.. code-block:: python

    print session.catalog.by_identifier(doi='10.1371/journal.pmed.0020124', view='stats').reader_count
