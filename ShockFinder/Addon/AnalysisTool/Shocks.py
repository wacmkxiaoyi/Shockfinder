# File type: <Function> return a new <Object: Data>
# By Junxiang H., 2023/07/02
# wacmk.com/cn Tech. Supp.

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:

try:
    from ShockFinder.Addon.AnalysisTool.Basic import *
    import ShockFinder.Addon.AnalysisTool.Mean as Mean

    # import ShockFinder.Addon.AnalysisTool.<packages name>
except:
    from Basic import *
    import Mean  # debug

    # import <packages name>
import copy
import numpy as np

need = []


# args will be inserted into Data Object
# vargs will not be inserted into Data Object
# ShockDeduct, Shock_x1, Shock_x2, Shock_x3
def get(Dataobj, quantity_name, args={}, vargs={"ShockDeduct": 0.1}):
    if type(quantity_name) in (np.ndarray, list, tuple):
        for i in quantity_name:
            Dataobj = get(Dataobj, i, args, vargs)
        return Dataobj
    Dataobj.quantities.update(args)
    newneed = copy.deepcopy(need)
    newneed += ["Divergence_" + quantity_name]
    for i in newneed:
        if (
            i not in Dataobj.quantities.keys()
            and i not in vargs.keys()
            and "KHI" not in i
        ):  # KHI mode
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    quantities = {}
    if "KHI" in quantity_name:
        div = copy.deepcopy(Dataobj.quantities[quantity_name])
    else:
        div = copy.deepcopy(Dataobj.quantities["Divergence_" + quantity_name])
    shockx1 = get_par(Dataobj, vargs, "Shock_bou_x1")
    if shockx1 == None:
        shockx1 = [Dataobj.grid["x1"][0], Dataobj.grid["x1"][-1]]
    shockx1ind = Mean.GetMeanRegionIndex(Dataobj, (0,), (shockx1,))[0]
    quantities["Shock_x1"] = Dataobj.grid["x1"][shockx1ind[0] : shockx1ind[1]]
    if Dataobj.quantities[quantity_name].ndim >= 2:
        shockx2 = get_par(Dataobj, vargs, "Shock_bou_x2")
        if shockx2 == None:
            shockx2 = [Dataobj.grid["x2"][0], Dataobj.grid["x2"][-1]]
        shockx2ind = Mean.GetMeanRegionIndex(Dataobj, (1,), (shockx2,))[0]
        quantities["Shock_x2"] = Dataobj.grid["x2"][shockx2ind[0] : shockx2ind[1]]
        if Dataobj.quantities[quantity_name].ndim == 3:
            shockx3 = get_par(Dataobj, vargs, "Shock_bou_x3")
            if shockx3 == None:
                shockx3 = [Dataobj.grid["x3"][0], Dataobj.grid["x3"][-1]]
            shockx3ind = Mean.GetMeanRegionIndex(Dataobj, (2,), (shockx3,))[0]
            quantities["Shock_x3"] = Dataobj.grid["x3"][shockx3ind[0] : shockx3ind[1]]
            div = div[
                shockx1ind[0] : shockx1ind[1],
                shockx2ind[0] : shockx2ind[1],
                shockx3ind[0] : shockx3ind[1],
            ]
        else:
            div = div[shockx1ind[0] : shockx1ind[1], shockx2ind[0] : shockx2ind[1]]
    else:
        div = div[shockx1ind[0] : shockx1ind[1]]
    sdu = get_par(Dataobj, vargs, "ShockDeduct", 0.1)
    sign = get_par(Dataobj, vargs, "Shockway", "Negative")
    if sign != "Negative" or "KHI" in quantity_name:
        div -= np.max(div) * sdu
        div[np.where(div < 0)] = 0.0
    else:
        div -= np.min(div) * sdu
        div[np.where(div > 0)] = 0.0
        div = -div
    quantities["Shock_" + quantity_name] = div
    if quantities["Shock_" + quantity_name].ndim == 1:  # 1d
        # 1d data support peak center mode

        def get_peak_center(array):
            peaks = []
            pb = -1
            pe = -1
            pmax = 0
            pmaxind = -1
            for i in range(len(array)):
                if array[i] == 0:
                    if pe != -1:  # useful check point
                        peaks.append(pmaxind)
                        pe = -1  # mark last check point is over
                    pb = i  # reset check point
                    pmax = 0
                elif pb != -1:  # if not begin:
                    pe = i
                    if array[i] > pmax:
                        pmax = array[i]
                        pmaxind = i
            return peaks

        pc = get_peak_center(div)
        quantities["Shock_" + quantity_name] = np.array(
            [div[i] if i in pc else 0 for i in range(len(div))]
        )
        quantities["Shock_Outermost_x1_" + quantity_name] = (
            0
            if len(np.where(quantities["Shock_" + quantity_name] != 0)[0]) == 0
            else quantities["Shock_x1"][
                np.where(quantities["Shock_" + quantity_name] != 0)[0][-1]
            ]
        )
    elif quantities["Shock_" + quantity_name].ndim == 2:  # 2d
        quantities["Shock_Outermost_x1_" + quantity_name] = np.array(
            [
                (
                    0
                    if len(np.where(i != 0)[0]) == 0
                    else quantities["Shock_x1"][np.where(i != 0)[0][-1]]
                )
                for i in quantities["Shock_" + quantity_name].T
            ]
        )  # default
        quantities["Shock_Outermost_x2_" + quantity_name] = np.array(
            [
                (
                    0
                    if len(np.where(i != 0)[0]) == 0
                    else quantities["Shock_x2"][np.where(i != 0)[0][-1]]
                )
                for i in quantities["Shock_" + quantity_name]
            ]
        )
    elif quantities["Shock_" + quantity_name].ndim == 3:
        quantities["Shock_Outermost_x1_" + quantity_name] = np.array(
            [
                np.array(
                    [
                        (
                            0
                            if len(np.where(j != 0)[0]) == 0
                            else quantities["Shock_x1"][np.where(j != 0)[0][-1]]
                        )
                        for j in i.T
                    ]
                )
                for i in quantities["Shock_" + quantity_name].T
            ]
        )
        quantities["Shock_Outermost_x2_" + quantity_name] = np.array(
            [
                np.array(
                    [
                        (
                            0
                            if len(np.where(j != 0)[0]) == 0
                            else quantities["Shock_x2"][np.where(j != 0)[0][-1]]
                        )
                        for j in i.T
                    ]
                )
                for i in quantities["Shock_" + quantity_name]
            ]
        )
        quantities["Shock_Outermost_x3_" + quantity_name] = np.array(
            [
                np.array(
                    [
                        (
                            0
                            if len(np.where(j != 0)[0]) == 0
                            else quantities["Shock_x3"][np.where(j != 0)[0][-1]]
                        )
                        for j in i
                    ]
                )
                for i in quantities["Shock_" + quantity_name]
            ]
        )

    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ["Shock_" + i for i in quantity_name.split(",")] + [
        "Shock_Outermost_x1_" + i for i in quantity_name.split(",")
    ]


