from setuptools import setup

setup(
    name = 'bump',
    version = '2.0.0a6',
    author = 'Ken Kundert',
    description = 'Manage version number and release date.',
    license = 'GPLv3+',
    scripts = "bump bump-convert".split(),
    install_requires = [
        'arrow',
        'docopt',
        'inform',
        'nestedtext',
        'shlib',
    ],
    zip_safe = True,
)
