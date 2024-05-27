import os

try:
    from ShockFinder.Config import ShockFinderDir

    SFXUIlib = os.path.join(ShockFinderDir, "Addon", "GUI", "XUIlib")
    SFXUIImagelib = os.path.join(SFXUIlib, "image")
    Image_SF7 = os.path.join(SFXUIImagelib, "Main_logo.png")
except:
    SFXUIImagelib = ""
    Image_SF7 = "Main_logo.png"


def SF7img_decode():
    try:
        os.rename(Image_SF7, os.path.join(SFXUIImagelib, "Main_logo.py"))
    except:
        pass


def SF7img_encode():
    try:
        os.rename(os.path.join(SFXUIImagelib, "Main_logo.py"), Image_SF7)
    except:
        pass


if __name__ == "__main__":
    SF7img_decode()
