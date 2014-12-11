# ===== PACKAGES =====
from netCDF4 import Dataset
from PIL import Image,PSDraw
from PIL.ImageColor import getrgb
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
# === custom package ===
from rgb2hex import rgb2hex

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

# ===== DATA IMPORT =====
def dataload(args):
   lat0 = args['lat']
   lon0 = args['lon']
   data2 = args['data'].split(',')
   data0 = data2[0]
   depth = int(data2[1])
   f = Dataset(args['file'],'r')
   lon = f.variables[lon0]
   lat = f.variables[lat0]
   data = f.variables[data0][depth,:,:]

   xlen = len(lon)
   ylen = len(lat)
   
   args['data'] = data
   args['lon'] = lon
   args['lat'] = lat
   args['xlen'] = xlen
   args['ylen'] = ylen
   return args

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

   # ===== COLORBAR CREATION =====
   clr = (cr1 + cr2)
   clr = clr[::-1000]
   widthclr = args['colorbar']
   heightclr = len(clr)

   imgclr = Image.new("RGB",(widthclr,heightclr),"white")
   drawclr = Draw(imgclr)

   for y,val in enumerate(clr):
      for x in range(widthclr):
         drawclr.point((x,y),getrgb(str(val)))
   
   return args, imgclr

# ===== MAP IMAGE CREATION =====
def mapdraw(args,colorbar):
   img = Image.new('RGB',(args['xlen'],args['ylen']),'white')
   draw = Draw(img)

   for key,value in args['datamap'].iteritems():
      draw.point(value,getrgb(str(key)))

   img2 = img.resize((args['y'],args['y']), Image.BILINEAR)

   imgclr = colorbar.resize((args['colorbar'],img2.size[1]), Image.BILINEAR)

   # ===== ENTIRE IMAGE CREATION W/ TEXT=====
   imgbox = Image.new('RGB',((300+args['y']+args['colorbar']),(img2.size[1]+200)),args['background'])
   imgbox.paste(img2,(100,100))
   imgbox.paste(imgclr,((200+img2.size[0]),100))

   drawbox = Draw(imgbox)
   title = args['title']
   titlesize = 50 # future user input
   font = truetype("/library/fonts/Arial.ttf",titlesize)
   smfontsize = 30 # future user input
   smfont = truetype("/library/fonts/Arial.ttf",smfontsize)
   titlewidth = font.getsize(title)[0]
   drawbox.text(((imgbox.size[0]/2 - titlewidth/2), titlesize/2),title,(0,0,0),font=font)

   drawbox.text(((imgbox.size[0] - 95),100),str(args['max']),(0,0,0),font=smfont)
   drawbox.text(((imgbox.size[0] - 95),(100 + img2.size[1] - smfontsize)),str(args['min']),(0,0,0),font=smfont)

   imgbox.show()
   if 'title' in args:
      title = args['title']+'_'+str(args['min'])+'_'+str(args['max'])+'.png'
   else:
      title = 'output_'+str(args['min'])+'_'+str(args['max'])+'.png'
   imgbox.save(args['save']+'/'+title)