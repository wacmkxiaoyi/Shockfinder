# File type: extension <Module> set
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

# This script updates automaticly! Do not Modify!
# Update time:2023-10-24 06:22:13

IO = {}
try:
    try:
        import ShockFinder.Addon.IO.HDF5 as HDF5
    except Exception as err:
        print("HDF5in ShockFinder dir importing error, reimporting in current dir")
        import HDF5
    IO["HDF5"] = HDF5
except Exception as err:
    print("Module: HDF5 import failure:", err)

if __name__ == "__main__":
    print("Testing Model:", __file__)
    print("IO:")
    for i in IO.keys():
        print(i, ":", IO[i])
        print("\t", IO[i].info)
