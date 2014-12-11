
####  Mapdraw: mapping program using PIL 
###### Jonathan &amp; Yennifer

Problem
=======
When mapping collected data to a world map, using the Basemap package within matplotlib, there are several disadvantages. Having a fair understanding of Python is necessary, and the code must be changed each time a figure is produced. Depending on how many data points are being mapped, what projection is being used, and the detail of the map this process can take several minutes. Also matplotlib is highly dependant on multiple packages and is not very user friendly. 

###Why does it matter? 
The matplotlib program is currently used by scientists and researches in order visualize geographical data. These potential matplotlib users may not know Python, may not have the time to learn it, or may even have difficulty with the multiple package installs necessary to run the matplotlib program. Also, the amount of coding required to create the mapping process for only one output is extensive and time consuming. 

Matplotlib method 
=================
Matplotlib is a python library that creates plots using a syntax similiar to MATLAB. The original method uses Matplotlib to take the dataset, a projection given by the Basemap extension, and a given linear color range to create a plot. 

 original code using Matplotlib can be seen here: https://github.com/jmclinn/CSC453-Project/blob/master/basemap-ex.py


Mapdraw
============

After looking at several libraries, we chose to use Pillow, which is an updated fork of the Python Imaging Library (PIL). Since Pillow is an image editing package, data points will be given color values based on a given value range that can be mapped out as pixels to create the image. The user can specialized their inputs (output size, color, title, etc.) using the command line.



Data Input and Manipulation
================================================

###Color Range

