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
import copy
import numpy as np

need = ["vx1"]


def get(Dataobj, args={}, vargs={}):
    Dataobj.quantities.update(args)
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    u = 0
    for i in ("vx1", "vx2", "vx3"):
        try:
            u += Dataobj.quantities[i] ** 2
        except:
            pass
    quantities = {"Velocity": u**0.5}
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ("Velocity",)


if __name__ == "__main__":
    pass
