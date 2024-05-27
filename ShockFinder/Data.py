# File type: Fixed <Class>
# By Junxiang H., 2023/07/1
# wacmk.com/cn Tech. Supp.

# Fixed files do not modify


class Data:
    def __init__(self, *args):
        self.grid = args[0]
        self.quantities = args[1]

    def update(self, quantities):
        self.quantities.update(quantities)
