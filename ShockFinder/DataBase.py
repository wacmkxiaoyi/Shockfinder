# File type: Fixed <Class>
# By Junxiang H., 2023/07/03
# wacmk.com/cn Tech. Supp.

# Fixed files do not modify
import ShockFinder.Data as Data
import ShockFinder.Addon.Time as Time


def get_par(args, name, default=None):
    try:
        return args[name]
    except:
        return default


def DBC_Findindex(databases, tind):
    for i in databases:
        try:
            return (i, i.tindex.index(tind))
        except:
            continue
    return None


def DataBaseConnect(*databases):
    print(
        *(
            ["Connecting databases:\n"]
            + [
                "\t" + str(i + 1) + ":\t" + str(databases[i]) + "\n"
                for i in range(len(databases))
            ]
        )
    )
    newdb = DataBase(databases[0].infomation, databases[0].printfun)
    for i in range(max([max(j.tindex) for j in databases]) + 1):
        result = DBC_Findindex(databases, i)
        if result != None:
            db, index = result
            newdb.data.append(db.data[index])
            newdb.tindex.append(db.tindex[index])
        else:
            newdb.data.append(None)
            newdb.tindex.append(-1)
    return newdb


class DataBase:
    data = []
    infomation = {}
    tindex = []
    anaf = []
    vargs = []
    resultnames = []
    loader = None
    filesname = None

    def __init__(self, infomation, printfun=print):
        self.infomation = infomation
        self.printfun = printfun

    def load_data(self, loader, **filesname):
        # for filename in filesname:
        # 	self.data.append(Data(*loader.load(filename)))
        # 	self.data[-1].update(self.infomation)
        self.loader = loader
        self.filesname = {int(i): filesname[i] for i in filesname.keys()}
        self.tindex = list(filesname.keys())

    def update_infomation(self, **infomation):
        self.infomation.update(infomation)
        [i.update(self.infomation) for i in self.data]

    def input_default(self):
        self.data[-1].update(self.infomation)

    def drop_buffer(self, *index):
        for ind in range(len(self.data)) if len(index) == 0 else index:
            self.data[ind] = None

    def update(self, *index, output=True, **quantities):
        if len(index) == 0:
            index = range(len(self.data))
        if output:
            self.printfun("Updating parameters:", quantities)
        for ind in index:
            try:
                self.data[ind].update(quantities)
            except:
                self.data.append(None)
                if output:
                    print("Warning: index", ind, "exceed, creating...")
                if len(self.data) == ind + 1:
                    self.data[ind] = Data.Data({}, quantities)
                    self.tindex.append(ind)

    def update_with_index(self, **quantities):  # 2d quantities
        for key in quantities.keys():
            self.update(int(key), output=False, **quantities[key])

    def analysis_data(self, analyze_fun, *index, **vargs):
        if len(index) == 0:
            index = range(len(self.data))
        info = get_par(vargs, "info")
        qtname = get_par(vargs, "quantity_name")
        resultname = get_par(vargs, "result")
        for ind in index:
            kwargs = {"Dataobj": self.data[ind]}
            if "quantity_name" in analyze_fun.__code__.co_varnames:
                kwargs["quantity_name"] = qtname
            if "vargs" in analyze_fun.__code__.co_varnames:
                kwargs["vargs"] = vargs
            self.printfun(
                'Analyzing "',
                info,
                '" with "',
                resultname,
                '" in index:',
                self.tindex[ind],
                "...",
            )
            self.data[ind] = analyze_fun(**kwargs)

    def save(self, *index, **vargs):
        IOfun = get_par(vargs, "IOfun")
        newrsn = []
        for i in self.resultnames:
            if type(i) not in (list, tuple):
                newrsn.append(i)
            else:
                for j in i:
                    newrsn.append(j)
        if IOfun != None:
            filename = get_par(vargs, "filename", str(int(Time.get_time())))
            if len(index) == 0:
                index = range(len(self.data))
            for ind in index:
                self.printfun("Saving results @ index:", self.tindex[ind], "...")
                pp = list(self.data[ind].grid.keys()) + newrsn + ["geometry"]
                IOfun(filename, self.data[ind], self.tindex[ind], *pp)
                DropBuffer = get_par(vargs, "DropBuffer", True)
                if DropBuffer:
                    self.drop_buffer(ind)

    def save_analyze_pars(self, anaf, **vargs):
        self.anaf.append(anaf)
        self.vargs.append(vargs)
        self.resultnames.append(get_par(vargs, "result"))

    def analyze(self):
        if self.loader == None:  # test mode
            for i in range(len(self.data)):
                for j in range(len(self.anaf)):
                    self.analysis_data(self.anaf[j], i, **self.vargs[j])
                self.save(i, **self.vargs[j])
        else:  # file mode
            for i in self.filesname.keys():
                self.printfun('Loading file "', self.filesname[i], '"...')
                self.data.append(self.loader(self.filesname[i]))
                self.input_default()
                for j in range(len(self.anaf)):
                    self.analysis_data(
                        self.anaf[j], len(self.data) - 1, **self.vargs[j]
                    )
                self.save(len(self.data) - 1, **self.vargs[j])

    def check_quantities(self, quantities=[], *index):
        if len(index) == 0:
            index = range(len(self.data))
        if type(quantities) not in (list, tuple):
            quantities = [quantities]
        for quantity in quantities:
            self.printfun('Checking quantity: "', quantity, '"...')
            for ind in index:
                try:
                    self.data[ind].quantities[quantity]
                except:
                    try:
                        self.printfun(
                            'Error: Quantity: "',
                            quantity,
                            '" not exists...',
                            color="red",
                        )
                    except:
                        self.printfun('Error: Quantity: "', quantity, '" not exists...')
                    return False
        return True

    def get_dimension(self, quantity_name="rho", index=-1):
        return self.data[index].quantities[quantity_name].ndim

    def get_geometry(self, index=-1):
        return self.data[index].quantities["geometry"]

    def build_test_data(self, testdatafun, **vargs):
        self.data = testdatafun(**vargs)
        self.update_infomation()
