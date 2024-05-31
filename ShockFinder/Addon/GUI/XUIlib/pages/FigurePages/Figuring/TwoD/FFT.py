import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
from XenonUI.XUIlib.page import update_entry, str_to_float, retype_string
from ShockFinder.Addon.Time import now

def page(self):  # support 0d
    bigbox = self.add_menu("Fast Fourier Transform", submenu=2)
    self.add_row(bigbox)
    self.add_title(bigbox, "Fast Fourier Transform (FFT)", fg="red", fontsize=24)
    self.add_title(bigbox, "(FFT only supports scale (0d))", fontsize=10)

    def reset_saved():
        self.tkobj.io_recv("Reseting 2D FFT configuration ...")
        savedbox.config(values=() + self.hdf5handler.read_config("2D", "FFT"))

    self.reset_funs.append(reset_saved)

    def load_saved(event):
        if savedbox.get() == "":
            return
        try:
            self.tkobj.io_recv(
                "Loading FFT configuration", savedbox.get(), "...", color="blue"
            )
            savedcfg = self.hdf5handler.read_config("2D", "FFT", savedbox.get())
            update_entry(entry_xtf, savedcfg["xtf"], False)
            update_entry(entry_xte, savedcfg["xte"], False)
            update_entry(entry_yrf, savedcfg["yrf"], False)
            update_entry(entry_yre, savedcfg["yre"], False)
            update_entry(entry_ytf, savedcfg["ytf"], False)
            update_entry(entry_yte, savedcfg["yte"], False)
            update_entry(entry_yrhof, savedcfg["yrhof"], False)
            update_entry(entry_yrhoe, savedcfg["yrhoe"], False)
            update_entry(entry_ylb, savedcfg["ylb"], False)
            update_entry(entry_yco, savedcfg["yco"], False)
            update_entry(entry_yls, savedcfg["yls"], False)
            update_entry(entry_yargs, savedcfg["yargs"], False)
            update_entry(entry_fx, savedcfg["fx"], False)
            update_entry(entry_fxa, savedcfg["fxa"], False)
            update_entry(entry_fxb, savedcfg["fxb"], False)
            update_entry(entry_fxs, savedcfg["fxs"], False)
            update_entry(entry_ft, savedcfg["ft"], False)
            update_entry(entry_fy, savedcfg["fy"], False)
            update_entry(entry_fya, savedcfg["fya"], False)
            update_entry(entry_fyb, savedcfg["fyb"], False)
            update_entry(entry_fys, savedcfg["fys"], False)
            update_entry(entry_fargs, savedcfg["fargs"], False)
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error: unknown key", err, color="red")

    def del_saved(event):
        if savedbox.get() == "" or not messagebox.askokcancel(
            "Delete Confirm", "Delete FFT configuration" + savedbox.get() + " ?"
        ):
            return
        self.tkobj.io_recv(
            "Deleting FFT configuration", savedbox.get(), "...", color="blue"
        )
        self.hdf5handler.del_config("2D", "FFT", savedbox.get())
        reset_saved()
        self.tkobj.io_recv("Operation completed", color="green")

    self.add_row(bigbox)
    self.add_title(bigbox, "Quick Box", fg="green")
    Label(self.add_row(bigbox, bx=100), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=100)
    Label(box, width=20, text="Saved Configurations | ").pack(side="left")
    savedbox = ttk.Combobox(
        box,
        width=17,
        height=10,
        values=() + self.hdf5handler.read_config("2D", "FFT"),
    )
    savedbox.pack(side="left")
    Label(box, text="|", width=3).pack(side="left")
    button = Button(box, text="Delete", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", del_saved)
    Label(box, width=3).pack(side="left")
    button = Button(box, text="Load", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", load_saved)
    Label(self.add_row(bigbox, bx=100), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    # line info
    self.add_row(bigbox)
    self.add_title(bigbox, "Line infomation", fg="green")
    Label(self.add_row(bigbox, bx=20), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=20)
    Label(box, width=8, text="Axis").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Quantity").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="unit of length").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="unit of time").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="unit of density").pack(side="left")
    box = self.add_row(bigbox, bx=20)
    Label(box, width=8).pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Label").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Color").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Linestyle").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Other Args").pack(side="left")
    Label(self.add_row(bigbox, bx=20), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=20)
    Label(box, width=8, text="X (Time)").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, text="Time Secquency", width=20).pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, text="-", width=20).pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_xtf = Entry(box, width=7)
    update_entry(entry_xtf, 1, False)
    entry_xtf.pack(side="left")
    Label(box, text="Utim^").pack(side="left")
    entry_xte = Entry(box, width=7)
    update_entry(entry_xte, 1, False)
    entry_xte.pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, text="-", width=20).pack(side="left")
    Label(self.add_row(bigbox, bx=20), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=20)
    Label(box, width=8, text="Y (FFT)").pack(side="left")
    Label(box, text="|").pack(side="left")
    self.FFT_Qt = ttk.Combobox(box, width=17, height=10, values=self.avqt[0])
    self.FFT_Qt.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_yrf = Entry(box, width=7)
    entry_yrf.pack(side="left")
    update_entry(entry_yrf, 1, False)
    Label(box, text="Ulen^").pack(side="left")
    entry_yre = Entry(box, width=7)
    entry_yre.pack(side="left")
    update_entry(entry_yre, 0, False)
    Label(box, text="|").pack(side="left")
    entry_ytf = Entry(box, width=7)
    entry_ytf.pack(side="left")
    update_entry(entry_ytf, 1, False)
    Label(box, text="Utim^").pack(side="left")
    entry_yte = Entry(box, width=7)
    entry_yte.pack(side="left")
    update_entry(entry_yte, 0, False)
    Label(box, text="|").pack(side="left")
    entry_yrhof = Entry(box, width=7)
    entry_yrhof.pack(side="left")
    update_entry(entry_yrhof, 1, False)
    Label(box, text="Urho^").pack(side="left")
    entry_yrhoe = Entry(box, width=7)
    entry_yrhoe.pack(side="left")
    update_entry(entry_yrhoe, 0, False)
    box = self.add_row(bigbox, bx=20)
    Label(box, width=8).pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_ylb = Entry(box, width=20)
    update_entry(entry_ylb, "None", False)
    update_entry(entry_ylb, "None", False)
    entry_ylb.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_yco = Entry(box, width=20)
    update_entry(entry_yco, "None", False)
    entry_yco.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_yls = Entry(box, width=20)
    update_entry(entry_yls, "-", False)
    entry_yls.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_yargs = Entry(box, width=20)
    entry_yargs.pack(side="left")
    Label(self.add_row(bigbox, bx=20), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    # Figure info
    self.add_row(bigbox)
    self.add_title(bigbox, "Figure infomation", fg="green")
    Label(self.add_row(bigbox), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox)
    Label(box, width=20, text="X").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="X limit").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="X scale").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Title").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    entry_fx = Entry(box, width=20)
    update_entry(entry_fx, "Frequency (Hz)", False)
    entry_fx.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fxa = Entry(box, width=8)
    entry_fxa.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_fxb = Entry(box, width=8)
    entry_fxb.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fxs = Entry(box, width=20)
    update_entry(entry_fxs, "None", False)
    entry_fxs.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_ft = Entry(box, width=20)
    entry_ft.pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    Label(box, width=20, text="Y").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Y limit").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Y Scale").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Other Args").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    entry_fy = Entry(box, width=20)
    update_entry(entry_fy, "Y", False)
    entry_fy.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fya = Entry(box, width=8)
    entry_fya.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_fyb = Entry(box, width=8)
    entry_fyb.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fys = Entry(box, width=20)
    update_entry(entry_fys, "None", False)
    entry_fys.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fargs = Entry(box, width=20)
    entry_fargs.pack(side="left")
    Label(self.add_row(bigbox), text="=" * 500).place(x=0, y=0, anchor="nw")  # end

    def drawfft(event):
        qt_value = self.FFT_Qt.get()
        if qt_value == "":
            return
        try:
            # if True:
            self.tkobj.io_recv("Figuring FFT with", qt_value, "...")
            # get figinfo
            figureinfo = self.get_figureinfo(
                entry_ft,
                entry_fx,
                entry_fy,
                entry_fxs,
                entry_fys,
                entry_fxa,
                entry_fxb,
                entry_fya,
                entry_fyb,
                entry_fargs,
            )
            self.tkobj.io_recv("Collected Figureinfo:", figureinfo)
            # get lineinfo

            factor = 1
            factor *= str_to_float(entry_yrf.get()) * self.unit_r ** str_to_float(
                entry_yre.get()
            )
            factor *= str_to_float(entry_ytf.get()) * self.unit_t ** str_to_float(
                entry_yte.get()
            )
            factor *= str_to_float(
                entry_yrhof.get()
            ) * self.unit_rho ** str_to_float(entry_yrhoe.get())
            ft = []
            tt = range(len(self.pageargs["Infobj"].database.data))
            if "Time" in figureinfo.keys():
                if type(figureinfo["Time"]) not in (list, tuple, np.ndarray):
                    figureinfo["Time"] = [figureinfo["Time"]]
                for i in range(len(figureinfo["Time"])):
                    if figureinfo["Time"][i] < -1:
                        figureinfo["Time"][i] = 0
                    elif figureinfo["Time"][i] > len(tt):
                        figureinfo["Time"][i] = tt[-1]
                tt = np.arange(*figureinfo["Time"])
            dt = (tt[-1] - tt[0]) / (len(tt) - 1)

            for i in tt:
                if self.pageargs["Infobj"].database.data[i] != None:
                    if qt_value not in self.pageargs["Infobj"].database.data[i].quantities:
                        break
                    ft.append(
                        self.pageargs["Infobj"]
                        .database.data[i]
                        .quantities[qt_value]
                        * factor
                    )
            ft = np.array(ft)
            if "Interval" in self.pageargs["Infobj"].database.infomation.keys():
                Interval = self.pageargs["Infobj"].database.infomation["Interval"]
            else:
                Interval = 1
            filt = False
            filv = 0
            cut = None
            ori = entry_yargs.get()
            newargs = ""
            for i in entry_yargs.get().split(";"):
                add = True
                iic = i.split("=")
                if len(iic) == 2:
                    if iic[0] == "linefilter":
                        filt = retype_string(iic[1])
                        add = False
                    elif iic[0] == "filterlevel":
                        filv = retype_string(iic[1])
                        add = False
                    elif iic[0] == "cut":
                        cut = retype_string(iic[1])
                        add = False
                if add:
                    newargs += i + ";"
            if newargs != "":
                newargs = newargs[:-1]
            ft = self.low_pass_filter(ft, filv, cut) if filt else ft
            update_entry(entry_yargs, newargs, False)
            x, y = self.pageargs["Infobj"].Config["AnalysisLib"]["FFT"](
                ft,
                unit=dt
                * str_to_float(entry_xtf.get())
                * self.unit_t ** str_to_float(entry_xte.get()),
                interval=Interval,
            )
            # lineinfo=self.get_lineinfo(x,y,entry_ylb,entry_yco,entry_yls,entry_yargs)
            # self.tkobj.io_recv("Collected lineinfo:",lineinfo)
            line = self.get_line(
                self.get_lineinfo(
                    x, y, entry_ylb, entry_yco, entry_yls, entry_yargs
                )
            )
            update_entry(entry_yargs, ori, False)
            self.pageargs["Infobj"].Config["Painter"]["P2D"].line(
                *line, **figureinfo
            )
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Figuring failure, error:", err, color="red")

    box = self.add_row(bigbox, bx=200)
    button = Button(box, text="Draw", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", drawfft)
    Label(box, width=5).pack(side="left")
    entry_save = Entry(box, width=15)
    entry_save.pack(side="left")
    Label(box, width=5).pack(side="left")

    def save(event):
        try:
            if entry_save != "":
                if entry_save.get() in self.hdf5handler.read_config(
                    "2D", "FFT"
                ) and not messagebox.askokcancel(
                    "Rewrite Confirm",
                    "Rewrite FFT configuration " + entry_save.get() + " ?",
                ):
                    return
                self.tkobj.io_recv(
                    "Saving FFT configuration",
                    entry_save.get(),
                    "...",
                    color="blue",
                )
                dd = {
                    "SavedTime": now(),
                    "xtf": entry_xtf.get(),
                    "xte": entry_xte.get(),
                    "yrf": entry_yrf.get(),
                    "yre": entry_yre.get(),
                    "ytf": entry_ytf.get(),
                    "yte": entry_yte.get(),
                    "yrhof": entry_yrhof.get(),
                    "yrhoe": entry_yrhoe.get(),
                    "ylb": entry_ylb.get(),
                    "yco": entry_yco.get(),
                    "yls": entry_yls.get(),
                    "yargs": entry_yargs.get(),
                    "fx": entry_fx.get(),
                    "fxa": entry_fxa.get(),
                    "fxb": entry_fxb.get(),
                    "fxs": entry_fxs.get(),
                    "ft": entry_ft.get(),
                    "fy": entry_fy.get(),
                    "fya": entry_fya.get(),
                    "fyb": entry_fyb.get(),
                    "fys": entry_fys.get(),
                    "fargs": entry_fargs.get(),
                }
                self.hdf5handler.write_config("2D", "FFT", {entry_save.get(): dd})
                reset_saved()
                self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv(err, color="red")

    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save)
