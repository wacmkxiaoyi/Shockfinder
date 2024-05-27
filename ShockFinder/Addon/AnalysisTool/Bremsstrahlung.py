# File type: <Function> return a new <Object: Data>
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:

try:
    import ShockFinder.Addon.AnalysisTool.Mean as Mean
    import ShockFinder.Addon.AnalysisTool.Differential as Differential
    from ShockFinder.Addon.AnalysisTool.Basic import *
except:
    import Mean  # debug
    import Differential
    from Basic import *
import numpy as np

need = ["rho", "geometry", "Temperature", "c", "mp", "gamma"]


def get(Dataobj, args={}, vargs={}):
    Dataobj.quantities.update(args)
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    quantities = {
        "Bremsstrahlung": Dataobj.quantities["rho"] ** 2
        * Dataobj.quantities["Temperature"] ** 0.5
        * 2
        * np.pi
        * 1.4e-27
        / Dataobj.quantities["mp"] ** 2
    }
    Dataobj.quantities.update(quantities)
    if Dataobj.quantities["geometry"] in ("SPHERICAL", "POLAR"):
        if Dataobj.quantities["geometry"] == "SPHERICAL":
            intfun = Differential.integrate_sph_body
        else:
            intfun = Differential.integrate_pol_body
    else:
        intfun = Differential.integrate_body
    INTRMAX = None
    if "INTRMAX" in args.keys():
        INTRMAX = args["INTRMAX"].split("$")[1]
    elif "INTRMAX" in vargs.keys():
        INTRMAX = vargs["INTRMAX"].split("$")[1]
    if INTRMAX == None:
        INTRMAX = Dataobj.grid["x1"]
        nc = Dataobj.quantities["Bremsstrahlung"]
    else:
        try:
            try:
                Index = Mean.GetMeanRegionIndex(
                    Dataobj, (0,), ((0, Dataobj.quantities[INTRMAX]),)
                )[0][1]
            except:
                Index = Mean.GetMeanRegionIndex(
                    Dataobj, (0,), ((0, Dataobj.grid[INTRMAX]),)
                )[0][1]
            nc = Dataobj.quantities["Bremsstrahlung"][:Index]
            INTRMAX = Dataobj.grid["x1"][:Index]
        except:
            print("Warning:", INTRMAX, "decode error")
            INTRMAX = Dataobj.grid["x1"]
            nc = Dataobj.quantities["Bremsstrahlung"]
    if Dataobj.quantities["Bremsstrahlung"].ndim == 3:  # 3d
        quantities = {
            "Total_Bremsstrahlung": intfun(
                nc, INTRMAX, Dataobj.grid["x2"], Dataobj.grid["x3"]
            )
        }
    elif Dataobj.quantities["Bremsstrahlung"].ndim == 2:  # 2d
        quantities = {"Total_Bremsstrahlung": intfun(nc, INTRMAX, Dataobj.grid["x2"])}
    elif Dataobj.quantities["Bremsstrahlung"].ndim == 1:  # 1d
        quantities = {"Total_Bremsstrahlung": intfun(nc, INTRMAX)}
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ("Bremsstrahlung", "Total_Bremsstrahlung")


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData
    import Temperature

    TestData = Temperature.get(TestData)
    TestData = get(TestData)
    print("Testing Result:", TestData.quantities["Bremsstrahlung"])
    print(
        Differential.integrate_sph_body(
            TestData.quantities["Bremsstrahlung"],
            TestData.grid["x1"],
            TestData.grid["x2"],
        )
    )
