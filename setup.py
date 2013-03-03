from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='MinecraftSwitch',
      version=version,
      description="Manage multiple minecraft environments on OS X",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Nick Murdoch',
      author_email='',
      url='http://github.org/flexo/minecraftswitch',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
