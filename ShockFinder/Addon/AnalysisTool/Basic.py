# File type: algroithm <Function> set
# By Junxiang H., 2023/07/02
# wacmk.com/cn Tech. Supp.


def get_par(Dataobj, vargs, quantity_name, default=None):
    if (
        quantity_name not in Dataobj.quantities.keys()
        and quantity_name not in vargs.keys()
    ):
        return default
    try:
        return vargs[quantity_name]
    except:
        return Dataobj.quantities[quantity_name]
