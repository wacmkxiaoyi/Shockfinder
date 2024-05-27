from tkinter import *
from tkinter import ttk
from XenonUI.XUIlib.page import update_entry, str_clean

def page(self):
    Quantities = self.add_menu("Quantities", submenu=1)
    self.add_row(Quantities)  # skip row (empty row)
    self.add_title(Quantities, "Quantities")
    Label(self.add_row(Quantities, bx=20), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(Quantities, bx=20)
    Label(box, text="Approach", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Target Quantity", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Saved Result", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Arguments", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Opera", width=5, fg="green").pack(side="left")
    operationlist = list(self.pageargs["Infobj"].Config["AnalysisTool"].keys()) + [
        "Gradient",
        "Divergence",
        "Harmonic",
        "Mean",
        "Radial",
    ]

    def get_result(qtname, qto):
        result = ""
        try:
            result = (
                self.pageargs["Infobj"]
                .Config["AnalysisTool"][qto]
                .result(qtname, qto)
            )
            if len(result) == 1:
                result = result[0]
            else:
                result = str(result)
        except:
            if qto in ("Gradient", "Divergence"):
                result = (
                    self.pageargs["Infobj"]
                    .Config["AnalysisLib"]["Differential"]
                    .result(qtname, qto)
                )
                if len(result) == 1:
                    result = result[0]
                else:
                    result = str(result)
            elif qto == "Harmonic":
                result = (
                    self.pageargs["Infobj"]
                    .Config["AnalysisLib"]["Harmonic_src"]
                    .result(qtname, qto)
                )
                if len(result) == 1:
                    result = result[0]
                else:
                    result = str(result)
            elif qto == "Mean":
                result = (
                    self.pageargs["Infobj"]
                    .Config["AnalysisLib"]["Mean_src"]
                    .result(qtname, qto)
                )
                if len(result) == 1:
                    result = result[0]
                else:
                    result = str(result)
            elif qto == "Radial":
                result = (
                    self.pageargs["Infobj"]
                    .Config["AnalysisLib"]["Radial_src"]
                    .result(qtname, qto)
                )
                if len(result) == 1:
                    result = result[0]
                else:
                    result = str(result)
        return strc_vva(result)

    def strc_vva(result):
        return (
            result.replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
        )

    def fun(index, box, cmbox1, entry2, entry3, entry4, button5, button6):
        def fun_set(event):
            update_entry(
                entry3,
                get_result(entry2.get().replace(" ", ""), cmbox1.get()).replace(
                    " ", ""
                ),
                False,
            )

        def fun_cre(event):
            if cmbox1.get() != "":
                update_entry(entry2, str_clean(entry2.get()))
                update_entry(entry3, str_clean(entry3.get()))
                update_entry(entry4, str_clean(entry4.get()))
                self.pars[f"{index}_{cmbox1.get()}"] = {}
                if strc_vva(entry2.get()) != "":
                    self.pars[f"{index}_{cmbox1.get()}"]["quantity_name"] = (
                        strc_vva(entry2.get())
                    )
                if strc_vva(entry3.get()) != "":
                    self.pars[f"{index}_{cmbox1.get()}"]["result"] = strc_vva(
                        entry3.get()
                    )
                for i in entry4.get().split(";"):
                    if i != "":
                        vi = i.split("=")
                        if len(vi) == 2:
                            qu, qv = vi
                            self.pars[f"{index}_{cmbox1.get()}"][qu] = qv.replace(
                                " ", ""
                            )
                        else:
                            self.tkobj.io_recv(
                                "Warning: arguments decode error:", i, color="blue"
                            )
                self.tkobj.io_recv(
                    "Add approach",
                    cmbox1.get(),
                    ";",
                    self.pars[f"{index}_{cmbox1.get()}"],
                )
                cmbox1.config(state="disable")
                button6.config(text="Modify")
                button6.bind("<ButtonRelease>", fun_del)

        def fun_del(event):
            if cmbox1.get() != "":
                try:
                    del self.pars[f"{index}_{cmbox1.get()}"]
                    self.tkobj.io_recv("Delete approach", cmbox1.get())
                except:
                    if event:
                        self.tkobj.io_recv(
                            "Warning: approach",
                            cmbox1.get(),
                            "dosen't exist!!!",
                            color="blue",
                        )
            cmbox1.config(state="normal")
            entry2.config(state="normal")
            entry3.config(state="normal")
            entry4.config(state="normal")
            button6.config(text="Save")
            button6.bind("<ButtonRelease>", fun_cre)

        def fun_reset(app, quantity_name, result, arguments):
            fun_del(None)
            cmbox1.set("")
            update_entry(entry2, "", False)
            update_entry(entry3, "", False)
            update_entry(entry4, "", False)
            if app != "":
                cmbox1.set(app)
                update_entry(entry2, quantity_name)
                update_entry(entry3, result)
                arg = ""
                for key, value in arguments.items():
                    arg += f"{key}={value};"
                update_entry(entry4, arg)
                fun_cre(None)

        button5.bind("<ButtonRelease>", fun_set)
        button6.bind("<ButtonRelease>", fun_cre)
        return fun_reset

    self.con_Approaches = []
    for i in range(self.parmax):
        Label(self.add_row(Quantities, bx=20), text="-" * 500).place(
            x=0, y=0, anchor="nw"
        )  # next
        box = self.add_row(Quantities, bx=20)
        cmbox1 = ttk.Combobox(
            box,
            width=18,
            height=len(operationlist) if len(operationlist) <= 10 else 10,
            values=operationlist,
        )
        cmbox1.pack(side="left")
        Label(box, text="| ").pack(side="left")
        entry2 = Entry(box, width=20)
        entry2.pack(side="left")
        Label(box, text="| ").pack(side="left")
        entry3 = Entry(box, width=14)
        entry3.pack(side="left")
        button5 = Button(box, text="Get", width=5)
        button5.pack(side="left")
        Label(box, text="| ").pack(side="left")
        entry4 = Entry(box, width=20)
        entry4.pack(side="left")
        Label(box, text="| ").pack(side="left")
        button6 = Button(box, text="Save", width=5)
        button6.pack(side="left")
        self.con_Approaches.append(
            fun(i, box, cmbox1, entry2, entry3, entry4, button5, button6)
        )
    Label(self.add_row(Quantities, bx=20), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end
