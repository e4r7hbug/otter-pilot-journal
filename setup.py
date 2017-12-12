#!/usr/bin/env python3
"""Otter Pilot command plugin."""
from setuptools import find_packages, setup

setup(
    name='otter-pilot-journal',
    description='Otter Pilot journal.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    include_package_data=True,
    namespace_packages=['otter'],
    install_requires=[
        'pendulum',
    ],
)
