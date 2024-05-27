# File type: <Function>
# By Junxiang H., 2023/07/03
# wacmk.com/cn Tech. Supp.
try:
    import ShockFinder.Addon.Painter.Basic as Basic
except:
    import Basic
import pandas as pd, numpy as np, copy


def CreateSurface(**args):
    x = Basic.get_par(args, "x")
    y = Basic.get_par(args, "y")
    z = Basic.get_par(args, "z")
    v = Basic.get_par(args, "v")
    if type(x) == type(None) or type(y) == type(None) or type(v) == type(None):
        return None
    label = Basic.get_par(args, "label", "")
    if type(z) != type(None):
        surface = {"x": x, "y": y, "v": v, "z": z}
    else:
        surface = {"x": x, "y": y, "v": v}
    surfaceinfo = {
        # "label":Basic.CharUndecode(label)
    }
    for i in args.keys():
        if i not in surfaceinfo.keys() and i not in surface.keys():
            surfaceinfo[i] = args[i]
    return (surface, surfaceinfo)


# Used to MySQL
def FormatSurface(Surface, Surfaceinfo, Surfaceid):
    newsurface = copy.deepcopy(Surface)
    if "z" in newsurface.keys():
        newsurface["v"] = [
            str(tuple([str(tuple(j.tolist())).replace(" ", "") for j in i]))
            .replace(" ", "")
            .replace('"', "")
            .replace("'", "")
            for i in newsurface["v"]
        ]
    else:
        newsurface["v"] = [
            str(tuple(i.tolist())).replace(" ", "") for i in newsurface["v"]
        ]
    Surfaceframe = pd.DataFrame(newsurface)
    Surfaceinfoframe = pd.DataFrame(Surfaceinfo, index=[Surfaceid])
    return (Surfaceframe, Surfaceinfoframe)


def DecodeSurface(Surfaceframe, Surfaceinfoframe):
    data = dict(
        zip(
            ["x", "y", "v", "z"],
            [
                np.array(list(Surfaceframe.to_dict()[i].values()))
                for i in Surfaceframe.keys()
            ],
        )
    )
    if "z" in data.keys():
        data["v"] = np.array(
            [
                np.array(
                    [
                        np.array(
                            [
                                float(k)
                                for k in j.replace("(", "").replace(")", "").split(",")
                            ]
                        )
                        for j in i.split("),(")
                    ]
                )
                for i in data["v"]
            ]
        )
    else:
        data["v"] = np.array(
            [
                np.array(
                    [float(j) for j in i.replace("(", "").replace(")", "").split(",")]
                )
                for i in data["v"]
            ]
        )
    data.update(Surfaceinfoframe.to_dict())
    return CreateSurface(**data)


def info():
    print("Module:", __file__)


if __name__ == "__main__":
    x = np.arange(0, 100)
    y = np.arange(0, 100)
    sur0, surinfo0 = CreateSurface(
        x=x,
        y=x,
        z=x,
        v=x.reshape(len(x), 1, 1)
        * (y.reshape(1, len(y), 1) - 100)
        * x.reshape(1, 1, len(x)),
    )
    # print(sur0)
    sur0frame, surinfo0infoframe = FormatSurface(sur0, surinfo0, 0)
    # print(sur0frame)
    # print(surinfo0infoframe)
    # print(DecodeSurface(sur0frame,surinfo0infoframe.loc[0])) #mysql
