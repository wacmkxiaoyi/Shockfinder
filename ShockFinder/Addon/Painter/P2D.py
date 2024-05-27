# File type: <Function> set
# By Junxiang H., 2023/07/03
# wacmk.com/cn Tech. Supp.

try:
    import ShockFinder.Addon.Painter.Basic as Basic
except:
    import Basic

from matplotlib import pyplot as plt, colors
import pandas as pd, numpy as np


def set_figure_info(**Figureinfo):
    title = Basic.CharUndecode(Basic.get_par(Figureinfo, "title", ""))
    x_axis = Basic.CharUndecode(Basic.get_par(Figureinfo, "x_axis", ""))
    y_axis = Basic.CharUndecode(Basic.get_par(Figureinfo, "y_axis", ""))
    xscale = Basic.get_par(Figureinfo, "xscale")
    yscale = Basic.get_par(Figureinfo, "yscale")
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    if xscale != None:
        plt.xscale(xscale)
    if yscale != None:
        plt.yscale(yscale)


def draw_aux_line(xmin, xmax, ymin, ymax, **Figureinfo):
    auxlines = {"vline": {}, "hline": {}, "linear": {}, "powerlaw": {}, "exponent": {}}

    def check(strc, ifi):
        if strc == ifi[: len(strc)]:
            return True
        return False

    for info, value in Figureinfo.items():
        igi = info.split("-", 1)
        for key in auxlines.keys():
            # default value
            if check(key, igi[0]):
                name = igi[0].split(key, 1)[1]
                if name not in auxlines[key].keys():
                    auxlines[key][name] = {}
                if len(igi) == 1 or igi[1] == "":
                    auxlines[key][name]["value"] = value
                else:
                    auxlines[key][name][igi[1]] = value
    step = 1e4
    for key, value in auxlines["vline"].items():
        # x=value
        if "linestyle" not in value.keys():
            value["linestyle"] = "--"
        if "label" not in value.keys() and key != "":
            value["label"] = key
        plt.vlines(
            x=value["value"],
            ymin=ymin,
            ymax=ymax,
            **Basic.clean_keys(value, Basic.linekeys)
        )
    for key, value in auxlines["hline"].items():
        # y=value
        if "linestyle" not in value.keys():
            value["linestyle"] = "--"
        if "label" not in value.keys() and key != "":
            value["label"] = key
        plt.hlines(
            value["value"],
            xmin=xmin,
            xmax=xmax,
            **Basic.clean_keys(value, Basic.linekeys)
        )
    for key, value in auxlines["linear"].items():
        # y=kx+b, k=1,b=b/value
        if "linestyle" not in value.keys():
            value["linestyle"] = "--"
        if "label" not in value.keys() and key != "":
            value["label"] = key
        x = np.arange(xmin, xmax, (xmax - xmin) / step)
        k = value["k"] if "k" in value.keys() else 1
        b = (
            value["b"]
            if "b" in value.keys()
            else value["value"] if "value" in value.keys() else 0
        )
        y = k * x + b
        plt.plot(x, y, **Basic.clean_keys(value, Basic.linekeys))
    for key, value in auxlines["powerlaw"].items():
        # y=ax^k+c, a=1,k=1,c=c/value
        if "linestyle" not in value.keys():
            value["linestyle"] = "--"
        if "label" not in value.keys() and key != "":
            value["label"] = key
        x = np.arange(xmin, xmax, (xmax - xmin) / step)
        a = value["a"] if "a" in value.keys() else 1
        k = value["k"] if "k" in value.keys() else 1
        c = (
            value["c"]
            if "c" in value.keys()
            else value["value"] if "value" in value.keys() else 0
        )
        y = a * x**k + c
        plt.plot(x, y, **Basic.clean_keys(value, Basic.linekeys))
    for key, value in auxlines["exponent"].items():
        # y=ae**x/r+c, a=1,r=1,c=c/value
        if "linestyle" not in value.keys():
            value["linestyle"] = "--"
        if "label" not in value.keys() and key != "":
            value["label"] = key
        x = np.arange(xmin, xmax, (xmax - xmin) / step)
        a = value["a"] if "a" in value.keys() else 1
        r = value["r"] if "r" in value.keys() else 1
        c = (
            value["c"]
            if "c" in value.keys()
            else value["value"] if "value" in value.keys() else 0
        )
        y = a * np.e ** (x / r) + c
        plt.plot(x, y, **Basic.clean_keys(value, Basic.linekeys))


def draw_line(lines):
    showlabel = False
    for line in lines:
        le, li = line
        plt.plot(le["x"], le["y"], **Basic.clean_keys(li, Basic.linekeys))
        if Basic.get_par(li, "label") != None:
            showlabel = True
    return showlabel