# if AvgTh mode is needed, please set AvgTh_cal=True
# The below code can be ignored, if set to False
AvgTh_cal = False


def get_AvgTh(Dataobj, args={}, vargs={"Mean_axis": (1,)}):
    try:
        if AvgTh_cal:
            newneed = copy.deepcopy(need)
            if "Mean_axis" not in newneed:
                newneed.append("Mean_axis")
            Dataobj.quantities.update(args)
            for i in newneed:
                if i not in Dataobj.quantities.keys() and i not in vargs.keys():
                    print("Warning: args:", i, "is needed without definding")
                    return Dataobj
            meanstr = ""
            try:
                meanaxis = vargs["Mean_axis"]
            except:
                meanaxis = Dataobj.quantities["Mean_axis"]
            for i in meanaxis:
                if "Mean_axis" + str(i) in vargs.keys():
                    meanstr += (
                        str(i)
                        + "@"
                        + str(
                            (
                                round(vargs["Mean_axis" + str(i)][0], 2),
                                round(vargs["Mean_axis" + str(i)][1], 2),
                            )
                        )
                        + "_"
                    )
                elif "Mean_axis" + str(i) in Dataobj.quantities.keys():
                    meanstr += (
                        str(i)
                        + "@"
                        + str(
                            (
                                round(Dataobj.quantities["Mean_axis" + str(i)][0], 2),
                                round(Dataobj.quantities["Mean_axis" + str(i)][1], 2),
                            )
                        )
                        + "_"
                    )
            quantities = {"AvgTh_" + meanstr + "<quantity name>": ...}  # update here
            Dataobj.quantities.update(quantities)
        else:
            print("Warning: AvgTh mode is not opened: <quantity name>")  # update here
    except:
        print("Warning: AvgTh mode is not definded:", __file__)  # update here
    return Dataobj


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData
    import Differential, math

    TestData = Differential.divergence(TestData, "rho")
    TestData = get(
        TestData,
        "rho",
        vargs={
            "ShockDeduct": 0.1,
            "Shock_bou_x1": (2, 9),
            "Shock_bou_x2": (0.1 * np.pi, 0.9 * np.pi),
        },
    )
    print("Testing Result:", TestData.quantities["Shock_rho"])  # update here!
    from matplotlib import pyplot as plt

    plt.figure("imshow", facecolor="lightgray")
    plt.imshow(
        TestData.quantities["Shock_rho"],
        cmap="RdBu",
        extent=[
            TestData.quantities["Shock_x1"][0],
            TestData.quantities["Shock_x1"][-1],
            TestData.quantities["Shock_x2"][0],
            TestData.quantities["Shock_x2"][-1],
        ],
    )
    plt.colorbar()
    plt.xticks(TestData.quantities["Shock_x1"])
    plt.yticks(TestData.quantities["Shock_x2"])
    plt.show()
    if AvgTh_cal:
        TestData = get_AvgTh(TestData)
        print(
            "Testing Result:", TestData.quantities["AvgTh_<quantity name>"]
        )  # update here!
