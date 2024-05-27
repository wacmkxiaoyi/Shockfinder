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
    # quantity_name=rho,prs len=2
    if type(quantity_name) == type(None):
        quantity_name = ("rho", "prs")
    newqt = [quantity_name[i : i + 2] for i in range(0, len(quantity_name), 2)]
    if len(newqt) > 1:
        for i in newqt:
            Dataobj = get(Dataobj, i, args, vargs)
        return Dataobj
    rho, prs = newqt[0]
    Dataobj.quantities.update(args)
    need = ["gamma", rho, "Gradient_" + rho + "_x1", prs, "Gradient_" + prs + "_x1"]
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed")
            return Dataobj
    fix_prs = copy.deepcopy(Dataobj.quantities[prs])
    fix_prs[np.where(fix_prs == 0)] = np.min(np.abs(fix_prs)) * get_par(
        Dataobj, vargs, "Minfix", 0.01
    )
    fix_rho = copy.deepcopy(Dataobj.quantities[rho])
    fix_rho[np.where(fix_rho == 0)] = np.min(np.abs(fix_rho)) * get_par(
        Dataobj, vargs, "Minfix", 0.01
    )
    quantities = {
        "BVF_"
        + rho
        + "_"
        + prs: (
            -1
            / fix_rho
            * Dataobj.quantities["Gradient_" + prs + "_x1"]
            * (
                1
                / Dataobj.quantities["gamma"]
                / fix_prs
                * Dataobj.quantities["Gradient_" + prs + "_x1"]
                - 1 / fix_rho * Dataobj.quantities["Gradient_" + rho + "_x1"]
            )
            if not np.all(fix_rho == 0) and not np.all(fix_prs == 0)
            else np.full(fix_prs.shape, 0.0)
        )
    }

    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    if quantity_name == "":
        quantity_name = "rho,prs"
    sstr = quantity_name.split(",")
    return [
        "BVF_" + sstr[i] + "_" + sstr[i + 1] for i in range(0, len(sstr), 2)
    ]  # this function will return result types shown in GUI


if __name__ == "__main__":
    pass
