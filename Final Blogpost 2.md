CSC253 Final Blogpost 2
==========
####  Mapping Program 
###### Jonathan &amp; Yennifer

Problem
=======
When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes.

Iinitial Goal
=============

For our first progress update we wanted to prove that we could plot the data quickly, with a package that allowed us the necessary flexibility (titles, colorbars, etc.). Since we're focused on efficiency, we needed to prove our plotting system will work quickly before we deal with the data manipulation involved in projection.

Pillow (PIL)
============

After looking at several libraries, we chose to use Pillow, which is an updated fork of the Python Imaging Library (PIL). Since Pillow is an image editing package, data points will be given color values based on a given value range that can be mapped out as pixels to create the image. An initial concern was that individual pixel placement would take too long, so our initial tests randomly generated datasets to obtain timing information. We altered the number of data points between 1 and 10 million, but the plotting of a 1000x1000 pixel image remained under 0.5 seconds. As this test shows, the advantage of using Pillow means the printing of the datamap is independent of dataset size. Instead, its determined by the image output size, and for the purpose of this project anything much larger than 1000x1000 pixels is unecessary.

Data Input and Manipulation (without projection)
================================================

#####Color Range

Next we took the input data and manipulated it into the form required by Pillow. This meant creating a linear color range, and its associated values within the dataset. Taking a hex value (ex. #000000 is black) for each max and min value, we used two functions developed by a developer named Ben Southgate (http://bsou.io/p/3) that create an array of a given length and two  that gives a linear color change between. That takes a length 'n' and two color values, and returns a linear range of length 'n' that spans between those two colors.

That code is available at https://github.com/jmclinn/CSC453-Project/blob/master/rgb2hex.py

#####Value to Color Mapping

Now we have a list of color values the length of our desired value range. The indeces within the list correspond to the difference between the desired value and the minimum in the range. Each value in the dataset is now paired with the required color and saved to a dictionary, where each key is a hex color and its value is a list of tuples, each of which corresponds to xy-coordinates within the image.

Additionally, a mask can be applied to certain values, or ranges of values. In this case a black mask is applied to the 'land' values, which were set to at most -1e34. The mask used catches all values less than this 'land' value. The rest of the value range is set to a max color of red, and min color of blue.

```python

# Data Import
# -----------
f = Dataset('SGSFlux19980302_Tanh10_K0050.nc','r') #import file
u_lat = f.variables['u_lat'][:]
u_lon = f.variables['u_lon'][:]
sgsflux = f.variables['sgsflux'][9,:,:] #data

xlen = len(u_lon)
ylen = len(u_lat)
xr = range(xlen)
yr = range(ylen)
vr = []

# Color Range Creation
# --------------------
cr0 = rgb2hex.linear_gradient("#FFFFFF","#FF0000",(20*1000+1))['hex']
cr1 = rgb2hex.linear_gradient("#0000FF","#FFFFFF",(20*1000+1))['hex']

# Color to Value Mapping
# ----------------------
dictlist = {}

for y,sl in enumerate(reversed(sgsflux)): # for each sublist within dataset (row)
   for x,i in enumerate(sl): # for each point in sublist (column)
      val = "#FFFFFF" #middle (0) value
      if i >= 0:
         if i <= 20:
            val = cr0[int(i*1000)] #find index in positive color range
         else:
            val = "#FF0000" #max positive color if exceeds range
      elif i < 0:
         if i >= (-20):
            val = cr1[int((20+i)*1000)] #find index in negative color range
         elif i <= ((-9.99)*math.e ** 33): # COLOR MASK APPLICATION
            val = "#000000" #mask color
         else:
            val = "#0000FF" #min negative color if exceeds range
      if val in dictlist:
         dictlist[val].append((x,y)) #add xy-coordinate to color key
      else:
         dictlist[val] = [(x,y)] #create new color key
```

#####Efficiency Differences

The original method used matplotlib to take the dataset, a projection given by the Basemap extension, and a given linear color range to create a plot. Using the same dataset as above (1,254,400 data points), this process took approximately 110 seconds. The plotting portion of this process took about 70 second, and while that included the projection mapping as well, our new process took just 16 seconds.

Once projection mapping is added to our process, we anticipate that it will at most double our execution time which is just half of the time taken by Matplotlib. This is because the majority of our processing time is assigning the color values to the dataset point by point, and the projection mapping is a similar process.

One added efficiency with our process is the inclusion of data masking within the color mapping. In Matplotlib the mask needed to be applied after the dataset was processed and plotted. For this data, that added another 30 seconds.

If we double our current time, bringing it to 30 seconds including projection, our process would be three times more efficient than when using Matplotlib. By having complete control over our data manipulation, we also have the opportunity to cache data at various stages, further increasing efficiency upon multiple iterations.

#####Image Comparison

<img src="http://storage.googleapis.com/random-jmclinn/basemap-ex-sm.png"></img>
<img src="http://storage.googleapis.com/random-jmclinn/sgs20-2-sm.png"></img>


Matplotlib program and execution 
=====================================


image ouput: 

![Matplotlib/Basemap Processed Data](http://storage.googleapis.com/random-jmclinn/basemap-ex-sm.png)


Output from Basemap and Matplotlib method:
```
data loaded
0.0844769477844
mask creation
0.004065990448
create Basemap
4.6259188652
grid lat/lon
0.0199291706085
data plotting
58.491672039
mask plotting
24.1573448181
```


Mapping Data Using Pillow: 
===========================

![Our Processed Data](http://storage.googleapis.com/random-jmclinn/sgs20-1-sm.png)

Output from new method that uses Pillow (PIL) to create plot:
```
Data Import
0.0063898563385
Data Processing
0.524234056473
Color Mapping
14.9274668694
Image Creation
0.588411092758
```

conclusions:
===========


Further Developement: 
======================
- create a library
- adding grid and stylistic detail
- create a user interface in python where the user can change color, transformation, lattitude longitude lines, image output size among other basic image properties. 
 





