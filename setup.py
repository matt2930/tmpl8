from importlib.metadata import entry_points
from setuptools import setup
from tmpl8 import __version__

setup_options = dict(
    name='tmpl8',
    version=__version__,
    description="Templating wrapper for CLI commands",
    author="Matthew Altberg",
    entry_points={
        'console_scripts': [
            'tmpl8=tmpl8.cli:main'
        ]
    },
    python_requires=">=3.7"
)

setup(**setup_options)
