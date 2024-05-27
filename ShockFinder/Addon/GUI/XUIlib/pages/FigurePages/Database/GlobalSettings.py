import os
from XenonUI.XUIlib.page import update_entry
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from ShockFinder.Config import ShockFinderDir
from multiprocessing import cpu_count

def page(self):
    GS = self.add_menu("Global Setting", submenu=1)
    self.add_row(GS)
    self.add_title(GS, "Global Setting")
    Label(self.add_row(GS, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(GS, bx=150)
    Label(box, text="Saved File", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    entry_SF = Entry(box, width=20)
    update_entry(entry_SF, os.path.join(ShockFinderDir, "SavedFigures.hdf5"), False)
    entry_SF.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def select_SF(event):
        folder_path = filedialog.askopenfilename()
        if folder_path != "":
            update_entry(entry_SF, folder_path, False)

    button_SF_SE = Button(box, text="Select", width=5)
    button_SF_SE.bind("<ButtonRelease>", select_SF)
    button_SF_SE.pack(side="left")
    Label(box, width=2).pack(side="left")

    def fun_SF(event):
        if entry_SF.get() != "" and (
            not os.path.exists(entry_SF.get())
            or self.hdf5handler.is_valid_hdf5(entry_SF.get())
            or messagebox.askokcancel(
                "Recreate Confirm",
                "The selected file is not a ShockFinder storage file, do you wish to create a new file?",
            )
        ):
            self.hdf5handler.set_file(entry_SF.get())
            [i() for i in self.reset_funs]

    button_SF = Button(box, text="Load", width=5)
    button_SF.bind("<ButtonRelease>", fun_SF)
    button_SF.pack(side="left")
    fun_SF(None)
    Label(self.add_row(GS, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(GS, bx=150)
    Label(box, text="Multi-Process Engine", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    egs = list(self.pageargs["Infobj"].Config["MultiprocessEngine"].keys()) + [None]
    MPE_ENG = ttk.Combobox(
        box, width=18, height=len(egs) if len(egs) <= 10 else 10, values=egs
    )
    if (
        self.pageargs["Infobj"].Default_MPE
        in self.pageargs["Infobj"].Config["MultiprocessEngine"]
    ):
        MPE_ENG.set(self.pageargs["Infobj"].Default_MPE)
    else:
        MPE_ENG.set(str(egs[0]))
    MPE_ENG.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_mpeeng(event):
        self.pageargs["Infobj"].set_MPE(MPE_ENG.get())
        self.tkobj.io_recv(
            "Updated Multi-process Engine to",
            self.pageargs["Infobj"].MultiprocessEngine,
        )

    button_mpeeng = Button(box, text="Update", width=5)
    button_mpeeng.bind("<ButtonRelease>", fun_mpeeng)
    button_mpeeng.pack(side="left")
    Label(self.add_row(GS, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(GS, bx=150)
    Label(box, text="Cores Num", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    MPE_PNUM = Entry(box, width=20)
    update_entry(MPE_PNUM, self.pageargs["Infobj"].LMPEINFO["pnum"], False)
    MPE_PNUM.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_MPE_PNUM(event):
        if (
            int(MPE_PNUM.get())
            > cpu_count() - self.pageargs["Infobj"].LMPEINFO["cpu_leave"]
        ):
            update_entry(
                MPE_PNUM,
                cpu_count() - self.pageargs["Infobj"].LMPEINFO["cpu_leave"],
                False,
            )
            self.pageargs["Infobj"].LMPEINFO["pnum"] = int(MPE_PNUM.get())
            self.tkobj.io_recv(
                "Updated Multi-process cores num to",
                self.pageargs["Infobj"].LMPEINFO["pnum"],
                "(Exceed upper limit,",
                self.pageargs["Infobj"].LMPEINFO["cpu_leave"],
                " used for maintaining system stable)",
                color="blue",
            )
        else:
            self.pageargs["Infobj"].LMPEINFO["pnum"] = int(MPE_PNUM.get())
            self.tkobj.io_recv(
                "Updated Multi-process cores num to",
                self.pageargs["Infobj"].LMPEINFO["pnum"],
            )

    button_MPE_PNUM = Button(box, text="Update", width=5)
    button_MPE_PNUM.bind("<ButtonRelease>", fun_MPE_PNUM)
    button_MPE_PNUM.pack(side="left")
    Label(self.add_row(GS, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(GS, bx=150)
    Label(box, text="Database Storage Engine", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    egs = list(self.pageargs["Infobj"].Config["IO"].keys())
    IO_ENG = ttk.Combobox(
        box, width=18, height=len(egs) if len(egs) <= 10 else 10, values=egs
    )
    if self.pageargs["Infobj"].Default_IO in self.pageargs["Infobj"].Config["IO"]:
        IO_ENG.set(self.pageargs["Infobj"].Default_IO)
    else:
        IO_ENG.set(egs[0])
    IO_ENG.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_IOENG(event):
        self.pageargs["Infobj"].set_IO(IO_ENG.get())
        self.tkobj.io_recv("Updated IO Engine to", self.pageargs["Infobj"].IO)

    button_IOENG = Button(box, text="Update", width=5)
    button_IOENG.bind("<ButtonRelease>", fun_IOENG)
    button_IOENG.pack(side="left")
    Label(self.add_row(GS, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end
