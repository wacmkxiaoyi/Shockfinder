import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
from XenonUI.XUIlib.page import update_entry, str_to_float
from ShockFinder.Addon.Time import now

def page(self):  # support 0d
    bigbox = self.add_menu("Time Sequency", submenu=2)
    self.add_row(bigbox)
    self.add_title(bigbox, "Time Sequency", fg="red", fontsize=24)
    self.add_title(bigbox, "(TimeSequency only supports 0D)", fontsize=10)

    def reset_saved():
        self.tkobj.io_recv("Reseting 2D TimeSequency configuration ...")
        savedbox.config(
            values=() + self.hdf5handler.read_config("2D", "TimeSequency")
        )

    self.reset_funs.append(reset_saved)

    def load_saved(event):
        if savedbox.get() == "":
            return
        try:
            self.tkobj.io_recv(
                "Loading TimeSequency configuration",
                savedbox.get(),
                "...",
                color="blue",
            )
            savedcfg = self.hdf5handler.read_config(
                "2D", "TimeSequency", savedbox.get()
            )
            update_entry(entry_xtf, savedcfg["xtf"], False)
            update_entry(entry_xte, savedcfg["xte"], False)
            update_entry(entry_syrf, savedcfg["syrf"], False)
            update_entry(entry_syre, savedcfg["syre"], False)
            update_entry(entry_sytf, savedcfg["sytf"], False)
            update_entry(entry_syte, savedcfg["syte"], False)
            update_entry(entry_syrhof, savedcfg["syrhof"], False)
            update_entry(entry_syrhoe, savedcfg["syrhoe"], False)
            update_entry(entry_sylb, savedcfg["sylb"], False)
            update_entry(entry_syco, savedcfg["syco"], False)
            update_entry(entry_syls, savedcfg["syls"], False)
            update_entry(entry_syargs, savedcfg["syargs"], False)
            for i in range(self.maxline):
                try:
                    update_entry(entry_yrf[i], savedcfg["yrf" + str(i)], False)
                    update_entry(entry_yre[i], savedcfg["yre" + str(i)], False)
                    update_entry(entry_ytf[i], savedcfg["ytf" + str(i)], False)
                    update_entry(entry_yte[i], savedcfg["yte" + str(i)], False)
                    update_entry(entry_yrhof[i], savedcfg["yrhof" + str(i)], False)
                    update_entry(entry_yrhoe[i], savedcfg["yrhoe" + str(i)], False)
                    update_entry(entry_ylb[i], savedcfg["ylb" + str(i)], False)
                    update_entry(entry_yco[i], savedcfg["yco" + str(i)], False)
                    update_entry(entry_yls[i], savedcfg["yls" + str(i)], False)
                    update_entry(entry_yargs[i], savedcfg["yargs" + str(i)], False)
                except:
                    pass
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
            "Delete Confirm",
            "Delete 2D TimeSequency configuration " + savedbox.get() + " ?",
        ):
            return
        self.tkobj.io_recv(
            "Deleting TimeSequency configuration",
            savedbox.get(),
            "...",
            color="blue",
        )
        self.hdf5handler.del_config("2D", "TimeSequency", savedbox.get())
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
        values=() + self.hdf5handler.read_config("2D", "TimeSequency"),
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
    Label(box, width=8, text="X").pack(side="left")
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
    Label(box, width=8, text="Y (Share X)").pack(side="left")
    Label(box, text="|").pack(side="left")
    self.TS_sy_qt = ttk.Combobox(box, width=17, height=10, values=self.avqt[0])
    self.TS_sy_qt.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_syrf = Entry(box, width=7)
    entry_syrf.pack(side="left")
    update_entry(entry_syrf, 1, False)
    Label(box, text="Ulen^").pack(side="left")
    entry_syre = Entry(box, width=7)
    entry_syre.pack(side="left")
    update_entry(entry_syre, 0, False)
    Label(box, text="|").pack(side="left")
    entry_sytf = Entry(box, width=7)
    entry_sytf.pack(side="left")
    update_entry(entry_sytf, 1, False)
    Label(box, text="Utim^").pack(side="left")
    entry_syte = Entry(box, width=7)
    entry_syte.pack(side="left")
    update_entry(entry_syte, 0, False)
    Label(box, text="|").pack(side="left")
    entry_syrhof = Entry(box, width=7)
    entry_syrhof.pack(side="left")
    update_entry(entry_syrhof, 1, False)
    Label(box, text="Urho^").pack(side="left")
    entry_syrhoe = Entry(box, width=7)
    entry_syrhoe.pack(side="left")
    update_entry(entry_syrhoe, 0, False)
    box = self.add_row(bigbox, bx=20)
    Label(box, width=8).pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_sylb = Entry(box, width=20)
    update_entry(entry_sylb, str(None), False)
    entry_sylb.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_syco = Entry(box, width=20)
    update_entry(entry_syco, str(None), False)
    entry_syco.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_syls = Entry(box, width=20)
    update_entry(entry_syls, "-", False)
    entry_syls.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_syargs = Entry(box, width=20)
    entry_syargs.pack(side="left")

    entry_yrf = []
    entry_yre = []
    entry_ytf = []
    entry_yte = []
    entry_yrhof = []
    entry_yrhoe = []
    entry_ylb = []
    entry_yco = []
    entry_yls = []
    entry_yargs = []
    self.TS_qt = []
    for i in range(self.maxline):
        Label(self.add_row(bigbox, bx=20), text="-" * 500).place(
            x=0, y=0, anchor="nw"
        )  # next
        box = self.add_row(bigbox, bx=20)
        Label(box, width=8, text="Y" + str(i + 1)).pack(side="left")
        Label(box, text="|").pack(side="left")
        self.TS_qt.append(
            ttk.Combobox(box, width=17, height=10, values=self.avqt[0])
        )
        self.TS_qt[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_yrf.append(Entry(box, width=7))
        entry_yrf[-1].pack(side="left")
        update_entry(entry_yrf[-1], 1, False)
        Label(box, text="Ulen^").pack(side="left")
        entry_yre.append(Entry(box, width=7))
        entry_yre[-1].pack(side="left")
        update_entry(entry_yre[-1], 0, False)
        Label(box, text="|").pack(side="left")
        entry_ytf.append(Entry(box, width=7))
        entry_ytf[-1].pack(side="left")
        update_entry(entry_ytf[-1], 1, False)
        Label(box, text="Utim^").pack(side="left")
        entry_yte.append(Entry(box, width=7))
        entry_yte[-1].pack(side="left")
        update_entry(entry_yte[-1], 0, False)
        Label(box, text="|").pack(side="left")
        entry_yrhof.append(Entry(box, width=7))
        entry_yrhof[-1].pack(side="left")
        update_entry(entry_yrhof[-1], 1, False)
        Label(box, text="Urho^").pack(side="left")
        entry_yrhoe.append(Entry(box, width=7))
        entry_yrhoe[-1].pack(side="left")
        update_entry(entry_yrhoe[-1], 0, False)
        box = self.add_row(bigbox, bx=20)
        Label(box, width=8).pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_ylb.append(Entry(box, width=20))
        update_entry(entry_ylb[-1], "None", False)
        entry_ylb[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_yco.append(Entry(box, width=20))
        update_entry(entry_yco[-1], "None", False)
        entry_yco[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_yls.append(Entry(box, width=20))
        update_entry(entry_yls[-1], "-", False)
        entry_yls[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_yargs.append(Entry(box, width=20))
        entry_yargs[-1].pack(side="left")
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
    update_entry(entry_fx, "X", False)
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

    def drawlines(event):
        # 			if True:
        try:
            x = []
            for i in range(len(self.pageargs["Infobj"].database.data)):
                if self.pageargs["Infobj"].database.data[i] != None:
                    x.append(
                        i
                        * str_to_float(entry_xtf.get())
                        * self.unit_t ** str_to_float(entry_xte.get())
                    )
            x = np.array(x)
            sy = self.get_y(
                self.TS_sy_qt,
                entry_syrf,
                entry_syre,
                entry_sytf,
                entry_syte,
                entry_syrhof,
                entry_syrhoe,
            )
            self.tkobj.io_recv("Figuring Lines ...")
            lines = []
            for i in range(self.maxline):
                y = self.get_y(
                    self.TS_qt[i],
                    entry_yrf[i],
                    entry_yre[i],
                    entry_ytf[i],
                    entry_yte[i],
                    entry_yrhof[i],
                    entry_yrhoe[i],
                )
                if str(y) != "False":
                    lines += self.get_line(
                        self.get_lineinfo(
                            x[: len(y)],
                            y,
                            entry_ylb[i],
                            entry_yco[i],
                            entry_yls[i],
                            entry_yargs[i],
                        )
                    )
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

            # begining to drow
            if str(sy) != "False":
                line_s = self.get_line(
                    self.get_lineinfo(
                        x[: len(sy)], sy, entry_sylb, entry_syco, entry_syls, entry_syargs
                    )
                )[0]
                self.pageargs["Infobj"].Config["Painter"]["P2D"].line_share_x(
                    line_s, *lines, **figureinfo
                )
            else:
                self.pageargs["Infobj"].Config["Painter"]["P2D"].line(
                    *lines, **figureinfo
                )

            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Figuring failure, error:", err, color="red")

    box = self.add_row(bigbox, bx=200)
    button = Button(box, text="Draw", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", drawlines)
    Label(box, width=5).pack(side="left")
    entry_save = Entry(box, width=15)
    entry_save.pack(side="left")
    Label(box, width=5).pack(side="left")

    def save(event):
        try:
            if entry_save != "":
                if entry_save.get() in self.hdf5handler.read_config(
                    "2D", "TimeSequency"
                ) and not messagebox.askokcancel(
                    "Rewrite Confirm",
                    "Rewrite 2D TimeSequency configuration "
                    + entry_save.get()
                    + " ?",
                ):
                    return
                self.tkobj.io_recv(
                    "Saving TimeSequency configuration",
                    entry_save.get(),
                    "...",
                    color="blue",
                )
                dd = {
                    "SavedTime": now(),
                    "xtf": entry_xtf.get(),
                    "xte": entry_xte.get(),
                    "syrf": entry_syrf.get(),
                    "syre": entry_syre.get(),
                    "sytf": entry_sytf.get(),
                    "syte": entry_syte.get(),
                    "syrhof": entry_syrhof.get(),
                    "syrhoe": entry_syrhoe.get(),
                    "sylb": entry_sylb.get(),
                    "syco": entry_syco.get(),
                    "syls": entry_syls.get(),
                    "syargs": entry_syargs.get(),
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
                for i in range(self.maxline):
                    try:
                        dd["yrf" + str(i)] = entry_yrf[i].get()
                        dd["yre" + str(i)] = entry_yre[i].get()
                        dd["ytf" + str(i)] = entry_ytf[i].get()
                        dd["yte" + str(i)] = entry_yte[i].get()
                        dd["yrhof" + str(i)] = entry_yrhof[i].get()
                        dd["yrhoe" + str(i)] = entry_yrhoe[i].get()
                        dd["ylb" + str(i)] = entry_ylb[i].get()
                        dd["yco" + str(i)] = entry_yco[i].get()
                        dd["yls" + str(i)] = entry_yls[i].get()
                        dd["yargs" + str(i)] = entry_yargs[i].get()
                    except:
                        pass
                self.hdf5handler.write_config(
                    "2D", "TimeSequency", {entry_save.get(): dd}
                )
                reset_saved()
                self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv(err, color="red")

    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save)
