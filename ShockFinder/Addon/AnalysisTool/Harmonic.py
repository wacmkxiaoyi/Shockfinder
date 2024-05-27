# File type: <Function> return a new <Object: Data>
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

# Spherical Only!!!!
# Support 2D (xoz plane only), 3D

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:
try:
    from ShockFinder.Addon.AnalysisTool.Basic import *
except:
    from Basic import *
from scipy.special import lpmv
import numpy as np
import math

need = []


# args will be inserted into Data Object
# vargs will not be inserted into Data Object
def cal_true_angle_th(angle, angle_begin, angle_end):
    return (angle - angle_begin) / (angle_end - angle_begin) * math.pi


def cal_true_angle_phi(angle, angle_begin, angle_end):
    return 2 * cal_true_angle_th(angle, angle_begin, angle_end)


def get(
    Dataobj, quantity_name, args={}, vargs={"Harmonic_Max_l": 3, "Harmonic_Max_m": 3}
):
    if type(quantity_name) in (np.ndarray, list, tuple):
        for i in quantity_name:
            Dataobj = get(Dataobj, i, args, vargs)
        return Dataobj
    Dataobj.quantities.update(args)
    for i in need + [quantity_name]:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    hm_lmax = get_par(Dataobj, vargs, "Harmonic_Max_l", 3)
    hm_mmax = get_par(Dataobj, vargs, "Harmonic_Max_m", 3)
    if Dataobj.quantities[quantity_name].ndim >= 2:
        angle_begin_th = get_par(Dataobj, vargs, "Harmonic_Th_beg")
        angle_begin_th = (
            angle_begin_th if angle_begin_th != None else Dataobj.grid["x2"][0]
        )
        angle_end_th = get_par(Dataobj, vargs, "Harmonic_Th_end")
        angle_end_th = angle_end_th if angle_end_th != None else Dataobj.grid["x2"][-1]
    else:
        print("Warning: Harmonic analysis only supports 2D (xoz plane) or 3D")
        return Dataobj
    if Dataobj.quantities[quantity_name].ndim == 3:
        angle_begin_phi = get_par(Dataobj, vargs, "Harmonic_Phi_beg")
        angle_begin_phi = (
            angle_begin_phi if angle_begin_phi != None else Dataobj.grid["x3"][0]
        )
        angle_end_phi = get_par(Dataobj, vargs, "Harmonic_Phi_end")
        angle_end_phi = (
            angle_end_phi if angle_end_phi != None else Dataobj.grid["x3"][-1]
        )
    quantities = {}
    trueangle = cal_true_angle_th(Dataobj.grid["x2"], angle_begin_th, angle_end_th)
    trueangle = trueangle.reshape((1, len(trueangle)))
    if Dataobj.quantities[quantity_name].ndim == 3:
        trueangle = trueangle.reshape((1, len(trueangle), 1))
        trueanglephi = cal_true_angle_phi(
            Dataobj.grid["x3"], angle_begin_phi, angle_end_phi
        )
        trueanglephi = trueanglephi.reshape((1, 1, len(trueanglephi)))
    for l in range(hm_lmax + 1):
        if Dataobj.quantities[quantity_name].ndim == 2:  # 2d
            quantities["Harmonic_l@" + str(l) + "_" + quantity_name] = (
                (l + 1)
                * Dataobj.quantities[quantity_name]
                * lpmv(0, l, np.cos(trueangle))
            )
        elif Dataobj.quantities[quantity_name].ndim == 3:  # 3d
            for m in range(max(-hm_mmax, -l), min(hm_mmax + 1, l + 1)):
                ct = (
                    (2 * l + 1)
                    * math.factorial(l - abs(m))
                    / (4 * math.pi * math.factorial(l + abs(m)))
                )
                quantities[
                    "Harmonic_l@" + str(l) + "_m@" + str(m) + "_" + quantity_name
                ] = (
                    Dataobj.quantities[quantity_name]
                    * math.e ** (m * trueanglephi * 1j)
                    * ct
                    * lpmv(m, l, np.cos(trueangle))
                )
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ["Harmonic_l@?_" + i for i in quantity_name.split(",")] + [
        "Harmonic_l@?_m@?_" + i for i in quantity_name.split(",")
    ]


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData

    TestData = get(TestData, "rho")
    print("Testing Result:", TestData.quantities["Harmonic_l@3_rho"])
