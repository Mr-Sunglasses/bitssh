from setuptools import setup, find_packages

setup(
    name='bitssh',
    version='1.0.0',
    description='A command-line tool for managing SSH connections',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bitssh=src.bitssh:main'
        ]
    },
    install_requires=[
        'rich',
        'inquirer'
    ]
)
