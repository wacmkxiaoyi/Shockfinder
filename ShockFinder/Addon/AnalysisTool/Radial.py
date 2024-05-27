# This is a model file for the Loader Addon
# It will be created when creating a new Loader
# Note!!!!: places which marke "<>" have to be updated, and delete "<>".

# File type: <Function> return a new <Object: Data>
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:

try:
    # if AvgTh_CAL is True
    import ShockFinder.Addon.AnalysisTool.Mean as Mean
    from ShockFinder.Addon.AnalysisTool.Basic import *
except:
    import Mean  # debug
    from Basic import *

import numpy as np

need = []


# args will be inserted into Data Object
# vargs will not be inserted into Data Object
def get(
    Dataobj,
    quantity_name,
    args={},
    vargs={"Radial_axis": (1,), "Radial_value": (None,)},
):
    if type(quantity_name) in (np.ndarray, list, tuple):
        for i in quantity_name:
            Dataobj = get(Dataobj, i, args, vargs)
        return Dataobj
    need = [quantity_name]
    Dataobj.quantities.update(args)
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    radialaxis = get_par(
        Dataobj, vargs, "Radial_axis", Dataobj.quantities[quantity_name].ndim - 1
    )
    if type(radialaxis) not in (list, tuple, np.ndarray):
        radialaxis = (radialaxis,)
    radialvalue = get_par(Dataobj, vargs, "Radial_value")
    if type(radialvalue) not in (list, tuple, np.ndarray):
        radialvalue = (radialvalue,)
    radialaxis = Mean.GetMeanAxis(radialaxis)
    radialindex = Mean.GetMeanRadialIndex(Dataobj, radialaxis, radialvalue)

    radial_str = ""
    # for i in range(len(radialaxis)):
    # 	if radialvalue[i]!=None:
    # 		radial_str+=str(radialaxis[i])+"@"+str(round(radialvalue[i],2))+"_"
    quantities = {
        "Radial_"
        + radial_str
        + quantity_name: Mean.GetMean(
            Dataobj.quantities[quantity_name], radialaxis, radialindex
        )
    }
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ["Radial_" + i for i in quantity_name.split(",")]


def get_boundary(Dataobj, quantity_name):
    if Dataobj.quantities[quantity_name].ndim == 3:  # 3d
        x1 = (
            Dataobj.quantities[quantity_name][:1, :, :],
            Dataobj.quantities[quantity_name][-1:, :, :],
        )
        x2 = (
            Dataobj.quantities[quantity_name][:, :1, :],
            Dataobj.quantities[quantity_name][:, -1:, :],
        )
        x3 = (
            Dataobj.quantities[quantity_name][:, :, :1],
            Dataobj.quantities[quantity_name][:, :, -1:],
        )
        return (x1, x2, x3)
    elif Dataobj.quantities[quantity_name].ndim == 2:  # 2d
        x1 = (
            Dataobj.quantities[quantity_name][:1, :],
            Dataobj.quantities[quantity_name][-1:, :],
        )
        x2 = (
            Dataobj.quantities[quantity_name][:, :1],
            Dataobj.quantities[quantity_name][:, -1:],
        )
        return (x1, x2)
    else:  # 1d
        x1 = (
            Dataobj.quantities[quantity_name][0],
            Dataobj.quantities[quantity_name][-1],
        )
        return (x1,)


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData

    TestData = get(TestData, "rho")
    print("Testing Result:", TestData.quantities["Radial_rho"])  # update
