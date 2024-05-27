from tkinter import *
from tkinter import ttk, filedialog
from XenonUI.XUIlib.page import update_entry

def page(self):
    # Loader
    IO = self.add_menu("Database Storage", submenu=1)
    self.pars["IO"] = {}
    self.add_row(IO)  # skip row (empty row)
    self.add_title(IO, "After-Analysis Data Storage")
    Label(self.add_row(IO, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(IO, bx=150)
    Label(box, text="Engine", width=20).pack(side="left")
    Label(box, text="|").pack(side="left")
    IO_ENG = ttk.Combobox(
        box,
        width=18,
        height=5,
        values=list(self.pageargs["Infobj"].Config["IO"].keys()),
    )
    if self.pageargs["Infobj"].Default_IO in self.pageargs["Infobj"].Config["IO"]:
        IO_ENG.set(self.pageargs["Infobj"].Default_IO)
    else:
        IO_ENG.set(list(self.pageargs["Infobj"].Config["IO"].keys())[0])
    IO_ENG.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_IO_ENG(event):
        self.pars["IO"]["Engine"] = IO_ENG.get()
        self.tkobj.io_recv("Updated IO-Engine to", self.pars["IO"]["Engine"])

    button_IO_ENG = Button(box, text="Update", width=5)
    button_IO_ENG.bind("<ButtonRelease>", fun_IO_ENG)
    button_IO_ENG.pack(side="left")
    self.pars["IO"]["Engine"] = IO_ENG.get()
    Label(self.add_row(IO, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(IO, bx=150)
    Label(box, text="Project name", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    IO_filename = Entry(box, width=15)
    IO_filename.pack(side="left")

    def fun_lfd(event):
        folder_path = filedialog.asksaveasfilename()
        if folder_path != "":
            update_entry(IO_filename, folder_path, False)

    button = Button(box, text="Select", width=5)
    button.bind("<ButtonRelease>", fun_lfd)
    button.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_filename(event):
        if IO_filename.get() != "":
            self.pars["IO"]["filename"] = IO_filename.get()
            self.tkobj.io_recv(
                "Updated IO-filename to", self.pars["IO"]["filename"]
            )
        else:
            if "filename" in self.pars["IO"].keys():
                del self.pars["IO"]

    button_filename = Button(box, text="Update", width=5)
    button_filename.bind("<ButtonRelease>", fun_filename)
    button_filename.pack(side="left")
    if IO_filename.get() != "":
        self.pars["IO"]["filename"] = IO_filename.get()
    Label(self.add_row(IO, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(IO, bx=150)
    Label(box, text="Drop Buffer", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    IO_DropBuffer = ttk.Combobox(box, width=18, height=2, values=[True, False])
    IO_DropBuffer.set(str(True))
    IO_DropBuffer.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_DropBuffer(event):
        self.pars["IO"]["DropBuffer"] = (
            True if IO_DropBuffer.get() == "True" else False
        )
        self.tkobj.io_recv(
            "Updated IO-DropBuffer to", self.pars["IO"]["DropBuffer"]
        )

    self.pars["IO"]["DropBuffer"] = True if IO_DropBuffer.get() == "True" else False
    button_DropBuffer = Button(box, text="Update", width=5)
    button_DropBuffer.bind("<ButtonRelease>", fun_DropBuffer)
    button_DropBuffer.pack(side="left")
    Label(self.add_row(IO, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    def fun_reset(Engine=None, filename=None, DropBuffer=None):
        if Engine:
            IO_ENG.set(Engine)
            fun_IO_ENG(None)
        if filename:
            update_entry(IO_filename, filename, False)
            fun_filename(None)
        if DropBuffer:
            update_entry(IO_DropBuffer, DropBuffer, False)
            fun_DropBuffer(None)

    self.con_IO = fun_reset
