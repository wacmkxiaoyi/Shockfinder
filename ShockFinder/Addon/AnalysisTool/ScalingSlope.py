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
    if type(quantity_name) in (np.ndarray, list, tuple):
        for i in quantity_name:
            Dataobj = get(Dataobj, i, args, vargs)
        return Dataobj
    Dataobj.quantities.update(args)
    axis = get_par(Dataobj, vargs, "Axis", "x1")
    need = [quantity_name, "Gradient_" + quantity_name + "_" + axis]
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed")
            return Dataobj
    fix_qt = copy.deepcopy(Dataobj.quantities[quantity_name])
    fix_qt[np.where(fix_qt == 0)] = np.min(np.abs(fix_qt)) * get_par(
        Dataobj, vargs, "Minfix", 0.01
    )
    quantities = {
        "ScalingSlope_"
        + quantity_name: (
            Dataobj.grid[axis].reshape(
                *[
                    (
                        Dataobj.quantities[quantity_name].shape[i]
                        if i == (0 if axis == "x1" else 1 if axis == "x2" else 2)
                        else 1
                    )
                    for i in range(Dataobj.quantities[quantity_name].ndim)
                ]
            )
            / fix_qt
            * Dataobj.quantities["Gradient_" + quantity_name + "_" + axis]
            if not np.all(fix_qt == 0)
            else np.full(fix_qt.shape, 0.0)
        )
    }
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return [
        "ScalingSlope_" + i for i in quantity_name.split(",")
    ]  # this function will return result types shown in GUI


if __name__ == "__main__":
    pass
