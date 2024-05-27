try:
    from ShockFinder.Config import *
except:
    Config = {}
    Default = {}
from ShockFinder.DataBase import DataBase
from ShockFinder.Update import Update
import numpy as np, copy, os
from multiprocessing import cpu_count


def args_cut(args, pnum):
    result = []
    for i in range(pnum):
        result.append([])
    cal_num = len(args)
    pp = 0
    for i in args:
        result[pp].append(i)
        pp += 1
        if pp == pnum:
            pp = 0
    return result


def test_database(
    num=None,
    tindex=None,
    printfun=print,
    geometry="SPHERICAL",
    grids=AnalysisLib["TestData"].grids_default_num,
    grids_map=AnalysisLib["TestData"].grids_default["SPHERICAL"],
):
    db = DataBase(Default, printfun)
    if num == None:
        num = 1
        tindex = [0]
    db.build_test_data(
        AnalysisLib["TestData"].get,
        num=num,
        geometry=geometry,
        grids=grids,
        grids_map=grids_map,
    )
    db.tindex = tindex if tindex != None else range(num)
    return db


def analyze(analyze_commands, filesname={}, testmode=False, print=print):
    if testmode:
        num = len(filesname)
        database = test_database(num, list(filesname.keys()), print)
    else:
        database = DataBase(infomation=Default, printfun=print)
        database.load_data(analyze_commands["Loader"], **filesname)
    quantities_name = []
    for i in analyze_commands.keys():
        if i == "Update":
            database.update(**analyze_commands[i])
        elif i == "Test" and analyze_commands[i]:
            # all tools
            vargs = {
                "Mean_axis": (1,),
                "Radial_axis": (1,),
                "Radial_value": (None,),
                "ShockDeduct": 0.1,
                "Harmonic_Max_l": 3,
                "Harmonic_Max_m": 3,
            }
            # if "IO" in analyze_commands.keys():
            # 	vargs.update(analyze_commands["IO"])
            # standard
            standard = (
                "SoundSpeed",
                "Temperature",
                "Entropy",
                "MachNumber",
                "Bremsstrahlung",
                "MassFlux",
            )
            quantities_name = ("rho", "prs", "vx1", "vx2", "vx3") + standard
            ext_tools = ("Harmonic", "Mean", "Gradient", "Divergence", "Radial")
            for j in standard:
                nvgs = copy.deepcopy(vargs)
                nvgs.update({"info": j, "result": j})
                anaf = AnalysisTool[j].get
                database.analysis_data(anaf, **nvgs)
                if not database.check_quantities(j):
                    exit()
            for j in quantities_name:
                for k in ext_tools:
                    nvgs = copy.deepcopy(vargs)
                    nvgs.update({"info": k, "quantity_name": j})
                    if k not in ("Harmonic", "Gradient"):
                        nvgs.update({"result": k + "_" + j})
                    elif k == "Harmonic" and database.get_geometry() == "SPHERICAL":
                        rrs = []
                        for l in range(vargs["Harmonic_Max_l"] + 1):
                            if database.get_dimension() == 2:
                                rrs.append(k + "_l@" + str(l) + "_" + j)
                            if database.get_dimension() == 3:
                                for m in range(
                                    max(-vargs["Harmonic_Max_l"], -l),
                                    min(vargs["Harmonic_Max_l"] + 1, l + 1),
                                ):
                                    rrs.append(
                                        k + "_l@" + str(l) + "_m@" + str(m) + "_" + j
                                    )
                        nvgs.update({"result": rrs})
                    elif k == "Gradient":
                        if database.get_dimension() == 2:
                            nvgs.update(
                                {"result": [k + "_" + j + "_x1", k + "_" + j + "_x2"]}
                            )
                        elif database.get_dimension() == 3:
                            nvgs.update(
                                {
                                    "result": [
                                        k + "_" + j + "_x1",
                                        k + "_" + j + "_x2",
                                        k + "_" + j + "_x3",
                                    ]
                                }
                            )
                    anaf = AnalysisLib[k]
                    database.analysis_data(anaf, **nvgs)
                    if k not in ("Harmonic", "Gradient"):
                        if not database.check_quantities(k + "_" + j):
                            exit()
                    elif k == "Harmonic" and database.get_geometry() == "SPHERICAL":
                        for l in range(vargs["Harmonic_Max_l"] + 1):
                            if (
                                database.get_dimension() == 2
                                and not database.check_quantities(
                                    k + "_l@" + str(l) + "_" + j
                                )
                            ):
                                exit()
                            if database.get_dimension() == 3:
                                for m in range(
                                    max(-vargs["Harmonic_Max_l"], -l),
                                    min(vargs["Harmonic_Max_l"] + 1, l + 1),
                                ):
                                    if not database.check_quantities(
                                        k + "_l@" + str(l) + "_m@" + str(m) + "_" + j
                                    ):
                                        exit()
                    elif k == "Gradient":
                        if (
                            database.get_dimension() == 2
                            and not database.check_quantities(
                                [k + "_" + j + "_x1", k + "_" + j + "_x2"]
                            )
                            or database.get_dimension() == 3
                            and not database.check_quantities(
                                [
                                    k + "_" + j + "_x1",
                                    k + "_" + j + "_x2",
                                    k + "_" + j + "_x3",
                                ]
                            )
                        ):
                            exit()
                nvgs = copy.deepcopy(vargs)
                nvgs.update({"info": "Shocks", "quantity_name": j})
                anaf = AnalysisTool["Shocks"].get
                database.analysis_data(anaf, **nvgs)
                if not database.check_quantities("Shock_" + j):
                    exit()
        elif i not in ("IO", "Loader"):
            quantities_name.append(i)
            analyze_commands[i].update({"info": i})
            if "IO" in analyze_commands.keys():
                analyze_commands[i].update(analyze_commands["IO"])
            if "result" not in analyze_commands[i].keys():
                pass
                # analyze_commands[i].update({"result":i})
            anaf = None
            try:
                anaf = AnalysisLib[i]
            except:
                try:
                    anaf = AnalysisTool[i].get
                except:
                    continue
            database.save_analyze_pars(anaf, **analyze_commands[i])
    database.analyze()
    print("Finished analyzing!")
    database.data = tuple(database.data)
    database.tindex = tuple(database.tindex)
    return database


