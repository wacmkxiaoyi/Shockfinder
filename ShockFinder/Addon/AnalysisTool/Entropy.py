# File type: <Function> return a new <Object: Data>
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:

try:
    import ShockFinder.Addon.AnalysisTool.Mean as Mean
    from ShockFinder.Addon.AnalysisTool.Basic import *
except:
    import Mean  # debug
    from Basic import *
import numpy as np
import copy

need = ["rho", "prs", "gamma"]


def get(Dataobj, args={}, vargs={}):
    Dataobj.quantities.update(args)
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    quantities = {
        "Entropy": Dataobj.quantities["prs"]
        / Dataobj.quantities["rho"] ** Dataobj.quantities["gamma"]
    }
    Dataobj.quantities.update(quantities)
    if "AvgTh" in vargs.keys() and vargs["AvgTh"] == True:
        Dataobj = get_AvgTh(Dataobj, args, vargs)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ("Entropy", "AvgTh_Entropy")


AvgTh_cal = True


def get_AvgTh(Dataobj, args={}, vargs={"Mean_axis": (1,)}):
    try:
        if AvgTh_cal:
            newneed = copy.deepcopy(need)
            Dataobj.quantities.update(args)
            for i in newneed:
                if i not in Dataobj.quantities.keys() and i not in vargs.keys():
                    print("Warning: args:", i, "is needed without definding")
                    return Dataobj
            meanstr = ""
            meanaxis = get_par(
                Dataobj, vargs, "Mean_axis", Dataobj.quantities["rho"].ndim - 1
            )
            if type(meanaxis) not in (list, tuple, np.ndarray):
                meanaxis = (meanaxis,)
            # for i in meanaxis:
            # 	meanstr+=str(i)+"@"+str((round(vargs["Mean_axis"+str(i)][0],2),round(vargs["Mean_axis"+str(i)][1],2)))+"_" if "Mean_axis"+str(i) in vargs.keys() else str(i)+"@"+str((round(Dataobj.quantities["Mean_axis"+str(i)][0],2),round(Dataobj.quantities["Mean_axis"+str(i)][1],2)))+"_" if "Mean_axis"+str(i) in Dataobj.quantities.keys() else ""
            quantities = {
                "AvgTh_"
                + meanstr
                + "Entropy": Mean.Mean(Dataobj, "prs", vargs)
                / Mean.Mean(Dataobj, "rho", vargs) ** Dataobj.quantities["gamma"]
            }  # update here
            Dataobj.quantities.update(quantities)
        else:
            print("Warning: AvgTh mode is not opened:", "Entropy")  # update here
    except:
        print("Warning: AvgTh mode is not definded or error:", __file__)  # update here
    return Dataobj


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData

    TestData = get(TestData)
    print("Testing Result:", TestData.quantities["Entropy"])
    if AvgTh_cal:
        TestData = get_AvgTh(TestData)
        print("Testing Result:", TestData.quantities["AvgTh_Entropy"])
