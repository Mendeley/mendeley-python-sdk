from setuptools import setup

__version__ = None
with open('mendeley/version.py') as f:
    exec(f.read())

setup(
    name='mendeley',
    version=__version__,
    packages=['mendeley'],
    url='http://dev.mendeley.com',
    license='MIT',
    author='Mendeley',
    author_email='api@mendeley.com',
    description='Python SDK for the Mendeley API',

    install_requires=[
        'arrow',
        'future',
        'memoized-property',
        'requests',
        'requests-oauthlib',
    ],

    tests_require=[
        'pytest',
        'vcrpy'
    ]
)
