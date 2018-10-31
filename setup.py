from distutils.core import setup
from distutils.extension import Extension
import os
import sys

script_args = sys.argv[1:]

setup(name='hrds',
      version='0.1',
      author='Jon Hill',
      author_email='jon.hill@york.ac.uk',
      description="hrds is a python package for obtaining points from a set of raster at different resolutions."+
      "You can request a point (or list of points) and hrds will return a value based on"+
      "the highest resolution dataset (as defined by the user) available at that point, blending"+
      "datasets in a buffer region to ensure consistancy.",
      url='https://github.com/stephankramer/uptide',
      packages = ['hrds'],
      keywords = ['raster', 'gis', 'modelling'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering'],
      script_args = script_args,
      ext_package = 'hrds',
      )
