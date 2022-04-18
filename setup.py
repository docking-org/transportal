import os
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='FDA Transportal',
    version='0.9-021219',
    long_description="A portal of transporters",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'transportal-manage = transportal.manage:run',
        ]
    },
    include_package_data=True,
    package_data={
        'initial-data': 'transportal/initial_data.json',
        'database': 'transportal/fdaTransporter.sqlite',
        'templates': 'transportal/templates/*',
        'media': 'transportal/media/*',
        'requirements': 'requirements.txt',
    },
    zip_safe=False,
    install_requires=[
        'Django==2.2.27',
        'mod-wsgi==4.6.5',
        'numpy==1.16.0',
        'pytz==2018.9',
    ],
    classifiers=[
        'Private :: Do Not Upload',
    ]
)
