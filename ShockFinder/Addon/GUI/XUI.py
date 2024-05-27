# Example.py
import os

try:
    from ShockFinder.Addon.GUI.XUIlib.XUIConfig import (
        Pages as Pages,
    )  # those folders/packages path modified by yourself
except:
    pass

from XenonUI import XUI
from XenonUI.XUIlib.SystemInfo import SystemInfo

try:
    from ShockFinder.Config import ShockFinderDir

    config_file = os.path.join(ShockFinderDir, "Addon", "GUI", "XUIlib", "XUIConfig.py")
except:
    config_file = os.path.join("XUIlib", "XUIConfig.py")
pages_import = "ShockFinder.Addon.GUI.XUIlib.pages"  # aa.bb.cc.pages


def CollectPages():
    pages_dir = os.path.join(*pages_import.split("."))
    import datetime

    pages_except = ("__init__", "page_model")

    def FileNamePreProcess(filename):
        filedir, filename = os.path.split(filename)
        fileindex, filetype = os.path.splitext(filename)
        return (fileindex.split(".")[-1], filedir, filetype.split(".")[1])

    def GetFiles(filedir=os.getcwd(), filetype=""):
        result = ()
        for file in os.listdir(filedir):
            if file.endswith(filetype):
                result += (os.path.join(filedir, file),)
        return result

    strc = (
        "#File type: extension <class page> set\n#By Junxiang H., 2023/07/9\n#wacmk.com/cn Tech. Supp.\n\n#This script updates automaticly! Do not Modify!\n#Update time:"
        + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + "\n\nPages={}\n"
    )
    try:
        vaild_pages = tuple(
            set([FileNamePreProcess(i)[0] for i in GetFiles(pages_dir, "py")])
            - set(pages_except)
        )
    except:
        vaild_pages = tuple(
            set(
                [
                    FileNamePreProcess(i)[0]
                    for i in GetFiles(os.path.join("XUIlib", "pages"), "py")
                ]
            )
            - set(pages_except)
        )
    for i in vaild_pages:
        strc += (
            "import "
            + pages_import
            + "."
            + i
            + " as "
            + i
            + "\n"
            + 'Pages["'
            + i
            + '"]='
            + i
            + "\n"
        )
    if "Help" not in vaild_pages:
        strc += 'import XenonUI.XUIlib.pages.Help as Help\nPages["Help"]=Help\n'
    if "Exit" not in vaild_pages:
        strc += 'import XenonUI.XUIlib.pages.Exit as Exit\nPages["Exit"]=Exit\n'
    file = open(config_file, "w")
    file.writelines(strc)
    file.close()


def show(**args):
    class XUIOBJ:
        def __init__(self, **args):
            try:
                from ShockFinder.Addon.GUI.XUIlib.image.config import SF7img_encode

                SF7img_encode()
            except:
                pass
            try:
                from ShockFinder.Addon.GUI.XUIlib.XUIConfig import (
                    Pages as Pages,
                )  # those folders/packages path modified by yourself
            except Exception as err:
                CollectPages()
                print("XUI error:", err)
                print("XUI reconfigurates completed, please rerun ShockFinder again")
                exit(0)
            args.update({"XUIOBJ": self})
            self.guiobj = XUI()
            self.guiobj.build(**args)
            # systeminfo
            self.systeminfo = SystemInfo(self.guiobj)
            self.systeminfo.lunch(1)
            self.Pages = {}
            for i in reversed(Pages.keys()):
                if i not in ("Exit", "Help"):
                    self.Pages[i] = Pages[i].page(self.guiobj, **args)
            if "Help" in Pages.keys():
                self.Pages["Help"] = Pages["Help"].page(self.guiobj, **args)
            if "Exit" in Pages.keys():
                self.Pages["Exit"] = Pages["Exit"].page(self.guiobj, **args)
            self.iofun = self.guiobj.io_recv

    return XUIOBJ(**args)


if __name__ == "__main__":
    show = os.path.exists(config_file)
    CollectPages()
    if show:
        xui = build()  # you can set some arguments in here as you need
        xui.guiobj.show()
    else:
        print("XUI configurates completed, please rerun script again")
