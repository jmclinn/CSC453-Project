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

Next we took the input data and manipulated it into the form required by Pillow. 

```


```

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
 





