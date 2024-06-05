import sys, os
import ShockFinder
from ShockFinder.Config import ShockFinderDir
from ShockFinder.Update import Update_all


def drop_bk(strc):
    if strc != "" and (
        strc[0] == "'" and strc[-1] == "'" or strc[0] == '"' and strc[-1] == '"'
    ):
        strc = strc[1:-1]
    return strc


if __name__ == "__main__":  # windows support
    gui = True
    for i in sys.argv[1:]:
        if "=" not in i:
            i = "file=" + i
        if i.split("=")[0] in ("f", "-f", "file"):
            ShockFinder.ShockFinder(drop_bk(i.split("=")[1]))
            gui = False
        elif i.split("=")[0] in ("u", "-u", "update"):
            Update_all()
            gui = False
        elif i.split("=")[0] in ("n", "-n", "new"):  # new=module@filename
            LoaderDir = os.path.join(ShockFinderDir, "Addon", "Loader")
            AnalysisToolDir = os.path.join(ShockFinderDir, "Addon", "AnalysisTool")
            PainterDir = os.path.join(ShockFinderDir, "Addon", "Painter")
            IODir = os.path.join(ShockFinderDir, "Addon", "IO")
            MultiprocessEngineDir = os.path.join(
                ShockFinderDir, "Addon", "MultiprocessEngine"
            )
            GUIDir = os.path.join(ShockFinderDir, "Addon", "GUI")
            modu = i.split("=")[1].split("@")[0]
            mfname = i.split("=")[1].split("@")[1]
            if modu in (
                "Loader",
                "AnalysisTool",
                "Painter",
                "IO",
                "MultiprocessEngine",
                "GUI",
            ):
                import shutil

                if modu == "Loader":
                    shutil.copy(mfname, LoaderDir)
                elif modu == "AnalysisTool":
                    shutil.copy(mfname, AnalysisToolDir)
                elif modu == "Painter":
                    shutil.copy(mfname, PainterDir)
                elif modu == "IO":
                    shutil.copy(mfname, IODir)
                elif modu == "MultiprocessEngine":
                    shutil.copy(mfname, MultiprocessEngineDir)
                elif modu == "GUI":
                    shutil.copy(mfname, GUIDir)
            Update_all()
            gui = False
    if gui:
        ShockFinder.ShockFinder()
