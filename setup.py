from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='twik',
      version=version,
      description="Twik is an application that makes it easier to generate secure and different passwords for each website.",
      keywords='twik password hash',
      author='Alexandre Possebom',
      author_email='alexandrepossebom@gmail.com',
      url='https://github.com/coxande/Twik',
      license='GPLv3',
      packages=['twik'],
      entry_points = {
          'console_scripts': ['twik = twik.twik:main'],
      },
      )
