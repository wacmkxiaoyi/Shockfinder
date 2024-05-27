# File BlackHoleMassFlux
# Only for 2D data, support SPHERICAL, POLAR, XOY
# 	edge: fall into black hole, match accretion rate.
# 		plus : escape from black hole, minor: fall into black hole
# 	inj: injet flow
# 		plus : accreted into system, minor: escape from system
# 	wind: wind
# 		plus: back to system, minor: escape from system
# 	outflow:
# 		plus: back to system, minor: escape from system
#   jet:
# 		plus: escape from bh,....
# in each case, positive flux means material go to accretion region
# ac_begin and ac_end are size of accretion region (Escapt Polar coordinate)

try:
    from ShockFinder.Addon.AnalysisTool.Basic import *
    import ShockFinder.Addon.AnalysisTool.Differential as Differential

    # if AvgTh_CAL is True
    # import ShockFinder.Addon.AnalysisTool.Mean as Mean
    # import ShockFinder.Addon.AnalysisTool.<packages name> as <packages name>
except Exception as err:
    print(err)
    from Basic import *
    import Differential

    # import Mean #debug
    # import <packages name>

need = []
# args will be inserted into Data Object
# vargs will not be inserted into Data Object
import numpy as np, math, copy


def get(Dataobj, quantity_name, args={}, vargs={}):
    # quantity_name=rho,Velocity [default]
    if type(quantity_name) == type(None):
        quantity_name = ("BVF_rho_prs", "Velocity")
    newqt = [quantity_name[i : i + 2] for i in range(0, len(quantity_name), 2)]
    if len(newqt) > 1:
        for i in newqt:
            Dataobj = get(Dataobj, i, args, vargs)
        return Dataobj
    bvf, velo = newqt[0]
    Dataobj.quantities.update(args)
    need = [bvf, "Gradient_" + velo + "_x1"]
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed")
            return Dataobj
    fix_qt = copy.deepcopy(Dataobj.quantities["Gradient_" + velo + "_x1"])
    fix_qt[np.where(fix_qt == 0)] = np.min(np.abs(fix_qt)) * get_par(
        Dataobj, vargs, "Minfix", 0.01
    )
    quantities = {
        "KHI_"
        + bvf
        + "_"
        + velo: (
            Dataobj.quantities[bvf] / fix_qt**2
            if not np.all(fix_qt == 0)
            else np.full(fix_qt.shape, 0.0)
        )
    }
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    if quantity_name == "":
        quantity_name = "BVF_rho_prs,Velocity"
    sstr = quantity_name.split(",")
    return [
        "KHI_" + sstr[i] + "_" + sstr[i + 1] for i in range(0, len(sstr), 2)
    ]  # this function will return result types shown in GUI


if __name__ == "__main__":
    pass
