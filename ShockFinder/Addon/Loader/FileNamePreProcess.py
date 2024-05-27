# File type: <Function> return tuple (time_index, dir, file_type)
# By Junxiang H., 2023/06/30
# wacmk.com/cn Tech. Supp.

import os


def FileNamePreProcess(filename):
    filedir, filename = os.path.split(filename)
    fileindex, filetype = os.path.splitext(filename)
    return (fileindex.split(".")[-1], filedir, filetype.split(".")[1])


if __name__ == "__main__":
    print("Testing Model:", __file__)
    testvar = "testfolder1/testfolder2/testfolder3/testindex.testtype"
    print("Testing Var:", testvar)
    print("Testing Result:", FileNamePreProcess(testvar))
