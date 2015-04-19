import os
import re

from setuptools import setup


classifiers = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet',
    'Topic :: Utilities',
]

with open('README.rst') as file_readme:
    readme = file_readme.read()

with open('HISTORY.rst') as file_history:
    history = file_history.read()

with open('requirements.txt') as file_requirements:
    requirements = file_requirements.read().splitlines()


def read_file(*paths):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, *paths)) as f:
        return f.read()


def get_version():
    """
    Pull version from module without loading module first. This was lovingly
    collected and adapted from
    https://github.com/pypa/virtualenv/blob/12.1.1/setup.py#L67.
    """
    version_file = read_file('csv2es.py')
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


settings = dict()
settings.update(
    name='csv2es',
    version=get_version(),
    description='Bulk import a CSV or TSV into Elastic Search',
    long_description=readme + '\n\n' + history,
    author='Ray Holder',
    license='Apache 2.0',
    url='https://github.com/rholder/csv2es',
    classifiers=classifiers,
    keywords='elasticsearch es pyelasticsearch csv tsv bulk import kibana',
    py_modules= ['csv2es'],
    entry_points='''
        [console_scripts]
        csv2es=csv2es:cli
    ''',
    test_suite='test_csv2es',
    install_requires=requirements,
)

# run this to push to PyPI because you will forget how to do this later
#   python setup.py sdist
#   twine upload dist/*
setup(**settings)
