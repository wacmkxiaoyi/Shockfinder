from XenonUI.XUIlib.page import update_entry, str_to_float
# logo=os.path.join("ShockFinder","Addon","GUI","XUIlib","image","F.png")
from ShockFinder.Addon.Time import now
from tkinter import *
from tkinter import ttk, messagebox


def page(self):
    bigbox = self.add_menu("Scatter", submenu=2)
    self.add_row(bigbox)
    self.add_title(bigbox, "3D Scatter", fg="red", fontsize=24)
    self.add_title(bigbox, "(3D Scatter 3d)", fontsize=10)

    def reset_saved():
        self.tkobj.io_recv("Reseting 3D Scatter configuration ...")
        savedbox.config(values=() + self.hdf5handler.read_config("3D", "Scatter"))

    self.reset_funs.append(reset_saved)

    def load_saved(event):
        if savedbox.get() == "":
            return
        try:
            self.tkobj.io_recv(
                "Loading 3D Scatter configuration",
                savedbox.get(),
                "...",
                color="blue",
            )
            savedcfg = self.hdf5handler.read_config("3D", "Scatter", savedbox.get())
            update_entry(entry_vrf, savedcfg["vrf"], False)
            update_entry(entry_vre, savedcfg["vre"], False)
            update_entry(entry_vtf, savedcfg["vtf"], False)
            update_entry(entry_vte, savedcfg["vte"], False)
            update_entry(entry_vrhof, savedcfg["vrhof"], False)
            update_entry(entry_vrhoe, savedcfg["vrhoe"], False)
            update_entry(entry_vargs, savedcfg["vargs"], False)
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
            "Delete 3D Scatter configuration " + savedbox.get() + " ?",
        ):
            return
        self.tkobj.io_recv(
            "Deleting 3D Scatter configuration", savedbox.get(), "...", color="blue"
        )
        self.hdf5handler.del_config("3D", "Scatter", savedbox.get())
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
        values=() + self.hdf5handler.read_config("3D", "Scatter"),
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
    self.add_title(bigbox, "Scatter infomation", fg="green")
    Label(self.add_row(bigbox), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox)
    Label(box, width=20, text="Quantity").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="unit of length").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="unit of time").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=20, text="unit of density").pack(side="left")
    box = self.add_row(bigbox)
    Label(box, width=20, text="Index").pack(side="left")
    Label(box, text="|").pack(side="left")
    Label(box, width=80, text="Other Arguments").pack(side="left")
    Label(self.add_row(bigbox), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(bigbox)
    self.P3DCat_Qt = ttk.Combobox(box, width=17, height=10, values=self.avqt[3])
    self.P3DCat_Qt.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_vrf = Entry(box, width=7)
    entry_vrf.pack(side="left")
    entry_vrf.insert(0, 1)
    Label(box, text="Ulen^").pack(side="left")
    entry_vre = Entry(box, width=7)
    entry_vre.pack(side="left")
    entry_vre.insert(0, 0)
    Label(box, text="|").pack(side="left")
    entry_vtf = Entry(box, width=7)
    entry_vtf.pack(side="left")
    entry_vtf.insert(0, 1)
    Label(box, text="Utim^").pack(side="left")
    entry_vte = Entry(box, width=7)
    entry_vte.pack(side="left")
    entry_vte.insert(0, 0)
    Label(box, text="|").pack(side="left")
    entry_vrhof = Entry(box, width=7)
    entry_vrhof.pack(side="left")
    entry_vrhof.insert(0, 1)
    Label(box, text="Urho^").pack(side="left")
    entry_vrhoe = Entry(box, width=7)
    entry_vrhoe.pack(side="left")
    entry_vrhoe.insert(0, 0)
    box = self.add_row(bigbox)
    self.P3DCat_index = ttk.Combobox(
        box, width=17, height=10, values=self.usefultindex
    )
    self.P3DCat_index.pack(side="left")
    Label(box, text="|").pack(side="left")
    entry_vargs = Entry(box, width=66)
    entry_vargs.pack(side="left")
    Label(self.add_row(bigbox), text="=" * 500).place(x=0, y=0, anchor="nw")  # end

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

    def drawsur3d(event):
        if self.P3DCat_Qt.get() == "" or self.P3DCat_index.get() == "":
            return
        try:
            self.tkobj.io_recv("Figuring Scatter with", self.P3DCat_Qt.get(), "...")
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
            factor = 1
            factor *= str_to_float(entry_vrf.get()) * self.unit_r ** str_to_float(
                entry_vre.get()
            )
            factor *= str_to_float(entry_vtf.get()) * self.unit_t ** str_to_float(
                entry_vte.get()
            )
            factor *= str_to_float(
                entry_vrhof.get()
            ) * self.unit_rho ** str_to_float(entry_vrhoe.get())
            ind = self.pageargs["Infobj"].database.tindex.index(
                int(self.P3DSur_index.get())
            )
            try:
                x = self.pageargs["Infobj"].database.data[ind].grid["x1"]
            except:
                x = self.pageargs["Infobj"].database.data[ind].quantities["x1"]
            try:
                y = self.pageargs["Infobj"].database.data[ind].grid["x2"]
            except:
                y = self.pageargs["Infobj"].database.data[ind].quantities["x2"]
            try:
                z = self.pageargs["Infobj"].database.data[ind].grid["x3"]
            except:
                z = self.pageargs["Infobj"].database.data[ind].quantities["x3"]

            if self.P3DCat_Qt.get() not in self.pageargs["Infobj"].database.data[ind].quantities:
                raise IndexError(f'The simulation dose not run to {ind}')

            v = (
                self.pageargs["Infobj"]
                .database.data[ind]
                .quantities[self.P3DCat_Qt.get()]
                * factor
            )
            if (
                self.pageargs["Infobj"].database.data[ind].quantities["geometry"]
                == "SPHERICAL"
            ):
                x, y, z, v = (
                    self.pageargs["Infobj"]
                    .Config["Painter"]["Basic"]
                    .rtp_to_xyz(x, y, z, v)
                )
            elif (
                self.pageargs["Infobj"].database.data[ind].quantities["geometry"]
                == "POLAR"
            ):
                x, y, z, v = (
                    self.pageargs["Infobj"]
                    .Config["Painter"]["Basic"]
                    .rzp_to_xyz(x, z, y, v)
                )  # rzp->xzy
            Scatterinfo = self.get_scatter3d(x, y, z, v, entry_vargs)
            self.tkobj.io_recv("Collected Scatterinfo:", Scatterinfo)
            Scatter = (
                self.pageargs["Infobj"]
                .Config["Painter"]["Scatter"]
                .CreateScatter(**Scatterinfo)
            )
            self.pageargs["Infobj"].Config["Painter"]["P3D"].scatter(
                Scatter, **figureinfo
            )
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Figuring failure, error:", err, color="red")

    box = self.add_row(bigbox, bx=200)
    button = Button(box, text="Draw", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", drawsur3d)
    Label(box, width=5).pack(side="left")
    entry_save = Entry(box, width=15)
    entry_save.pack(side="left")
    Label(box, width=5).pack(side="left")

    def save(event):
        try:
            if entry_save != "":
                if entry_save.get() in self.hdf5handler.read_config(
                    "3D", "Scatter"
                ) and not messagebox.askokcancel(
                    "Rewrite Confirm",
                    "Rewrite 3D Scatter configuration " + entry_save.get() + " ?",
                ):
                    return
                self.tkobj.io_recv(
                    "Saving 3D Scatter configuration",
                    entry_save.get(),
                    "...",
                    color="blue",
                )
                dd = {
                    "SavedTime": now(),
                    "vrf": entry_vrf.get(),
                    "vre": entry_vre.get(),
                    "vtf": entry_vtf.get(),
                    "vte": entry_vte.get(),
                    "vrhof": entry_vrhof.get(),
                    "vrhoe": entry_vrhoe.get(),
                    "vargs": entry_vargs.get(),
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
                self.hdf5handler.write_config(
                    "3D", "Scatter", {entry_save.get(): dd}
                )
                reset_saved()
                self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv(err, color="red")

    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save)
