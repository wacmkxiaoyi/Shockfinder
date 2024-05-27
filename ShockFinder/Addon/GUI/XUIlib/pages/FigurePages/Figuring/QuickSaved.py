from tkinter import *
from tkinter import ttk, messagebox

def page(self):
    bigbox = self.add_menu("Quick Saved", submenu=1)
    self.add_row(bigbox)
    self.add_title(bigbox, "Quick Saved", fg="red", fontsize=24)

    def reorganize_keys(d):
        # Determine if the dictionary contains nested dictionaries
        first_value = next(iter(d.values()))
        if isinstance(first_value, dict):
            # If d is a dictionary of dictionaries
            inner_keys = list(first_value.keys())
            transformed = {
                k: {outer_k: v[k] if k in v else None for outer_k, v in d.items()}
                for k in inner_keys
            }
            return transformed
        else:
            # If d is a simple dictionary
            return {str(index): item for index, item in enumerate(d)}

    def list_to_dict(lst, attr, key=None):
        # If key is a string, convert it into a tuple
        if isinstance(key, str):
            key = (key,)

        # Extract the attribute from each object and proceed based on the key
        def extract_data(item):
            data = getattr(item, attr, None)
            if data is None:
                return None
            if isinstance(key, (tuple, list)):
                return {k: v for k, v in data.items() if k in key}
            else:
                return data

        # Get transformed data for the list
        transformed_data = {
            str(index): extract_data(item) for index, item in enumerate(lst)
        }

        # Check if any item had the attribute missing and return None if so
        if any(value is None for value in transformed_data.values()):
            return None

        return transformed_data

    self.add_row(bigbox)
    self.add_title(bigbox, "0d Data", fg="green")

    def reset_0D():
        self.tkobj.io_recv("Reseting 0d data set ...")
        box_0D.config(values=self.hdf5handler.read_data("0D"))

    self.reset_funs.append(reset_0D)

    def load_0D(event):
        if box_0D.get() == "":
            return
        varname = box_0D.get() if entry_as_0D.get() == "" else entry_as_0D.get()
        self.tkobj.io_recv(
            "Loading 0d data", box_0D.get(), "as", varname, "...", color="blue"
        )
        try:
            dataget = {varname: self.hdf5handler.read_data("0D", box_0D.get())}
            self.pageargs["Infobj"].database.update_with_index(
                **reorganize_keys(dataget)
            )
            self.avqt[0].append(varname)
            self.reload()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def save_0D(event):
        if self.box_0D.get() == "":
            return
        varname = (
            self.box_0D.get() if entry_to_0D.get() == "" else entry_to_0D.get()
        )
        if varname in self.hdf5handler.read_data(
            "0D"
        ) and not messagebox.askokcancel(
            "Rewrite Confirm", "Rewrite 0d Data " + varname + " ?"
        ):
            return
        self.tkobj.io_recv(
            "Saving 0d data", self.box_0D.get(), "to", varname, "...", color="blue"
        )
        try:
            self.hdf5handler.write_data(
                "0D",
                {
                    varname: reorganize_keys(
                        list_to_dict(
                            self.pageargs["Infobj"].database.data,
                            "quantities",
                            self.box_0D.get(),
                        )
                    )[self.box_0D.get()]
                },
            )
            reset_0D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def del_0D(event):
        if box_0D.get() == "" or not messagebox.askokcancel(
            "Delete Confirm", "Delete 0d Data " + box_0D.get() + " ?"
        ):
            return
        self.tkobj.io_recv("Deleting 0d data", box_0D.get())
        try:
            self.hdf5handler.del_data("0D", box_0D.get())
            reset_0D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Load", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    box_0D = ttk.Combobox(
        box, width=17, height=10, values=self.hdf5handler.read_data("0D")
    )
    box_0D.pack(side="left")
    Label(box, text="as").pack(side="left")
    entry_as_0D = Entry(box, width=17)
    entry_as_0D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Load", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", load_0D)
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Delete", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", del_0D)
    Label(self.add_row(bigbox, bx=130), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Save", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    self.box_0D = ttk.Combobox(box, width=17, height=10)
    self.box_0D.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_to_0D = Entry(box, width=17)
    entry_to_0D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save_0D)
    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    self.add_row(bigbox)
    self.add_title(bigbox, "1D Data", fg="green")

    def reset_1D():
        self.tkobj.io_recv("Reseting 1D data set ...")
        box_1D.config(values=self.hdf5handler.read_data("1D"))

    self.reset_funs.append(reset_1D)

    def load_1D(event):
        if box_1D.get() == "":
            return
        varname = box_1D.get() if entry_as_1D.get() == "" else entry_as_1D.get()
        self.tkobj.io_recv(
            "Loading 1D data", box_1D.get(), "as", varname, "...", color="blue"
        )
        try:
            dataget = {varname: self.hdf5handler.read_data("1D", box_1D.get())}
            self.pageargs["Infobj"].database.update_with_index(
                **reorganize_keys(dataget)
            )
            if varname not in ("x1", "x2", "x3"):
                self.avqt[1].append(varname)
            self.reload()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def save_1D(event):
        if self.box_1D.get() == "":
            return
        varname = (
            self.box_1D.get() if entry_to_1D.get() == "" else entry_to_1D.get()
        )
        if varname in self.hdf5handler.read_data(
            "1D"
        ) and not messagebox.askokcancel(
            "Rewrite Confirm", "Rewrite 1D Data " + varname + " ?"
        ):
            return
        self.tkobj.io_recv(
            "Saving 1D data", self.box_1D.get(), "to", varname, "...", color="blue"
        )
        try:
            try:
                self.hdf5handler.write_data(
                    "1D",
                    {
                        varname: reorganize_keys(
                            list_to_dict(
                                self.pageargs["Infobj"].database.data,
                                "quantities",
                                self.box_1D.get(),
                            )
                        )[self.box_1D.get()]
                    },
                )
            except:
                self.tkobj.io_recv(
                    self.box_1D.get(),
                    "no found in quantities libaries, try to find in grid libaries...",
                )
                self.hdf5handler.write_data(
                    "1D",
                    {
                        varname: reorganize_keys(
                            list_to_dict(
                                self.pageargs["Infobj"].database.data,
                                "grid",
                                self.box_1D.get(),
                            )
                        )[self.box_1D.get()]
                    },
                )
            reset_1D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def del_1D(event):
        if box_1D.get() == "" or not messagebox.askokcancel(
            "Delete Confirm", "Delete 1D Data " + box_1D.get() + " ?"
        ):
            return
        self.tkobj.io_recv("Deleting 1D data", box_1D.get())
        try:
            self.hdf5handler.del_data("1D", box_1D.get())
            reset_1D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Load", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    box_1D = ttk.Combobox(
        box, width=17, height=10, values=self.hdf5handler.read_data("1D")
    )
    box_1D.pack(side="left")
    Label(box, text="as").pack(side="left")
    entry_as_1D = Entry(box, width=17)
    entry_as_1D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Load", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", load_1D)
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Delete", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", del_1D)
    Label(self.add_row(bigbox, bx=130), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Save", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    self.box_1D = ttk.Combobox(box, width=17, height=10)
    self.box_1D.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_to_1D = Entry(box, width=17)
    entry_to_1D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save_1D)
    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    self.add_row(bigbox)
    self.add_title(bigbox, "2D Data", fg="green")

    def reset_2D():
        self.tkobj.io_recv("Reseting 2D data set ...")
        box_2D.config(values=self.hdf5handler.read_data("2D"))

    self.reset_funs.append(reset_2D)

    def load_2D(event):
        if box_2D.get() == "":
            return
        varname = box_2D.get() if entry_as_2D.get() == "" else entry_as_2D.get()
        self.tkobj.io_recv(
            "Loading 2D data", box_2D.get(), "as", varname, "...", color="blue"
        )
        try:
            dataget = {varname: self.hdf5handler.read_data("2D", box_2D.get())}
            self.pageargs["Infobj"].database.update_with_index(
                **reorganize_keys(dataget)
            )
            self.avqt[2].append(varname)
            self.reload()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def save_2D(event):
        if self.box_2D.get() == "":
            return
        varname = (
            self.box_2D.get() if entry_to_2D.get() == "" else entry_to_2D.get()
        )
        if varname in self.hdf5handler.read_data(
            "2D"
        ) and not messagebox.askokcancel(
            "Rewrite Confirm", "Rewrite 2D Data " + varname + " ?"
        ):
            return
        self.tkobj.io_recv(
            "Saving 2D data", self.box_2D.get(), "to", varname, "...", color="blue"
        )
        try:
            self.hdf5handler.write_data(
                "2D",
                {
                    varname: reorganize_keys(
                        list_to_dict(
                            self.pageargs["Infobj"].database.data,
                            "quantities",
                            self.box_2D.get(),
                        )
                    )[self.box_2D.get()]
                },
            )
            reset_2D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def del_2D(event):
        if box_2D.get() == "" or not messagebox.askokcancel(
            "Delete Confirm", "Delete 2D Data " + box_2D.get() + " ?"
        ):
            return
        self.tkobj.io_recv("Deleting 2D data", box_2D.get())
        try:
            self.hdf5handler.del_data("2D", box_2D.get())
            reset_2D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Load", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    box_2D = ttk.Combobox(
        box, width=17, height=10, values=self.hdf5handler.read_data("2D")
    )
    box_2D.pack(side="left")
    Label(box, text="as").pack(side="left")
    entry_as_2D = Entry(box, width=17)
    entry_as_2D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Load", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", load_2D)
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Delete", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", del_2D)
    Label(self.add_row(bigbox, bx=130), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Save", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    self.box_2D = ttk.Combobox(box, width=17, height=10)
    self.box_2D.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_to_2D = Entry(box, width=17)
    entry_to_2D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save_2D)
    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end

    self.add_row(bigbox)
    self.add_title(bigbox, "3D Data", fg="green")

    def reset_3D():
        self.tkobj.io_recv("Reseting 3D data set ...")
        box_3D.config(values=self.hdf5handler.read_data("3D"))

    self.reset_funs.append(reset_3D)

    def load_3D(event):
        if box_3D.get() == "":
            return
        varname = box_3D.get() if entry_as_3D.get() == "" else entry_as_3D.get()
        self.tkobj.io_recv(
            "Loading 3D data", box_3D.get(), "as", varname, "...", color="blue"
        )
        try:
            dataget = {varname: self.hdf5handler.read_data("3D", box_3D.get())}
            self.pageargs["Infobj"].database.update_with_index(
                **reorganize_keys(dataget)
            )
            self.avqt[3].append(varname)
            self.reload()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def save_3D(event):
        if self.box_3D.get() == "":
            return
        varname = (
            self.box_3D.get() if entry_to_3D.get() == "" else entry_to_3D.get()
        )
        if varname in self.hdf5handler.read_data(
            "3D"
        ) and not messagebox.askokcancel(
            "Rewrite Confirm", "Rewrite 3D Data " + varname + " ?"
        ):
            return
        self.tkobj.io_recv(
            "Saving 3D data", self.box_3D.get(), "to", varname, "...", color="blue"
        )
        try:
            self.hdf5handler.write_data(
                "3D",
                {
                    varname: reorganize_keys(
                        list_to_dict(
                            self.pageargs["Infobj"].database.data,
                            "quantities",
                            self.box_3D.get(),
                        )
                    )[self.box_3D.get()]
                },
            )
            reset_3D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    def del_3D(event):
        if box_3D.get() == "" or not messagebox.askokcancel(
            "Delete Confirm", "Delete 3D Data " + box_3D.get() + " ?"
        ):
            return
        self.tkobj.io_recv("Deleting 3D data", box_3D.get())
        try:
            self.hdf5handler.del_data("3D", box_3D.get())
            reset_3D()
            self.tkobj.io_recv("Operation completed", color="green")
        except Exception as err:
            self.tkobj.io_recv("Error:", err, color="red")

    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # begin
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Load", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    box_3D = ttk.Combobox(
        box, width=17, height=10, values=self.hdf5handler.read_data("3D")
    )
    box_3D.pack(side="left")
    Label(box, text="as").pack(side="left")
    entry_as_3D = Entry(box, width=17)
    entry_as_3D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Load", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", load_3D)
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Delete", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", del_3D)
    Label(self.add_row(bigbox, bx=130), text="-" * 500).place(
        x=0, y=0, anchor="nw"
    )  # next
    box = self.add_row(bigbox, bx=130)
    Label(box, text="Save", width=5).pack(side="left")
    Label(box, text="|").pack(side="left")
    self.box_3D = ttk.Combobox(box, width=17, height=10)
    self.box_3D.pack(side="left")
    Label(box, text="to").pack(side="left")
    entry_to_3D = Entry(box, width=17)
    entry_to_3D.pack(side="left")
    Label(box, text="|").pack(side="left")
    button = Button(box, text="Save", width=10)
    button.pack(side="left")
    button.bind("<ButtonRelease>", save_3D)
    Label(self.add_row(bigbox, bx=130), text="=" * 500).place(
        x=0, y=0, anchor="nw"
    )  # end
