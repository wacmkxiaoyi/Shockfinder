# File type: <Function> return a new <Object: Data>
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

# if you would like to import some packages,
# during the data loading.
# Please put that packages into this folder and using:

need = ["vx1", "vx2", "vx3", "rho"]
import numpy as np


# args will be inserted into Data Object
# vargs will not be inserted into Data Object
def get(Dataobj, args={}, vargs={}):
    Dataobj.quantities.update(args)
    for i in need:
        if i not in Dataobj.quantities.keys() and i not in vargs.keys():
            print("Warning: args:", i, "is needed without definding")
            return Dataobj
    quantities = {
        # operation with dict args
        # ...
    }
    for i in range(Dataobj.quantities["rho"].ndim):
        quantities["MassFlux_x" + str(i + 1)] = (
            Dataobj.quantities["rho"] * Dataobj.quantities["vx" + str(i + 1)]
        )
    Dataobj.quantities.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    return ("MassFlux_x1", "MassFlux_x2", "MassFlux_x3")


if __name__ == "__main__":
    print("Testing Model:", __file__)
    from TestData import TestData

    TestData = get(TestData)
    print("Testing Result:MassFlux_x1", TestData.quantities["MassFlux_x1"])
