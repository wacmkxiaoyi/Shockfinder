# This is a model file for XUI page
# Junxiang H. 2023.07.09

from XenonUI.XUIlib.page import page, Image_A
from .AnalyzePages.GlobalSettings import MultiprocessingEngine, IO, Loader
from .AnalyzePages.AnalysisSettings import Parameters, Quantities
from .AnalyzePages import Save

class page(page):
    img = {"logo": Image_A}
    pars = {}
    parmax = 50
    
    def initial(self):
        self.set_image(self.img["logo"])
        Save.page(self)
        self.add_useless_menu("Global Settings↓")
        MultiprocessingEngine.page(self)
        IO.page(self)
        Loader.page(self)
        self.add_useless_menu("Analysis↓")
        Parameters.page(self)
        Quantities.page(self)
