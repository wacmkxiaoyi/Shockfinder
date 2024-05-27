# File type: <Function> return dict
# By Junxiang H., 2023/07/02
# wacmk.com/cn Tech. Supp.

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:


try:
    from ShockFinder.Addon.AnalysisTool.Basic import *
    import ShockFinder.Addon.AnalysisTool.Differential as Differential

    # if AvgTh_CAL is True
    # import ShockFinder.Addon.AnalysisTool.Mean
    # import ShockFinder.Addon.AnalysisTool.<packages name>
except:
    from Basic import *
    import Differential

    # import Mean #debug
    # import <packages name>
import numpy as np
from scipy.optimize import fsolve
import math

# rs gravitational type: rs=1 2GM/c**2, rs=2 GM/c**2
# args will be inserted into Data Object
# vargs will not be inserted into Data Object
c = 3.0e10
mu = 0.5
k = 1.380649e-16
mp = 1.6726231e-24
G = 6.67430e-8
Msun = 1.989e33
et = 6.7e-29


def Equilibrium(rb, lam, mach, gamma=4 / 3, rs=1, eng=0, theta_inj=0, steps=10000):
    def cal_vR(sintheta):
        return (
            (2 * mach**2 * (gamma - 1) / (mach**2 * (gamma - 1) * sintheta**2 + 2))
            * (
                eng
                + rs / (2 * (rb - rs))
                - lam**2 * math.cos(theta_inj) ** 2 / 2 / rb**2 / sintheta**2
            )
        ) ** 0.5

    def cal_theta(i):
        sintheta = i[0]
        return (
            rb**2 * (1 - sintheta**2)
            - 2
            * rb
            * sintheta
            * (rb * sintheta - rs) ** 2
            / rs**2
            * cal_vR(sintheta) ** 2
            / mach**2
            * gamma
        )

    quantities = {}
    quantities["Accretion_x2_beg"] = math.asin(fsolve(cal_theta, [1])[0])
    quantities["Accretion_x2_end"] = math.pi - quantities["Accretion_x2_beg"]
    psc = np.array(
        [
            cal_vR(math.sin(i))
            for i in np.arange(
                quantities["Accretion_x2_beg"],
                quantities["Accretion_x2_end"],
                (quantities["Accretion_x2_end"] - quantities["Accretion_x2_beg"])
                / steps,
            )
        ]
    )
    quantities["Accretion_vR"] = np.array([psc for i in range(steps)])
    quantities["Accretion_InjFlux"] = Differential.integrate_sph_sur(
        quantities["Accretion_vR"],
        np.arange(0, rb, rb / steps),
        th=np.arange(
            quantities["Accretion_x2_beg"],
            quantities["Accretion_x2_end"],
            (quantities["Accretion_x2_end"] - quantities["Accretion_x2_beg"]) / steps,
        ),
        rr=("max",),
        surface=("r",),
    )[0]
    quantities["Accretion_Min_Tem"] = (
        cal_vR(math.sin(math.pi / 2)) ** 2 * c**2 * mu * mp / mach**2 / gamma / k
    )
    quantities["rs"] = rs
    return quantities


def SphericalGrid(rbeg, rend, tbeg, tend, rgnum):
    def cal_detr(i):
        detr = i[0]
        return [
            detr / rbeg
            - 2
            * ((rend / (rbeg + detr)) ** (1 / (rgnum - 1)) - 1)
            / ((rend / (rbeg + detr)) ** (1 / (rgnum - 1)) + 1)
        ]

    def cal_ptr(detr, detphi):
        return abs(
            math.log(rend / (rbeg + detr), 10)
            - rgnum * math.log((2 + detphi) / (2 - detphi), 10)
        )

    detr = fsolve(cal_detr, [0.02])[0]
    detphi = detr / rbeg
    div = (tend - tbeg) / detphi
    result = 0
    if div != int(div):
        div_a = int(div)
        detphi_a = (tend - tbeg) / div_a
        detr_a = rbeg * detphi_a
        div_b = int(div) + 1
        detphi_b = (tend - tbeg) / div_b
        detr_b = rbeg * detphi_b
        if cal_ptr(detr_a, detphi_a) > cal_ptr(detr_b, detphi_b):
            result = (detr_b, div_b)
        else:
            result = (detr_a, div_a)
    else:
        result = (detr, div)
    quantities = {
        "r_beg": rbeg,
        "r1": result[0],
        "r_end": rend,
        "r_grid_num": rgnum,
        "th_beg": tbeg,
        "th_end": tend,
        "th_grid_num": result[1],
        "grid_error": cal_ptr(result[0], (tend - tbeg) / result[1]),
    }
    return quantities


def Unit(
    mass, injflux, injrho, hequantities, basic_m=Msun, basic_r=2 * G / c**2, basic_v=c
):
    quantities = {}
    quantities["unit_r"] = mass * basic_r * basic_m / hequantities["rs"]
    quantities["unit_t"] = quantities["unit_r"] / basic_v
    quantities["unit_rho"] = (
        injflux
        / injrho
        / hequantities["Accretion_InjFlux"]
        / quantities["unit_r"] ** 2
        / basic_v
    )
    # quantities["unit_rho"]*=0.001 #to g/cm**3
    # quantities["unit_r"]*=100 #to cm
    return quantities


def EdditionMassFlux_to_MassFlux(massflux, rb, unit_r):  # to g/s
    return massflux * rb * unit_r * mp * c / et


def YearMassFlux_to_MassFlux(massflux, basic_m=Msun):
    return massflux * Msun / 86400 / 365


if __name__ == "__main__":
    print("Testing Model:", __file__)
    # from TestData import TestData
    # TestData=get(TestData)
    # print("Testing Result:", TestData.quantities[<quantity name>]) #update here!
    eq = Equilibrium(200, 1.75, 5)
    print(eq)
    print(SphericalGrid(2, 200, 0.1 * math.pi, 0.9 * math.pi, 512))
    print(Unit(10, YearMassFlux_to_MassFlux(1e-11), 1, eq))
