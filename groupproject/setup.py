from setuptools import setup

setup(
    name='groupproject',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)