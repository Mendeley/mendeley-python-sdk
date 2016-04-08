# Mendeley Python SDK

![Monthly downloads](https://img.shields.io/pypi/dm/mendeley.svg)
![Pypi version](https://img.shields.io/pypi/v/mendeley.svg)
![Format](https://img.shields.io/pypi/format/mendeley.svg)
![License](https://img.shields.io/pypi/l/mendeley.svg)
![Docs](https://readthedocs.org/projects/mendeley-python/badge/?version=latest)
![Build status](https://travis-ci.org/Mendeley/mendeley-python-sdk.svg?branch=master)

The Mendeley Python SDK provides access to the [Mendeley API](https://www.mendeley.com).  For more information on the API and its capabilities, see the [Mendeley developer portal](http://dev.mendeley.com).

## Installation

You might like to set up a virtualenv for your project that uses the Mendeley API. See this [virtualenv tutorial](http://simononsoftware.com/virtualenv-tutorial-part-2/) for instructions. IDEs like IntelliJ with the Python plugin or PyCharm can also help you manage a virtualenv.

Install dependencies from [PyPI](https://pypi.python.org/pypi/mendeley) using [pip](http://www.pip-installer.org/en/latest/), a package manager for Python.

    pip install mendeley

## Documentation

Full documentation, including examples, can be found on [ReadTheDocs](https://mendeley-python.readthedocs.org/).

## Continuous integration

See the [Travis CI build](https://travis-ci.org/Mendeley/mendeley-python-sdk) to find:

- The current build status
- Logs from the SDK being exercised against the live API (this may be helpful if you are stuck when building your own application)

## Compatibility

- Our SDK is tested on CI against both Python 2 and 3. Inspect the .travis.yml file to find out which specific Python versions have been tested with this project.
- Both builds in the build matrix must pass in order for the overall build for a commit to pass.
- If you are working on the code, the 'future' library and the [compatible idioms guide](http://python-future.org/compatible_idioms.html) can help you to support both versions. 

## Contributing to the SDK

### Submission method

1. Fork the repository
2. Make your changes (please add tests - they will be exercised)
3. Propose a pull request back to our repository. The CI system will test your changes on top of the current master commit, so we can see if they will work.

### Dependency setup

1. Set up a virtualenv if you like.
2. Run `pip install -r requirements.txt`

### Testing your changes

#### Prerequisites

1. Register a Mendeley platform app.
2. Set the Mendeley API client ID and secret as environment variables in your shell:

        export MENDELEY_CLIENT_ID=[your app client ID]
        export MENDELEY_CLIENT_SECRET=[your app client secret]

#### To run tests the normal way

1. Create a **test user account** that you can safely make a mess inside. **WARNING:** Our user flow test suite exercises the API as a particular Mendeley user. The suite contains tests that will delete all documents associated with that account. **Do not** use your personal Mendeley account!
2. Set the necessary extra credentials:

        export MENDELEY_ACCESS_TOKEN=[user's access token]
        export MENDELEY_REDIRECT_URI=[redirect URI of your app]

3. Turn on the VCR cache (if you like) by setting `recordMode: once` in the test config YAML file.
4. Run all tests in the test suite:

        py.test

#### To replicate CI testing

In the CI environment, it is not (yet) possible to test interactions with API endpoints that require user access tokens. We can only exercise tests that use the client credentials flow. You must put any tests which CI cannot run in the test/manual folder, so that the CI test run command can ignore them.

1. Turn off the VCR cache (CI only makes sense when running against the real API) by setting `recordMode: all` the test config YAML file.
2. Run the test suite ignoring 'user mode' tests that require user access tokens:

        py.test --ignore=test/manual/

### Writing documentation

- Documentation is generated using Sphinx, and hosted on [ReadTheDocs](https://mendeley-python.readthedocs.org/). There are some pages in the docs directory in the repository, which refer to classes. The classes themselves have comments with a special format to generate the documentation - think Javadoc.
- If you add or change a public method, you should update the documentation comments.
- If you add new classes, you must include them in the correct place in the docs directory.


## Sample applications

- [mendeley-api-python-catalog-example](https://github.com/Mendeley/mendeley-api-python-catalog-example), a command-line application for accessing the Mendeley catalog.
- [mendeley-api-python-example](https://github.com/Mendeley/mendeley-api-python-example), a Flask Web application for accessing a user's library.

