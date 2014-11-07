CSC453-Project
==============

#####Optimized method for mapping data to various projections

###### Jonathan &amp; Yennifer


Project Proposal
================

When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes.

Caching the compiled data prior to plotting was originally considered as a potential performance boost, but the majority of the time taken turns out to be the actual plotting of the data. In several tests, the data gathering took around 1/10 the time of plotting the data. There are still potential optimizations to be done however. During the plotting step using Basemap and matplotlib there are several combined steps. A colormap is assigned to the data, and then the data is morphed on to a desired projection.

By separating out this process into several steps we will look at several potential optimization processes. There is the option to pickle or cache the projected data, the color-mapped data, or some version of both which we could then more readily plot. There is also the potential to use an animation based process, like ubigraph, to allow for more real-time switching between projections given a particular data set.

Overall we want to create a faster, easier to use method for plotting projected data commonly used by research scientists and data analysts.
