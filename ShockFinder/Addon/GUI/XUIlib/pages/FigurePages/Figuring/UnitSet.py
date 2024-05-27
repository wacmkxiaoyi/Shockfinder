from XenonUI.XUIlib.page import update_entry, str_to_float
from tkinter import *
from tkinter import ttk, messagebox
from ShockFinder.Addon.Time import now

def page(self):
    bigbox = self.add_menu("Set Units", submenu=1)
    self.add_row(bigbox)
    self.add_title(bigbox, "Units", fg="red", fontsize=22)

    # Quick box
    def reset_savedunits():
        self.tkobj.io_recv("Reseting Units set ...")
        savedbox.config(values=() + self.hdf5handler.read_units())

    self.reset_funs.append(reset_savedunits)

    def load_savedunits(event):
        if savedbox.get() == "":
            return
        try:
            self.tkobj.io_recv("Loading units", savedbox.get(), "...", color="blue")
            savedunits = self.hdf5handler.read_units(savedbox.get())
            update_entry(entry_r, savedunits["length"], False)
            update_entry(entry_t, savedunits["time"], False)
            fun_set_units(None)
            update_entry(entry_rho, savedunits["density"], False)
            fun_rho(None)
            update_entry(entry_rb, savedunits["rb"], False)
            update_entry(entry_lam, savedunits["lam"], False)
            update_entry(entry_mach, savedunits["mach"], False)
            update_entry(entry_rb, savedunits["rb"], False)
            update_entry(entry_mass, savedunits["mass"], False)
            update_entry(entry_gamma, savedunits["gamma"], False)
            update_entry(entry_rs, savedunits["rs"], False)
            update_entry(entry_theinj, savedunits["theinj"], False)
            update_entry(entry_enginj, savedunits["enginj"], False)
            update_entry(entry_mfinj, savedunits["mfinj"], False)
            update_entry(entry_rhoinj, savedunits["rhoinj"], False)
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error: unknown key", err, color="red")

    def del_savedunits(event):
        if savedbox.get() == "" or not messagebox.askokcancel(
            "Delete Confirm", "Delete unit " + savedbox.get() + " ?"
        ):
            return
        self.tkobj.io_recv("Deleting units", savedbox.get(), "...", color="blue")
        self.hdf5handler.del_units(savedbox.get())
        reset_savedunits()
        self.tkobj.io_recv("Operation completed", color="green")

    self.add_row(bigbox)
    self.add_title(bigbox, "Quick Box", fg="green")
    Label(self.add_row(bigbox, bx=100), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=100)
    Label(box, width=20, text="Saved Configurations | ").pack(side="left")
    savedbox = ttk.Combobox(
        box, width=17, height=10, values=() + self.hdf5handler.read_units()
    )
    savedbox.pack(side="left")
    Label(box, text="|", width=3).pack(side="left")
    button = Button(box, text="Delete", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", del_savedunits)
    Label(box, width=3).pack(side="left")
    button = Button(box, text="Load", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", load_savedunits)
    Label(self.add_row(bigbox, bx=100), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    self.add_row(bigbox)
    self.add_title(bigbox, "Set by manual")
    Label(self.add_row(bigbox, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=150)
    Label(box, text="length (cm)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_r = Entry(box, width=20)
    entry_r.pack(side="left")

    def fun_set_units(event):
        if entry_r.get() != "":
            try:
                self.unit_r = str_to_float(entry_r.get())
                self.tkobj.io_recv("Set unit of length to", self.unit_r, "(cm)")
                self.unit_t = str_to_float(entry_t.get())
                self.tkobj.io_recv("Set unit of time to", self.unit_t, "(s)")
                self.unit_v = self.unit_r / self.unit_t
                update_entry(entry_v, self.unit_v)
                self.tkobj.io_recv("Set unit of velocity to", self.unit_v, "(cm/s)")
            except Exception as err:
                self.tkobj.io_recv(err, color="red")

    Label(box, text="| ").pack(side="left")
    button = Button(box, text="Set", width=5)
    button.pack(side="left")
    button.bind("<ButtonRelease>", fun_set_units)
    Label(self.add_row(bigbox, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=150)
    Label(box, text="time (s)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_t = Entry(box, width=20)
    entry_t.pack(side="left")
    Label(box, text="| ").pack(side="left")
    button = Button(box, text="Set", width=5)
    button.pack(side="left")
    button.bind("<ButtonRelease>", fun_set_units)
    Label(self.add_row(bigbox, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=150)
    Label(box, text="velocity (cm/s)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_v = Entry(box, width=20)
    entry_v.pack(side="left")
    entry_v.config(state="readonly")
    Label(self.add_row(bigbox, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=150)
    Label(box, text="density (g/cm^3)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_rho = Entry(box, width=20)
    entry_rho.pack(side="left")

    def fun_rho(event):
        if entry_rho.get() != "":
            try:
                self.unit_rho = str_to_float(entry_rho.get())
                self.tkobj.io_recv(
                    "Set unit of density to", self.unit_rho, "(g/cm^3)"
                )
            except Exception as err:
                self.tkobj.io_recv(err, color="red")

    Label(box, text="| ").pack(side="left")
    button = Button(box, text="Set", width=5)
    button.pack(side="left")
    button.bind("<ButtonRelease>", fun_rho)
    Label(self.add_row(bigbox, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    def fun_equ(event=None):
        try:
            rb = str_to_float(entry_rb.get())
        except Exception as err:
            return self.tkobj.io_recv(
                "Read Outer boundary error:", err, color="red"
            )
        try:
            lam = str_to_float(entry_lam.get())
        except Exception as err:
            return self.tkobj.io_recv("Read Lambda error:", err, color="red")
        try:
            mach = str_to_float(entry_mach.get())
        except Exception as err:
            return self.tkobj.io_recv("Read Mach number error:", err, color="red")
        try:
            mass = str_to_float(entry_mass.get())
        except Exception as err:
            return self.tkobj.io_recv("Read Mass error:", err, color="red")
        try:
            gamma = str_to_float(entry_gamma.get())
        except Exception as err:
            return self.tkobj.io_recv("Read gamma error:", err, color="red")
        try:
            rs = int(entry_rs.get())
        except Exception as err:
            return self.tkobj.io_recv("Read Radius type error:", err, color="red")
        try:
            theta_inj = str_to_float(entry_theinj.get())
        except Exception as err:
            return self.tkobj.io_recv("Read Theta@Inject error:", err, color="red")
        try:
            eng = str_to_float(entry_enginj.get())
        except Exception as err:
            return self.tkobj.io_recv(
                "Read Net energy@Inject error:", err, color="red"
            )
        try:
            injflux = str_to_float(entry_mfinj.get())
        except Exception as err:
            return self.tkobj.io_recv(
                "Read Massflux@Inject error:", err, color="red"
            )
        try:
            injrho = str_to_float(entry_rhoinj.get())
        except Exception as err:
            return self.tkobj.io_recv(
                "Read Density@Inject error:", err, color="red"
            )
        hequantities = (
            self.pageargs["Infobj"]
            .Config["AnalysisLib"]["Equilibrium"]
            .Equilibrium(rb, lam, mach, gamma, rs, eng, theta_inj)
        )
        units = (
            self.pageargs["Infobj"]
            .Config["AnalysisLib"]["Equilibrium"]
            .Unit(
                mass,
                self.pageargs["Infobj"]
                .Config["AnalysisLib"]["Equilibrium"]
                .YearMassFlux_to_MassFlux(injflux),
                injrho,
                hequantities,
            )
        )
        self.unit_r = units["unit_r"]
        update_entry(entry_r, self.unit_r, False)
        self.unit_t = units["unit_t"]
        update_entry(entry_t, self.unit_t, False)
        self.unit_v = units["unit_r"] / units["unit_t"]
        update_entry(entry_v, self.unit_v)
        self.unit_rho = units["unit_rho"]
        update_entry(entry_rho, self.unit_rho, False)
        if event != None:
            self.tkobj.io_recv("Set unit of length to", self.unit_r, "(cm)")
            self.tkobj.io_recv("Set unit of time to", self.unit_t, "(s)")
            self.tkobj.io_recv("Set unit of density to", self.unit_rho, "(g/cm^3)")
            self.tkobj.io_recv("Set unit of velocity to", self.unit_v, "(cm/s)")

    self.add_row(bigbox)
    self.add_title(bigbox, "Set from Equilibrium")
    Label(self.add_row(bigbox, bx=200), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Outer boundary", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_rb = Entry(box, width=20)
    entry_rb.pack(side="left")
    update_entry(entry_rb, 200, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Lambda", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_lam = Entry(box, width=20)
    entry_lam.pack(side="left")
    update_entry(entry_lam, 1.75, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Mach number", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_mach = Entry(box, width=20)
    entry_mach.pack(side="left")
    update_entry(entry_mach, 5, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Mass", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_mass = Entry(box, width=20)
    entry_mass.pack(side="left")
    update_entry(entry_mass, 10, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="gamma", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_gamma = Entry(box, width=20)
    entry_gamma.pack(side="left")
    update_entry(entry_gamma, 4/3, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Radius type (rs)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_rs = ttk.Combobox(box, width=20, height=2, values=[1, 2])
    entry_rs.pack(side="left")
    entry_rs.set(1)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Theta@Inject", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_theinj = Entry(box, width=20)
    entry_theinj.pack(side="left")
    update_entry(entry_theinj, 0, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Net energy@Inject", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_enginj = Entry(box, width=20)
    entry_enginj.pack(side="left")
    update_entry(entry_enginj, 0, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Massflux@Inject (Msun/yr)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_mfinj = Entry(box, width=20)
    entry_mfinj.pack(side="left")
    update_entry(entry_mfinj, 6.25e-11, False)
    Label(self.add_row(bigbox, bx=200), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=200)
    Label(box, text="Density@Inject (dimle)", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_rhoinj = Entry(box, width=20)
    entry_rhoinj.pack(side="left")
    update_entry(entry_rhoinj, 1, False)
    Label(self.add_row(bigbox, bx=200), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end
    box = self.add_row(bigbox, bx=200)
    button = Button(box, text="Calculate", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", fun_equ)
    Label(box, width=5).pack(side="left")
    entry_save = Entry(box, width=15)
    entry_save.pack(side="left")
    Label(box, width=5).pack(side="left")

    def save(event):
        try:
            if entry_save != "":
                if (
                    entry_save.get() in self.hdf5handler.read_units()
                    and not messagebox.askokcancel(
                        "Rewrite Confirm", "Rewrite unit " + entry_save.get() + " ?"
                    )
                ):
                    return
                self.tkobj.io_recv(
                    "Saving units", entry_save.get(), "...", color="blue"
                )
                dd = {
                    "SavedTime": now(),
                    "length": entry_r.get(),
                    "time": entry_t.get(),
                    "density": entry_rho.get(),
                    "rb": entry_rb.get(),
                    "lam": entry_lam.get(),
                    "mach": entry_mach.get(),
                    "rb": entry_rb.get(),
                    "mass": entry_mass.get(),
                    "gamma": entry_gamma.get(),
                    "rs": entry_rs.get(),
                    "theinj": entry_theinj.get(),
                    "enginj": entry_enginj.get(),
                    "mfinj": entry_mfinj.get(),
                    "rhoinj": entry_rhoinj.get(),
                }
                self.hdf5handler.write_units({entry_save.get(): dd})
                reset_savedunits()
                self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv(err, color="red")

    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save)
    fun_equ()
