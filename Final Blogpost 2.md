CSC253 Final Blogpost 2
==========
####  Mapping Program 
###### Jonathan &amp; Yennifer

Introduction:
============
When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes.

Our Program uses the Pillow, a friendly PIL (python Imaging Library) fork which allows us to image mapping data more efficiently and rapidly. 


Matplotlib program and execution: 
=====================================


image ouput: 

![Matplotlib/Basemap Processed Data](https://dl-web.dropbox.com/get/TCS453/basemap-ex-sm.png?_subject_uid=43009455&w=AACGOpOdpuS9KqOQGdgww1EIm3U1i6H4ytZ1eVQB_9GtVg)


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

![Our Processed Data](https://dl-web.dropbox.com/get/TCS453/sgs20-sm.png?_subject_uid=43009455&w=AACLhlFDz4-P13BOcjxrdpUWPKvDJHD4ZInS2NgeR1MUug)

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
 





