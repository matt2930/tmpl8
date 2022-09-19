from setuptools import setup, find_packages
from tmpl8 import __version__

install_requires = [
    'pyyaml',
    'jinja2'
]

setup_options = dict(
    name='tmpl8',
    version=__version__,
    description='Templating wrapper for CLI commands',
    packages=find_packages(include=('tmpl8', 'tmpl8.*')),
    author='Matthew Altberg',
    install_requires=install_requires,
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'pre-commit'
        ]
    },
    entry_points={
        'console_scripts': [
            'tmpl8=tmpl8.cli:main'
        ]
    },
    python_requires=">=3.7",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)

setup(**setup_options)
