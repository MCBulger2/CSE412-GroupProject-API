from setuptools import setup

setup(
    name='groupproject',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask', 'flask_cors', 'psycopg2-binary', 'bcrypt'
    ],
)
