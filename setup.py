from setuptools import setup

setup(
    name='bump',
    version='1.8.6',
    author='Ken Kundert',
    description='Manage version number and release date.',
    license='GPLv3+',
    scripts=['bump'],
    install_requires=[
        'arrow',
        'docopt',
        'inform',
        'shlib',
    ],
)
