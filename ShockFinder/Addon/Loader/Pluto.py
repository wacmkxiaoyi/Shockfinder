# File type: <Function> return <Object: Data>
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

try:
    import ShockFinder.Addon.Loader.Pluto_lib.pload as pp
except:
    import Pluto_lib.pload as pp

try:
    import ShockFinder.Addon.Loader.FileNamePreProcess as FNPP
except:
    import FileNamePreProcess as FNPP

try:
    import ShockFinder.Data as Data
except:
    pass


def load(filename):
    # Loading Process
    fileindex, filedir, filetype = FNPP.FileNamePreProcess(filename)
    import os

    filedir = os.path.join(filedir, "dbl.out").rsplit("dbl.out")[0]
    read = pp.pload(int(fileindex), w_dir=filedir, datatype=filetype)
    grid = {}
    # GEOMETRY:	SPHERICAL	CYLINDRICAL		POLAR					CARTESIAN
    # 			x1-x2-x3	x1-x2			x1-x2-x3				x1-x2-x3
    # 			r-theta-phi r-z				r-phi(or theta)-z		x-y-z
    grid["x1"] = read.x1  # updated here
    grid["x2"] = read.x2  # updated here
    grid["x3"] = read.x3  # updated here
    # basic quantities
    quantities = {}
    # user definded...
    try:  # vector model
        quantities["vx1"] = read.vx1
    except:
        pass
    try:  # vector model
        quantities["vx2"] = read.vx2
    except:
        pass
    try:  # vector model
        quantities["vx3"] = read.vx3
    except:
        pass
    quantities["SimTime"] = read.SimTime
    quantities["geometry"] = read.geometry
    quantities["rho"] = read.rho
    quantities["prs"] = read.prs
    try:  # vector model
        quantities["Bx1"] = read.Bx1
    except:
        pass
    try:  # vector model
        quantities["Bx2"] = read.Bx2
    except:
        pass
    try:  # vector model
        quantities["Bx3"] = read.Bx3
    except:
        pass
    try:
        dt = Data.Data(grid, quantities)
        return dt
    except:
        return (grid, quantities)
