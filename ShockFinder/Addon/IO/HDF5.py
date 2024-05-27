# File type: <Function> set
# By Junxiang H., 2023/07/5
# wacmk.com/cn Tech. Supp.
try:
    import ShockFinder.Addon.Time as Time
except:
    import datetime

    class tt:
        def now():
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


import h5py, numpy as np, os

Filetype = "hdf5"


def PreSave(filename, *quantities_name, **databaseinfo):
    if "pnum" in databaseinfo.keys():
        pnum = databaseinfo["pnum"]
    else:
        pnum = 1
    tfilename = databaseinfo["projectname"]
    ssfname = tfilename
    if "/" in tfilename:
        ssfname = tfilename.split("/")[-1]
    if "\\" in tfilename:
        ssfname = tfilename.split("\\")[-1]
    if not os.path.exists(tfilename):
        os.makedirs(tfilename)
    for i in range(0, pnum):
        subfilename = os.path.join(tfilename, ssfname + str(i) + "." + Filetype)
        subfile = h5py.File(subfilename, "w")
        subfile.create_group("Data")
        subfile.close()
    hdffile = h5py.File(filename, "w")
    for i in databaseinfo.keys():
        try:
            hdffile.attrs[i] = databaseinfo[i]
        except:
            hdffile.attrs[i] = str(databaseinfo[i])
    hdffile.attrs["Time"] = Time.now()
    hdffile.attrs["HDF5LABEL"] = "ShockFinderDataFile"
    hdffile.close()


def Save(filename, data, index, *quantities_name):
    hdffile = h5py.File(filename, "a")
    g_dt = hdffile["Data"]
    try:
        g_dti = g_dt.create_group(str(index))
        g_dtig = g_dti.create_group("Grid")
        g_dtiq = g_dti.create_group("Quantities")
    except Exception as err:
        g_dti = g_dt[str(index)]
        g_dtig = g_dti["Grid"]
        g_dtiq = g_dti["Quantities"]
    for i in quantities_name:
        try:
            g_dtiq.create_dataset(i, data=data.quantities[i])
        except Exception as err1:
            try:
                g_dtig.create_dataset(i, data=data.grid[i])
            except Exception as err2:
                pass
                # print("Error:",err1,err2)
    hdffile.close()


try:
    import ShockFinder.DataBase as DataBase
    import ShockFinder.Data as Data

    def Load(filename, MPE=None, print=print, **vargs):
        filename = filename.rsplit("." + Filetype, 1)[0]
        hdffile = h5py.File(filename + "." + Filetype, "r")
        dbinfo = {}
        for i in hdffile.attrs.keys():
            dbinfo[i] = hdffile.attrs[i]
            if dbinfo[i] == "None":
                dbinfo[i] = None
        if (
            "HDF5LABEL" not in hdffile.attrs
            or hdffile.attrs["HDF5LABEL"] != "ShockFinderDataFile"
        ):
            # print("Error: \"",filename,"\" is not a ShockFinder data file")
            return None
        hdffile.close()
        if MPE == None:
            return DataBase.DataBaseConnect(
                *[
                    load_fun(dbinfo["projectname"], i, dbinfo, print)
                    for i in range(dbinfo["pnum"])
                ]
            )
        # MPE mode
        mpe = MPE.build(load_fun, **vargs)
        return DataBase.DataBaseConnect(
            *mpe.fun(dbinfo["projectname"], mpe.Array(range(dbinfo["pnum"])), dbinfo)
        )

except:

    def Load(filename, MPE=None, **vargs):
        print("Load module build failure, please use orther IO modules")


def load_fun(projectname, projectindex, dbinfo, print=print):
    ndb = DataBase.DataBase(infomation={}, printfun=print)
    ssfname = projectname
    if "/" in projectname:
        ssfname = projectname.split("/")[-1]
    if "\\" in projectname:
        ssfname = projectname.split("\\")[-1]
    subfile = os.path.join(projectname, ssfname + str(projectindex) + "." + Filetype)
    hdffile = h5py.File(subfile, "r")
    for i in sorted(hdffile["Data"].keys(), key=lambda x: int(x)):
        print('Loading "', i, '" in "', subfile, '"')
        grid = {}
        g_dtg = hdffile["Data"][i]["Grid"]
        for j in g_dtg.keys():
            grid[j] = np.array(g_dtg[j])
        quantities = {}
        g_dtq = hdffile["Data"][i]["Quantities"]
        for j in g_dtq.keys():
            quantities[j] = np.array(g_dtq[j])
            if quantities[j].ndim == 0:
                try:
                    quantities[j] = float(quantities[j])
                except:
                    quantities[j] = quantities[j].item().decode("utf-8")
                    if quantities[j] == "True":
                        quantities[j] = True
                    elif quantities[j] == "False":
                        quantities[j] = False
                    elif "," in quantities[j]:
                        quantities[j] = quantities[j].split(",")
        ndb.data.append(Data.Data(grid, quantities))
        ndb.tindex.append(int(i))
    ndb.update_infomation(**dbinfo)
    hdffile.close()
    ndb.data = tuple(ndb.data)
    ndb.tindex = tuple(ndb.tindex)
    print("Loading finished, waiting for database connection")
    return ndb
