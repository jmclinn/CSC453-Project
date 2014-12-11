CSC253 Final Blogpost 
=============================
####  Mapdraw: mapping program using PIL 
###### Jonathan &amp; Yennifer

Problem
=======
When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes. Also matplotlib is highly dependant on multiple packages and is not very user friendly. 

#####Why does it matter?


Matplotlib method 
=================
The original method used Matplotlib to take the dataset, a projection given by the Basemap extension, and a given linear color range to create a plot. 

 original code using Matplotlib can be seen here: https://github.com/jmclinn/CSC453-Project/blob/master/basemap-ex.py


Pillow (PIL)
============

After looking at several libraries, we chose to use Pillow, which is an updated fork of the Python Imaging Library (PIL). Since Pillow is an image editing package, data points will be given color values based on a given value range that can be mapped out as pixels to create the image. An initial concern was that individual pixel placement would take too long, so our initial tests randomly generated datasets to obtain timing information. We altered the number of data points between 1 and 10 million, but the plotting of a 1000x1000 pixel image remained under 0.5 seconds. As this test shows, the advantage of using Pillow is that the printing of the datamap is independent of dataset size. Instead, its determined by the image output size, and for the purpose of this project anything much larger than 1000x1000 pixels is unecessary.

Data Input and Manipulation
================================================

#####Color Range

We took the input data and manipulated it into the form required by Pillow. This meant creating a linear color range, and its associated values within the dataset. Taking a hex value (ex. #000000 is black) for each max and min value, we used two functions developed by a developer named Ben Southgate (http://bsou.io/p/3). These functions take a length 'n' and two color values, and return a linear range of length 'n' that spans between those two colors.

Thacode is available at https://github.com/jmclinn/CSC453-Project/blob/master/rgb2hex.py

#####Value to Color Mapping

Now we have a list of color values the length of our desired value range. The indeces within the list correspond to the difference between the desired value and the minimum in the range. Each value in the dataset is now paired with the required color and saved to a dictionary, where each key is a hex color and its value is a list of tuples, each of which corresponds to xy-coordinates within the image.

Additionally, a mask can be applied to certain values, or ranges of values. In this case a black mask is applied to the 'land' values, which were set to at most -1e34. The mask catches all values less than this 'land' value. The rest of the value range is set to a max color of red, and min color of blue.


#####Data Import


#####Tranformation 



#####Image creation 




##### user interface


Results
========

#####Efficiency Differences






#####Image Comparison

<img src=""></img>
<img src=""></img>

The first image is from the Matplotlib process, where the Cylindrical Equidistant map projection is applied. The difference in latitude values close to the poles can be clearly seen in our process' output (on the right). Otherwise everything is working as expected without any loss in clarity.

Further Developement 
======================
- 
- 
 




