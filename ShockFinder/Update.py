# File type: <Function> set
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

# This script updates automaticly! Do not Modify!
import os
import numpy as np

try:
    from ShockFinder.Addon.Time import *
    import ShockFinder.Addon.Loader.FilesPreProcess as FilesPreProcess
    import ShockFinder.Addon.Loader.FileNamePreProcess as FileNamePreProcess
    from ShockFinder.Config import ShockFinderDir

    LoaderDir = os.path.join(ShockFinderDir, "Addon", "Loader")
    AnalysisToolDir = os.path.join(ShockFinderDir, "Addon", "AnalysisTool")
    PainterDir = os.path.join(ShockFinderDir, "Addon", "Painter")
    IODir = os.path.join(ShockFinderDir, "Addon", "IO")
    MultiprocessEngineDir = os.path.join(ShockFinderDir, "Addon", "MultiprocessEngine")
    GUIDir = os.path.join(ShockFinderDir, "Addon", "GUI")
except:
    from Addon.Time import *
    import Addon.Loader.FilesPreProcess as FilesPreProcess
    import Addon.Loader.FileNamePreProcess as FileNamePreProcess

    ShockFinderDir = ""
    LoaderDir = os.path.join("Addon", "Loader")
    AnalysisToolDir = os.path.join("Addon", "AnalysisTool")
    PainterDir = os.path.join("Addon", "Painter")
    IODir = os.path.join("Addon", "IO")
    MultiprocessEngineDir = os.path.join("Addon", "MultiprocessEngine")
    GUIDir = os.path.join("Addon", "GUI")
LoaderPass = (
    "__init__",
    "Config",
    "FileNamePreProcess",
    "FilesPreProcess",
    "LoaderModel",
)
AnalysisToolPass = (
    "__init__",
    "Config",
    "AnalysisToolModel",
    "Basic",
    "TestData",
    "Differential",
    "Equilibrium",
    "Mean",
    "Radial",
    "Harmonic",
    "FastFourierTransform",
)
PainterPass = ("__init__", "Config")
IOPass = ("__init__", "Config", "MySQL")
MultiprocessEnginePass = ("__init__", "Config")
GUIPass = ("__init__", "Config")


def get_header_end(modulename, main_fun_name="info"):
    Header = (
        "#File type: extension <Module> set\n#By Junxiang H., 2023/07/1\n#wacmk.com/cn Tech. Supp.\n\n#This script updates automaticly! Do not Modify!\n#Update time:"
        + now()
        + "\n\n"
        + modulename
        + "={}\n"
    )
    End = (
        'if __name__=="__main__":\n\tprint("Testing Model:",__file__)\n\tprint("'
        + modulename
        + ':")\n\tfor i in '
        + modulename
        + '.keys():\n\t\tprint(i,":",'
        + modulename
        + '[i])\n\t\tprint("\\t",'
        + modulename
        + "[i]."
        + main_fun_name
        + ")"
    )
    return (Header, End)


def get_filesstr(modulename, moduledir, modulepass):
    FilesStr = ""
    for i in tuple(
        set(
            [
                FileNamePreProcess.FileNamePreProcess(i)[0]
                for i in FilesPreProcess.GetFiles(moduledir, "py")
            ]
        )
        - set(modulepass)
    ):
        FilesStr += (
            "try:\n\ttry:\n\t\timport ShockFinder.Addon."
            + modulename
            + "."
            + i
            + " as "
            + i
            + '\n\texcept Exception as err:\n\t\tprint("'
            + i
            + 'in ShockFinder dir importing error, reimporting in current dir")\n\t\timport '
            + i
            + "\n\t"
            + modulename
            + '["'
            + i
            + '"]='
            + i
            + '\nexcept Exception as err:\n\tprint("Module: '
            + i
            + ' import failure:",err)\n\n'
        )
    return FilesStr


def Write(cdir, cname, header, body, end):
    filename = os.path.join(cdir, cname)
    file = open(filename, "w")
    file.writelines((header, body, end))
    file.close()


def Update(modulename, moduledir, modulepass, main_fun_name="info", cname="Config.py"):
    print("Update:", modulename, ">>>", os.path.join(moduledir, cname))
    header, end = get_header_end(modulename, main_fun_name)
    Write(
        moduledir, cname, header, get_filesstr(modulename, moduledir, modulepass), end
    )


def Update_all():
    Update("Loader", LoaderDir, LoaderPass, "load")
    Update("AnalysisTool", AnalysisToolDir, AnalysisToolPass, "get")
    Update("Painter", PainterDir, PainterPass)
    Update("MultiprocessEngine", MultiprocessEngineDir, MultiprocessEnginePass, "build")
    Update("GUI", GUIDir, GUIPass, "show")
    Update("IO", IODir, IOPass)


if __name__ == "__main__":
    Update_all()
