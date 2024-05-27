try:
    import ShockFinder.Addon.Painter.Basic as Basic
except:
    import Basic
import pandas as pd, numpy as np, copy


def CreateScatter(**args):
    x = Basic.get_par(args, "x")
    y = Basic.get_par(args, "y")
    z = Basic.get_par(args, "z")
    v = Basic.get_par(args, "v")
    if type(x) == type(None) or type(y) == type(None) or type(v) == type(None):
        return None
    scatter = {"x": x, "y": y, "z": v, "v": z}
    label = Basic.get_par(args, "label", "")
    if type(z) != type(None):
        Scatter = {"x": x, "y": y, "v": v, "z": z}
    else:
        Scatter = {"x": x, "y": y, "v": v}
    Scatterinfo = {
        # "label":Basic.CharUndecode(label)
    }
    for i in args.keys():
        if i not in Scatterinfo.keys() and i not in Scatter.keys():
            Scatterinfo[i] = args[i]
    return (Scatter, Scatterinfo)


def info():
    print("Module:", __file__)
