# Junxiang H. 2023.07.09
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import Image_H, page
from ShockFinder.Config import ShockFinderVersion
from ShockFinder.Addon.GUI.XUIlib.image.config import Image_SF7
from tkinter import *


class page(page):
    img = {"main_logo": Image_SF7, "logo": Image_H}

    def page_default(self):
        self.default_page_smbindex = self.add_menu(
            "ShockFinder " + str(ShockFinderVersion)
        )
        self.default_page_roindex = self.add_item(
            self.default_page_smbindex, self.ro_height
        )
        add_image(
            self.tkobj.ro_item[self.fmbindex][self.default_page_smbindex][
                self.default_page_roindex
            ][1],
            self.img["main_logo"],
            width=self.ro_width,
            height=self.ro_height,
        )

    def page_Document(self):
        intro = self.add_menu("Readme")
        self.add_item(intro, 50)
        self.add_title(intro, "Document of ShockFinder please see:", fg="red")
        self.add_title(intro, "https://www.github/wacmkxiaoyi/shockfinder", fontsize=10)

    def page_author_information(self):
        aui = self.add_menu("Author information")
        self.add_item(aui, 50)
        self.add_title(aui, "Physics Algorithm", fontsize=12)
        self.add_title(aui, "C. B. Singh & Junxiang H.", fg="black", height=100)
        self.add_title(aui, "GUI Frame Design/IO Engine/DBMS", fontsize=12)
        self.add_title(aui, "Junxiang H. (XUIv1.1)", fg="black", height=100)
        self.add_title(aui, "Multi-processes Algorithm/Engine Design", fontsize=12)
        self.add_title(aui, "Junxiang H. & Weihui L. (XMEv3.0)", fg="black")

    def initial(self):
        self.set_image(self.img["logo"])
        self.page_default()
        self.page_author_information()
        self.page_Document()

    def show(self):
        self.tkobj.open_smb(None, self.fmbindex)
        self.tkobj.open_ro(None, self.fmbindex, self.default_page_smbindex)
