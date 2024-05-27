# File type: extension <Module> set
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

# This script updates automaticly! Do not Modify!
# Update time:2023-10-24 06:22:13

MultiprocessEngine = {}
try:
    try:
        import ShockFinder.Addon.MultiprocessEngine.XME as XME
    except Exception as err:
        print("XMEin ShockFinder dir importing error, reimporting in current dir")
        import XME
    MultiprocessEngine["XME"] = XME
except Exception as err:
    print("Module: XME import failure:", err)

if __name__ == "__main__":
    print("Testing Model:", __file__)
    print("MultiprocessEngine:")
    for i in MultiprocessEngine.keys():
        print(i, ":", MultiprocessEngine[i])
        print("\t", MultiprocessEngine[i].build)
