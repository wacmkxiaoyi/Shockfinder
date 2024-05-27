import h5py
import os
import numpy as np


class ShockFinderFiguresHDF5:
    def __init__(self, output=print):
        self.filename = None
        self.output = output

    def set_file(self, filename):
        self.filename = filename
        if not self.is_valid_hdf5():
            self.create_new_hdf5()

    def is_valid_hdf5(self, filename=None):
        if filename == None:
            filename = self.filename
        if filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return False

        try:
            with h5py.File(filename, "r") as f:
                if (
                    "HDF5LABEL" in f.attrs
                    and f.attrs["HDF5LABEL"] == "ShockFinderSavedFile"
                ):
                    return True
        except:
            pass
        return False

    def create_new_hdf5(self):
        with h5py.File(self.filename, "w") as f:
            f.attrs["HDF5LABEL"] = "ShockFinderSavedFile"

            # Create primary groups
            f.create_group("Data")
            f.create_group("Units")
            configurations = f.create_group("Configurations")

            # Create subgroups for Data
            for dimension in ["0D", "1D", "2D", "3D"]:
                f.create_group(f"Data/{dimension}")

            # Create subgroups for Configurations
            config_2d = configurations.create_group("2D")
            config_3d = configurations.create_group("3D")

            # Second-level subgroups for Configurations/2d
            for subgroup in ["TimeSequency", "FFT", "Lines", "Surfaces"]:
                config_2d.create_group(subgroup)

            # Second-level subgroups for Configurations/3d
            for subgroup in ["TimeSequency", "Lines", "Surfaces", "Scatter"]:
                config_3d.create_group(subgroup)

    def read_units(self, group_name=None):
        if self.filename == None:
            self.output("Error: no vaild hdf5 file selected")
            return {}
        data = {}
        with h5py.File(self.filename, "r") as f:
            units_group = f["Units"]

            def read_subgroup(subgroup):
                subgroup_data = {}
                for key in subgroup.keys():
                    value = subgroup[key][()]
                    if isinstance(value, bytes):
                        value = value.decode()
                    subgroup_data[key] = value
                return subgroup_data

            if group_name:
                if group_name in units_group:
                    return read_subgroup(
                        units_group[group_name]
                    )  # Return a one-level dictionary
                self.output(f"Unit '{group_name}' does not exist.")
                return {}

            return tuple(units_group.keys())  # only return keys
            for subgroup_name in units_group.keys():
                data[subgroup_name] = read_subgroup(units_group[subgroup_name])

        return data

    def write_units(self, data_dict):
        if self.filename == None:
            self.output("Error: no vaild hdf5 file selected")
            return None
        with h5py.File(self.filename, "a") as f:
            units_group = f.require_group("Units")

            for subgroup_name, subgroup_data in data_dict.items():
                subgroup = units_group.require_group(subgroup_name)
                for key, value in subgroup_data.items():
                    if key in subgroup:
                        del subgroup[key]
                    subgroup.create_dataset(key, data=value)

    def del_units(self, group_name):
        if self.filename == None:
            self.output("Error: no vaild hdf5 file selected")
            return None
        with h5py.File(self.filename, "a") as f:  # Open the file in append mode
            units_group = f["Units"]
            if group_name in units_group:  # Check if the subgroup exists
                del units_group[group_name]  # Delete the subgroup
            else:
                self.output(f"Unit '{group_name}' does not exist.")

    def read_config(self, secondary, tertiary, subgroup_name=None):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return {}

        with h5py.File(self.filename, "r") as f:
            group_path = f"Configurations/{secondary}/{tertiary}"

            # Helper function to read a subgroup's datasets and return them as a dictionary
            def read_subgroup(subgroup):
                data = {}
                for key in subgroup.keys():
                    value = subgroup[key][()]
                    if isinstance(value, bytes):
                        value = value.decode()
                    data[key] = value
                return data

            # If subgroup_name is specified, return its datasets as a one-level dictionary
            if subgroup_name:
                if subgroup_name in f[group_path]:
                    return read_subgroup(f[f"{group_path}/{subgroup_name}"])
                else:
                    self.output(f"Configuration '{subgroup_name}' does not exist.")
                    return (
                        {}
                    )  # Return an empty dictionary if the subgroup doesn't exist

            return tuple(f[group_path].keys())  # only return keys
            # If subgroup_name is not specified, return all data as a two-level dictionary
            data = {}
            for sub_name in f[group_path].keys():
                data[sub_name] = read_subgroup(f[f"{group_path}/{sub_name}"])

            return data

    def write_config(self, secondary, tertiary, data_dict):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return

        with h5py.File(self.filename, "a") as f:
            group_path = f"Configurations/{secondary}/{tertiary}"
            target_group = f.require_group(group_path)

            # Iterate over subgroups in the two-level dictionary
            for subgroup_name, subgroup_data in data_dict.items():
                subgroup = target_group.require_group(subgroup_name)

                # Write datasets for each subgroup
                for key, value in subgroup_data.items():
                    if key in subgroup:
                        del subgroup[key]
                    subgroup.create_dataset(key, data=value)

    def del_config(self, secondary, tertiary, subgroup_name_to_delete=None):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return

        with h5py.File(self.filename, "a") as f:
            group_path = f"Configurations/{secondary}/{tertiary}"

            if subgroup_name_to_delete:
                if subgroup_name_to_delete in f[group_path]:
                    del f[f"{group_path}/{subgroup_name_to_delete}"]
                else:
                    self.output(
                        f"Configuration '{subgroup_name_to_delete}' does not exist."
                    )
                    return (
                        {}
                    )  # Return an empty dictionary if the subgroup doesn't exist
            else:
                for subgroup in list(f[group_path].keys()):
                    del f[f"{group_path}/{subgroup}"]

    def read_data(self, dimension, subgroup=None):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return {}

        with h5py.File(self.filename, "r") as f:
            if f"Data/{dimension}" not in f:
                return
            target_group = f[f"Data/{dimension}"]

            # If subgroup is specified
            if subgroup:
                if subgroup in target_group:
                    subgroup_data = target_group[subgroup]
                    data = {}
                    for key in subgroup_data.keys():
                        value = subgroup_data[key][()]
                        if isinstance(value, bytes):
                            value = value.decode()
                        data[key] = value
                    return data
                self.output(f"Data '{subgroup}' does not exist.")
                return {}  # Return an empty dictionary if the subgroup doesn't exist

            # If subgroup is not specified, return all data as a two-level dictionary
            return tuple(target_group.keys())  # only return keys
            data = {}
            for sub_name in target_group.keys():
                subgroup_data = target_group[sub_name]
                dataset_dict = {}
                for key in subgroup_data.keys():
                    value = subgroup_data[key][()]
                    if isinstance(value, bytes):
                        value = value.decode()
                    dataset_dict[key] = value
                data[sub_name] = dataset_dict

            return data

    def write_data(self, dimension, data_dict):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return

        with h5py.File(self.filename, "a") as f:
            for subgroup, datasets in data_dict.items():
                group_path = f"Data/{dimension}/{subgroup}"
                subgroup = f.require_group(group_path)

                for key, value in datasets.items():
                    if key in subgroup:
                        del subgroup[key]
                    subgroup.create_dataset(key, data=value)

    def read_data(self, dimension, subgroup=None):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return {}

        with h5py.File(self.filename, "r") as f:
            data = {}

            if subgroup:  # If a specific subgroup is given
                if subgroup not in f[f"Data/{dimension}"]:
                    self.output(
                        f"Data '{subgroup}' does not exist under 'Data/{dimension}'."
                    )
                    return {}
                target_group = f[f"Data/{dimension}/{subgroup}"]
                for key in sorted(
                    target_group.keys(), key=int
                ):  # Sort keys as integers
                    value = target_group[key][()]
                    if isinstance(value, bytes):
                        value = value.decode()
                    data[key] = value
                return data
            return tuple(f[f"Data/{dimension}"].keys())
            main_group = f[f"Data/{dimension}"]
            for subgroup_name in sorted(
                main_group.keys(), key=int
            ):  # Sort keys as integers
                target_group = main_group[subgroup_name]
                subgroup_data = {}
                for key in sorted(
                    target_group.keys(), key=int
                ):  # Sort keys as integers
                    value = target_group[key][()]
                    if isinstance(value, bytes):
                        value = value.decode()
                    subgroup_data[key] = value
                data[subgroup_name] = subgroup_data

            return data

    def del_data(self, dimension, dataset_name_to_delete=None):
        if self.filename is None:
            self.output("Error: no vaild hdf5 file selected")
            return

        with h5py.File(self.filename, "a") as f:
            group_path = f"Data/{dimension}"

            if dataset_name_to_delete:
                if dataset_name_to_delete in f[group_path]:
                    del f[f"{group_path}/{dataset_name_to_delete}"]
                else:
                    self.output(
                        f"Data '{dataset_name_to_delete}' does not exist under '{group_path}'."
                    )
            else:
                for dataset in list(f[group_path].keys()):
                    del f[f"{group_path}/{dataset}"]
