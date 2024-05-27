# File type: Basic Default Value and libraries, please modify with the situation
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

import os

ShockFinderVersion = 7.4
ShockFinderDir = os.path.join(__file__.rsplit("ShockFinder", 1)[0], "ShockFinder")
ShockFinderHeader = (
    "■■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■",
    "■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■■",
    "■■■■■■■■■□△■■■■■■■■■■■■■■■■■■■■■",
    "■■■■■■■■□■△■◁■■■■■■■ShockFinder v" + str(ShockFinderVersion) + "■■■■",
    "■■■■■■■□■■△■■■■■■■■■■■■■■■■■■■■■",
    "■■■■◁■□■■■■■■■■■■Junxiang H. &  C. B. Singh■■",
    "■■■■■■■□■■▽■■■■■■■■■■■■■■■■■■■■■",
    "■■■■■■■■□■▽■◁■■■■■wacmk.com/cn Tech. Supp.■■",
    "■■■■■■■■■□▽■■■■■■■■■■■■■■■■■■■■■",
    "■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■■",
    "■■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■",
)
[print(i) for i in ShockFinderHeader]
print("\n")
# To Data Object
Default = {
    "output": True,
    "logfile": None,
    "c": 3.0e10,
    "mu": 0.5,
    "k": 1.380649e-16,
    "mp": 1.6726231e-24,
    "gamma": 4 / 3,
}
print("Loading general libraries...")
import ShockFinder.Addon.Time as Time
import ShockFinder.Addon.ConfigReader as ConfigReader

GeneralLib = {
    "Time": Time,
    "ConfigReader": ConfigReader,
}

print("Loading multiprocessing engines library")
try:
    import ShockFinder.Addon.MultiprocessEngine.Config as MConfig

    MultiprocessEngine = MConfig.MultiprocessEngine
except Exception as err:
    print("Loading error:", err, "Please rebuild the config file")

print("Loading analysis tool libraries...")
import ShockFinder.Addon.AnalysisTool.Differential as Differential
import ShockFinder.Addon.AnalysisTool.Equilibrium as Equilibrium
import ShockFinder.Addon.AnalysisTool.Harmonic as Harmonic
import ShockFinder.Addon.AnalysisTool.Mean as Mean
import ShockFinder.Addon.AnalysisTool.Radial as Radial
import ShockFinder.Addon.AnalysisTool.TestData as TestData
import ShockFinder.Addon.AnalysisTool.FastFourierTransform as FastFourierTransform

AnalysisLib = {
    "Differential": Differential,
    "Gradient": Differential.gradient,
    "Divergence": Differential.divergence,
    "Harmonic": Harmonic.get,
    "Harmonic_src": Harmonic,
    "Equilibrium": Equilibrium,
    "Mean": Mean.get,
    "Mean_src": Mean,
    "Radial": Radial.get,
    "Radial_src": Radial,
    "TestData": TestData,
    "FFT": FastFourierTransform.get,
}

print("Loading analysis tools...")
try:
    import ShockFinder.Addon.AnalysisTool.Config as AConfig

    AnalysisTool = AConfig.AnalysisTool
except Exception as err:
    print("Loading error:", err, "Please rebuild the config file")

print("Loading file loader libraries...")
import ShockFinder.Addon.Loader.FilesPreProcess as FPP
import ShockFinder.Addon.Loader.FileNamePreProcess as FNPP

LoaderLib = {"FPP": FPP, "FNPP": FNPP}

print("Loading file loaders...")
try:
    import ShockFinder.Addon.Loader.Config as LConfig

    Loader = LConfig.Loader
except Exception as err:
    print("Loading error:", err, "Please rebuild the config file")

print("Loading figure painters...")
try:
    import ShockFinder.Addon.Painter.Config as PConfig

    Painter = PConfig.Painter
except Exception as err:
    print("Loading error:", err, "Please rebuild the config file")

print("Loading IO engines...")
try:
    import ShockFinder.Addon.IO.Config as IConfig

    IO = IConfig.IO
except Exception as err:
    print("Loading error:", err, "Please rebuild the config file")

print("Loading GUI...")
try:
    import ShockFinder.Addon.GUI.Config as GConfig

    GUI = GConfig.GUI
except Exception as err:
    print("Loading error:", err, "Please rebuild the config file")

try:
    Config = {
        "GeneralLib": GeneralLib,
        "MultiprocessEngine": MultiprocessEngine,
        "AnalysisLib": AnalysisLib,
        "AnalysisTool": AnalysisTool,
        "LoaderLib": LoaderLib,
        "Loader": Loader,
        "Painter": Painter,
        "IO": IO,
        "GUI": GUI,
    }
except Exception as err:
    print("Config setup error:", err, "Please rebuild the config file")
