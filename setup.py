from setuptools import setup
import re

with open('src/cli.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(),
                        re.MULTILINE).group(1)

with open('requirements.txt', 'r') as req_file:
    requirements = req_file.read().splitlines()

setup(name='OMDbCLI',
      version=version,
      packages=['src'],
      install_requires=requirements,
      tests_require=['pytest'],
      entry_points={'console_scripts': ['omdbcli = src.cli:main']})
