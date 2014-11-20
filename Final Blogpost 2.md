CSC253 Final Blogpost 2
==========
#### Pillo Mapping Program 
###### Jonathan &amp; Yennifer

Introduction:
============
When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes.

Our Program uses the Pillow, a friendly PIL (python Imaging Library) fork which allows us to image mapping data more efficiently and rapidly. 


Matplotlib program and execution: 
=====================================


image ouput: 

![alt text](https://lh6.googleusercontent.com/oLYMtP9y_GFA44aH2giG9AwAF2DrOT20TEFn7n0g5vr1MLHzCUsXFFk5DtiZ4WM6WH7q-XYTbcA=w1109-h663)


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
- create a user interface in python 
- adding grid and stylistic detail 





