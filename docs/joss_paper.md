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
bibliography: paper.bib
---

# Summary

Multiscale modelling of geophysical domains requires data to set up initial conditions
such as bathymetry or topography. These data are typically in the form of GIS
rasters and can be derived from a number of sources. Typically, a single
data source is used which has a fixed spatial resolution. However, in multiscale
models, e.g. [Martin-Short2015], the scale of the model can vary by four or 
more orders of magnitude, e.g. from kilometre- to sub-metre-scale. In order to
use the high resolution data set in the area of highest model resolution one
must blend this limited-area highest resolution data with a wider area coarse
resolution dataset. A choice therefor has to be made to either sacrifice some resolution
or create a very large data file. For a wide region zooming into metre-scale processes this 
data file could be terrabytes in size when resampled at the resolution of the highest
resolution dataset.

``HRDS`` is a solution to this problem as it allows a user to extract data 
from an arbitrary point from a stack of rasters, each of which can have different
extents and resolutions. As these rasters are unlikely to agree on the topographic/
bathymetric height where they overlap, a linear distance buffer is created to smoothly
blend the two datasets together. The user can specify the distance over which this buffer
acts. The user gives HRDS a base raster which is low resolution but covers the whole extent 
of the domain to be modelled and then a stack of other rasters in priority order (typically increasing
in resolution) along with a corresponding list of buffer distances. ``HRDS`` then calculates
the linear buffers and stores these as rasters. The user can then request data at an arbitrary 
point.

An example of HRDS in use is shown in Figure 1. Left are the original raster datasets. There 
are clear artifacts introduced between the base raster and the next 

# Citations 

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

# Figures

Figures can be included like this: ![Example figure.](figure.png)

# Acknowledgements

I acknowledge the University of York and World University Network for
funding my sabbatical visit which enabled this work to be completed. Also
thanks to Tristan Salles and Jody Webster for hosting me at the 
University of Sydney. 

# References
