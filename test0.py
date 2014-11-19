from netCDF4 import Dataset
import math
import random
from PIL import Image
from PIL.ImageColor import getrgb
from PIL.ImageDraw import Draw

from rgb2hex import rgb2hex

import time
t0 = time.time()

f = Dataset('SGSFlux19980302_Tanh10_K0050.nc','r')
u_lat = f.variables['u_lat'][:]
u_lon = f.variables['u_lon'][:]
#kmt = f.variables['KMT']#[:,:]
sgsflux = f.variables['sgsflux'][9,:,:]

t1 = time.time() - t0
print "Data Import"
print t1

xlen = len(u_lon)
ylen = len(u_lat)
xr = range(xlen)
yr = range(ylen)
vr = []

for x in reversed(sgsflux):
   for y in x:
      vr.append(y)

cr0 = rgb2hex.linear_gradient("#FFFFFF","#FF0000",(20*1000+1))['hex']# + rgb2hex.linear_gradient("#FF0000","#000000",(10*1000+1))['hex']
#cr1 = rgb2hex.linear_gradient("#000000","#0000FF",(10*1000+1))['hex'] + rgb2hex.linear_gradient("#0000FF","#FFFFFF",(10*1000+1))['hex']
cr1 = rgb2hex.linear_gradient("#0000FF","#FFFFFF",(20*1000+1))['hex']
dictlist = {}

t2 = time.time() - t0 - t1
print "Data Processing"
print t2

for n,i in enumerate(vr):
   val = "#FFFFFF"
   if i >= 0:
      if i <= 20:
         val = cr0[int(i*1000)]
         #val = "#EEEEEE"
      else:
         val = "#FF0000"
   elif i < 0:
      if i >= (-20):
         val = cr1[int((20+i)*1000)]
         #val = "#EEEEEE"
      elif i <= ((-9.99)*math.e ** 33):
         val = "#000000"
      else:
         val = "#0000FF"
   
#   elif i <= 0 and i >= (-100):
#      val = cr1[int((100+i)*1000)]
#   elif i <= ((-9.99)*math.e ** 33):
#      val = "#000000"
   if val in dictlist:
      dictlist[val].append((n%xlen,n//ylen))
   else:
       dictlist[val] = [(n%xlen,n//ylen)]

t3 = time.time() - t0 - t1 - t2
print "Color Mapping"
print t3


# ================
# Create new image
# ================
img = Image.new('RGB',(xlen,xlen),"white")
draw = Draw(img)

for key,value in dictlist.iteritems():
#   for value in dictlist[str(key)]:
   draw.point(value,getrgb(str(key)))

img.show()
   
t4 = time.time() - t0 - t1 - t2 - t3
print "Image Creation"
print t4
