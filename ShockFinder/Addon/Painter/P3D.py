# File type: <Function> set
# By Junxiang H., 2023/07/03
# wacmk.com/cn Tech. Supp.

try:
    import ShockFinder.Addon.Painter.Basic as Basic
except:
    import Basic

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd, numpy as np


def set_figure_info(ax, **Figureinfo):
    title = Basic.CharUndecode(Basic.get_par(Figureinfo, "title", ""))
    x_axis = Basic.CharUndecode(Basic.get_par(Figureinfo, "x_axis", ""))
    y_axis = Basic.CharUndecode(Basic.get_par(Figureinfo, "y_axis", ""))
    z_axis = Basic.CharUndecode(Basic.get_par(Figureinfo, "z_axis", ""))
    x_lim = Basic.get_par(Figureinfo, "x_lim")
    y_lim = Basic.get_par(Figureinfo, "y_lim")
    z_lim = Basic.get_par(Figureinfo, "z_lim")
    if x_lim != None:
        ax.set_xlim(*x_lim)
    if y_lim != None:
        ax.set_ylim(*y_lim)
    if z_lim != None:
        ax.set_zlim(*z_lim)
    ax.set_title(title)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_zlabel(z_axis)


def line(*lines, **Figureinfo):
    showlabel = False
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    set_figure_info(ax, **Figureinfo)
    for line in lines:
        le, li = line
        ax.plot(le["x"], le["y"], le["z"], **Basic.clean_keys(li, Basic.linekeys))
        if Basic.get_par(li, "label") != None:
            showlabel = True
    if showlabel:
        ax.legend()
    plt.show()


def surface(surface, **Figureinfo):  #
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    set_figure_info(ax, **Figureinfo)
    sf, sfi = surface
    x, y = np.meshgrid(sf["x"], sf["y"])
    suf = ax.plot_surface(x.T, y.T, sf["v"], **Basic.clean_kwargs(sfi, ax.plot_surface))
    if str(Basic.get_par(Figureinfo, "contour", False)) == "True":
        ax.contour(x.T, y.T, sf["v"], zdir="z", offset=-1, cmap=plt.get_cmap("rainbow"))
    plt.colorbar(suf)
    plt.show()


def scatter(scatter, **Figureinfo):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    set_figure_info(ax, **Figureinfo)
    sc, sci = scatter
    sci["facecolors"] = plt.cm.jet(sc["v"])
    surf = ax.plot_surface(
        sc["x"], sc["y"], sc["z"], **Basic.clean_kwargs(sci, ax.plot_surface)
    )
    plt.colorbar(surf, orientation="vertical")
    plt.show()


def info():
    print("Module:", __file__)


if __name__ == "__main__":
    import Line, Surface, math

    """
	x=np.arange(100)
	y=np.arange(0,2*np.pi,2*0.01*np.pi)
	z=np.sin(y)/x
	l=Line.CreateLine(x=x,y=y,z=z,label="$\\frac{sin(y)}{x}$")
	line(l,label=True,title="Test")
	
	"""
    r = np.arange(50)
    t = np.arange(0, (1 + 0.02) * np.pi, 1 * 0.02 * np.pi)
    p = np.arange(0, (2 + 0.02) * np.pi, 2 * 0.02 * np.pi)
    v = r.reshape(50, 1, 1) * np.sin(t).reshape(1, 51, 1) * np.cos(p).reshape(1, 1, 51)
    x, y, z, v = Basic.rtp_to_xyz(r, t, p, v)
    cx = np.full((len(r),), 10)
    cy = r
    cz = r
    x, y, v = Basic._3D_to_2D(x, y, z, v, cx, cy, cz)
    # x,y,v=Basic.rop_to_xoy(r,p,v)
    # print(v)
    sf = Surface.CreateSurface(x=x, y=y, v=v, cmap="hot")
    surface(sf, x_axis="x", y_axis="y", z_axis="z")
