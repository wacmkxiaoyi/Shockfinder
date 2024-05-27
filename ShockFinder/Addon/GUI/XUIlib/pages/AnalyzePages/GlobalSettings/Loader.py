import os
from tkinter import *
from tkinter import ttk, filedialog
from XenonUI.XUIlib.page import update_entry

def page(self):
    # Loader
    Loader = self.add_menu("Simulation Data Loader", submenu=1)
    self.pars["Loader"] = {}
    self.add_row(Loader)  # skip row (empty row)
    self.add_title(Loader, "Simulation Data Loader")
    Label(self.add_row(Loader, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(Loader, bx=150)
    Label(box, text="Type", width=20).pack(side="left")
    Label(box, text="|").pack(side="left")
    Loader_ENG = ttk.Combobox(
        box,
        width=18,
        height=5,
        values=list(self.pageargs["Infobj"].Config["Loader"].keys()),
    )
    Loader_ENG.set(list(self.pageargs["Infobj"].Config["Loader"].keys())[0])
    Loader_ENG.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_Loader_ENG(event):
        self.pars["Loader"]["Engine"] = Loader_ENG.get()
        self.tkobj.io_recv(
            "Updated Loader-Engine to", self.pars["Loader"]["Engine"]
        )

    button_fun_Loader_ENG = Button(box, text="Update", width=5)
    button_fun_Loader_ENG.bind("<ButtonRelease>", fun_Loader_ENG)
    button_fun_Loader_ENG.pack(side="left")
    self.pars["Loader"]["Engine"] = Loader_ENG.get()
    Label(self.add_row(Loader, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(Loader, bx=150)
    Label(box, text="File Dir", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    Loader_FileDir = Entry(box, width=15)
    update_entry(Loader_FileDir, os.getcwd(), False)
    Loader_FileDir.pack(side="left")

    def fun_lfd(event):
        folder_path = filedialog.askdirectory()
        if folder_path != "":
            update_entry(Loader_FileDir, folder_path, False)

    button = Button(box, text="Select", width=5)
    button.bind("<ButtonRelease>", fun_lfd)
    button.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_Loader_FileDir(event):
        self.pars["Loader"]["FileDir"] = Loader_FileDir.get()
        self.tkobj.io_recv(
            "Updated Loader-FileDir to", self.pars["Loader"]["FileDir"]
        )

    button_Loader_FileDir = Button(box, text="Update", width=5)
    button_Loader_FileDir.bind("<ButtonRelease>", fun_Loader_FileDir)
    button_Loader_FileDir.pack(side="left")
    self.pars["Loader"]["FileDir"] = Loader_FileDir.get()
    Label(self.add_row(Loader, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(Loader, bx=150)
    Label(box, text="File Prefix", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    Loader_FilePrefix = Entry(box, width=20)
    update_entry(Loader_FilePrefix, "data.", False)
    Loader_FilePrefix.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_Loader_FilePrefix(event):
        self.pars["Loader"]["FilePrefix"] = Loader_FilePrefix.get()
        self.tkobj.io_recv(
            "Updated Loader-FilePrefix to", self.pars["Loader"]["FilePrefix"]
        )

    button_Loader_FilePrefix = Button(box, text="Update", width=5)
    button_Loader_FilePrefix.bind("<ButtonRelease>", fun_Loader_FilePrefix)
    button_Loader_FilePrefix.pack(side="left")
    self.pars["Loader"]["FilePrefix"] = Loader_FilePrefix.get()
    Label(self.add_row(Loader, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(Loader, bx=150)
    Label(box, text="File Format", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    Loader_FileFormat = Entry(box, width=20)
    update_entry(Loader_FileFormat, "04d", False)
    Loader_FileFormat.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_Loader_FileFormat(event):
        self.pars["Loader"]["FileFormat"] = Loader_FileFormat.get()
        self.tkobj.io_recv(
            "Updated Loader-Format to", self.pars["Loader"]["FileFormat"]
        )

    button_Loader_FileFormat = Button(box, text="Update", width=5)
    button_Loader_FileFormat.bind("<ButtonRelease>", fun_Loader_FileFormat)
    button_Loader_FileFormat.pack(side="left")
    self.pars["Loader"]["FileFormat"] = Loader_FileFormat.get()
    Label(self.add_row(Loader, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(Loader, bx=150)
    Label(box, text="File type", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    Loader_Filetype = Entry(box, width=20)
    update_entry(Loader_Filetype, "dbl", False)
    Loader_Filetype.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_Loader_Filetype(event):
        self.pars["Loader"]["FileType"] = Loader_Filetype.get()
        self.tkobj.io_recv(
            "Updated Loader-Filetype to", self.pars["Loader"]["FileType"]
        )

    button_Loader_Filetype = Button(box, text="Update", width=5)
    button_Loader_Filetype.bind("<ButtonRelease>", fun_Loader_Filetype)
    button_Loader_Filetype.pack(side="left")
    self.pars["Loader"]["FileType"] = Loader_Filetype.get()
    Label(self.add_row(Loader, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(Loader, bx=150)
    Label(box, text="Interval", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    Loader_InterVal = Entry(box, width=20)
    update_entry(Loader_InterVal, 1, False)
    Loader_InterVal.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_Loader_InterVal(event):
        self.pars["Loader"]["Interval"] = int(Loader_InterVal.get())
        self.tkobj.io_recv(
            "Updated Loader-Interval to", self.pars["Loader"]["Interval"]
        )

    button_Loader_InterVal = Button(box, text="Update", width=5)
    button_Loader_InterVal.bind("<ButtonRelease>", fun_Loader_InterVal)
    button_Loader_InterVal.pack(side="left")
    self.pars["Loader"]["Interval"] = int(Loader_InterVal.get())
    Label(self.add_row(Loader, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    def fun_reset(
        Engine=None,
        FileDir=None,
        FilePrefix=None,
        FileFormat=None,
        FileType=None,
        Interval=None,
    ):
        if Engine:
            Loader_ENG.set(Engine)
        else:
            Loader_ENG.set(list(self.pageargs["Infobj"].Config["Loader"].keys())[0])
        fun_Loader_ENG(None)
        if FileDir:
            update_entry(Loader_FileDir, FileDir, False)
            fun_Loader_FileDir(None)
        if FileType:
            update_entry(Loader_Filetype, FileType, False)
            fun_Loader_Filetype(None)
        if FilePrefix:
            update_entry(Loader_FilePrefix, FilePrefix, False)
            fun_Loader_FilePrefix(None)
        if FileFormat:
            update_entry(Loader_FileFormat, FileFormat, False)
            fun_Loader_FileFormat(None)
        if Interval:
            update_entry(Loader_InterVal, Interval, False)
            fun_Loader_InterVal(None)

    self.con_Loader = fun_reset
