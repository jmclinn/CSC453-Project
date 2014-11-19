# SGS Flux Data Mapping w/ Land Masked
# ====================================
# when (ref #) appears, refer to number in ref.txt

# Import necessary packages
# -------------------------
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from mpl_toolkits.basemap import Basemap
import math
import time
# Read data file
# --------------
t0 = time.time()

f = Dataset('SGSFlux19980302_Tanh10_K0050.nc','r');

# Retreive the necessary data
# ---------------------------
u_lat = f.variables['u_lat'][:]
u_lon = f.variables['u_lon'][:]
kmt = f.variables['KMT']#[:,:]
sgsflux = f.variables['sgsflux'][9,:,:]

t1 = time.time() - t0
print "data loaded"
print t1


# Establish the land areas, for masking (anything < -1*e^34)
# ----------------------------------------------------------
sgsland = np.ma.masked_greater(sgsflux, (((-1)*math.e ** 34)+1))

t2 = time.time() - t0 - t1
print "mask creation"
print t2

# Establish Basemap with desired projection
# -----------------------------------------
# a full list of parameter explanations and options is available (ref 0)
# -----------------------------------------
m = Basemap(projection='cyl', # set projection type (ref 1)
#    lat_0=0, lon_0=30, # for use with 'ortho'-like projections (ref 2)
    resolution='l', area_thresh=5, # resolution and area threshold (ref 3)
    llcrnrlon=-83, llcrnrlat=-19.89, # set corners of display area (lon and lat values)
    urcrnrlon=15, urcrnrlat=72.63)
 
##m.drawcoastlines(color='green') # coastline color
##m.drawcountries(color='green') # country boundaries color
#m.fillcontinents(color='white') # continent fill (disable if 'land' is being masked)
##m.drawmapboundary() 

# Choose how lat and lon lines are drawn
# --------------------------------------
# np.arange (start, stop, step size)
# labels=[left, right, top, bottom]
# other options are available (ref 0)
# --------------------------------------
##m.drawmeridians(np.arange(0, 360, 30),labels=[False,False,False,True])
##m.drawparallels(np.arange(-90, 90, 30),labels=[True,False,False,False])

t3 = time.time() - t0 - t1 - t2
print "create Basemap"
print t3

# create grid of lat and lon values
LON,LAT=np.meshgrid(u_lon,u_lat)
x,y = m(LON,LAT)

t4 = time.time() - t0 - t1 - t2 - t3
print "grid lat/lon"
print t4


# Custom color dictionary ('cdict') creation
# ------------------------------------------
# instructions & references at (ref 4)
# ------------------------------------------
cdict = {'red': ((0.0, 0.0, 0.0),
                  (0.5, 1.0, 1.0),
                  (1.0, 1.0, 1.0)),
         'green': ((0.0, 0.0, 0.0),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.0, 0.0)),
         'blue': ((0.0, 1.0, 1.0),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.0, 0.0))}

# Apply custom color dictionary to a colormap
# -------------------------------------------
cmap1 = clr.LinearSegmentedColormap('colormap1',cdict,256)


# Map values
# ----------
# x-range, y-range, value set, min value of color range (anything lower will map to lowest value color, max of color range, color map to choose from (either 'built-in name' or cmap1 for custom cdict))
# ----------
#cs = m.pcolor(x,y,kmt,cmap=cmap1) # this plots the kmt values
cs = m.pcolor(x,y,sgsflux,vmin=-20,vmax=20,cmap=cmap1)# (set cmap=cmap1 for custom color map to be used.) This plots the sgs-flux values
##plt.colorbar() # creates colorbar to be placed next to plot

t5 = time.time() - t0 - t1 - t2 - t3 - t4
print "data plotting"
print t5

# Creates a second cdict (completely black) to create the black mask
# ------------------------------------------------------------------
cdict2 = {'red': ((0.0, 0.0, 0.0),
                  (0.5, 0.0, 0.0),
                  (1.0, 0.0, 0.0)),
         'green': ((0.0, 0.0, 0.0),
                  (0.5, 0.0, 0.0),
                  (1.0, 0.0, 0.0)),
         'blue': ((0.0, 0.0, 0.0),
                  (0.5, 0.0, 0.0),
                  (1.0, 0.0, 0.0))}

cmap2 = clr.LinearSegmentedColormap('colormap2',cdict2,256)

# Create 'land' mask on same plot as value set
# --------------------------------------------
cs = m.pcolor(x,y,sgsland,cmap=cmap2)

t6 = time.time() - t0 - t1 - t2 - t3 - t4 - t5
print "mask plotting"
print t6

# Create title of plot and display the image
# ------------------------------------------
# title display options at (ref 5)
# ------------------------------------------
##plt.title("The Cascade Rate - SGSFLUX")
plt.show()

#t7 = time.time() - t0 - t1 - t2 - t3 - t4 - t5 - t6
#print "print plot"
#print t7
