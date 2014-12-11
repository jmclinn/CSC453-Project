
####  Mapdraw: mapping program using PIL 
###### Jonathan &amp; Yennifer

Problem
=======
When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes. Also matplotlib is highly dependant on multiple packages and is not very user friendly. 

###Why does it matter? 
The matplotlib program is currently used by scientists and researches in order visualize geographical data. These potential matplotlib users may not know Python, may not have the time to learn it, or may even have difficulty with the multiple package installs that necessary. The amount of coding required to create the mapping process for one output is extensive and too time consuming for potential users. 

Matplotlib method 
=================
The original method used Matplotlib to take the dataset, a projection given by the Basemap extension, and a given linear color range to create a plot. 

 original code using Matplotlib can be seen here: https://github.com/jmclinn/CSC453-Project/blob/master/basemap-ex.py


Mapdraw
============

After looking at several libraries, we chose to use Pillow, which is an updated fork of the Python Imaging Library (PIL). Since Pillow is an image editing package, data points will be given color values based on a given value range that can be mapped out as pixels to create the image. The user can specialized their inputs (output size, color, title, etc.) using the command line.



Data Input and Manipulation
================================================

###Color Range

We took the input data and manipulated it into the form required by Pillow. This meant creating a linear color range, and its associated values within the dataset. Taking a hex value (ex. #000000 is black) for each max and min value, we used two functions developed by a developer named Ben Southgate (http://bsou.io/p/3). These functions take a length 'n' and two color values, and return a linear range of length 'n' that spans between those two colors.

The code is available at https://github.com/jmclinn/CSC453-Project/blob/master/rgb2hex.py

###Value to Color Mapping

Now we have a list of color values the length of our desired value range. The indeces within the list correspond to the difference between the desired value and the minimum in the range. Each value in the dataset is now paired with the required color and saved to a dictionary, where each key is a hex color and its value is a list of tuples, each of which corresponds to xy-coordinates within the image.

Additionally, a mask can be applied to certain values, or ranges of values. In this case a black mask is applied to the 'land' values, which were set to at most -1e34. The mask catches all values less than this 'land' value. The rest of the value range is set to a max color of red, and min color of blue.

```python 
# ===== COLOR MAP =====
def colormap(args):
   rangelen = args['max'] - args['min']
   rangemid = args['min'] + (rangelen / 2)
   rangemax = args['max']
   rangemin = args['min']
   
   cr2 = rgb2hex.linear_gradient(args['colors'][1],args['colors'][2],(int(rangelen/2*1000))+1)['hex']
   cr1 = rgb2hex.linear_gradient(args['colors'][0],args['colors'][1],(int(rangelen/2*1000))+1)['hex']
   dictlist = {}

   # === PAIR DATA WITH COLOR MAP ===
   for y,sl in enumerate(args['data']): # for each sublist within dataset (row)
      for x,i in enumerate(sl): # for each point in sublist (column)
         val = args['colors'][1]
         #top half of data range
         if i > rangemid:
            if i <= rangemax:
               val = cr2[int((i - (rangemin + rangelen/2)) * 1000)]
            else:
               val = args['colors'][2]
         #bottom half of data range
         elif i < rangemid:
            if i >= rangemin:
               val = cr1[int((i - rangemin) * 1000)]
            else:
               val = args['colors'][0] 
         # mask
         if 'mask' in args:
            if i <= args['mask'][0]:
               val = args['mask'][1]
         # add to dict
         if val in dictlist:
            dictlist[val].append((x,y))
         else:
            dictlist[val] = [(x,y)]
            
   args['datamap'] = dictlist

     
```


###Transformation 
<img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/transform.png" height="300" ></img>

###Image creation 

In this process the data is paired with a color map and an image is created using predetermined default values. The color map dictionary places color at specific pixels to create an image.


###User interface
The user places the desired parameters in the command lineas shown below. This program allows the user to modify the colors, colorbar range, title, and folder location among other attributes. 


Results
========
###Color mapping efficiency 
With matplotlib, the mapping process involves color mixing strategies whereas Mapdraw is able to simplify this method so that the user can input hex values to create color range.

###Time Efficiency 

Unlike matplotlib which takes a total of 74 seconds, the Mapdraw method completed the mapping and projection process in only 15 seconds. Mapdraw does not require the user to know Python because it allows the user to modify the code from the command line.Mapdraw eliminates the need to download multiple packages therefore saving the user even more time. 


###Image Comparison

<img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/transform.png" height="200" ><img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/transform.png" height="200" display= "inline" ></img>

   <div class="caption"> Matplotlib. </div><div class="caption"display="inline"> Mapdraw. </div>


The first image is from the Matplotlib process, where the Cylindrical Equidistant map projection is applied. The difference in latitude values close to the poles can be clearly seen in our process' output (on the right). Otherwise everything is working as expected without any loss in clarity.

Further Developement 
======================
- transformation changes as argument input 
- add more customization of inputs ( color map structure, data matrix structures)
-multiple outputs with single command 
- pair with visual interface



