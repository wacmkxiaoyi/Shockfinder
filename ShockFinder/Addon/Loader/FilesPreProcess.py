# File type: extension <Function> set
# By Junxiang H., 2023/06/30
# wacmk.com/cn Tech. Supp.

import os


# return Filesdir/Filename.type
def GetFiles(FileDir=os.getcwd(), FilePrefix="data.", FileFormat="04d", FileType="dbl"):
    """
    for root, dirs,files in os.walk(FileDir,topdown=False):
            for file in files:
                    if file.endswith(FileType):
                            result+=(os.path.join(root,file),)
    """
    i = 0
    files = os.listdir(FileDir)
    result = []
    while True:
        file = f"{FilePrefix}{i:{FileFormat}}.{FileType}"
        if file in files:
            result.append(os.path.join(FileDir, file))
            i += 1
        else:
            break
    return result


if __name__ == "__main__":
    print("Testing Model:", __file__)
    print("Testing Function:", GetFiles)
    print("Testing Result:", GetFiles(FileType="py"))