def line(*lines, **Figureinfo):
    set_figure_info(**Figureinfo)
    x_lim = Basic.get_par(Figureinfo, "x_lim")
    y_lim = Basic.get_par(Figureinfo, "y_lim")
    if x_lim != None:
        plt.xlim(*x_lim)
    if y_lim != None:
        plt.ylim(*y_lim)
    showlabel = draw_line(lines)
    tt = np.array(
        [
            np.array([min(i[0]["x"]), max(i[0]["x"]), min(i[0]["y"]), max(i[0]["y"])])
            for i in lines
        ]
    ).T
    draw_aux_line(min(tt[0]), max(tt[1]), min(tt[2]), max(tt[3]), **Figureinfo)
    if showlabel:
        plt.legend()
    plt.show()


def line_share_x(line2, *line1, **Figureinfo):
    set_figure_info(**Figureinfo)
    x_lim = Basic.get_par(Figureinfo, "x_lim")
    y_lim = Basic.get_par(Figureinfo, "y_lim")
    if x_lim != None:
        plt.xlim(*x_lim)
    if y_lim != None:
        plt.ylim(*y_lim)
    showlabel = draw_line(line1)
    tx = plt.twinx()
    y2 = Basic.get_par(Figureinfo, "y_axis2")
    if y2 != None:
        tx.set_ylabel(y2)
    le, li = line2
    tx.plot(le["x"], le["y"], **Basic.clean_keys(li, Basic.linekeys))
    if Basic.get_par(li, "label") != None:
        showlabel = True
    y_lim2 = Basic.get_par(Figureinfo, "y_lim2")
    if y_lim2 != None:
        tx.set_ylim(*y_lim2)
    tt = np.array(
        [
            np.array([min(i[0]["x"]), max(i[0]["x"]), min(i[0]["y"]), max(i[0]["y"])])
            for i in line1
        ]
    ).T
    draw_aux_line(min(tt[0]), max(tt[1]), min(tt[2]), max(tt[3]), **Figureinfo)
    if showlabel:
        plt.legend()
    plt.show()


def line_share_y(line2, *line1, **Figureinfo):
    set_figure_info(**Figureinfo)
    x_lim = Basic.get_par(Figureinfo, "x_lim")
    y_lim = Basic.get_par(Figureinfo, "y_lim")
    if x_lim != None:
        plt.xlim(*x_lim)
    if y_lim != None:
        plt.ylim(*y_lim)
    showlabel = draw_line(line1)
    tx = plt.twiny()
    x2 = Basic.get_par(Figureinfo, "x_axis2")
    if x2 != None:
        tx.set_xlabel(x2)
    le, li = line2
    tx.plot(le["x"], le["y"], **Basic.clean_keys(li, Basic.linekeys))
    if Basic.get_par(li, "label") != None:
        showlabel = True
    x_lim2 = Basic.get_par(Figureinfo, "x_lim2")
    if x_lim2 != None:
        tx.set_xlim(*x_lim2)
    tt = np.array(
        [
            np.array([min(i[0]["x"]), max(i[0]["x"]), min(i[0]["y"]), max(i[0]["y"])])
            for i in line1
        ]
    ).T
    draw_aux_line(min(tt[0]), max(tt[1]), min(tt[2]), max(tt[3]), **Figureinfo)
    if showlabel:
        plt.legend()
    plt.show()


def surface(surface, **Figureinfo):
    set_figure_info(**Figureinfo)
    sf, sfi = surface
    x_lim = Basic.get_par(Figureinfo, "x_lim")
    y_lim = Basic.get_par(Figureinfo, "y_lim")
    if x_lim != None:
        plt.xticks(*x_lim)
    else:
        plt.xticks(
            [
                i[int(len(i) / 2)]
                for i in np.split(sf["x"][: 10 * int(len(sf["x"]) / 10)], 10)
            ]
            if len(sf["x"]) > 10
            else sf["x"]
        )
    if y_lim != None:
        plt.yticks(*y_lim)
    else:
        plt.yticks(
            [
                i[int(len(i) / 2)]
                for i in np.split(sf["y"][: 10 * int(len(sf["y"]) / 10)], 10)
            ]
            if len(sf["y"]) > 10
            else sf["y"]
        )
    # plt.figure("imshow",facecolor="lightgray")
    plt.imshow(
        np.flipud(sf["v"].T),
        cmap="RdBu",
        extent=[sf["x"][0], sf["x"][-1], sf["y"][0], sf["y"][-1]],
        norm=colors.LogNorm(),
        **Basic.clean_kwargs(sfi, plt.imshow)
    )
    plt.colorbar()
    plt.show()


def info():
    print("Module:", __file__)


if __name__ == "__main__":
    import Line, Surface, math

    x = np.arange(0, 100, 0.1)
    l1 = Line.CreateLine(x=x, y=x**2, label="$x^2$")
    l2 = Line.CreateLine(x=x, y=x**3, label="$x^3$")
    line_share_y(l2, l1, label=True, title="Test")

    r = np.arange(100)
    p = np.arange(0, (2 + 0.01) * np.pi, 2 * 0.01 * np.pi)
    from scipy.special import lpmv

    v = lpmv(0, 3, r).reshape(100, 1) * (np.cos(p) ** 2).reshape(1, 101)
    x, y, v = Basic.rop_to_xoy(r, p, v)
    # print(v)
    sf = Surface.CreateSurface(x=x, y=y, v=v)
    surface(sf)
