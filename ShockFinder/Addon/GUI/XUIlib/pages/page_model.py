# This is a model file for XUI page
# Junxiang H. 2023.07.09
import os
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *

logo = os.path.join("ShockFinder", "Addon", "GUI", "XUIlib", "image", "Figure.png")


class page(page):
    img = {"logo": logo}

    def page_menu1(self):
        self.menu1 = self.add_menu("menu1")
        self.add_item(self.menu1, self.ro_height)
        # ...

    def page_menu2(self):
        self.menu2 = self.add_menu("menu2")
        self.add_item(self.menu1, self.ro_height)
        # ...

    def initial(self):
        self.set_image(self.img["logo"])
        self.page_menu1()
        self.page_menu2()

    def show(self):  # Default page
        self.tkobj.open_smb(None, self.fmbindex)
        self.tkobj.open_ro(None, self.fmbindex, self.menu1)
