from XenonUI.XUIlib.page import update_entry

# logo=os.path.join("ShockFinder","Addon","GUI","XUIlib","image","F.png")
from ShockFinder.Addon.Time import now
from tkinter import *
from tkinter import ttk, messagebox

def page(self):  # support 0d
    bigbox = self.add_menu("Lines", submenu=2)
    self.add_row(bigbox)
    self.add_title(bigbox, "3D Lines", fg="red", fontsize=24)
    self.add_title(bigbox, "(Lins only supports 1D)", fontsize=10)

    def reset_saved():
        self.tkobj.io_recv("Reseting 3D Lines configuration ...")
        savedbox.config(values=() + self.hdf5handler.read_config("3D", "Lines"))

    self.reset_funs.append(reset_saved)

    def load_saved(event):
        if savedbox.get() == "":
            return
        try:
            self.tkobj.io_recv(
                "Loading 3D Lines configuration",
                savedbox.get(),
                "...",
                color="blue",
            )
            savedcfg = self.hdf5handler.read_config("3D", "Lines", savedbox.get())
            update_entry(entry_xrf, savedcfg["xrf"], False)
            update_entry(entry_xre, savedcfg["xre"], False)
            update_entry(entry_xtf, savedcfg["xtf"], False)
            update_entry(entry_xte, savedcfg["xte"], False)
            update_entry(entry_xrhof, savedcfg["xrhof"], False)
            update_entry(entry_xrhoe, savedcfg["xrhoe"], False)
            update_entry(entry_yrf, savedcfg["yrf"], False)
            update_entry(entry_yre, savedcfg["yre"], False)
            update_entry(entry_ytf, savedcfg["ytf"], False)
            update_entry(entry_yte, savedcfg["yte"], False)
            update_entry(entry_yrhof, savedcfg["yrhof"], False)
            update_entry(entry_yrhoe, savedcfg["yrhoe"], False)
            for i in range(self.maxline):
                try:
                    update_entry(entry_zrf[i], savedcfg["zrf" + str(i)], False)
                    update_entry(entry_zre[i], savedcfg["zre" + str(i)], False)
                    update_entry(entry_ztf[i], savedcfg["ztf" + str(i)], False)
                    update_entry(entry_zte[i], savedcfg["zte" + str(i)], False)
                    update_entry(entry_zrhof[i], savedcfg["zrhof" + str(i)], False)
                    update_entry(entry_zrhoe[i], savedcfg["zrhoe" + str(i)], False)
                    update_entry(entry_zlb[i], savedcfg["zlb" + str(i)], False)
                    update_entry(entry_zco[i], savedcfg["zco" + str(i)], False)
                    update_entry(entry_zls[i], savedcfg["zls" + str(i)], False)
                    update_entry(entry_zargs[i], savedcfg["zargs" + str(i)], False)
                except:
                    pass
            update_entry(entry_fx, savedcfg["fx"], False)
            update_entry(entry_fxa, savedcfg["fxa"], False)
            update_entry(entry_fxb, savedcfg["fxb"], False)
            update_entry(entry_ft, savedcfg["ft"], False)
            update_entry(entry_fy, savedcfg["fy"], False)
            update_entry(entry_fya, savedcfg["fya"], False)
            update_entry(entry_fyb, savedcfg["fyb"], False)
            update_entry(entry_fz, savedcfg["fz"], False)
            update_entry(entry_fza, savedcfg["fza"], False)
            update_entry(entry_fzb, savedcfg["fzb"], False)
            update_entry(entry_fargs, savedcfg["fargs"], False)
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error: unknown key", err, color="red")

    def del_saved(event):
        if savedbox.get() == "" or not messagebox.askokcancel(
            "Delete Confirm",
            "Delete 3D Line configuration " + savedbox.get() + " ?",
        ):
            return
        self.tkobj.io_recv(
            "Deleting 3D Lines configuration", savedbox.get(), "...", color="blue"
        )
        self.hdf5handler.del_config("3D", "Lines", savedbox.get())
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
        values=() + self.hdf5handler.read_config("3D", "Lines"),
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
    Label(box, width=8, text="Index").pack(side="left")
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
    Label(box, width=2, text="x").pack(side="left")
    self.Line3d_x_index = ttk.Combobox(
        box, width=3, height=10, values=self.usefultindex
    )
    self.Line3d_x_index.pack(side="left")
    Label(box, text="|").pack(side="left")
    self.Line3d_x_qt = ttk.Combobox(
        box, width=17, height=10, values=["x1", "x2", "x3"] + self.avqt[1]
    )
    self.Line3d_x_qt.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_xrf = Entry(box, width=7)
    entry_xrf.pack(side="left")
    entry_xrf.insert(0, 1)
    Label(box, text="Ulen^").pack(side="left")
    entry_xre = Entry(box, width=7)
    entry_xre.pack(side="left")
    entry_xre.insert(0, 0)
    Label(box, text="|").pack(side="left")
    entry_xtf = Entry(box, width=7)
    entry_xtf.pack(side="left")
    entry_xtf.insert(0, 1)
    Label(box, text="Utim^").pack(side="left")
    entry_xte = Entry(box, width=7)
    entry_xte.pack(side="left")
    entry_xte.insert(0, 0)
    Label(box, text="|").pack(side="left")
    entry_xrhof = Entry(box, width=7)
    entry_xrhof.pack(side="left")
    entry_xrhof.insert(0, 1)
    Label(box, text="Urho^").pack(side="left")
    entry_xrhoe = Entry(box, width=7)
    entry_xrhoe.pack(side="left")
    entry_xrhoe.insert(0, 0)
    Label(self.add_row(bigbox, bx=20), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=20)
    Label(box, width=2, text="Y").pack(side="left")
    self.Line3d_y_index = ttk.Combobox(
        box, width=3, height=10, values=self.usefultindex
    )
    self.Line3d_y_index.pack(side="left")
    Label(box, text="|").pack(side="left")
    self.Line3d_y_qt = ttk.Combobox(
        box, width=17, height=10, values=["x1", "x2", "x3"] + self.avqt[1]
    )
    self.Line3d_y_qt.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_yrf = Entry(box, width=7)
    entry_yrf.pack(side="left")
    entry_yrf.insert(0, 1)
    Label(box, text="Ulen^").pack(side="left")
    entry_yre = Entry(box, width=7)
    entry_yre.pack(side="left")
    entry_yre.insert(0, 0)
    Label(box, text="|").pack(side="left")
    entry_ytf = Entry(box, width=7)
    entry_ytf.pack(side="left")
    entry_ytf.insert(0, 1)
    Label(box, text="Utim^").pack(side="left")
    entry_yte = Entry(box, width=7)
    entry_yte.pack(side="left")
    entry_yte.insert(0, 0)
    Label(box, text="|").pack(side="left")
    entry_yrhof = Entry(box, width=7)
    entry_yrhof.pack(side="left")
    entry_yrhof.insert(0, 1)
    Label(box, text="Urho^").pack(side="left")
    entry_yrhoe = Entry(box, width=7)
    entry_yrhoe.pack(side="left")
    entry_yrhoe.insert(0, 0)

    entry_zrf = []
    entry_zre = []
    entry_ztf = []
    entry_zte = []
    entry_zrhof = []
    entry_zrhoe = []
    entry_zlb = []
    entry_zco = []
    entry_zls = []
    entry_zargs = []
    self.Line3d_z_qt = []
    self.Line3d_z_index = []
    for i in range(self.maxline):
        Label(self.add_row(bigbox, bx=20), text="-" * 500).place(
            x=0, y=0, anchor="nw"
        )  # next
        box = self.add_row(bigbox, bx=20)
        Label(box, width=8, text="Z" + str(i + 1)).pack(side="left")
        Label(box, text="|").pack(side="left")
        self.Line3d_z_qt.append(
            ttk.Combobox(
                box, width=17, height=10, values=["x1", "x2", "x3"] + self.avqt[1]
            )
        )
        self.Line3d_z_qt[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_zrf.append(Entry(box, width=7))
        entry_zrf[-1].pack(side="left")
        entry_zrf[-1].insert(0, 1)
        Label(box, text="Ulen^").pack(side="left")
        entry_zre.append(Entry(box, width=7))
        entry_zre[-1].pack(side="left")
        entry_zre[-1].insert(0, 0)
        Label(box, text="|").pack(side="left")
        entry_ztf.append(Entry(box, width=7))
        entry_ztf[-1].pack(side="left")
        entry_ztf[-1].insert(0, 1)
        Label(box, text="Utim^").pack(side="left")
        entry_zte.append(Entry(box, width=7))
        entry_zte[-1].pack(side="left")
        entry_zte[-1].insert(0, 0)
        Label(box, text="|").pack(side="left")
        entry_zrhof.append(Entry(box, width=7))
        entry_zrhof[-1].pack(side="left")
        entry_zrhof[-1].insert(0, 1)
        Label(box, text="Urho^").pack(side="left")
        entry_zrhoe.append(Entry(box, width=7))
        entry_zrhoe[-1].pack(side="left")
        entry_zrhoe[-1].insert(0, 0)
        box = self.add_row(bigbox, bx=20)
        self.Line3d_z_index.append(
            ttk.Combobox(box, width=6, height=10, values=self.usefultindex)
        )
        self.Line3d_z_index[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_zlb.append(Entry(box, width=20))
        entry_zlb[-1].insert(0, str(None))
        entry_zlb[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_zco.append(Entry(box, width=20))
        entry_zco[-1].insert(0, str(None))
        entry_zco[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_zls.append(Entry(box, width=20))
        entry_zls[-1].insert(0, "-")
        entry_zls[-1].pack(side="left")
        Label(box, text="|").pack(side="left")
        entry_zargs.append(Entry(box, width=20))
        entry_zargs[-1].pack(side="left")
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
    Label(box, width=40, text="X limit").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Title").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    entry_fx = Entry(box, width=20)
    entry_fx.insert(0, "X")
    entry_fx.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fxa = Entry(box, width=19)
    entry_fxa.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_fxb = Entry(box, width=19)
    entry_fxb.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_ft = Entry(box, width=20)
    entry_ft.pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    Label(box, width=20, text="Y").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=40, text="Y limit").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    entry_fy = Entry(box, width=20)
    entry_fy.insert(0, "Y")
    entry_fy.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fya = Entry(box, width=19)
    entry_fya.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_fyb = Entry(box, width=19)
    entry_fyb.pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    Label(box, width=20, text="Z").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=40, text="Z limit").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="Other Args").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    entry_fz = Entry(box, width=20)
    entry_fz.insert(0, "Z")
    entry_fz.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fza = Entry(box, width=19)
    entry_fza.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_fzb = Entry(box, width=19)
    entry_fzb.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_fargs = Entry(box, width=20)
    entry_fargs.pack(side="left")
    Label(self.add_row(bigbox), text="=" * 500).place(x=0, y=0, anchor="nw")  # end

    def drawlines(event):
        try:
            x = self.get_x(
                self.Line3d_x_qt,
                entry_xrf,
                entry_xre,
                entry_xtf,
                entry_xte,
                entry_xrhof,
                entry_xrhoe,
                self.Line3d_x_index,
            )
            if str(x) == "False":
                return
            y = self.get_x(
                self.Line3d_y_qt,
                entry_yrf,
                entry_yre,
                entry_ytf,
                entry_yte,
                entry_yrhof,
                entry_yrhoe,
                self.Line3d_y_index,
            )
            if str(y) == "False":
                return
            self.tkobj.io_recv("Figuring Lines ...")
            lines = []
            for i in range(self.maxline):
                z = self.get_x(
                    self.Line3d_z_qt[i],
                    entry_zrf[i],
                    entry_zre[i],
                    entry_ztf[i],
                    entry_zte[i],
                    entry_zrhof[i],
                    entry_zrhoe[i],
                    self.Line3d_z_index[i],
                )
                if str(z) != "False":
                    lines += self.get_line(
                        self.get_lineinfo3d(
                            x,
                            y,
                            z,
                            entry_zlb[i],
                            entry_zco[i],
                            entry_zls[i],
                            entry_zargs[i],
                        )
                    )
                # get figinfo
            figureinfo = self.get_figureinfo3d(
                entry_ft,
                entry_fx,
                entry_fy,
                entry_fz,
                entry_fxa,
                entry_fxb,
                entry_fya,
                entry_fyb,
                entry_fza,
                entry_fzb,
                entry_fargs,
            )
            self.tkobj.io_recv("Collected Figureinfo:", figureinfo)

            # begining to drow

            self.pageargs["Infobj"].Config["Painter"]["P3D"].line(
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
                    "3D", "Lines"
                ) and not messagebox.askokcancel(
                    "Rewrite Confirm",
                    "Rewrite 3D line configuration " + entry_save.get() + " ?",
                ):
                    return
                self.tkobj.io_recv(
                    "Saving 3D Lines configuration",
                    entry_save.get(),
                    "...",
                    color="blue",
                )
                dd = {
                    "SavedTime": now(),
                    "xrf": entry_xrf.get(),
                    "xre": entry_xre.get(),
                    "xtf": entry_xtf.get(),
                    "xte": entry_xte.get(),
                    "xrhof": entry_xrhof.get(),
                    "xrhoe": entry_xrhoe.get(),
                    "yrf": entry_yrf.get(),
                    "yre": entry_yre.get(),
                    "ytf": entry_ytf.get(),
                    "yte": entry_yte.get(),
                    "yrhof": entry_yrhof.get(),
                    "yrhoe": entry_yrhoe.get(),
                    "fx": entry_fx.get(),
                    "fxa": entry_fxa.get(),
                    "fxb": entry_fxb.get(),
                    "ft": entry_ft.get(),
                    "fy": entry_fy.get(),
                    "fya": entry_fya.get(),
                    "fyb": entry_fyb.get(),
                    "fz": entry_fz.get(),
                    "fza": entry_fza.get(),
                    "fzb": entry_fzb.get(),
                    "fargs": entry_fargs.get(),
                }
                for i in range(self.maxline):
                    try:
                        dd["zrf" + str(i)] = entry_zrf[i].get()
                        dd["zre" + str(i)] = entry_zre[i].get()
                        dd["ztf" + str(i)] = entry_ztf[i].get()
                        dd["zte" + str(i)] = entry_zte[i].get()
                        dd["zrhof" + str(i)] = entry_zrhof[i].get()
                        dd["zrhoe" + str(i)] = entry_zrhoe[i].get()
                        dd["zlb" + str(i)] = entry_zlb[i].get()
                        dd["zco" + str(i)] = entry_zco[i].get()
                        dd["zls" + str(i)] = entry_zls[i].get()
                        dd["zargs" + str(i)] = entry_zargs[i].get()
                    except:
                        pass
                self.hdf5handler.write_config("3D", "Lines", {entry_save.get(): dd})
                reset_saved()
                self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv(err, color="red")

    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save)
