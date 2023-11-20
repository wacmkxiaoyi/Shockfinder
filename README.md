# ShockFinder

**ShockFinder** is an interactive scientic simulation data analysis software based on python and supports multi-process, multi-mode, I/O access and drawing.

Author: Junxiang H. & C. B. Singh<br>
If you have any questions and suggestions<br>
Please contact: [wacmkxiaoyi@gmail.com](mailto:wacmkxiaoyi@gmail.com)

You can access [**Outdate version**](https://github.com/wacmkxiaoyi/Shockfinder/releases) (i.e., \< V5.0) here.

Latest Version: 7.3.0, date: 2023-11-13

# Install

Please follow one of the ways to install **ShockFinder**


```shell
pip3 install ShockFinder
```

If you want to use multi-processes during analysis and reading, it is recommended to use the [**XME**](https://www.github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine) interface of the **WACMK-Xenon** software set, which can be installed through the following command:

```shell
pip3 install XME
```

If you have better multiprocessing engine, you can definde it by using ShockFinder inline command ***-n=MultiprocessEngine@configname***. 

At the same time, we are very encourage that you use our GUI engine [**XenonUI**](https://www.github.com/wacmkxiaoyi/Xenon-UI) to assist your analysis work. You can install it by following command:

```shell
pip3 install XenonUI
```

**Notice**: **XenonUI** supports UNIX and windows systems, but the **tkinter** libraries have to be installed! More detail see [https://www.github.com/wacmkxiaoyi/Xenon-UI](https://www.github.com/wacmkxiaoyi/Xenon-UI).

# Useage

Enter the following code and save it into a file (like ***shockfind.py***, version >=7.1)

```python
try:
	import XME
except:
	print("Warning: The default Multiprocess Engine XME is not installed, Multiprocess mode might not be used!")
	print("Please type: pip3 install XME to install")
	print("More infomation see: https://github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine")
	print("\n")
try:
	import XenonUI
except:
	print("Warning: The default GUI Engine XUI (XenonUI) is not installed, GUI mode might not be used!")
	print("Please type: pip3 install XenonUI to install")
	print("More infomation see: https://github.com/wacmkxiaoyi/Xenon-UI")
	print("\n")

import sys,os
import ShockFinder
from ShockFinder.Config import ShockFinderDir
from ShockFinder.Update import Update_all

def drop_bk(strc):
	if strc!="" and (strc[0]=="'" and strc[-1]=="'" or strc[0]=='"' and strc[-1]=='"'):
		strc=strc[1:-1]
	return strc
if __name__=="__main__":#windows support
	gui=True
	for i in sys.argv[1:]:
		if "=" not in i:
			i="file="+i
		if i.split("=")[0] in ("f","-f","file"):
			ShockFinder.ShockFinder(drop_bk(i.split("=")[1]))
			gui=False
		elif i.split("=")[0] in ("u","-u","update"):
			Update_all()
			gui=False
		elif i.split("=")[0] in ("n","-n","new"):#new=module@filename
			LoaderDir=os.path.join(ShockFinderDir,"Addon","Loader")
			AnalysisToolDir=os.path.join(ShockFinderDir,"Addon","AnalysisTool")
			PainterDir=os.path.join(ShockFinderDir,"Addon","Painter")
			IODir=os.path.join(ShockFinderDir,"Addon","IO")
			MultiprocessEngineDir=os.path.join(ShockFinderDir,"Addon","MultiprocessEngine")
			GUIDir=os.path.join(ShockFinderDir,"Addon","GUI")
			modu=i.split("=")[1].split("@")[0]
			mfname=i.split("=")[1].split("@")[1]
			if modu in ("Loader","AnalysisTool","Painter","IO","MultiprocessEngine","GUI"):
				import shutil
				if modu=="Loader":
					shutil.copy(mfname,LoaderDir)
				elif modu=="AnalysisTool":
					shutil.copy(mfname,AnalysisToolDir)
				elif modu=="Painter":
					shutil.copy(mfname,PainterDir)
				elif modu=="IO":
					shutil.copy(mfname,IODir)
				elif modu=="MultiprocessEngine":
					shutil.copy(mfname,MultiprocessEngineDir)
				elif modu=="GUI":
					shutil.copy(mfname,GUIDir)
			Update_all()
			gui=False
	if gui:
		ShockFinder.ShockFinder()
```

# GUI MODE

GUI mode is used to **generate analysis configuration files** and **visualize analysis results**!

Enter GUI mode:

```shell
python shockfind.py
```

The GUI engine for the ShockFinder is **XUI** (see https://github.com/wacmkxiaoyi/Xenon-UI). 

Four pages are available: **Analysis**, **Graph**, **Help** and **Exit**

The **Exit** page is used to interrupt multi-thread monitoring and exit Shockfinder. **Help** displays some basic information about ShockFinder (such as version, author)

## Page analysis

The **Analysis** page has three menus, **Save Configuration**, **Global Settings** and **Analysis**

### Global Settings

The menu **Global Settings** has three submenus:

1. **Multiprocess**: Regarding the configuration of multi-process analysis, the default multi-process engine is **XME** (see https://github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine, some advanced options can be clicked here Link).

2. **Database Storage**: Configuration used to store analysis data. The default engine is **HDF5**, the default project name (save target file name) is **current timestamp**, and Drop Buffer is the buffer analysis process. Medium transparency (default and recommended **True**)

3. **Simulation Data Loader**: In this submenu you must define the type of simulation data used.

### Analysis

Menu **Analysis** has two sub-menus:

1. **Parameters**: in here you can define the global variable during the analyzing

2. **Quantities**: in here you can define which analysis approch will be used during the analyzing

### Save Configurations:

1. Button **Test**: to test cn the analysis process proceed normally

2. Button **Save**: save the analysis configuration file

## Page Figure

Page **Figure** has Two Menus, **Database**, and **Figure**

### Database

Menu **Database** has two sub-menus:

1. **Load**: before you figure the picture you like, you should load the **after-analyzing data** firstly. In this menu, data reading, browsing, and other functions can be performed

2. **Global Settings**: the configuration of loader of **after-analyzing data**

### Figure

Menu **Figure** has three sub-menus: **Set unit**, **2d** and **3d** (easy to understand without additional explanation)

# Parallel analysis mode (PAM)

After producing the analysis configration file (e.g., config1.ini, config2.ini), you can start to analyze:

```shell
python shockfinder.py -f=config1.ini -f=config2.ini ...
```

# How to add a new type of simulation or analysis method:

ShockFinder recommends two module models:

1. **LoaderModel.py**:
```python
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
```

2. **AnalysisToolModel.py**:
```python
#This is a model file for the Loader Addon
#It will be created when creating a new Loader
#Note!!!!: places which marke "<>" have to be updated, and delete "<>".

#File type: <Function> return a new <Object: Data>
#By Junxiang H., 2023/07/01
#wacmk.com/cn Tech. Supp.

#if you would like to import some packages,
#during the data loading.
#Please put that packages into this folder and using:

try:
	from ShockFinder.Addon.AnalysisTool.Basic import *
	#if AvgTh_CAL is True
	#import ShockFinder.Addon.AnalysisTool.Mean as Mean
	#import ShockFinder.Addon.AnalysisTool.<packages name> as <packages name>
except:
	from Basic import *
	#import Mean #debug
	#import <packages name>

need=[]
#args will be inserted into Data Object
#vargs will not be inserted into Data Object
import numpy as np
def get(Dataobj,args={},vargs={}):
	Dataobj.quantities.update(args)
	for i in need:
		if i not in Dataobj.quantities.keys() and i not in vargs.keys():
			print("Warning: args:",i,"is needed without definding")
			return Dataobj
	quantities={
		#operation with dict args
		#...
		<quantity name>:... #update here
	}
	Dataobj.quantities.update(quantities)
	return Dataobj
def result(quantity_name=None,anafname=None):
	return () #this function will return result types shown in GUI
#if AvgTh mode is needed, please set AvgTh_cal=True
#The below code can be ignored, if set to False
AvgTh_cal=False
def get_AvgTh(Dataobj,args={},vargs={"Mean_axis":(1,)}):
	try:
		if AvgTh_cal:
			import copy
			newneed=copy.copy(need)
			if "Mean_axis" not in newneed:
				newneed.append("Mean_axis")
			Dataobj.quantities.update(args)
			for i in newneed:
				if i not in Dataobj.quantities.keys() and i not in vargs.keys():
					print("Warning: args:",i,"is needed without definding")
					return Dataobj
			meanstr=""
			try:
				meanaxis=vargs["Mean_axis"]
			except:
				meanaxis=Dataobj.quantities["Mean_axis"]
			for i in meanaxis:
				meanstr+=str(i)+"@"+str((round(vargs["Mean_axis"+str(i)][0],2),round(vargs["Mean_axis"+str(i)][1],2)))+"_" if "Mean_axis"+str(i) in vargs.keys() else meanstr+=str(i)+"@"+str((round(Dataobj.quantities["Mean_axis"+str(i)][0],2),round(Dataobj.quantities["Mean_axis"+str(i)][1],2)))+"_" if "Mean_axis"+str(i) in Dataobj.quantities.keys() else ""
			quantities={"AvgTh_"+meanstr+"<quantity name>":...} #update here
			Dataobj.quantities.update(quantities)
		else:
			print("Warning: AvgTh mode is not opened: <quantity name>") #update here
	except:
		print("Warning: AvgTh mode is not definded:", __file__) #update here
	return Dataobj

if __name__=="__main__":
	print("Testing Model:",__file__)
	from TestData import TestData
	TestData=get(TestData)
	print("Testing Result:", TestData.quantities[<quantity name>]) #update here!
	if AvgTh_cal:
		TestData=get_AvgTh(TestData)
		print("Testing Result:", TestData.quantities["AvgTh_<quantity name>"]) #update here!
```

Once done, you must place it into the ShockFinder directory by using

```shell
python shockfinder.py -n={module@filename/path}
```

in the DOC window. The new simulated data type or analysis method will then be displayed in **GUI** mode.

## Example:


We will present here an analytical method suitable for our current working model for calculating mass fluxes (i.e. accretion rates, etc.)

```python
#File BlackHoleMassFlux.py
#WACMK Tech
#Only for 2D data, support SPHERICAL, POLAR, XOY
#	edge: fall into black hole, match accretion rate.
# 		plus : escape from black hole, minor: fall into black hole
#	inj: injet flow
#		plus : accreted into system, minor: escape from system
#	wind: wind
#		plus: back to system, minor: escape from system
#	outflow:
#		plus: back to system, minor: escape from system	
#   jet:
#		plus: escape from bh,....
#in each case, positive flux means material go to accretion region
#ac_begin and ac_end are size of accretion region (Escapt Polar coordinate)

try:
	from ShockFinder.Addon.AnalysisTool.Basic import *
	from ShockFinder.Addon.AnalysisTool.Differential import integrate_sph_sur,integrate_pol_sur,integrate_surface,get_closest_index
	#if AvgTh_CAL is True
	#import ShockFinder.Addon.AnalysisTool.Mean as Mean
	#import ShockFinder.Addon.AnalysisTool.<packages name> as <packages name>
except Exception as err:
	print(err)
	from Basic import *
	#import Mean #debug
	#import <packages name>

need=["MassFlux_x1","MassFlux_x2"]
#args will be inserted into Data Object
#vargs will not be inserted into Data Object
import numpy as np
def get(Dataobj,args={},vargs={}):
	Dataobj.quantities.update(args)
	for i in need:
		if i not in Dataobj.quantities.keys() and i not in vargs.keys():
			print("Warning: args:",i,"is needed")
			return Dataobj

	if Dataobj.quantities["geometry"] == "SPHERICAL": #2d spherical
		if "ac_begin" not in vargs.keys() or "ac_end" not in vargs.keys():
			print("Warning: args: ac_begin and ac_end are needed")
			return Dataobj
		edge=integrate_sph_sur(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],rr=("min",),tr=(((vargs["ac_begin"],vargs["ac_end"]),),),surface=("r",))[0]
		jet=integrate_sph_sur(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],rr=("min",),tr=(((Dataobj.grid["x2"][0],vargs["ac_begin"]),(vargs["ac_end"],Dataobj.grid["x2"][-1])),),surface=("r",))[0]
		inj=integrate_sph_sur(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],rr=("max",),tr=(((vargs["ac_begin"],vargs["ac_end"]),),),surface=("-r",))[0]
		outflow=integrate_sph_sur(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],rr=("max",),tr=(((Dataobj.grid["x2"][0],vargs["ac_begin"]),(vargs["ac_end"],Dataobj.grid["x2"][-1])),),surface=("-r",))[0]
		thid1=get_closest_index(vargs["ac_begin"],Dataobj.grid["x2"])
		thid2=get_closest_index(vargs["ac_end"],Dataobj.grid["x2"])
		wind=sum(integrate_sph_sur(Dataobj.quantities["MassFlux_x2"][:,thid1:thid2],Dataobj.grid["x1"],Dataobj.grid["x2"][thid1:thid2],tr=("min","max"),surface=("th","-th")))
	elif Dataobj.quantities["geometry"] == "POLAR": #2d polar
		edge=integrate_pol_sur(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],rr=("min",),surface=("r",))[0]
		jet=0 # no jet in 2D polar
		inj=integrate_pol_sur(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],rr=("max",),surface=("-r",))[0]
		outflow=0#no out flow
		wind=0 #no wind
	else:
		if "ac_begin" not in vargs.keys() or "ac_end" not in vargs.keys():
			print("Warning: args: ac_begin and ac_end are needed")
			return Dataobj
		inner=Dataobj.grid["x1"][0]
		edge=integrate_surface(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],xr=("min",),yr=(((-inner,inner),),),surface=("x"))[0]
		j1index=get_closest_index(-inner,Dataobj.grid["x2"])
		j2index=get_closest_index(inner,Dataobj.grid["x2"])
		jet=integrate_surface(Dataobj.quantities["MassFlux_x2"][:,:j1index],Dataobj.grid["x1"],Dataobj.grid["x2"][:j1index],yr=("max",),xr=(((0,inner),),),surface=("-y"))[0]+integrate_surface(Dataobj.quantities["MassFlux_x2"][:,j2index:],Dataobj.grid["x1"],Dataobj.grid["x2"][j2index:],yr=("min",),xr=(((0,inner),),),surface=("y"))[0]
		wind=sum(integrate_surface(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"][:j1index],xr=("min",),yr=(((Dataobj.grid["x2"][0],-inner),(inner,Dataobj.grid["x2"][-1])),),surface=("x",)))+sum(integrate_surface(Dataobj.quantities["MassFlux_x2"],Dataobj.grid["x1"],Dataobj.grid["x2"],yr=("min","max"),surface=("y","-y")))
		inj=integrate_surface(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],xr=("max",),yr=(((vargs["ac_begin"],vargs["ac_end"]),),),surface=("-x"))[0]
		outflow=integrate_surface(Dataobj.quantities["MassFlux_x1"],Dataobj.grid["x1"],Dataobj.grid["x2"],xr=("max",),yr=(((Dataobj.grid["x2"][0],vargs["ac_begin"]),(vargs["ac_end"],Dataobj.grid["x2"][-1])),),surface=("-x",))[0]
	quantities={
		"MassFlux_edge":edge,
		"MassFlux_wind":wind,
		"MassFlux_inj":inj,
		"MassFlux_outflow":outflow,
		"MassFlux_jet":jet,
		"MassFlux_Toutflow":-(outflow+wind),
		"MassFlux_Accretion":-(edge+jet)
	}
	Dataobj.quantities.update(quantities)
	return Dataobj
def result(quantity_name=None,anafname=None):
	return ("MassFlux_edge","MassFlux_Toutflow") #this function will return result types shown in GUI
```

```shell
python shockfinder.py -n=AnalysisTool@BlackHoleMassFlux.py
```
