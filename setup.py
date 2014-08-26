from setuptools import setup

setup(
    name='mendeley',
    version='0.0.1',
    packages=['mendeley'],
    url='http://dev.mendeley.com',
    license='MIT',
    author='Mendeley',
    author_email='api@mendeley.com',
    description='Python SDK for the Mendeley API',

    install_requires=[
        'arrow',
        'future',
        'requests-oauthlib',
    ],

    tests_require=[
        'pytest',
        'vcrpy'
    ]
)
