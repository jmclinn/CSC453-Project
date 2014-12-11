import sys
from mapdraw import mapdraw

# ===== USER INPUT PARSE =====
#argnum = len((sys.argv)/2)
args = {}
print len(sys.argv)
if len(sys.argv) > 1:
   for i,arg in enumerate(sys.argv[1::2]):
#      print i
      print arg
      args[arg] = sys.argv[2*i+2]
      print args[arg]

args = mapdraw.setargs(args)
if 'file' in args:
   args = mapdraw.dataload(args)
   args = mapdraw.transform(args)
   args, colorbar = mapdraw.colormap(args)
   mapdraw.mapdraw(args,colorbar)
else:
   print 'Location of data file not included in arguments'
   print args