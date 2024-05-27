# File type: <Function>
# By Junxiang H., 2023/07/03
# wacmk.com/cn Tech. Supp.
try:
    import ShockFinder.Addon.Painter.Basic as Basic
except:
    import Basic
import pandas as pd, numpy as np
from scipy.optimize import curve_fit

try:
    from lmfit.models import *

    # import lmfit.model
except:
    print(
        'Warning: The "lmfit" is not installed, auto-Lorentzian-fitting is not supported!'
    )
    print("Please type: pip3 install lmfit to install")
    print("More infomation see: https://lmfit.github.io/")
    print("\n")


def lorentzian(f, A, f0, gamma):
    return A / (1 + ((f - f0) / gamma) ** 2)


def lorentzian_fit(x, y, init_gamma_rate="10%", method="lm"):
    # Perform Lorentzian fitting
    init_gamma_rate = (
        float(init_gamma_rate[:-1]) / 100
        if type(init_gamma_rate) == str and init_gamma_rate[-1] == "%"
        else float(init_gamma_rate)
    )
    initial_guess = [
        np.max(y),
        x[np.argmax(y)],
        init_gamma_rate * (np.max(x) - np.min(x)),
    ]  # A, f0, gamma
    fit_params, covariance = curve_fit(
        lorentzian, x, y, p0=initial_guess, method=method
    )

    # Extract the fitted parameters
    fit_amplitude, fit_peak_frequency, fit_width = fit_params
    return lorentzian(x, fit_amplitude, fit_peak_frequency, fit_width)


def Fitting(x, y, *peak_data, default_mode="gl"):
    """Fit multiple Lorentzian peaks to the given data."""
    xdraft = "(x-center+abs(x-center))/2"
    '''
	class DraftPowerLawModel(lmfit.model.Model):
		def __init__(self, independent_vars=['x'], prefix='', nan_policy='raise',
				 **kwargs):
			kwargs.update({'prefix': prefix, 'nan_policy': nan_policy,
						   'independent_vars': independent_vars})
			def dfpl(x, amplitude=1, exponent=1.0, center=1.0,sign=1):
				return amplitude*(1+(sign*(x-center+np.abs(x-center))/2)**exponent)
			super().__init__(dfpl, **kwargs)

		def guess(self, data, x, **kwargs):
			"""Estimate initial model parameter values from data."""
			try:
				expon, amp = np.polyfit(np.log(x[np.where(x)>self.initcenter]+1.e-14), np.log(data[np.where(x)>self.initcenter]+1.e-14), 1)
			except TypeError:
				expon, amp = 1, np.log(abs(max(data[np.where(x)>self.initcenter])+1.e-9))

			pars = self.make_params(amplitude=np.exp(amp), exponent=expon,center=self.initcenter)
			return update_param_vals(pars, self.prefix, **kwargs)
	class DraftExponentialModel(lmfit.model.Model):
		def __init__(self, independent_vars=['x'], prefix='', nan_policy='raise',
				 **kwargs):
			kwargs.update({'prefix': prefix, 'nan_policy': nan_policy,
						   'independent_vars': independent_vars})
			def dfexp(x, amplitude=1, decay=1, center=1.0,sign=1):
				decay = not_zero(decay)
				return amplitude*(1+np.exp(-sign*(x-center+np.abs(x-center))/2/decay))
			super().__init__(dfexp, **kwargs)
		def guess(self, data, x, **kwargs):
			"""Estimate initial model parameter values from data."""
			try:
				sval, oval = np.polyfit(x[np.where(x)>self.initcenter], np.log(abs(data[np.where(x)>self.initcenter])+1.e-15), 1)
			except TypeError:
				sval, oval = 1., np.log(abs(max(data[np.where(x)>self.initcenter])+1.e-9))
			pars = self.make_params(amplitude=np.exp(oval), decay=-1.0/sval,center=self.initcenter)
			return update_param_vals(pars, self.prefix, **kwargs)
	'''

    def DraftPowerLawModel(prefix=""):
        script = """
def dfp(x, amplitude=1, exponent=1.0, center=1.0,factor=1.0):
	return amplitude*(1+factor*((x-center+abs(x-center))/2)**exponent)
			"""
        return ExpressionModel(
            "dfp(x,amplitude,exponent,center,factor)",
            init_script=script,
            independent_vars=["x"],
            nan_policy="omit",
        )

    def DraftExponentialModel(prefix=""):
        script = """
def dfexp(x, amplitude=1, factor=1, center=1.0):
	return amplitude*exp((x-center+abs(x-center))/2*factor)
			"""
        return ExpressionModel(
            "dfexp(x,amplitude,factor,center)",
            init_script=script,
            independent_vars=["x"],
            nan_policy="omit",
        )

    BuiltinModels = {
        "l": LorentzianModel,
        "L": SplitLorentzianModel,
        "p": PowerLawModel,
        "P": DraftPowerLawModel,
        "g": GaussianModel,
        "G": ExponentialGaussianModel,
        "I": LinearModel,
        "Q": QuadraticModel,
        "N": PolynomialModel,
        "e": ExponentialModel,
        "E": DraftExponentialModel,
        "S": SineModel,
        "c": ConstantModel,
    }
    if len(peak_data) == 0:
        model = LorentzianModel(prefix="Main")
        result = model.fit(y, model.make_params(), x=x)
    else:
        peak_data = list(peak_data)
        models = ConstantModel(prefix="BKG")
        params = models.make_params(c=0)
        for i in range(len(peak_data)):
            if type(peak_data[i]) != dict:
                peak_data[i] = {"name": "p" + str(i), "center": peak_data[i]}
            model = []
            if "mode" in peak_data[i].keys():
                mode = peak_data[i]["mode"]["value"]
            else:
                mode = default_mode
            for j in mode:
                model.append(BuiltinModels[j](prefix=peak_data[i]["name"] + "_" + j))
                if j in "PE":
                    newkwargs = {}
                    for k in peak_data[i].keys():
                        if k not in ("mode", "name"):
                            if k not in newkwargs.keys():
                                newkwargs[k] = peak_data[i][k]
                            else:
                                newkwargs[k].update(peak_data[i][k])
                    # print(peak_data[i])
                    params.update(model[-1].make_params(**newkwargs))
                else:
                    params.update(model[-1].make_params())
                    for k in peak_data[i].keys():
                        try:
                            params[peak_data[i]["name"] + "_" + j + k].set(
                                **peak_data[i][k]
                            )
                        except Exception as err:
                            # print(err)
                            pass
                models += model[-1]
        init = models.eval(params, x=x)
        try:
            result = models.fit(y, params, x=x)
        except Exception as err:
            print(err)
            try:
                result = models.fit(y, params, x=x, nan_policy="omit")
            except:
                result = models.fit(y, params, x=x, nan_policy="propagate")
    return result


