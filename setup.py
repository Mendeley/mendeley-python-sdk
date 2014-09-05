from setuptools import setup

__version__ = None
with open('mendeley/version.py') as f:
    exec(f.read())

setup(
    name='mendeley',
    version=__version__,
    packages=['mendeley', 'mendeley.models', 'mendeley.resources'],
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
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
