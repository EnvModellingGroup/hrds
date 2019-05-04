import setuptools

DESCRIPTION = """
hrds is a python package for obtaining points from a set of rasters at
different resolutions. You can request a point (or list of points) and
hrds will return a value based on the highest resolution dataset (as
defined by the user) available at that point, blending datasets in a
buffer region to ensure consistancy.
"""


def get_version():
    """
    kludgy, but lets you set version in one place, and have it in the
    package
    """
    with open("hrds/__init__.py") as initfile:
        for line in initfile:
            parts = line.strip().split("=")
            if parts[0].strip() == "__version__":
                version = parts[1].strip().strip("'").strip('"')
                return version
    raise ValueError("no __version__ defined in package __init__")


setuptools.setup(name='hrds',
                 version=get_version(),
                 author='Jon Hill',
                 author_email='jon.hill@york.ac.uk',
                 description=DESCRIPTION,
                 url='https://github.com/EnvModellingGroup/hrds',
                 packages=setuptools.find_packages(),
                 keywords=['raster', 'gis', 'modelling'],
                 classifiers=[
                   'Development Status :: 4 - Beta',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering'],
                 )
