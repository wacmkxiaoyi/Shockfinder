#This is a model file for the Loader Addon
#It will be created when creating a new Loader
#Note!!!!: places which marke "<>" have to be updated, and delete "<>".

#File type: <Function> return <Object: Data>
#By Junxiang H., 2023/06/30
#wacmk.com/cn Tech. Supp.

#var filename includes the file_dir

#if you would like to import some packages,
#during the data loading.
#Please put that packages into this folder and using:

'''
try:
	import ShockFinder.Addon.Loader.<package1name> as <package1name>
	import ShockFinder.Addon.Loader.<package2name> as <package2name>
	#...
except:
	import <package1name> #debug
	import <package2name> #debug
	#...
'''


#A default Loader Addon can preprocess the filename,
#into to a formation with (time_index, file_dir, file_type)
#You can denote the below sentence to use it.

'''
try:
	import ShockFinder.Addon.Loader.FileNamePreProcess.FileNamePreProcess as FNPP
except:
	import FileNamePreProcess.FileNamePreProcess #debug
'''

try:
	import ShockFinder.Data
except:
	pass
def load(filename): #updated here
	#Loading Process
	read=<reader Process>(filename) #updated here
	#grid definded
	grid={}
	#GEOMETRY:	SPHERICAL	CYLINDRICAL		POLAR		CARTESIAN
	#			x1-x2-x3	x1-x2			x1-x2-x3	x1-x2-x3
	#			r-theta-phi r-z				r-phi-z		x-y-z
	grid["x1"]=read.<x1> #updated here
	grid["x2"]=read.<x2> #updated here
	grid["x3"]=read.<x3> #updated here 
	#basic quantities
	quantities={}
	quantities["vx1"]=read.<vx1> #updated here
	quantities["vx2"]=read.<vx2> #updated here
	quantities["vx3"]=read.<vx3> #updated here
	quantities["rho"]=read.<rho> #updated here
	quantities["prs"]=read.<prs> #updated here
	quantities["geometry"]=read.<geometry>
	#user definded...
	try:
		return Data.Data(grid,quantities)
	except:
		return (grid,quantities)