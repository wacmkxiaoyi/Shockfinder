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