Authentication
==============

There are three ways to authenticate with the Mendeley Python SDK.  Before you start, you'll need to have registered
your application at the `developer portal <http://dev.mendeley.com>`_.

Authorization code flow
-----------------------

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
-------------------

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
-----------------------

This flow does not require the user to log in.  However, it only provides access to a limited set of resources (the
read-only Mendeley Catalog of crowd sourced documents).

.. code-block:: python

    from mendeley import Mendeley

    # These values should match the ones supplied when registering your application.
    mendeley = Mendeley(client_id, client_secret=client_secret)

    auth = mendeley.start_implicit_grant_flow()
    session = auth.authenticate()