def get_par(args, name, default=None):
    try:
        return args[name]
    except:
        return default


class ShockFinder:
    Default_MPE = "XME"
    Default_IO = "HDF5"
    Default_GUI = "XUI"
    try:
        MultiprocessEngine = MultiprocessEngine[Default_MPE]
    except:
        MultiprocessEngine = None
    try:
        IO = IO[Default_IO]
    except:
        IO = None
    try:
        GUI = GUI[Default_GUI]
    except:
        GUI = None
    Config = Config
    MPE = None
    database = DataBase({})
    testmode = False

    def __init__(self, config_file=None):
        self.setup_testdb(printfun=print)
        if config_file != None:  # MPA MODE
            self.command(GeneralLib["ConfigReader"].get_config(config_file))
        else:  # GUI MODE
            # set default load info
            self.LMPEINFO = {}
            self.LMPEINFO["cpu_leave"] = 1  # left 1 maintains system stable
            self.LMPEINFO["cpu_logicmax"] = 4  # set a maximul
            self.LMPEINFO["pnum"] = (
                cpu_count() - self.LMPEINFO["cpu_leave"]
                if cpu_count() > self.LMPEINFO["cpu_leave"]
                and cpu_count() <= self.LMPEINFO["cpu_logicmax"]
                else (
                    self.LMPEINFO["cpu_logicmax"]
                    if cpu_count() > self.LMPEINFO["cpu_logicmax"]
                    else self.LMPEINFO["cpu_leave"]
                )
            )
            if self.GUI != None:
                self.GUIobj = self.GUI.show(
                    **{
                        "Infobj": self,
                        "windows_title": "ShockFinder " + str(ShockFinderVersion),
                    }
                )
                # self.database.printfun=self.GUIobj.iofun # is not needed in logical
                self.GUIobj.iofun("Wellcome to use ShockFinder ^_^", color="green")
                self.GUIobj.guiobj.show()
                # self.GUI.CollectPages()

    def setup_testdb(self, **kwargs):
        try:
            del self.testdb
        except:
            pass
        if "printfun" not in kwargs.keys():
            kwargs.update({"printfun": self.GUIobj.iofun})
        self.testdb = test_database(**kwargs)

    def set_MPE(self, mpe):
        try:
            self.MultiprocessEngine = MultiprocessEngine[mpe]
        except Exception as err:
            try:
                self.GUIobj.iofun(err, color="red")
            except:
                print(err)

    def set_IO(self, io):
        try:
            self.IO = IO[io]
        except Exception as err:
            try:
                self.GUIobj.iofun(err, color="red")
            except:
                print(err)

    def load(self, filename):
        try:
            if self.IO != None:
                tmpdb = self.IO.Load(filename, self.MultiprocessEngine, **self.LMPEINFO)
                if type(tmpdb) == type(None):
                    self.GUIobj.iofun(
                        "Loading error:",
                        filename,
                        "is not a ShockFinder data file",
                        color="red",
                    )
                    return False
                self.database = tmpdb
                return True
            self.GUIobj.iofun("No IO module selected", color="blue")
            return False
        except Exception as err:
            try:
                self.GUIobj.iofun(
                    "Load database",
                    filename,
                    " failure! (Error:",
                    err,
                    ")",
                    color="red",
                )
            except:
                print(err)
            return False

    def command(self, command):
        analyze_commands = {}
        filesname = {}
        for i in command.keys():
            values = command[i]
            if i == "MultiprocessEngine":
                self.MultiprocessEngine = MultiprocessEngine[values["Engine"]]
                self.MPE = self.MultiprocessEngine.build(analyze, **values)
            elif i == "IO":
                self.IO = IO[values["Engine"]]
                qtname = []
                for ii in command.keys():
                    qtname += (
                        ii
                        if ii
                        not in (
                            "MultiprocessEngine",
                            "IO",
                            "Testdata",
                            "Update",
                            "Test",
                        )
                        else ""
                    )
                databaseinfo = self.testdb.infomation
                if "Loader" in command.keys():
                    databaseinfo.update(
                        {
                            "FilePrefix": get_par(
                                command["Loader"], "FilePrefix", "data."
                            ),
                            "FileFormat": get_par(
                                command["Loader"], "FileFormat", "04d"
                            ),
                            "FileDir": get_par(
                                command["Loader"], "FileDir", os.getcwd()
                            ),
                            "FileType": get_par(command["Loader"], "FileType", "dbl"),
                            "Interval": get_par(command["Loader"], "Interval", 1),
                        }
                    )
                else:
                    databaseinfo.update({"Interval": 1})
                tfname = get_par(
                    values, "filename", str(int(GeneralLib["Time"].get_time()))
                )
                filename = tfname + "." + self.IO.Filetype

                databaseinfo.update(
                    {
                        "pnum": 1 if self.MPE == None else self.MPE.pnum,
                        "projectname": tfname,
                    }
                )
                self.IO.PreSave(filename, *qtname, **databaseinfo)
                analyze_commands["IO"] = values
                analyze_commands["IO"].update(
                    {"IOfun": self.IO.Save, "filename": filename, "projectname": tfname}
                )
            elif i == "Loader":
                analyze_commands[i] = Loader[values["Engine"]].load
                allfiles = LoaderLib["FPP"].GetFiles(
                    get_par(values, "FileDir", os.getcwd()),
                    get_par(values, "FilePrefix", "data."),
                    get_par(values, "FileFormat", "04d"),
                    get_par(values, "FileType", "dbl"),
                )
                if self.MPE != None:
                    TrueIndex = args_cut(
                        range(0, len(allfiles), get_par(values, "Interval", 1)),
                        self.MPE.pnum,
                    )
                    filesname = [
                        {str(j): allfiles[j] for j in TrueIndex[i]}
                        for i in range(self.MPE.pnum)
                    ]
                else:
                    TrueIndex = range(0, len(allfiles), get_par(values, "Interval", 1))
                    for j in TrueIndex:
                        filesname[str(j)] = allfiles[j]
            elif i == "Testdata":
                self.testmode = True
                if self.MPE != None:
                    TrueIndex = args_cut(range(values["num"]), self.MPE.pnum)
                    filesname = [
                        {j: j for j in TrueIndex[i]} for i in range(self.MPE.pnum)
                    ]
                else:
                    for i in range(values["num"]):
                        filesname[i] = i
                # self.use_test_data(*num)
            else:
                analyze_commands[i] = values
        self.analyze(analyze_commands, filesname)

    def analyze(self, analyze_commands, filesname):  #
        if self.MPE != None:
            anacmd = []
            for i in range(self.MPE.pnum):
                anacmd.append(copy.deepcopy(analyze_commands))
                tfilename = anacmd[i]["IO"]["projectname"]
                ssfname = tfilename
                if "/" in tfilename:
                    ssfname = tfilename.split("/")[-1]
                if "\\" in tfilename:
                    ssfname = tfilename.split("\\")[-1]
                if anacmd[i]["IO"]["Engine"] == "HDF5":
                    anacmd[i]["IO"]["filename"] = os.path.join(
                        tfilename, ssfname + str(i) + "." + self.IO.Filetype
                    )
            self.MPE.fun(
                self.MPE.Array(anacmd), self.MPE.Array(filesname), self.testmode
            )
        else:
            analyze(analyze_commands, filesname)
