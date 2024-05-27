# File type: algroithm <Function> set
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

try:
    from ShockFinder.Addon.AnalysisTool.Basic import *
except:
    from Basic import *
import numpy as np


def GetMeanAxis(meanaxis=(1, 2)):
    return np.flip(np.sort(meanaxis))


def GetMeanRegion(Dataobj, meanaxis, vargs={}):  # True Value
    meanaxisregion = []
    for i in meanaxis:
        try:
            meanaxisregion.append(vargs["Mean_axis" + str(i)])
        except:
            try:
                meanaxisregion.append(Dataobj.quantities["Mean_axis" + str(i)])
            except:
                meanaxisregion.append(
                    [
                        Dataobj.grid["x" + str(i + 1)][0],
                        Dataobj.grid["x" + str(i + 1)][-1],
                    ]
                )
    return meanaxisregion


def GetMeanRegionIndex(Dataobj, meanaxis, meanaxisregion):
    index = []
    for i in range(len(meanaxis)):
        index.append(
            [
                np.where(
                    Dataobj.grid["x" + str(meanaxis[i] + 1)] >= meanaxisregion[i][0]
                )[0][0],
                np.where(
                    Dataobj.grid["x" + str(meanaxis[i] + 1)] <= meanaxisregion[i][1]
                )[0][-1]
                + 1,
            ]
        )
    return index


def GetMeanRadialIndex(Dataobj, meanaxis, radial):
    index = []
    for i in range(len(meanaxis)):
        if radial[i] == None:
            ind = len(Dataobj.grid["x" + str(meanaxis[i] + 1)]) / 2
            if int(ind) == ind:
                index.append([int(ind) - 1, int(ind) + 1])
            else:
                index.append([int(ind) + 1, int(ind) + 2])
        elif radial[i] >= min(Dataobj.grid["x" + str(meanaxis[i] + 1)]) and radial[
            i
        ] <= max(Dataobj.grid["x" + str(meanaxis[i] + 1)]):
            if radial[i] in Dataobj.grid["x" + str(meanaxis[i] + 1)]:
                ind = np.where(Dataobj.grid["x" + str(meanaxis[i] + 1)] == radial[i])[
                    0
                ][0]
                index.append([ind, ind + 1])
            else:
                index.append(
                    [
                        np.where(
                            np.where(
                                Dataobj.grid["x" + str(meanaxis[i] + 1)] <= radial[i]
                            )[0][-1],
                            Dataobj.grid["x" + str(meanaxis[i] + 1)] >= radial[i],
                        )[0][0]
                        + 1
                    ]
                )
        else:
            index.append([-1, -1])
    return index


def GetMean(quantity, meanaxis, meanindex):
    new_quantity = quantity
    try:  # 3d
        for i in range(len(meanaxis)):
            if meanaxis[i] == 0:
                new_quantity = new_quantity[meanindex[i][0] : meanindex[i][1], :, :]
            elif meanaxis[i] == 1:
                new_quantity = new_quantity[:, meanindex[i][0] : meanindex[i][1], :]
            elif meanaxis[i] == 2:
                new_quantity = new_quantity[:, :, meanindex[i][0] : meanindex[i][1]]
    except:  # 2d
        for i in range(len(meanaxis)):
            if meanaxis[i] == 0:
                new_quantity = new_quantity[meanindex[i][0] : meanindex[i][1], :]
            elif meanaxis[i] == 1:
                new_quantity = new_quantity[:, meanindex[i][0] : meanindex[i][1]]
    for i in meanaxis:
        new_quantity = np.mean(new_quantity, i)
    return new_quantity


def Mean(Dataobj, quantity_name, vargs={"Mean_axis": (1,)}):
    meanaxis = get_par(
        Dataobj, vargs, "Mean_axis", Dataobj.quantities[quantity_name].ndim - 1
    )
    if type(meanaxis) not in (list, tuple, np.ndarray):
        meanaxis = (meanaxis,)
    meanaxis = GetMeanAxis(meanaxis)
    meanregion = GetMeanRegion(Dataobj, meanaxis, vargs)
    meanindex = GetMeanRegionIndex(Dataobj, meanaxis, meanregion)
    return GetMean(Dataobj.quantities[quantity_name], meanaxis, meanindex)


def get(Dataobj, quantity_name, args={}, vargs={"Mean_axis": (1,)}):
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
    meanstr = ""
    meanaxis = get_par(
        Dataobj, vargs, "Mean_axis", Dataobj.quantities[quantity_name].ndim - 1
    )
    if type(meanaxis) not in (list, tuple, np.ndarray):
        meanaxis = (meanaxis,)
    # for i in meanaxis:
    # 	if "Mean_axis"+str(i) in vargs.keys():
    # 		meanstr+=str(i)+"@"+str((round(vargs["Mean_axis"+str(i)][0],2),round(vargs["Mean_axis"+str(i)][1],2)))+"_"
    # 	elif "Mean_axis"+str(i) in Dataobj.quantities.keys():
    # 		meanstr+=str(i)+"@"+str((round(Dataobj.quantities["Mean_axis"+str(i)][0],2),round(Dataobj.quantities["Mean_axis"+str(i)][1],2)))+"_"
    quantities = {
        "Mean_" + meanstr + quantity_name: Mean(Dataobj, quantity_name, vargs)
    }
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ["Mean_" + i for i in quantity_name.split(",")]


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData

    TestData = get(TestData, "rho")
    print("Testing Result:", TestData.quantities["Mean_rho"])  # update
