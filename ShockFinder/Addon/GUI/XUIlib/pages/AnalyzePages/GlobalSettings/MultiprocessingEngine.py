from tkinter import *
from tkinter import ttk, filedialog
from multiprocessing import cpu_count
from XenonUI.XUIlib.page import update_entry

def page(self):
    MPE = self.add_menu("Multi-process", submenu=1)
    self.pars["MultiprocessEngine"] = {}
    # Multiprocessing
    self.add_row(MPE)  # skip row (empty row)
    self.add_title(MPE, "Multi-process")
    Label(self.add_row(MPE, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(MPE, bx=150)
    Label(box, text="Engine", width=20).pack(side="left")
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
        self.pars["MultiprocessEngine"]["Engine"] = MPE_ENG.get()
        self.tkobj.io_recv(
            "Updated MultiprocessEngine-Engine to",
            self.pars["MultiprocessEngine"]["Engine"],
        )

    self.pars["MultiprocessEngine"]["Engine"] = MPE_ENG.get()
    button_mpeeng = Button(box, text="Update", width=5)
    button_mpeeng.bind("<ButtonRelease>", fun_mpeeng)
    button_mpeeng.pack(side="left")
    Label(self.add_row(MPE, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(MPE, bx=150)
    Label(box, text="Cores Num", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    MPE_PNUM = Entry(box, width=20)
    update_entry(MPE_PNUM, cpu_count() if cpu_count() <= 4 and cpu_count() > 1 else 4 if cpu_count() > 4 else 1, False)
    MPE_PNUM.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_MPE_PNUM(event):
        self.pars["MultiprocessEngine"]["pnum"] = int(MPE_PNUM.get())
        self.tkobj.io_recv(
            "Updated MultiprocessEngine-pnum to",
            self.pars["MultiprocessEngine"]["pnum"],
        )

    self.pars["MultiprocessEngine"]["pnum"] = int(MPE_PNUM.get())
    button_MPE_PNUM = Button(box, text="Update", width=5)
    button_MPE_PNUM.bind("<ButtonRelease>", fun_MPE_PNUM)
    button_MPE_PNUM.pack(side="left")
    Label(self.add_row(MPE, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(MPE, bx=150)
    Label(box, text="Use log", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    MPE_do_with_log = ttk.Combobox(box, width=18, height=2, values=[True, False])
    MPE_do_with_log.set(str(True))
    MPE_do_with_log.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_button_do_with_log(event):
        self.pars["MultiprocessEngine"]["do_with_log"] = (
            True if MPE_do_with_log.get() == "True" else False
        )
        self.tkobj.io_recv(
            "Updated MultiprocessEngine-do_with_log to",
            self.pars["MultiprocessEngine"]["do_with_log"],
        )

    self.pars["MultiprocessEngine"]["do_with_log"] = (
        True if MPE_do_with_log.get() == "True" else False
    )
    button_do_with_log = Button(box, text="Update", width=5)
    button_do_with_log.bind("<ButtonRelease>", fun_button_do_with_log)
    button_do_with_log.pack(side="left")
    Label(self.add_row(MPE, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(MPE, bx=150)
    Label(box, text="Log file", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    MPE_logfile = Entry(box, width=15)
    update_entry(MPE_logfile, str(None), False)
    MPE_logfile.pack(side="left")

    def fun_selete_logfile(event):
        folder_path = filedialog.asksaveasfilename()
        if folder_path != "":
            update_entry(MPE_logfile, folder_path, False)

    button = Button(box, text="Select", width=5)
    button.bind("<ButtonRelease>", fun_selete_logfile)
    button.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_logfile(event):
        if MPE_logfile.get() != "":
            self.pars["MultiprocessEngine"]["logfile"] = (
                None if MPE_logfile.get() == "None" else MPE_logfile.get()
            )
            self.tkobj.io_recv(
                "Updated MultiprocessEngine-logfile to",
                self.pars["MultiprocessEngine"]["logfile"],
            )

    self.pars["MultiprocessEngine"]["logfile"] = (
        None if MPE_logfile.get() == "None" else MPE_logfile.get()
    )
    button_logfile = Button(box, text="Update", width=5)
    button_logfile.bind("<ButtonRelease>", fun_logfile)
    button_logfile.pack(side="left")
    Label(self.add_row(MPE, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(MPE, bx=150)
    Label(box, text="Show MPE info", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    MPE_show_version_info = ttk.Combobox(
        box, width=18, height=2, values=[True, False]
    )
    MPE_show_version_info.set(str(True))
    MPE_show_version_info.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_show_version_info(event):
        self.pars["MultiprocessEngine"]["show_version_info"] = (
            True if MPE_show_version_info.get() == "True" else False
        )
        self.tkobj.io_recv(
            "Updated MultiprocessEngine-show_version_info to",
            self.pars["MultiprocessEngine"]["show_version_info"],
        )

    button_show_version_info = Button(box, text="Update", width=5)
    button_show_version_info.bind("<ButtonRelease>", fun_show_version_info)
    button_show_version_info.pack(side="left")
    self.pars["MultiprocessEngine"]["show_version_info"] = (
        True if MPE_show_version_info.get() == "True" else False
    )
    Label(self.add_row(MPE, bx=150), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(MPE, bx=150)
    Label(box, text="Show log in screen", width=20).pack(side="left")
    Label(box, text="| ").pack(side="left")
    MPE_print_in_screen = ttk.Combobox(
        box, width=18, height=2, values=[True, False]
    )
    MPE_print_in_screen.set(str(True))
    MPE_print_in_screen.pack(side="left")
    Label(box, text="| ").pack(side="left")

    def fun_sprint_in_screen(event):
        self.pars["MultiprocessEngine"]["print_in_screen"] = (
            True if MPE_print_in_screen.get() == "True" else False
        )
        self.tkobj.io_recv(
            "Updated MultiprocessEngine-print_in_screen to",
            self.pars["MultiprocessEngine"]["print_in_screen"],
        )

    self.pars["MultiprocessEngine"]["print_in_screen"] = (
        True if MPE_print_in_screen.get() == "True" else False
    )
    button_print_in_screen = Button(box, text="Update", width=5)
    button_print_in_screen.bind("<ButtonRelease>", fun_sprint_in_screen)
    button_print_in_screen.pack(side="left")
    Label(self.add_row(MPE, bx=150), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    def fun_reset(
        Engine=None,
        pnum=None,
        do_with_log=None,
        logfile=None,
        show_version_info=None,
        print_in_screen=None,
    ):
        if Engine:
            MPE_ENG.set(Engine)
            fun_mpeeng(None)
        if pnum:
            update_entry(MPE_PNUM, pnum, False)
            fun_MPE_PNUM(None)
        if do_with_log:
            MPE_do_with_log.set(do_with_log)
            fun_button_do_with_log(None)
        if logfile:
            update_entry(MPE_logfile, logfile, False)
            fun_logfile(None)
        if show_version_info:
            MPE_show_version_info.set(show_version_info)
            fun_show_version_info(None)
        if print_in_screen:
            MPE_print_in_screen.set(print_in_screen)
            fun_sprint_in_screen(None)

    self.con_MultiprocessEngine = fun_reset
