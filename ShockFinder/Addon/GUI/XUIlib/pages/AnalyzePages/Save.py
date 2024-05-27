import copy
from tkinter import ttk, filedialog
from tkinter import *
from ShockFinder.Addon.ConfigReader import get_config
from XenonUI.XUIlib.page import str_to_float, retype_string, update_entry
import ShockFinder.Addon.Time as Time

def page(self):
    save = self.add_menu("Save Configuration")
    self.add_row(save)  # skip row (empty row)
    self.add_title(save, "Save Configuration")
    box = self.add_row(save, bx=260)

    def Load(event):
        file_path = filedialog.askopenfilename()
        if file_path != "":
            cfg = get_config(file_path)
            try:
                del cfg["Test"]
            except:
                pass
            anafs = []
            for key, value in cfg.items():
                if key in ("MultiprocessEngine", "IO", "Loader"):
                    eval(f"self.con_{key}(**value)")
                elif key == "Update":
                    vl = list(value.items())
                    vl += [("", "")] * (self.parmax - len(vl))
                    for i in range(self.parmax):
                        self.con_Update[i](*vl[i])
                else:
                    anaf = {
                        "app": key,
                        "quantity_name": "",
                        "result": "",
                        "arguments": {},
                    }
                    for k, v in value.items():
                        if k in ("quantity_name", "result"):
                            if type(v) not in (tuple, list):
                                anaf[k] = v
                            else:
                                vv = ""
                                for s in v:
                                    vv += f"{s},"
                                anaf[k] = vv[:-1] if vv != "" else ""
                        else:
                            if type(v) not in (tuple, list):
                                anaf["arguments"][k] = v
                            else:
                                vv = ""
                                for s in v:
                                    vv += f"{s},"
                                anaf["arguments"][k] = vv[:-1] if vv != "" else ""
                    anafs.append(anaf)
            anafs += [
                {"app": "", "quantity_name": "", "result": "", "arguments": {}}
            ] * (self.parmax - len(anafs))
            for i in range(self.parmax):
                self.con_Approaches[i](**anafs[i])

    button = Button(box, text="Load", width=5)
    button.pack(side="left")
    button.bind("<ButtonRelease>", Load)
    Label(box, width=6).pack(side="left")

    def get_anafs():
        def get_key(key):
            newkey = ""
            for s in key.split("_")[1:]:
                newkey += f"_{s}"
            return newkey[1:] if newkey != "" else newkey

        newdicts = {
            key: value
            for key, value in self.pars.items()
            if key not in ("MultiprocessEngine", "IO", "Loader", "Update")
        }
        sorted_keys = sorted(newdicts.keys(), key=lambda x: int(x.split("_")[0]))
        return {get_key(key): newdicts[key] for key in sorted_keys}

    def Test(event):
        grids = []
        for i in (grid_x1.get(), grid_x2.get(), grid_x3.get()):
            if i not in ("", "None", "0"):
                grids.append(int(i))
        grids = tuple(grids)
        grids_map = (
            (str_to_float(x1_beg.get()), str_to_float(x1_end.get())),
            (str_to_float(x2_beg.get()), str_to_float(x2_end.get())),
            (str_to_float(x3_beg.get()), str_to_float(x3_end.get())),
        )[: len(grids)]
        self.tkobj.io_recv("Got Test Data infomation:")
        self.tkobj.io_recv("Geometry:", geometry.get(), color="blue")
        gridsinfo = ""
        for i in grids:
            gridsinfo += str(i) + " X "
        if gridsinfo != "":
            gridsinfo = gridsinfo[:-3]
        self.tkobj.io_recv(
            "Grids:", gridsinfo, "(" + str(len(grids_map)) + "d)", color="blue"
        )
        for i in range(len(grids_map)):
            self.tkobj.io_recv(
                "x" + str(i + 1) + ": From",
                grids_map[i][0],
                "To",
                grids_map[i][1],
                color="blue",
            )
        self.tkobj.io_recv("Creating Test Database...")
        self.pageargs["Infobj"].setup_testdb(
            geometry=geometry.get(), grids=grids, grids_map=grids_map
        )
        self.tkobj.io_recv(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.tkobj.io_recv("Got Commands:")
        for key, value in self.pars.items():
            self.tkobj.io_recv(key, ":", value, color="blue")
        self.tkobj.io_recv(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.pageargs["Infobj"].testdb.update(**self.pars["Update"])
        self.tkobj.io_recv("Ready for testing..............")
        for key, value in get_anafs().items():
            try:
                anaf = self.pageargs["Infobj"].Config["AnalysisTool"][key].get
            except:
                try:
                    anaf = self.pageargs["Infobj"].Config["AnalysisLib"][key]
                except:
                    self.tkobj.io_recv("Unknown approach:", key, color="red")
                    continue
            pas = copy.deepcopy(value)
            pas.update({"info": key})
            for j in pas:
                pas[j] = retype_string(pas[j])
            self.pageargs["Infobj"].testdb.analysis_data(anaf, **pas)
            if "result" in pas:
                self.pageargs["Infobj"].testdb.check_quantities(pas["result"])
        self.tkobj.io_recv("Operation completed", color="green")

    button = Button(box, text="Test", width=5)
    button.pack(side="left")
    button.bind("<ButtonRelease>", Test)

    def Save(event):
        file = filedialog.asksaveasfile()
        if file != None:
            self.tkobj.io_recv("Collecting Parameters:")
            for key, value in self.pars.items():
                self.tkobj.io_recv(key, ":", value)
            self.tkobj.io_recv("Saving to file @", file)
            strc = "#ShockFinder Analyzing Configurations\n"
            try:
                strc += "#Built at " + Time.now() + "\n"
            except:
                pass
            strc += "#Wacmk.cn/com\n"
            strc += "#https://www.github.com/wacmkxiaoyi/shockfinder\n\n"
            # write MPE
            for key in (
                "MultiprocessEngine",
                "IO",
                "Loader",
                "Update",
            ):  # maintain sequency
                if key in self.pars:
                    strc += key
                    for k, v in self.pars[key].items():
                        strc += f";{k}={v}"
                    strc += ";\n"
            for key, value in get_anafs().items():
                strc += key
                for k, v in value.items():
                    strc += f";{k}={v}"
                strc += ";\n"
            file.writelines(strc)
            file.close()
            self.tkobj.io_recv("Operation completed", color="green")

    Label(box, width=6).pack(side="left")
    button = Button(box, text="Save", width=5)
    button.pack(side="left")
    button.bind("<ButtonRelease>", Save)
    self.add_row(save)
    self.add_title(save, "Test Parameters", fg="green", fontsize=22)
    Label(self.add_row(save, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(save, bx=250)
    Label(box, text="Geometry").pack(side="left")
    Label(box, text="|").pack(side="left")
    geometry = ttk.Combobox(
        box, width=18, values=("SPHERICAL", "POLAR", "CYLINDRICAL", "CARTESIAN")
    )
    geometry.set("SPHERICAL")
    geometry.pack(side="left")
    Label(box, text="|").pack(side="left")

    def save_geo(event=None):
        defaultinfo = (
            self.pageargs["Infobj"]
            .Config["AnalysisLib"]["TestData"]
            .grids_default[geometry.get()]
        )
        # x1
        try:
            update_entry(
                grid_x1,
                self.pageargs["Infobj"]
                .Config["AnalysisLib"]["TestData"]
                .grids_default_num[0],
                False,
            )
        except:
            pass
        try:
            update_entry(x1_beg, defaultinfo[0][0], False)
        except:
            pass
        try:
            update_entry(x1_end, defaultinfo[0][1], False)
        except:
            pass

        # x2
        try:
            update_entry(
                grid_x2,
                self.pageargs["Infobj"]
                .Config["AnalysisLib"]["TestData"]
                .grids_default_num[1],
                False,
            )
        except:
            pass
        try:
            update_entry(x2_beg, defaultinfo[1][0], False)
        except:
            pass
        try:
            update_entry(x2_end, defaultinfo[1][1], False)
        except:
            pass

        # x3
        try:
            update_entry(
                grid_x3,
                self.pageargs["Infobj"]
                .Config["AnalysisLib"]["TestData"]
                .grids_default_num[2],
                False,
            )
        except:
            pass
        try:
            update_entry(x3_beg, defaultinfo[2][0], False)
        except:
            pass
        try:
            update_entry(x3_end, defaultinfo[2][1], False)
        except:
            pass

    button_geo = Button(box, text="Save")
    button_geo.pack(side="left")
    button_geo.bind("<ButtonRelease>", save_geo)

    Label(self.add_row(save, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(save, bx=150)
    Label(box, text="Grid_x1").pack(side="left")
    Label(box, text="|").pack(side="left")
    grid_x1 = Entry(box, width=10)
    grid_x1.pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, text="From ").pack(side="left")
    x1_beg = Entry(box, width=15)
    x1_beg.pack(side="left")
    Label(box, text=" to ").pack(side="left")
    x1_end = Entry(box, width=15)
    x1_end.pack(side="left")
    Label(self.add_row(save, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(save, bx=150)
    Label(box, text="Grid_x2").pack(side="left")
    Label(box, text="|").pack(side="left")
    grid_x2 = Entry(box, width=10)
    grid_x2.pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, text="From ").pack(side="left")
    x2_beg = Entry(box, width=15)
    x2_beg.pack(side="left")
    Label(box, text=" to ").pack(side="left")
    x2_end = Entry(box, width=15)
    x2_end.pack(side="left")
    Label(self.add_row(save, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(save, bx=150)
    Label(box, text="Grid_x3").pack(side="left")
    Label(box, text="|").pack(side="left")
    grid_x3 = Entry(box, width=10)
    grid_x3.pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, text="From ").pack(side="left")
    x3_beg = Entry(box, width=15)
    x3_beg.pack(side="left")
    Label(box, text=" to ").pack(side="left")
    x3_end = Entry(box, width=15)
    x3_end.pack(side="left")
    Label(self.add_row(save, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end
    save_geo()
