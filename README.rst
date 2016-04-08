Mendeley Python SDK
===================

.. image:: https://img.shields.io/pypi/dm/mendeley.svg
  :target: https://pypi.python.org/pypi/mendeley/
.. image:: https://img.shields.io/pypi/v/mendeley.svg
  :target: https://pypi.python.org/pypi/mendeley/
.. image:: https://img.shields.io/pypi/format/mendeley.svg
  :target: https://pypi.python.org/pypi/mendeley/
.. image:: https://img.shields.io/pypi/l/mendeley.svg
  :target: https://pypi.python.org/pypi/mendeley/
.. image:: https://readthedocs.org/projects/mendeley-python/badge/?version=latest
  :target: https://readthedocs.org/projects/mendeley-python/?badge=latest
.. image:: https://travis-ci.org/Mendeley/mendeley-python-sdk.svg?branch=master
  :target: https://travis-ci.org/Mendeley/mendeley-python-sdk

The Mendeley Python SDK provides access to the `Mendeley <http://www.mendeley.com>`_ API.  For more information on the
API and its capabilities, see the `developer portal <http://dev.mendeley.com>`_.

Installation
------------

You might like to set up a virtualenv for your project that uses the Mendeley API. See this [virtualenv tutorial](http://simononsoftware.com/virtualenv-tutorial-part-2/) for instructions. IDEs like IntelliJ with the Python plugin or PyCharm can also help you manage a virtualenv.

Install dependencies from `PyPI <https://pypi.python.org/pypi>`_ using `pip <http://www.pip-installer.org/en/latest/>`_, a
package manager for Python.

.. code-block:: bash

    pip install mendeley

Documentation
-------------

Full documentation, including examples, can be found on `ReadTheDocs <http://mendeley-python.readthedocs.org/>`_.

Compatibility
-------------

- General notes: Our SDK is tested on CI against both Python 2 and 3. Both builds in the build matrix must pass in order for the overall build for a commit to pass. If you are working on the code, the 'future' library and the `compatible idioms guide <http://python-future.org/compatible_idioms.html>` can help you to support both versions. 
- Specific versions: Inspect the .travis.yml file to find out which Python versions have been tested with this project.

Development
-----------

Dependency setup:

1. Set up a virtualenv if you like.
2. Run pip install -r requirements.txt

Testing your changes:

- You must register a Mendeley platform app.
- You must have at least a Mendeley API client ID and secret to run the tests.
- In the CI environment, it is not (yet) possible to test interactions with API endpoints that require user access tokens. You must put any tests which CI cannot run in the test/manual folder, so that the CI test run command can ignore them.
- You should run all tests *locally* on your dev workstation. WARNING: Our user flow test suite exercises the API as a particular Mendeley user. The suite contains tests that will delete all documents associated with that account. Don't use your personal Mendeley account!

Sample applications
-------------------

- `mendeley-api-python-example <https://github.com/Mendeley/mendeley-api-python-example>`_, a
  `Flask <http://flask.pocoo.org/>`_ web application for accessing a user's library.
- `mendeley-api-python-catalog-example <https://github.com/Mendeley/mendeley-api-python-catalog-example>`_, a
  command-line application for accessing the Mendeley catalog.

