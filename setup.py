import re
from setuptools import setup

# Influence for this inspired by https://goo.gl/Pi51aC
version = None
for line in open('./podcasts/__init__.py'):
  m = re.search(r'__version__\s*=\s*(.*)', line)
  if m:
    version = m.group(1).strip()[1:-1]  # quotes
    break
assert version

setup(
    name='py-podcast',
    version=version,
    description='Podcast Series / Episodes Data Retrieval and Storage in Python',
    author='Joe Antonakakis',
    author_email='jma353@cornell.edu',
    url='https://github.com/Jma353/py-podcast',
    license='MIT',
    packages=['podcasts'],
    include_package_data=True,
    package_data={
        '': ['README.rst']
    },
    install_requires=[
        'appdirs>=1.4.2',
        'feedparser>=5.2.1',
        'lxml>=3.7.3',
        'packaging>=16.8',
        'pyparsing>=2.1.10',
        'requests>=2.13.0',
        'six>=1.10.0',
    ],
    tests_require=[
        'nose>=1.3.7',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