def CreateLine(**args):
    x = Basic.get_par(args, "x")
    y = Basic.get_par(args, "y")
    z = Basic.get_par(args, "z")
    if type(x) == type(None) or type(y) == type(None):
        return None
    label = Basic.get_par(args, "label", "")
    color = Basic.get_par(args, "color")
    linestyle = Basic.get_par(args, "linestyle", "-")
    if type(z) != type(None):
        line = {"x": x, "y": y, "z": z}
    else:
        line = {"x": x, "y": y}
    lineinfo = {
        "label": None if label == None else Basic.CharUndecode(label),
        "color": Basic.set_None(color),
        "linestyle": linestyle,
    }
    for i in args.keys():
        if i not in lineinfo.keys() and i not in line.keys():
            lineinfo[i] = args[i]
    return (line, lineinfo)


def FormatLine(line, lineinfo, lineid):
    lineframe = pd.DataFrame(line, dtype=float)
    lineinfoframe = pd.DataFrame(lineinfo, index=[lineid])
    return (lineframe, lineinfoframe)


def DecodeLine(lineframe, lineinfoframe):
    data = dict(
        zip(
            ["x", "y", "z"],
            [np.array(list(lineframe.to_dict()[i].values())) for i in lineframe.keys()],
        )
    )
    data.update(lineinfoframe.to_dict())
    return CreateLine(**data)


def info():
    print("Module:", __file__)


if __name__ == "__main__":
    x = np.arange(0, 100, 0.1)
    line0, lineinfo0 = CreateLine(x=x, y=x**2)
    line0frame, line0infoframe = FormatLine(line0, lineinfo0, 0)
    # print(line0frame,"\n",line0infoframe)
    print(DecodeLine(line0frame, line0infoframe.loc[0]))
