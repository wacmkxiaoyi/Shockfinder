from tkinter import *
from XenonUI.XUIlib.page import update_entry, str_clean, str_to_float

def page(self):
    # Parameters
    Parameters = self.add_menu("Parameters", submenu=1)
    self.pars["Update"] = {}
    self.add_row(Parameters)  # skip row (empty row)
    self.add_title(Parameters, "Parameters")
    Label(self.add_row(Parameters, bx=190), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(Parameters, bx=190)
    Label(box, text="Parameter Name", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Parameter Value", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Opera", width=5, fg="green").pack(side="left")
    keys = set(self.pageargs["Infobj"].testdb.data[0].quantities.keys()) - set(
        (
            "vx1",
            "vx2",
            "vx3",
            "SimTime",
            "geometry",
            "rho",
            "prs",
            "Bx1",
            "Bx2",
            "Bx3",
            "output",
            "logfile",
        )
    )

    def fun(box, entry1, entry2, button, value=None):
        def fun_del(event):
            if entry1.get() != "":
                try:
                    del self.pars["Update"][entry1.get()]
                    self.tkobj.io_recv("Delete parameter", entry1.get())
                except:
                    if event:
                        self.tkobj.io_recv(
                            "Warning: parameter",
                            entry1.get(),
                            "dosen't exist!!!",
                            color="blue",
                        )
            entry1.config(state="normal")
            entry2.config(state="normal")
            button.config(text="Save")
            button.bind("<ButtonRelease>", fun_cre)

        def fun_cre(event):
            if entry1.get() != "":
                update_entry(entry1, str_clean(entry1.get()))
                update_entry(entry2, str_clean(entry2.get()))
                self.pars["Update"][entry1.get()] = str_to_float(entry2.get())
                self.tkobj.io_recv(
                    "Add parameter",
                    entry1.get(),
                    "to",
                    self.pars["Update"][entry1.get()],
                )
                button.config(text="Modify")
                button.bind("<ButtonRelease>", fun_del)

        def fun_reset(key, value):
            fun_del(None)
            update_entry(entry1, "", False)
            update_entry(entry2, "", False)
            if key != "":
                update_entry(entry1, key)
                update_entry(entry2, value)
                fun_cre(None)

        if entry1.get() != "":  # normal
            if value is not None:
                update_entry(entry2, str(value), False)
            else:
                try:
                    update_entry(entry2, str(
                            self.pageargs["Infobj"].testdb.data[0].quantities[entry1.get()]), False)
                except Exception as err:
                    print(err)
            self.pars["Update"][entry1.get()] = str_to_float(entry2.get())
            entry1.config(state="readonly")
            entry2.config(state="readonly")
            button.config(text="Modify")
            button.bind("<ButtonRelease>", fun_del)
        else:
            button.config(text="Save")
            button.bind("<ButtonRelease>", fun_cre)
        return fun_reset

    self.con_Update = []
    for i in range(self.parmax):
        Label(self.add_row(Parameters, bx=190), text="-" * 500).place(
            x=0, y=0, anchor="nw"
        )  # next
        box = self.add_row(Parameters, bx=190)
        entry1 = Entry(box, width=20)
        if i < len(keys):
            update_entry(entry1, list(keys)[i], False)
        entry1.pack(side="left")
        Label(box, text="| ").pack(side="left")
        entry2 = Entry(box, width=20)
        entry2.pack(side="left")
        Label(box, text="| ").pack(side="left")
        button = Button(box, width=5)
        button.pack(side="left")
        self.con_Update.append(fun(box, entry1, entry2, button))
    Label(self.add_row(Parameters, bx=190), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end