We took the input data and manipulated it into the form required by Pillow. This meant creating a linear color range, and its associated values within the dataset. Taking a hex value (ex. #000000 is black) for each max and min value, we used two functions developed by a developer named Ben Southgate (http://bsou.io/p/3). These functions take a length 'n' and two color values, and return a linear range of length 'n' that spans between those two colors.

The code is available at:

https://github.com/jmclinn/CSC453-Project/blob/master/mapdraw/mapdraw/rgb2hex/rgb2hex.py

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

This code shows the process of adding a transformation to the data. The transformation equation used is hadcoded in this example, and has no relation to any geographical accuracy. Every fifth row of data the size of the transformed row is increased. This process is explained in detail below.

```python

# ===== TRANSFORMATION =====
def transform(args):
   data = args['data']
   ylen = args['ylen']
   data2 = []
   for i,row in enumerate(reversed(data)):
      if i < 5:
         stage = 1
      else:
         stage = i // 5
      for k in range(stage):
         data2.append(row)

   total = len(data2)
   data3 = data2[0::int(round(total/ylen))]
   ylen = len(data3)
   
   args['data'] = data3
   args['ylen'] = ylen
   return args
```

Prior to applying the transform to the image the command line arguments are parsed, and defaults are applied to any missing arguments. This process is explained later in the 'User Interface' section. From the arguments given the data is imported with the netCDF4 library. The data is an array of arrays, representing a matrix form. The position of each inner array represents the row, and the inner data points are the values for each column within that row.

For this transformation we only adjust the y-axis, or latitude, of the data, but x and y transformations are just as easily implemented. To improve efficiency we avoided any numerical operations on the actual values. The basic process is shown below in the figure.

<img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/transform.png" height="300" ></img>

The initial data matrix is run through a transformation equation that is a function of either latitude or longitude. Normalizing our data to its global position, we add rows and columns as necessary based on the equation. For our example, as shown above, the top of the image represented the largest reduction in size in our transformation, so we
took this as our starting point where there is a one-to-one translation between the data and the transformation. As we move down the matrix there is an increase in the number of additional times each row is represented in the transform.

Once the transform matrix is complete we can adjust the fidelity of the data that is processed by the program by uniformly deleting rows throughout the dataset's range. The more rows (or columns) removed the faster the data can be processed. This can also be used to preserve ratios between x and y when a transformation is done on only one axis. In our case data is removed to reduce the data's y-length to match what is was prior to addition of the rows for the transformation.

###Image creation 

In this process the data is paired with a color map and an image is created using predetermined default values. The color map dictionary places color at specific pixels to create an image.

```python
# ===== MAP IMAGE CREATION =====
def mapdraw(args,colorbar):
   img = Image.new('RGB',(args['xlen'],args['ylen']),'white')
   draw = Draw(img)

   for key,value in args['datamap'].iteritems():
      draw.point(value,getrgb(str(key)))

   img2 = img.resize((args['y'],args['y']), Image.BILINEAR)

   imgclr = colorbar.resize((args['colorbar'],img2.size[1]), Image.BILINEAR)

```

###User interface
The user places the desired parameters in the command lineas shown below. This program allows the user to modify the colors, colorbar range, title, and folder location among other attributes. The system then displays all the input data to the user showing both the default and input values. An example of an ouput to a specific user input is shown below:

```
mapdraw User$  python map.py file sgs.nc lat u_lat lon u_lon data sgsflux,9 title "SGS FLUX" mask -1230000000000000,#000000 save results max 10 min -10 colors "#FFAA00,#AAFF00,#00AAFF" 
21
file
sgs.nc
lat
u_lat
lon
u_lon
data
sgsflux,9
title
SGS FLUX
mask
-1230000000000000,#000000
save
results
max
10
min
-10
colors
#FFAA00,#AAFF00,#00AAFF
```

<img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/SGS%20FLUX_-10_10.png" height="300" ></img>

If the user chooses not to input parameters the rogram defaults to predetermined values as shown in the code block below. 

```python 
# ===== ARGUMENT PARSING AND SETTING DEFAULTS =====
def setargs(args):
   if 'title' not in args:
      args['title'] = ''
   if 'colors' not in args:
      args['colors'] = ['#0000FF','#FFFFFF','#FF0000']
   else:
      args['colors'] = args['colors'].split(',')
   if 'max' not in args:
      args['max'] = 10
   else:
      if '.' in args['max']:
         args['max'] = float(args['max'])
      else:
         args['max'] = int(args['max'])
   if 'min' not in args:
      args['min'] = -10
   else:
      if '.' in args['min']:
         args['min'] = float(args['min'])
      else:
         args['min'] = int(args['min'])
   if 'colorbar' not in args:
      args['colorbar'] = 100
   else: 
      args['colorbar'] = int(args['colorbar'])
   if 'y' not in args:
      args['y'] = 1000
   else:
      args['y'] = int(args['y'])
   if 'mask' in args:
      args['mask'] = args['mask'].split(',')
      args['mask'][0] = int(args['mask'][0]) 
   if 'background' not in args:
      args['background'] = 'white'
   if 'save' not in args:
      args['save'] = ''
   
   return args

```


Results
========
###Color mapping efficiency 
With matplotlib, the mapping process involves color mixing strategies whereas Mapdraw is able to simplify this method so that the user can input hex values to create the color range. This is efficient in that the user does not have knowledge of color mixing or edit the actual python code in order to set the range. 
     
Matplotlib color Mixing:
```
Custom color dictionary ('cdict') creation
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
  ```
Mapdraw color range user input: 

```
python map.py file sgs.nc lat u_lat lon u_lon data colors "#FFAA00,#AAFF00,#00AAFF"
```


###Time Efficiency 

Unlike matplotlib which takes approximately 74 seconds, the Mapdraw method completed the mapping and projection process in approximately 15 seconds. Mapdraw does not require the user to know Python because it allows the user to modify the code from the command line and it eliminates the need to download multiple packages therefore saving the user even more time. 


###Image Comparison

<img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/basemap20.png" height="300" ></img><img src="https://github.com/jmclinn/CSC453-Project/blob/master/images/SGS%20FLUX_-20_20.png" height="300" display= "inline"></img>

The first image is from the Matplotlib process, where the Cylindrical Equidistant map projection is applied. The difference in latitude values close to the poles can be clearly seen in our process' output (on the right) due to the difference in transformation method. Otherwise, everything is working as expected without any loss in clarity.

Further Developement 
======================
- transformation changes as argument input 
- add more customization of inputs ( color map structure, data matrix structures)
-multiple outputs with single command 
- pair with visual interface



