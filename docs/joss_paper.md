---
title: 'HRDS: A Python package for heiarachical raster datasets'
tags:
  - Python
  - numerical modelling
  - gis
authors:
  - name: Jon Hill
    orcid: 0000-0003-1340-4373
    affiliation: "1"
affiliations:
 - name: Department of Environment and Geography, University of York, UK
   index: 1
date: 15 November 2018
bibliography: papers.bib
---

# Summary

Multi-scale modelling of geophysical domains requires data to set up initial conditions
such as bathymetry or topography. These data are typically in the form of GIS
rasters and can be derived from a number of sources. Typically, a single
data source is used which has a fixed spatial resolution. However, in multi-scale
models, e.g. [Martin-Short2015], the spatial scale of the model can vary by four or 
more orders of magnitude, e.g. from kilometre- to sub-metre-scale. In order to
use the high resolution data set in the area of highest model resolution one
must blend this limited-area highest resolution data with a wider area coarse
resolution dataset. A choice therefore has to be made to either sacrifice some 
resolution or create a very large data file. For a wide region zooming into 
metre-scale processes this data file could be terabytes in size when re-sampled 
at the resolution of the highest resolution dataset. This problem is particularly
acute when using GIS tools such as ```qmesh``` [Avdis2018] to generate meshes from 
contours or other derivatives of the raster data.

``HRDS`` is a solution to this problem as it allows a user to extract data 
from an arbitrary point from a stack of rasters, each of which can have different
extents and resolutions. ```HRDS``` is based on the ```GDAL``` library [GDALOGR2018]
so can load all common raster formats. As these rasters are unlikely to 
agree on the topographic/bathymetric height where they overlap, a linear distance 
buffer is created to smoothly
blend the two datasets together. The user can specify the distance over which this 
buffer acts. The user gives HRDS a base raster which is low resolution but covers 
the whole extent of the domain to be modelled and then a stack of other rasters in 
priority order (typically increasing in resolution) along with a corresponding list 
of buffer distances. ``HRDS`` then calculates the linear buffers and stores these 
as rasters. The user can then request data at an arbitrary point which is
calculated via bilinear interpolation. There are limitations in this approach 
in that rasters cannot be partially overlapped: all but the base raster must 
be entirely contained within another raster. This may be resolved in future
versions.

This software solves a particular problem when using multiscale numerical models, 
in that in using high resolution meshes, high resoution data is required, but for 
spatially limited regions. By blending a heirachy of data sources, ```HRDS``` overcomes
this problem and enables multiscale numerical problems to use spatially appropriate
data to be used with minimal effort.

# Acknowledgements

I acknowledge the University of York and World University Network for
funding my sabbatical visit which enabled this work to be completed. Also
thanks to Tristan Salles and Jody Webster for hosting me at the 
University of Sydney. 

# References
