# This is a model file for XUI page
# Junxiang H. 2023.07.09
import numpy as np
from XenonUI.XUIlib.page import Image_F, str_to_float, checkNone, page, retype_string
from ShockFinder.Addon.GUI.XUIlib.ShockFinderFiguresHDF5 import ShockFinderFiguresHDF5
import copy
from .FigurePages.Database import GlobalSettings, LoadData
from .FigurePages.Figuring import UnitSet, QuickSaved
from .FigurePages.Figuring.TwoD import TimeSequency, Surface2d, Line2d, FFT
from .FigurePages.Figuring.ThreeD import Line3d, Scatter3d, Surface3d, TimeSequency3d

class page(page):
    img = {"logo": Image_F}
    unit_t = None
    unit_r = None
    unit_rho = None
    unit_v = None
    avqt = [[], [], [], []]
    avgr = []
    usefultindex = []
    infomation_max = 100
    maxline = 10
    maxcross = 20
    reset_funs = []

    def low_pass_filter(self, signal, window_size, cut):
        """Apply a low-pass filter to the input signal."""
        if cut:
            if type(cut) not in (list, tuple):
                signal[np.where(signal > cut)] = cut
            else:
                try:
                    signal[np.where(signal < cut[0])] = cut[0]
                    signal[np.where(signal > cut[1])] = cut[1]
                except:
                    signal[np.where(signal > cut[0])] = cut[0]
        return (
            np.convolve(signal, np.ones(window_size) / window_size, mode="same")
            if window_size != 0
            else signal
        )

    def Fitting(self, lineinfo):
        x = lineinfo["x"]
        y = lineinfo["y"]
        line = []

        def get_MARK(strc, x, y, lfi):
            if type(strc) in (list, tuple, np.ndarray):
                result = ""
                for i in strc:
                    result += get_MARK(i, x, y, lfi)
                return result
            elif strc != None and "MARK" in strc:
                return str(
                    round(x[np.argmax(y)], 2 if len(strc[4:]) == 0 else int(strc[4:]))
                )
            elif strc == "lfi":
                return str(lfi)
            return strc

        def get_MARK_bottom(strc, x, y, lfi):
            if type(strc) in (list, tuple, np.ndarray):
                result = ""
                for i in strc:
                    result += get_MARK(i, x, y, lfi)
                return result
            elif strc != None and "MARK" in strc:
                return str(
                    round(x[np.argmin(y)], 2 if len(strc[4:]) == 0 else int(strc[4:]))
                )
            elif strc == "lfi":
                return str(lfi)
            return strc

        def get_info(key, lfind, lineinfo, default):
            return (
                (default if key not in lineinfo.keys() else lineinfo[key])
                if key + lfind not in lineinfo.keys()
                else lineinfo[key + lfind]
            )

        lf = get_info("lf", "", lineinfo, "").lower()
        if lf != "manual":
            peakinfos = []
            lfl = {}
            lfc = {}
            lfs = {}
            lfr = get_info("lfr", "", lineinfo, (x[0], x[-1]))
            autox = copy.deepcopy(
                x[np.where(x >= lfr[0])[0][0] : np.where(x <= lfr[1])[0][-1] + 1]
            )
            autoy = copy.deepcopy(
                y[np.where(x >= lfr[0])[0][0] : np.where(x <= lfr[1])[0][-1] + 1]
            )

            lfremove = get_info("lfrem", "", lineinfo, ())
            lfshow = get_info("lfshow", "", lineinfo, "total").lower()
            # lf_min=get_info("lfmin","",lineinfo,np.min(autoy))
            # lf_max=get_info("lfmax","",lineinfo,np.max(autoy))
            checks = ("debug", "show", "red", "rem", "s", "l", "c", "r")

            def i_check(strc, checks):
                for i in checks:
                    if strc[: len(i)] == i:
                        return True
                return False

            def get_fitpar(ind, other={}):
                result = {"name": ind}
                result.update(other)
                short = {"ce": "center", "am": "amplitude", "sig": "sigma"}

                def parname_replace(parname):
                    if parname in short.keys():
                        return short[parname]
                    return parname

                def rotate_set_par(pars, key, res=None):
                    if res == None:
                        res = result
                    if len(pars) > 1:
                        if parname_replace(pars[0]) not in res.keys():
                            res[parname_replace(pars[0])] = {}
                        res[parname_replace(pars[0])] = rotate_set_par(
                            pars[1:], key, res[parname_replace(pars[0])]
                        )
                    else:
                        res[parname_replace(pars[0])] = lineinfo[key]
                    return res

                for i in lineinfo.keys():  # gobal mode
                    if "lf-" == i[:3]:  # got a parameter
                        pars = i.split("-")[1:]
                        if len(pars) == 1:
                            if parname_replace(pars[0]) not in result.keys():
                                result[parname_replace(pars[0])] = {
                                    "value": lineinfo[i]
                                }
                            else:
                                result[parname_replace(pars[0])]["value"] = lineinfo[i]
                        elif len(pars) > 1:
                            result = rotate_set_par(pars, i)
                for i in lineinfo.keys():
                    if "lf" + ind + "-" == i[: 3 + len(ind)]:  # got a parameter
                        pars = i.split("-")[1:]
                        if len(pars) == 1:
                            if parname_replace(pars[0]) not in result.keys():
                                result[parname_replace(pars[0])] = {
                                    "value": lineinfo[i]
                                }
                            else:
                                result[parname_replace(pars[0])]["value"] = lineinfo[i]
                        elif len(pars) > 1:
                            result = rotate_set_par(pars, i)
                if "amplitude" not in result.keys():
                    result["amplitude"] = {
                        "value": 2 * (np.max(autoy) - np.min(autoy))
                    }  # ,"min":np.min(autoy),"max":2*np.max(autoy)}
                return result

            if lf != "auto":
                for i in lineinfo.keys():
                    if (
                        "lf" in i
                        and "lf" == i[:2]
                        and not i_check(i[2:], checks)
                        and "-" not in i
                        and i != "lf"
                    ):
                        lfl[i[2:]] = get_info("lfl", i[2:], lineinfo, None)
                        lfc[i[2:]] = get_info("lfc", i[2:], lineinfo, None)
                        lfs[i[2:]] = get_info("lfs", i[2:], lineinfo, ":")
                        peakinfos.append(
                            get_fitpar(i[2:], {"center": {"value": lineinfo[i]}})
                        )
            else:
                lfreduce = get_info("lfred", "", lineinfo, 0.1)
                newy = copy.deepcopy(autoy)
                newy -= np.max(newy) * lfreduce
                newy[np.where(newy < 0)] = 0
                peaks = []
                pb = -1
                pe = -1
                pmax = 0
                pmaxind = -1
                for i in range(len(autox)):
                    if newy[i] == 0:
                        if pe != -1:  # useful check point
                            peaks.append(pmaxind)
                            pe = -1  # mark last check point is over
                        pb = i  # reset check point
                        pmax = 0
                    elif pb != -1:  # if not begin:
                        pe = i
                        if newy[i] > pmax:
                            pmax = newy[i]
                            pmaxind = i

                stt = ""
                for i in range(len(peaks)):
                    stt += str(round(autox[peaks[i]], 2)) + ", "
                    peakinfos += [
                        {
                            "name": "p" + str(i),
                            "center": {"value": autox[peaks[i]]},
                            "amplitude": {
                                "value": autoy[peaks[i]],
                                #"min": lf_min,
                                "max": autoy[peaks[i]],
                            },
                        }
                    ]
                    lfc["p" + str(i)] = get_info("lfc", "p" + str(i), lineinfo, None)
                    lfs["p" + str(i)] = get_info("lfs", "p" + str(i), lineinfo, ":")
                    lfl["p" + str(i)] = get_info("lfl", "p" + str(i), lineinfo, None)
                if stt != "":
                    stt = stt[:-2]
                    self.tkobj.io_recv("Got peaks: (", len(peaks), ")", stt)
                if get_info("lfdebug", "", lineinfo, False):
                    line.append(
                        self.pageargs["Infobj"]
                        .Config["Painter"]["Line"]
                        .CreateLine(**{"x": autox, "y": newy, "label": "debug"})
                    )
                    peakinfos = []
            if len(peakinfos) != 0:
                result = (
                    self.pageargs["Infobj"]
                    .Config["Painter"]["Line"]
                    .Fitting(autox, autoy, *peakinfos)
                )
                if lfshow in ("total", "both"):
                    lorlineinfo = {
                        "x": autox,
                        "y": result.best_fit,
                        "color": get_info("lfc", "t", lineinfo, "red"),
                        "linestyle": get_info("lfs", "t", lineinfo, "--"),
                    }
                    lorlineinfo.update(
                        {
                            "label": get_MARK(
                                get_info("lfl", "t", lineinfo, "Fitting"),
                                autox,
                                result.best_fit,
                                "Fitting",
                            )
                        }
                    )
                    line.append(
                        self.pageargs["Infobj"]
                        .Config["Painter"]["Line"]
                        .CreateLine(**lorlineinfo)
                    )
                if lfshow in ("peak", "both"):
                    nn = 0
                    for name, comp in result.eval_components().items():
                        inde = name.split("_")[0]
                        if name != "BKG" and nn not in lfremove:
                            lorlineinfo = {
                                "x": autox,
                                "y": comp,
                                "color": lfc[inde] if name != "BKG" else None,
                                "linestyle": lfs[inde] if name != "BKG" else "--",
                            }
                            lorlineinfo.update(
                                {
                                    "label": get_MARK(
                                        lfl[inde] if name != "BKG" else "BKG",
                                        autox,
                                        comp,
                                        inde,
                                    )
                                }
                            )
                            line.append(
                                self.pageargs["Infobj"]
                                .Config["Painter"]["Line"]
                                .CreateLine(**lorlineinfo)
                            )
                            nn += 1

            else:
                """
                peakinfos=[{
                        "name":"Main",
                        "center":x[np.argmax(y)],
                        "amplitude":np.max(y)-np.min(y)
                }]
                lfl["Main"]=get_info("lfl","",lineinfo,None)
                lfc["Main"]=get_info("lfc","",lineinfo,None)
                lfs["Main"]=get_info("lfs","",lineinfo,":")
                """
                pass
        else:
            lf = False
            lfr = []
            lfg = []
            lfm = []
            lfl = []
            lfc = []
            lfs = []
            for i in lineinfo.keys():
                if (
                    "lf" in i
                    and "lf" == i[:2]
                    and i[2] not in ("c", "g", "l", "m", "s")
                    and i != "lf"
                ):
                    lfg.append(get_info("lfg", i[2:], lineinfo, "10%"))
                    lfm.append(get_info("lfm", i[2:], lineinfo, "dogbox"))
                    lfl.append(get_info("lfl", i[2:], lineinfo, None))
                    lfc.append(get_info("lfc", i[2:], lineinfo, None))
                    lfs.append(get_info("lfs", i[2:], lineinfo, ":"))
                    lfr.append(lineinfo[i])
            if len(lfr) != 0:
                for i in range(len(lfr)):
                    lorlineinfo = {
                        "x": x[
                            np.where(x >= lfr[i][0])[0][0] : np.where(x <= lfr[i][1])[
                                0
                            ][-1]
                            + 1
                        ],
                        "y": self.pageargs["Infobj"]
                        .Config["Painter"]["Line"]
                        .lorentzian_fit(
                            x[
                                np.where(x >= lfr[i][0])[0][0] : np.where(
                                    x <= lfr[i][1]
                                )[0][-1]
                                + 1
                            ],
                            y[
                                np.where(x >= lfr[i][0])[0][0] : np.where(
                                    x <= lfr[i][1]
                                )[0][-1]
                                + 1
                            ],
                            lfg[i],
                            lfm[i],
                        ),
                        "color": lfc[i],
                        "linestyle": lfs[i],
                    }
                    lorlineinfo.update(
                        {
                            "label": get_MARK(
                                lfl[i], lorlineinfo["x"], lorlineinfo["y"], i
                            )
                        }
                    )
                    line.append(
                        self.pageargs["Infobj"]
                        .Config["Painter"]["Line"]
                        .CreateLine(**lorlineinfo)
                    )
        return line

    def get_line(self, lineinfo):
        return [
            self.pageargs["Infobj"].Config["Painter"]["Line"].CreateLine(**lineinfo)
        ] + self.Fitting(lineinfo)

    def get_x(self, qt, rf, re, tf, te, rhof, rhoe, index):
        if qt.get() == "" or index.get() == "":
            return False
        factor = 1
        factor *= str_to_float(rf.get()) * self.unit_r ** str_to_float(re.get())
        factor *= str_to_float(tf.get()) * self.unit_t ** str_to_float(te.get())
        factor *= str_to_float(rhof.get()) * self.unit_rho ** str_to_float(rhoe.get())
        ind = self.pageargs["Infobj"].database.tindex.index(int(index.get()))
        if qt.get() in self.pageargs["Infobj"].database.data[ind].grid:
            return factor * self.pageargs["Infobj"].database.data[ind].grid[qt.get()]
        elif qt.get() in self.pageargs["Infobj"].database.data[ind].quantities:
            return (
                factor * self.pageargs["Infobj"].database.data[ind].quantities[qt.get()]
            )
        else:
            raise IndexError(f'The simulation does not run to {ind}')
        return False

    def get_y(self, qt, rf, re, tf, te, rhof, rhoe):
        qt_value = qt.get()
        if qt_value == "":
            return False
        factor = 1
        factor *= str_to_float(rf.get()) * self.unit_r ** str_to_float(re.get())
        factor *= str_to_float(tf.get()) * self.unit_t ** str_to_float(te.get())
        factor *= str_to_float(rhof.get()) * self.unit_rho ** str_to_float(rhoe.get())
        result = []
        for i in self.pageargs["Infobj"].database.data:
            if i != None:
                if qt_value not in i.quantities:
                    break
                result.append(i.quantities[qt_value] * factor)
        return np.array(result)

    def get_lineinfo(self, x, y, ylb, yco, yls, yargs):
        lineinfo = {
            "x": x,
            "y": y,
            "label": checkNone(ylb.get()),
            "color": checkNone(yco.get()),
            "linestyle": yls.get(),
        }
        for i in yargs.get().split(";"):
            iic = i.split("=")
            if len(iic) == 2:
                lineinfo.update({iic[0]: retype_string(iic[1])})

        def get_par(key, default):
            return lineinfo[key] if key in lineinfo.keys() else default

        lineinfo["y"] = (
            self.low_pass_filter(
                lineinfo["y"], get_par("filterlevel", 0), get_par("cut", None)
            )
            if get_par("linefilter", False)
            else lineinfo["y"]
        )
        return lineinfo

    def get_lineinfo3d(self, x, y, z, zlb, zco, zls, zargs):
        lineinfo = {
            "x": x,
            "y": y,
            "z": z,
            "label": checkNone(zlb.get()),
            "color": checkNone(zco.get()),
            "linestyle": zls.get(),
        }
        for i in zargs.get().split(";"):
            iic = i.split("=")
            if len(iic) == 2:
                lineinfo.update({iic[0]: retype_string(iic[1])})

        def get_par(key, default):
            return lineinfo[key] if key in lineinfo.keys() else default

        lineinfo["z"] = (
            self.low_pass_filter(
                lineinfo["z"], get_par("filterlevel", 0), get_par("cut", None)
            )
            if get_par("linefilter", False)
            else lineinfo["z"]
        )
        return lineinfo

    def get_figureinfo(self, ft, fx, fy, fxs, fys, fxa, fxb, fya, fyb, fargs):
        figureinfo = {
            "title": ft.get(),
            "x_axis": fx.get(),
            "y_axis": fy.get(),
            "xscale": checkNone(fxs.get()),
            "yscale": checkNone(fys.get()),
            "x_lim": (
                None
                if fxa.get() == "" or fxb.get() == ""
                else (str_to_float(fxa.get()), str_to_float(fxb.get()))
            ),
            "y_lim": (
                None
                if fya.get() == "" or fyb.get() == ""
                else (str_to_float(fya.get()), str_to_float(fyb.get()))
            ),
        }
        for i in fargs.get().split(";"):
            iic = i.split("=")
            if len(iic) == 2:
                figureinfo.update({iic[0]: retype_string(iic[1])})
        return figureinfo

    def get_figureinfo3d(self, ft, fx, fy, fz, fxa, fxb, fya, fyb, fza, fzb, fargs):
        figureinfo = {
            "title": ft.get(),
            "x_axis": fx.get(),
            "y_axis": fy.get(),
            "z_axis": fz.get(),
            "x_lim": (
                None
                if fxa.get() == "" or fxb.get() == ""
                else (str_to_float(fxa.get()), str_to_float(fxb.get()))
            ),
            "y_lim": (
                None
                if fya.get() == "" or fyb.get() == ""
                else (str_to_float(fya.get()), str_to_float(fyb.get()))
            ),
            "z_lim": (
                None
                if fza.get() == "" or fzb.get() == ""
                else (str_to_float(fza.get()), str_to_float(fzb.get()))
            ),
        }
        for i in fargs.get().split(";"):
            iic = i.split("=")
            if len(iic) == 2:
                figureinfo.update({iic[0]: retype_string(iic[1])})
        return figureinfo

    def get_surfaceinfo(self, x, y, v, vargs):
        surfaceinfo = {"x": x, "y": y, "v": v}
        for i in vargs.get().split(";"):
            iic = i.split("=")
            if len(iic) == 2:
                surfaceinfo.update({iic[0]: retype_string(iic[1])})
        return surfaceinfo

    def get_scatter3d(self, x, y, z, v, vargs):
        Scatterinfo = {"x": x, "y": y, "z": z, "v": v}
        for i in vargs.get().split(";"):
            iic = i.split("=")
            if len(iic) == 2:
                Scatterinfo.update({iic[0]: retype_string(iic[1])})
        return Scatterinfo

    def reload(self):
        self.usefultindex = []
        for i in range(len(self.pageargs["Infobj"].database.data)):
            if self.pageargs["Infobj"].database.data[i] != None:
                self.usefultindex.append(self.pageargs["Infobj"].database.tindex[i])
        for index, value in enumerate(self.avqt):
            self.avqt[index] = list(set(self.avqt))
        self.LD_index.config(values=self.usefultindex)
        self.FFT_Qt.config(values=[""] + self.avqt[0])
        self.box_0D.config(values=[""] + self.avqt[0] + ["geometry"])
        self.box_1D.config(values=[""] + ["x1", "x2", "x3"] + self.avqt[1])
        self.box_2D.config(values=[""] + self.avqt[2])
        self.box_3D.config(values=[""] + self.avqt[3])
        self.P2DSur_Qt.config(values=[""] + self.avqt[2])
        self.P2DSur_index.config(values=[""] + self.usefultindex)
        self.P3DSur_Qt.config(values=[""] + self.avqt[2] + self.avqt[3])
        self.P3DSur_index.config(values=[""] + self.usefultindex)
        self.P3DCat_Qt.config(values=[""] + self.avqt[2] + self.avqt[3])
        self.P3DCat_index.config(values=[""] + self.usefultindex)
        Lineusage = [""] + ["x1", "x2", "x3"] + self.avqt[1]
        # ["TimeSequency"]+
        self.Line2d_x_qt.config(values=Lineusage)
        self.Line2d_x_index.config(values=[""] + self.usefultindex)
        self.Line2d_sy_qt.config(values=Lineusage)
        self.Line2d_sy_index.config(values=[""] + self.usefultindex)
        self.Line3d_x_qt.config(values=Lineusage)
        self.Line3d_x_index.config(values=[""] + self.usefultindex)
        self.Line3d_y_qt.config(values=Lineusage)
        self.Line3d_y_index.config(values=[""] + self.usefultindex)
        self.TS3d_y_qt.config(values=Lineusage)
        self.TS_sy_qt.config(values=[""] + self.avqt[0])
        for i in range(self.maxline):
            self.Line2d_y_qt[i].config(values=Lineusage)
            self.Line2d_y_index[i].config(values=[""] + self.usefultindex)
            self.Line3d_z_qt[i].config(values=Lineusage)
            self.Line3d_z_index[i].config(values=[""] + self.usefultindex)
            self.TS_qt[i].config(values=[""] + self.avqt[0])
            self.TS3d_z_qt[i].config(values=Lineusage)

    def initial(self):
        self.hdf5handler = ShockFinderFiguresHDF5(self.tkobj.io_recv)
        self.set_image(self.img["logo"])
        self.add_useless_menu("Database↓")
        LoadData.page(self)
        GlobalSettings.page(self)
        self.add_useless_menu("Figure↓")
        UnitSet.page(self)
        QuickSaved.page(self)
        self.add_useless_menu("-------2D-------")
        TimeSequency.page(self)
        FFT.page(self)
        Line2d.page(self)
        Surface2d.page(self)
        self.add_useless_menu("-------3D-------")
        TimeSequency3d.page(self)
        Line3d.page(self)
        Scatter3d.page(self)
        Surface3d.page(self)
