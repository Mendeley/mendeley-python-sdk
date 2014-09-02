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
        'arrow==0.4.4',
        'future==0.13.0',
        'memoized-property==1.0.2',
        'requests==2.3.0',
        'requests-oauthlib==0.4.1',
    ],

    tests_require=[
        'pytest==2.6.1',
        'vcrpy==1.0.2'
    ]
)
