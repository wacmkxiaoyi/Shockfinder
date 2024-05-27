from tkinter import *
from tkinter import ttk, filedialog
import numpy as np
from XenonUI.XUIlib.page import str_to_float, update_entry

def page(self):
    LD = self.add_menu("Load", submenu=1)
    self.add_row(LD)
    self.add_title(LD, "Load Database")
    box = self.add_row(LD, bx=260)
    entry = Entry(box, width=20)

    def select(event):
        folder_path = filedialog.askopenfilename()
        if folder_path != "":
            update_entry(entry, folder_path, False)

    button1 = Button(box, text="Select", width=5)
    button1.bind("<ButtonRelease>", select)
    button1.pack(side="left")
    entry.pack(side="left")
    self.add_title(
        LD, "(Please check the progress in DOC window!)", fontsize=8, fg="red"
    )

    def load(event):
        if entry.get() != "":
            if self.pageargs["Infobj"].load(entry.get()):
                self.avqt = [[], [], [], []]
                self.avgr = []
                for i in self.pageargs["Infobj"].database.data[0].grid.keys():
                    self.avgr.append(i)
                for i in self.pageargs["Infobj"].database.data[0].quantities.keys():
                    if (
                        type(self.pageargs["Infobj"].database.data[0].quantities[i])
                        == np.ndarray
                    ):
                        self.avqt[
                            self.pageargs["Infobj"]
                            .database.data[0]
                            .quantities[i]
                            .ndim
                        ].append(i)
                    else:
                        try:
                            str_to_float(
                                self.pageargs["Infobj"]
                                .database.data[0]
                                .quantities[i]
                            )
                            self.avqt[0].append(i)
                        except:
                            pass
                self.reload()
                self.tkobj.io_recv("Load", entry.get(), "completed", color="green")

    def view(event):
        self.tkobj.io_recv("Collecting data in", self.LD_index.get())
        ind = self.pageargs["Infobj"].database.tindex.index(
            int(self.LD_index.get())
        )
        update_entry(x1, "")
        update_entry(x2, "")
        update_entry(x3, "")
        if "x1" in self.avgr:
            update_entry(
                x1, str(self.pageargs["Infobj"].database.data[ind].grid["x1"])
            )
        if "x2" in self.avgr:
            update_entry(
                x2, str(self.pageargs["Infobj"].database.data[ind].grid["x2"])
            )
        if "x3" in self.avgr:
            update_entry(
                x3, str(self.pageargs["Infobj"].database.data[ind].grid["x3"])
            )
        keys = list(self.pageargs["Infobj"].database.data[ind].quantities.keys())
        for i in range(self.infomation_max):
            update_entry(
                qtv[i],
                (
                    ""
                    if i >= len(keys)
                    else str(
                        self.pageargs["Infobj"]
                        .database.data[ind]
                        .quantities[keys[i]]
                    )
                ),
            )
            qtn[i].config(
                text=(
                    ""
                    if i >= len(keys)
                    else (
                        keys[i]
                        if type(
                            self.pageargs["Infobj"]
                            .database.data[ind]
                            .quantities[keys[i]]
                        )
                        != np.ndarray
                        else "("
                        + str(
                            self.pageargs["Infobj"]
                            .database.data[ind]
                            .quantities[keys[i]]
                            .ndim
                        )
                        + "D)"
                        + keys[i]
                    )
                )
            )

    button2 = Button(box, text="Load", width=5)
    button2.bind("<ButtonRelease>", load)
    button2.pack(side="left")
    self.add_row(LD)
    box = self.add_row(LD, bx=220)
    Label(box, text="Select An Index:", width=20).pack(side="left")
    self.LD_index = ttk.Combobox(box, width=5, height=10)
    self.LD_index.pack(side="left")
    button = Button(box, text="view", width=5)
    button.bind("<ButtonRelease>", view)
    button.pack(side="left")
    self.add_row(LD)
    self.add_title(LD, "Grids viewer", fg="green", fontsize=14)
    Label(self.add_row(LD), text="=" * 500).place(x=0, y=0, anchor="nw")  # begin
    box = self.add_row(LD)
    Label(box, text="Grid Name", width=10, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Grids Value", width=80, fg="green").pack(side="left")
    Label(self.add_row(LD), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(LD)
    Label(box, width=10, text="x1").pack(side="left")
    Label(box, text="| ").pack(side="left")
    x1 = Entry(box, width=80)
    x1.config(state="readonly")
    x1.pack(side="left")
    Label(self.add_row(LD), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(LD)
    Label(box, width=10, text="x2").pack(side="left")
    Label(box, text="| ").pack(side="left")
    x2 = Entry(box, width=80)
    x2.config(state="readonly")
    x2.pack(side="left")
    Label(self.add_row(LD), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
    box = self.add_row(LD)
    Label(box, width=10, text="x3").pack(side="left")
    Label(box, text="| ").pack(side="left")
    x3 = Entry(box, width=80)
    x3.config(state="readonly")
    x3.pack(side="left")
    Label(self.add_row(LD), text="=" * 500).place(x=0, y=0, anchor="nw")  # end
    self.add_row(LD)
    self.add_title(LD, "Quantities viewer", fg="green", fontsize=14)
    Label(self.add_row(LD), text="=" * 500).place(x=0, y=0, anchor="nw")  # begin
    box = self.add_row(LD)
    Label(box, text="ID", width=5, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Quantity Name", width=20, fg="green").pack(side="left")
    Label(box, text="| ").pack(side="left")
    Label(box, text="Quantity Value", width=60, fg="green").pack(side="left")
    qtn = []
    qtv = []
    for i in range(self.infomation_max):
        Label(self.add_row(LD), text="-" * 500).place(x=0, y=0, anchor="nw")  # next
        box = self.add_row(LD)
        Label(box, text=i, width=5).pack(side="left")
        Label(box, text="| ").pack(side="left")
        qtn.append(Label(box, width=20))
        qtn[-1].pack(side="left")
        Label(box, text="| ").pack(side="left")
        qtv.append(Entry(box, width=60))
        qtv[-1].config(state="readonly")
        qtv[-1].pack(side="left")
    Label(self.add_row(LD), text="=" * 500).place(x=0, y=0, anchor="nw")  # end
