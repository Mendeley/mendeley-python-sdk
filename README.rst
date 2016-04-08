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

First, set up a virtualenv for the project (if you like). See this [virtualenv tutorial](http://simononsoftware.com/virtualenv-tutorial-part-2/) for instructions. IDEs like IntelliJ with the Python plugin or PyCharm can also help you manage a virtualenv.

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

To obtain dependencies for this project, follow the steps in the .travis.yml file.

Important notes about testing:

- You will require at least a Mendeley API client ID and secret to run the tests.
- In the CI environment, it is not (yet) possible to test interactions with API endpoints that require user access tokens. Any tests which are precluded from working in the CI environment should be located in the test/manual folder, so that the test run command can ignore them.
- However, it is possible to run all tests *locally* on your dev workstation, if you have registered a platform app, and you have obtained a user account that you don't mind testing against (and making a mess inside).

Sample applications
-------------------

There are two sample applications that illustrate how to use the SDK:

- `mendeley-api-python-example <https://github.com/Mendeley/mendeley-api-python-example>`_, a
  `Flask <http://flask.pocoo.org/>`_ web application for accessing a user's library.
- `mendeley-api-python-catalog-example <https://github.com/Mendeley/mendeley-api-python-catalog-example>`_, a
  command-line application for accessing the Mendeley catalog.

