# File type: extension <Module> set
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

# This script updates automaticly! Do not Modify!
# Update time:2023-11-13 23:07:30

Painter = {}
try:
    try:
        import ShockFinder.Addon.Painter.Surface as Surface
    except Exception as err:
        print("Surfacein ShockFinder dir importing error, reimporting in current dir")
        import Surface
    Painter["Surface"] = Surface
except Exception as err:
    print("Module: Surface import failure:", err)

try:
    try:
        import ShockFinder.Addon.Painter.Basic as Basic
    except Exception as err:
        print("Basicin ShockFinder dir importing error, reimporting in current dir")
        import Basic
    Painter["Basic"] = Basic
except Exception as err:
    print("Module: Basic import failure:", err)

try:
    try:
        import ShockFinder.Addon.Painter.Scatter as Scatter
    except Exception as err:
        print("Scatterin ShockFinder dir importing error, reimporting in current dir")
        import Scatter
    Painter["Scatter"] = Scatter
except Exception as err:
    print("Module: Scatter import failure:", err)

try:
    try:
        import ShockFinder.Addon.Painter.P2D as P2D
    except Exception as err:
        print("P2Din ShockFinder dir importing error, reimporting in current dir")
        import P2D
    Painter["P2D"] = P2D
except Exception as err:
    print("Module: P2D import failure:", err)

try:
    try:
        import ShockFinder.Addon.Painter.P3D as P3D
    except Exception as err:
        print("P3Din ShockFinder dir importing error, reimporting in current dir")
        import P3D
    Painter["P3D"] = P3D
except Exception as err:
    print("Module: P3D import failure:", err)

try:
    try:
        import ShockFinder.Addon.Painter.Line as Line
    except Exception as err:
        print("Linein ShockFinder dir importing error, reimporting in current dir")
        import Line
    Painter["Line"] = Line
except Exception as err:
    print("Module: Line import failure:", err)

if __name__ == "__main__":
    print("Testing Model:", __file__)
    print("Painter:")
    for i in Painter.keys():
        print(i, ":", Painter[i])
        print("\t", Painter[i].info)
