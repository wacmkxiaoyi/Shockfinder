# File type: Fixed <Function> return <Object: Data>
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

# Fixed files do not modify

try:
    from ShockFinder.Addon.Loader.Config import Loader
except:
    from Addon.Loader.Config import Loader


def Load(filename, loadername):
    return Loader[loadername].load(filename)
