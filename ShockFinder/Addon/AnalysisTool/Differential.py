# File type: algroithm <Function> set
# By Junxiang H., 2023/07/01
# wacmk.com/cn Tech. Supp.

import numpy as np


def get_dx(a):
    if a.ndim == 3:
        return a[1:, :, :] - a[:-1, :, :]
    elif a.ndim == 2:
        return a[1:, :] - a[:-1, :]
    else:
        return a[1:] - a[:-1]


def get_x(a):
    if a.ndim == 3:
        return (a[1:, :, :] + a[:-1, :, :]) / 2
    elif a.ndim == 2:
        return (a[1:, :] + a[:-1, :]) / 2
    else:
        return (a[1:] + a[:-1]) / 2


def get_dy(a):
    if a.ndim == 3:
        return a[:, 1:, :] - a[:, :-1, :]
    elif a.ndim == 2:
        return a[:, 1:] - a[:, :-1]
    else:
        return None


def get_y(a):
    if a.ndim == 3:
        return (a[:, 1:, :] + a[:, :-1, :]) / 2
    elif a.ndim == 2:
        return (a[:, 1:] + a[:, :-1]) / 2
    else:
        return None


def get_dz(a):
    if a.ndim == 3:
        return a[:, :, 1:] - a[:, :, :-1]
    else:
        return None


def get_z(a):
    if a.ndim == 3:
        return (a[:, :, 1:] + a[:, :, :-1]) / 2
    else:
        return None


def gradient(Dataobj, quantity_name):
    if type(quantity_name) in (np.ndarray, list, tuple):
        for i in quantity_name:
            Dataobj = gradient(Dataobj, i)
        return Dataobj
    if (
        "geometry" not in Dataobj.quantities.keys()
        or quantity_name not in Dataobj.quantities.keys()
    ):
        print(
            "Warning: args: geometry and",
            quantity_name,
            "are needed without definding in 3d gradient calculation",
        )
        return Dataobj
    quantities = {}
    if Dataobj.quantities[quantity_name].ndim == 1:  # 1d
        quantities["Gradient_" + quantity_name + "_x1"] = np.gradient(
            Dataobj.quantities[quantity_name], Dataobj.grid["x1"]
        )
    elif Dataobj.quantities[quantity_name].ndim == 2:  # 2d
        gd = np.gradient(
            Dataobj.quantities[quantity_name], Dataobj.grid["x1"], Dataobj.grid["x2"]
        )
        if Dataobj.quantities["geometry"] in ("SPHERICAL", "POLAR"):
            quantities["Gradient_" + quantity_name + "_x1"] = gd[0]
            quantities["Gradient_" + quantity_name + "_x2"] = gd[1] / Dataobj.grid[
                "x1"
            ].reshape((len(Dataobj.grid["x1"]), 1))
        else:
            quantities["Gradient_" + quantity_name + "_x1"] = gd[0]
            quantities["Gradient_" + quantity_name + "_x2"] = gd[1]
    elif Dataobj.quantities[quantity_name].ndim == 3:  # 3d
        gd = np.gradient(
            Dataobj.quantities[quantity_name],
            Dataobj.grid["x1"],
            Dataobj.grid["x2"],
            Dataobj.grid["x3"],
        )
        if Dataobj.quantities["geometry"] in ("SPHERICAL", "POLAR"):
            quantities["Gradient_" + quantity_name + "_x1"] = gd[0]
            quantities["Gradient_" + quantity_name + "_x2"] = gd[1] / Dataobj.grid[
                "x1"
            ].reshape((len(Dataobj.grid["x1"]), 1, 1))
            if Dataobj.quantities["geometry"] == "SPHERICAL":
                quantities["Gradient_" + quantity_name + "_x3"] = (
                    gd[2]
                    / Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]), 1, 1))
                    / np.sin(
                        Dataobj.grid["x2"].reshape((1, len(Dataobj.grid["x2"]), 1))
                    )
                )
            else:
                quantities["Gradient_" + quantity_name + "_x3"] = gd[2]
        else:
            quantities["Gradient_" + quantity_name + "_x1"] = gd[0]
            quantities["Gradient_" + quantity_name + "_x2"] = gd[2]
            quantities["Gradient_" + quantity_name + "_x3"] = gd[3]
    Dataobj.update(quantities)
    return Dataobj


def divergence_xyz(F, x=None, y=None, z=None):
    """
    Compute the divergence of a vector field F in XYZ coordinates.

    Parameters:
    - F: Multidimensional array where the last dimension corresponds to the components of the field.
              F can be 1D ([Fx]), 2D ([Fx, Fy]), or 3D ([Fx, Fy, Fz]).
    - x, y, z: Arrays representing the grids in the x, y, and z directions, respectively

    Returns:
    - divF: Array representing the divergence of F. Shape corresponds to the input field.
    """

    if F.ndim == 1:  # 1D
        return np.gradient(F, x)

    elif F.ndim == 2:  # 2D
        dFxdx = np.gradient(F, x, axis=0)
        dFydy = np.gradient(F, y, axis=1)
        return dFxdx + dFydy

    elif F.ndim == 3:  # 3D
        dFxdx = np.gradient(F, x, axis=0)
        dFydy = np.gradient(F, y, axis=1)
        dFzdz = np.gradient(F, z, axis=2)
        return dFxdx + dFydy + dFzdz


def divergence_pol(F, r, phi=None, z=None):
    """
    Compute the divergence of a vector field F in cylindrical coordinates (r, phi, z).

    Parameters:
    - F: Multidimensional array where the last dimension corresponds to the components of the field.
             F can be 1D ([Fr]), 2D ([Fr, Fphi]), or 3D ([Fr, Fphi, Fz]).
    - r, phi, z: Arrays representing the grids in the r, phi, and z directions, respectively.

    Returns:
    - divF: Array representing the divergence of F. Shape corresponds to the input field.
    """

    if F.ndim == 1:  # 1D
        return np.gradient(r * F, r) / r

    elif F.ndim == 2:  # 2D
        drFr_dr = np.gradient(r * F, r, axis=0)
        dFphi_dphi = np.gradient(F, phi, axis=1)
        return (drFr_dr + dFphi_dphi) / r.reshape(len(r), 1)

    elif F.ndim == 3:  # 3D
        drFr_dr = np.gradient(r.reshape(len(r), 1, 1) * F, r, axis=0)
        dFphi_dphi = np.gradient(F, phi, axis=1)
        dFz_dz = np.gradient(F, z, axis=2)
        return (drFr_dr + dFphi_dphi) / r.reshape(len(r), 1, 1) + dFz_dz


def divergence_sph(F, r, theta=None, phi=None):
    """
    Compute the divergence of a vector field F in spherical coordinates (r, theta, phi).

    Parameters:
    - F: Array where the last dimension corresponds to the components of the field.
             F can be 1D (just Fr), 2D ([Fr, Ftheta]) or 3D ([Fr, Ftheta, Fphi]).
    - r, theta, phi: Arrays representing the grids in the r, theta, and phi directions.

    Returns:
    - divF: Array representing the divergence of F. Shape corresponds to the input field.
    """
    if F.ndim == 1:  # 1D (just Radial)
        dFr_dr = np.gradient(F, r)
        return (2 / r) * F + dFr_dr

    elif F.ndim == 2:  # 2D (Radial and Polar angle)
        drFr_dr = np.gradient(r.reshape(len(r), 1) ** 2 * F, r, axis=0)
        dFtheta_dtheta = np.gradient(
            np.sin(theta).reshape(1, len(theta)) * F, theta, axis=1
        )
        return (1 / r.reshape(len(r), 1) ** 2) * drFr_dr + (
            1 / (r.reshape(len(r), 1) * np.sin(theta).reshape(1, len(theta)))
        ) * dFtheta_dtheta

    elif F.ndim == 3:  # 3D
        drFr_dr = np.gradient(r.reshape(len(r), 1, 1) ** 2 * F, r, axis=0)
        dFtheta_dtheta = np.gradient(
            np.sin(theta).reshape(1, len(theta), 1) * F, theta, axis=1
        )
        dFphi_dphi = np.gradient(F, phi, axis=2)
        return (1 / r.reshape(len(r), 1, 1) ** 2) * drFr_dr + (
            1 / (r.reshape(len(r), 1, 1) * np.sin(theta).reshape(1, len(theta), 1))
        ) * (dFtheta_dtheta + dFphi_dphi)


def divergence(Dataobj, quantity_name):
    if type(quantity_name) in (np.ndarray, list, tuple):
        for i in quantity_name:
            Dataobj = divergence(Dataobj, i)
        return Dataobj
    quantities = {}
    if (
        "geometry" not in Dataobj.quantities.keys()
        or quantity_name not in Dataobj.quantities.keys()
    ):
        print(
            "Warning: args: geometry and",
            quantity_name,
            "are needed without definding in 3d gradient calculation",
        )
        return Dataobj
    if Dataobj.quantities["geometry"] == "SPHERICAL":
        fun = divergence_sph
    elif Dataobj.quantities["geometry"] == "POLAR":
        fun = divergence_pol
    else:
        fun = divergence_xyz
    try:
        quantities["Divergence_" + quantity_name] = fun(
            Dataobj.quantities[quantity_name],
            Dataobj.grid["x1"],
            Dataobj.grid["x2"],
            Dataobj.grid["x3"],
        )
    except:
        try:
            quantities["Divergence_" + quantity_name] = fun(
                Dataobj.quantities[quantity_name],
                Dataobj.grid["x1"],
                Dataobj.grid["x2"],
            )
        except:
            quantities["Divergence_" + quantity_name] = fun(
                Dataobj.quantities[quantity_name], Dataobj.grid["x1"]
            )

    """
    #abort
    if Dataobj.quantities[quantity_name].ndim==1:#1d
        if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
            if Dataobj.quantities["geometry"]=="SPHERICAL":
                quantities["Divergence_"+quantity_name]=np.gradient(Dataobj.grid["x1"]**2*Dataobj.quantities[quantity_name],Dataobj.grid["x1"])/Dataobj.grid["x1"]**2
            else:
                quantities["Divergence_"+quantity_name]=np.gradient(Dataobj.grid["x1"]*Dataobj.quantities[quantity_name],Dataobj.grid["x1"])/Dataobj.grid["x1"]
        else:
            quantities["Divergence_"+quantity_name]=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"])
    elif Dataobj.quantities[quantity_name].ndim==2:#2d
        if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
            if Dataobj.quantities["geometry"]=="SPHERICAL":
                gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))**2*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))**2
                gd2=np.gradient(np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]))))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]))))
            else:
                gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))
                gd2=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1))
        else:
            gd1,gd2=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"])
        quantities["Divergence_"+quantity_name]=gd1+gd2
    elif Dataobj.quantities[quantity_name].ndim==3:#3d
        if Dataobj.quantities["geometry"] in ("SPHERICAL","POLAR"):
            if Dataobj.quantities["geometry"]=="SPHERICAL":
                gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))**2*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))**2
                gd2=np.gradient(np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))
                gd3=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[2]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))/np.sin(Dataobj.grid["x2"].reshape((1,len(Dataobj.grid["x2"]),1)))
            else:
                gd1=np.gradient(Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))*Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[0]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))
                gd2=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[1]/Dataobj.grid["x1"].reshape((len(Dataobj.grid["x1"]),1,1))
                gd3=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])[2]
        else:
            gd1,gd2,gd3=np.gradient(Dataobj.quantities[quantity_name],Dataobj.grid["x1"],Dataobj.grid["x2"],Dataobj.grid["x3"])
        quantities["Divergence_"+quantity_name]=gd1+gd2+gd3
    """
    Dataobj.update(quantities)
    return Dataobj


def result(quantity_name=None, anafname=None):
    if anafname == "Gradient":
        return [
            "Gradient_" + i + "_x1" for i in quantity_name.split(",")
        ]  # +["Gradient_"+i+"_x2" for i in quantity_name.split(",")]+["Gradient_"+i+"_x3" for i in quantity_name.split(",")]
    elif anafname == "Divergence":
        return ["Divergence_" + i for i in quantity_name.split(",")]
    return ()


"""
#abort!
def integrate(fx,x): #inte@ f(x)dx
    if len(x)>0:
        result=integrate(fx,x[1:])
        if type(result) !=np.ndarray or result.ndim==0:
            result=np.full((len(x[0]),),result)
        return np.trapz(result,x=x[0])  
    return fx

def integrate_single(fx,x):
    if type(fx) !=np.ndarray or fx.ndim==0:
        fx=np.full((len(x),),fx)
    return np.trapz(fx,x)


def integrate_body(f,x,y=None,z=None):
    if type(f)!=np.ndarray or f.ndim<=1:
        if type(y)==None:
            y=np.arange(0,1,1/len(x))
        if type(z)==None:
            z=np.arange(0,1,1/len(x))
        return integrate_single(integrate(f,(y,z)),x)
    elif f.ndim==2:
        if type(y)==None:
            y=np.arange(0,1,1/len(f[0]))
        if type(z)==None:
            z=np.arange(0,1,1/len(f[0]))
        return integrate(integrate_single(f,z),(x,y))
    elif f.ndim==3:
        if type(y)==None:
            y=np.arange(0,1,1/len(f[0]))
        if type(z)==None:
            z=np.arange(0,1,1/len(f[0][0]))
        return integrate(f,(x,y,z))

def integrate_surface_xoy(f,x=None,y=None,default_step=10000):
    if type(f)!=np.ndarray or f.ndim<=1:
        if type(x)==None:
            x=np.arange(0,1,1/len(f))
        if type(y)==None:
            y=np.arange(0,1,1/default_step)
        return integrate(f,(x,y))
    elif f.ndim>=2:
        if type(x)==None:
            x=np.arange(0,1,1/len(f))
        if type(y)==None:
            y=np.arange(0,1,1/len(f[0]))
        return integrate(f,(x,y))

def integrate_sph_body(f,r,th=None,phi=None):
    if type(f) !=np.ndarray or f.ndim<=1:
        if type(th)==type(None):
            th=np.arange(0,np.pi,np.pi/len(r))
        if type(phi)==type(None):
            phi=np.arange(0,2*np.pi,2*np.pi/len(r))
        return integrate_single(f*r**2*integrate(np.sin(th),(th,phi)),r)
    elif f.ndim==2:#r th
        if type(th)==type(None):
            th=np.arange(0,np.pi,np.pi/len(f[0]))
        if type(phi)==type(None):
            phi=np.arange(0,2*np.pi,2*np.pi/len(r))
        return integrate(f*r.reshape((len(r),1))**2*np.sin(th.reshape((1,len(th))))*integrate_single(1,phi),(r,th))
    else: #r th phi
        if type(th)==type(None):
            th=np.arange(0,np.pi,np.pi/len(f[0]))
        if type(phi)==type(None):
            phi=np.arange(0,2*np.pi,2*np.pi/len(f[0][0]))
        return integrate(f*r.reshape((len(r),1,1))**2*np.sin(th.reshape((1,len(th),1))),(r,th,phi))

def integrate_sph_sur(f,r,th=None,phi=None,default_step=10000): #r is fixed
    if type(th)==type(None):
        if type(f) !=np.ndarray or f.ndim==0:
            th=np.arange(0,np.pi,np.pi/default_step)
        elif f.ndim==1:
            th=np.arange(0,np.pi,np.pi/len(f))
        elif f.ndim==2:
            th=np.arange(0,np.pi,np.pi/len(f[0]))
        elif f.ndim==3:
            th=np.arange(0,np.pi,np.pi/len(f[0][0]))
    if type(phi)==type(None):
        if type(f) !=np.ndarray or f.ndim==0:
            phi=np.arange(0,2*np.pi,2*np.pi/default_step)
        elif f.ndim==1:
            phi=np.arange(0,2*np.pi,2*np.pi/len(f))
        elif f.ndim==2:
            phi=np.arange(0,2*np.pi,2*np.pi/len(f[0]))
        elif f.ndim==3:
            phi=np.arange(0,2*np.pi,2*np.pi/len(f[0][0]))
    if type(f) !=np.ndarray or f.ndim<=1: #th
        return integrate_single(f*r**2*np.sin(th)*integrate_single(1,phi),th)
    elif f.ndim==2: #th phi
        return integrate(f*r**2*np.sin(th.reshape((1,len(th)))),(th,phi))
    elif f.ndim==3: #th phi
        return integrate(f*r**2*np.sin(th.reshape((1,len(th),1))),(th,phi))

def integrate_pol_body(f,r,phi=None,z=None):
    #f=f(x,th,z)
    if type(f) !=np.ndarray or f.ndim<=1: #r 
        if type(phi)==type(None):
            phi=np.arange(0,2*np.pi,2*np.pi/len(r))
        if type(z)==type(None):
            z=np.arange(0,1,1/len(r))
        return integrate_single(f*r*integrate(1,(phi,z)),r)
    elif f.ndim==2:#r phi
        if type(phi)==type(None):
            phi=np.arange(0,2*np.pi,2*np.pi/len(f[0]))
        if type(z)==type(None):
            z=np.arange(0,1,1/len(r))
        return integrate(f*r.reshape((len(r),1))*integrate_single(1,z),(r,phi))
    else: #x z th
        if type(phi)==type(None):
            phi=np.arange(0,2*np.pi,2*np.pi/len(f[0]))
        if type(z)==type(None):
            z=np.arange(0,1,1/len(f[0][0]))
        return integrate(f*r.reshape((len(r),1,1))*phi.reshape((1,len(phi),1)),(r,phi,z))


def integrate_pol_sur_xoz(f,x,z,phi=None,default_step=10000): #x is fixed
    if type(phi)==type(None):
        if type(f) !=np.ndarray or f.ndim==0:
            phi=np.arange(0,np.pi,2*np.pi/default_step)
        elif f.ndim==1:
            phi=np.arange(0,np.pi,2*np.pi/len(f))
        elif f.ndim==2:
            phi=np.arange(0,np.pi,2*np.pi/len(f[0]))
        elif f.ndim==3:
            phi=np.arange(0,np.pi,2*np.pi/len(f[0][0]))
    if type(f) !=np.ndarray or f.ndim<=1: #z
        return integrate_single(f*x*integrate_single(1,phi),z)
    elif f.ndim==2: #z th
        return integrate(f*x*phi.reshape((1,len(phi))),(phi,z))
    elif f.ndim==3: #z th
        return integrate(f*x*phi.reshape((1,len(phi),1)),(phi,z))


def integrate_pol_sur_xop(f,x,z,phi=None,default_step=10000): #z is fixed
    if type(phi)==type(None):
        if type(f) !=np.ndarray or f.ndim==0:
            phi=np.arange(0,np.pi,2*np.pi/default_step)
        elif f.ndim==1:
            phi=np.arange(0,np.pi,2*np.pi/len(f))
        elif f.ndim==2:
            phi=np.arange(0,np.pi,2*np.pi/len(f[0]))
        elif f.ndim==3:
            phi=np.arange(0,np.pi,2*np.pi/len(f[0][0]))
    if type(f) !=np.ndarray or f.ndim<=1: #x
        return integrate_single(f*x*integrate_single(1,phi),x)
    elif f.ndim==2: #x th
        return integrate(f*x.reshape((len(x),1))*phi.reshape((1,len(phi))),(x,phi))
    elif f.ndim==3: #x th
        return integrate(f*x.reshape((len(x),1,1))*phi.reshape((1,len(phi),1)),(x,phi))

"""


def integrate_body(fx, x=None, y=None, z=None):  # by chat
    if type(fx) in (float, int):
        mark = 1
        if x != None:
            mark *= x[-1] - x[0]
        if y != None:
            mark *= y[-1] - y[0]
        if z != None:
            mark *= z[-1] - z[0]
        return mark * fx
    if fx.ndim == 1:
        x = np.linspace(0, 1, len(fx)) if x is None else x
        if len(x) != len(fx):
            raise ValueError("Length of x must match the length of 1D fx.")
        result = np.trapz(fx, x)

    elif fx.ndim == 2:
        x = np.linspace(0, 1, fx.shape[0]) if x is None else x
        y = np.linspace(0, 1, fx.shape[1]) if y is None else y

        if len(x) != fx.shape[0]:
            raise ValueError("Length of x must match the first dimension of 2D fx.")
        if len(y) != fx.shape[1]:
            raise ValueError("Length of y must match the second dimension of 2D fx.")

        result = np.trapz(np.trapz(fx, y, axis=-1), x, axis=0)

    elif fx.ndim == 3:
        x = np.linspace(0, 1, fx.shape[0]) if x is None else x
        y = np.linspace(0, 1, fx.shape[1]) if y is None else y
        z = np.linspace(0, 1, fx.shape[2]) if z is None else z

        if len(x) != fx.shape[0]:
            raise ValueError("Length of x must match the first dimension of 3D fx.")
        if len(y) != fx.shape[1]:
            raise ValueError("Length of y must match the second dimension of 3D fx.")
        if len(z) != fx.shape[2]:
            raise ValueError("Length of z must match the third dimension of 3D fx.")

        result = np.trapz(np.trapz(np.trapz(fx, z, axis=-1), y, axis=-1), x, axis=0)

    else:
        raise ValueError("The fx array should be either 1D, 2D, or 3D.")

    if not isinstance(result, (float, np.float64)):
        raise ValueError("Integration did not result in a scalar value as expected.")

    return result


def integrate_pol_body2(f, r=None, phi=None, z=None):
    # Default values
    # Default values
    r = np.linspace(0, 1, f.shape[0]) if r is None else r
    phi = np.linspace(0, 2 * np.pi, f.shape[1]) if phi is None and f.ndim > 1 else phi
    z = np.linspace(0, 1, f.shape[2]) if z is None and f.ndim == 3 else z

    # Check shapes
    if len(r) != f.shape[0]:
        raise ValueError("Length of r must match the first dimension of f.")
    if f.ndim > 1 and len(phi) != f.shape[1]:
        raise ValueError("Length of phi must match the second dimension of f.")
    if f.ndim == 3 and len(z) != f.shape[2]:
        raise ValueError("Length of z must match the third dimension of f.")

    # Integration
    result = f

    # For 1D data
    if f.ndim == 1:
        result = np.trapz(result * r, r)

    # For 2D and 3D data
    else:
        if f.ndim >= 2:
            result = np.trapz(
                result * r[:, np.newaxis], r, axis=0
            )  # account for the r in the differential
            if result.ndim > 1:  # check if the result is still multidimensional
                result = np.trapz(result, phi, axis=-1)

        if result.ndim > 1:  # check again, to integrate over z if needed
            result = np.trapz(result, z, axis=-1)

    return result


def integrate_pol_body(f, r=None, phi=None, z=None):
    if type(f) in (float, int):
        mark = 1
        if r != None:
            mark *= 0.5 * (r[-1] ** 2 - r[0] ** 2)
        if phi != None:
            mark *= phi
        else:
            mark *= np.pi
        if z != None:
            mark *= z[-1] - z[0]
        return mark * f
    # Default values
    r_values = np.linspace(0, 1, f.shape[0]) if r is None else r
    try:
        phi_values = np.linspace(0, 2 * np.pi, f.shape[1]) if phi is None else phi
    except:
        phi_values = np.linspace(0, 2 * np.pi, 100) if phi is None else phi
    try:
        z_values = np.linspace(0, 1, f.shape[2]) if z is None else z
    except:
        z_values = np.linspace(0, 1, 100) if z is None else z
    # Integration
    result = f

    # 1D data: f is symmetric in both phi and z directions
    if f.ndim == 1:
        result = np.trapz(result * r_values, r_values)
        result *= phi_values[-1] - phi_values[0]  # Integration over phi
        result *= z_values[-1] - z_values[0]  # Integration over z

    # 2D data: f is considered homogeneous in r and z if r isn't provided
    elif f.ndim == 2:
        if r is None:
            result = np.mean(result, axis=0)  # Mean over r (homogeneous)
            result *= 0.5 * (r_values[-1] ** 2 - r_values[0] ** 2)  # Integration over r
        else:
            result = np.trapz(result * r_values[:, np.newaxis], r_values, axis=0)

        result = np.trapz(result, phi_values)
        result *= z_values[-1] - z_values[0]  # Integration over z

    # 3D data: No assumed symmetries
    else:
        result = np.trapz(result * r_values[:, np.newaxis, np.newaxis], r_values, axis=0)
        result = np.trapz(result, phi_values, axis=0)
        result = np.trapz(result, z_values)

    if not isinstance(result, (float, np.float64)):
        raise ValueError("Integration did not result in a scalar value as expected.")

    return result


def integrate_sph_body(f, r=None, th=None, phi=None):
    if type(f) in (float, int):
        mark = 1
        if r != None:
            mark *= (r[-1] ** 3 - r[0] ** 3) / 3
        else:
            mark /= 3
        if th != None:
            mark *= np.cos(th[0]) - np.cos(th[-1])
        else:
            mark *= 2
        if phi != None:
            mark *= phi[-1] - phi[0]
        else:
            mark *= 2 * np.pi
        return mark * f
    # Default values
    r_values = np.linspace(0, 1, f.shape[0]) if r is None else r
    try:
        th_values = np.linspace(0, np.pi, f.shape[1]) if th is None else th
    except:
        th_values = np.linspace(0, np.pi, 100) if th is None else th
    try:
        phi_values = np.linspace(0, 2 * np.pi, f.shape[2]) if phi is None else phi
    except:
        phi_values = np.linspace(0, 2 * np.pi, 100) if phi is None else phi

    # Integration
    result = f

    # 1D data: f is symmetric in both theta and phi directions
    if f.ndim == 1:
        result = np.trapz(result * r_values**2, r_values)
        result *= phi_values[-1] - phi_values[0]  # Integration over phi
        result *= np.cos(th_values[0]) - np.cos(th_values[-1])  # Integration over theta

    # 2D data: f is considered homogeneous in r and phi if r isn't provided
    elif f.ndim == 2:
        if r is None:
            result = np.mean(result, axis=0)  # Mean over r (homogeneous)
            result *= (r_values[-1] ** 3 - r_values[0] ** 3) / 3  # Integration over r
        else:
            result = np.trapz(result * r_values[:, np.newaxis] ** 2, r_values, axis=0)

        result = np.trapz(result * np.sin(th_values), th_values)
        result *= phi_values[-1] - phi_values[0]  # Integration over phi

    # 3D data: No assumed symmetries
    else:
        result = np.trapz(
            result * r_values[:, np.newaxis, np.newaxis] ** 2, r_values, axis=0
        )
        result = np.trapz(result * np.sin(th_values[:, np.newaxis]), th_values, axis=0)
        result = np.trapz(result, phi_values)

    if not isinstance(result, (float, np.float64)):
        raise ValueError("Integration did not result in a scalar value as expected.")

    return result


def get_closest_index(value, dim):
    return min(range(len(dim)), key=lambda i: abs(dim[i] - value))


def get_indices_for_range(value_range, dim):
    return [
        get_closest_index(value_range[0], dim),
        get_closest_index(value_range[1], dim),
    ]


def get_indices_for_ranges(value_ranges, dim):
    return [get_indices_for_range(value_range, dim) for value_range in value_ranges]


def integrate_surface(f, x, y, z=None, xr=(), yr=(), zr=(), surface=()):
    if not surface:
        raise ValueError("Please specify a surface to integrate over.")

    if len(xr) > len(surface):
        raise ValueError("Length of xr must not exceed the length of surface.")
    if len(yr) > len(surface):
        raise ValueError("Length of yr must not exceed the length of surface.")
    if type(z) != type(None) and len(zr) > len(surface):
        raise ValueError("Length of zr must not exceed the length of surface.")

    # Helper function to get index closest to the value

    # Initialize the total flux

    result = []
    for i, surf in enumerate(surface):
        total_flux = 0
        sign = 1 if not surf.startswith("-") else -1
        surf_dim = surf[-1]  # Extract the dimension

        boundaries = {"min": 0, "max": -1}

        # Determine range or boundary based on the surface dimension
        if surf_dim == "x":
            boundary = xr[i] if i < len(xr) else "both"
            y_vals = (
                get_indices_for_ranges(yr[i], y)
                if i < len(yr) and len(yr[i]) > 0
                else []
            )
            z_vals = (
                get_indices_for_ranges(zr[i], z)
                if type(z) != type(None) and i < len(zr) and len(zr[i]) > 0
                else []
            )
            if y_vals == z_vals and y_vals == []:
                y_vals.append(range(len(y) + 1))
                if f.ndim == 3:
                    for j in y_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(y_vals)):
                        z_vals.append(zr[i][j])
            elif y_vals == []:
                for j in z_vals:
                    y_vals.append(range(len(y) + 1))
            elif z_vals == []:
                if f.ndim == 3:
                    for j in y_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(y_vals)):
                        z_vals.append(zr[i][j])

        elif surf_dim == "y":
            boundary = yr[i] if i < len(yr) else "both"
            x_vals = (
                get_indices_for_ranges(xr[i], x)
                if i < len(xr) and len(xr[i]) > 0
                else []
            )
            z_vals = (
                get_indices_for_ranges(zr[i], z)
                if type(z) != type(None) and i < len(zr) and len(zr[i]) > 0
                else []
            )
            if x_vals == z_vals and x_vals == []:
                x_vals.append(range(len(x) + 1))
                if f.ndim == 3:
                    for j in x_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(x_vals)):
                        z_vals.append(zr[i][j])
            elif x_vals == []:
                for j in z_vals:
                    x_vals.append(range(len(x) + 1))
            elif z_vals == []:
                if f.ndim == 3:
                    for j in x_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(x_vals)):
                        z_vals.append(zr[i][j])

        elif surf_dim == "z":
            boundary = zr[i] if i < len(zr) else "both"
            x_vals = (
                get_indices_for_ranges(xr[i], x)
                if i < len(xr) and len(xr[i]) > 0
                else []
            )
            y_vals = (
                get_indices_for_ranges(yr[i], y)
                if i < len(yr) and len(yr[i]) > 0
                else []
            )
            if x_vals == y_vals and x_vals == []:
                x_vals.append(range(len(x) + 1))
                y_vals.append(range(len(y) + 1))
            elif x_vals == []:
                for j in y_vals:
                    x_vals.append(range(len(x) + 1))
            elif y_vals == []:
                for j in x_vals:
                    y_vals.append(range(len(y) + 1))

        # Check for 0 values
        if boundary == 0:
            boundary = "min"

        # Calculate flux based on explicit grid values
        if surf_dim == "x":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(y_vals)):
                    slice_data = (
                        f[boundary_val, y_vals[j][0] : y_vals[j][-1]]
                        if f.ndim == 2
                        else f[boundary_val, y_vals[j][0] : y_vals[j][-1]][
                            :, z_vals[j][0] : z_vals[j][-1]
                        ]
                    )
                    tmpl = np.trapz(slice_data, y[y_vals[j][0] : y_vals[j][-1]], axis=0)
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, z[z_vals[j][0] : z_vals[j][-1]])
                    elif len(z_vals) > 0:
                        tmpl *= z_vals[j][-1] - z_vals[j][0]
                    total_flux += sign * tmpl

        elif surf_dim == "y":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(x_vals)):
                    slice_data = (
                        f[x_vals[j][0] : x_vals[j][-1], boundary_val]
                        if f.ndim == 2
                        else f[x_vals[j][0] : x_vals[j][-1], boundary_val][
                            :, z_vals[j][0] : z_vals[j][-1]
                        ]
                    )
                    tmpl = np.trapz(slice_data, x[x_vals[j][0] : x_vals[j][-1]], axis=0)
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, z[z_vals[j][0] : z_vals[j][-1]])
                    elif len(z_vals) > 0:
                        tmpl *= z_vals[j][-1] - z_vals[j][0]
                    total_flux += sign * tmpl

        elif surf_dim == "z":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(x_vals)):
                    slice_data = f[x_vals[j][0] : x_vals[j][-1], :, boundary_val][
                        :, y_vals[j][0] : y_vals[j][-1]
                    ]
                    tmpl = np.trapz(slice_data, x[x_vals[j][0] : x_vals[j][-1]], axis=0)
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, y[y_vals[j][0] : y_vals[j][-1]])
                    total_flux += sign * tmpl

        result.append(total_flux)

    return result


def integrate_pol_sur(f, r, phi, z=None, rr=(), pr=(), zr=(), surface=()):
    if not surface:
        raise ValueError("Please specify a surface to integrate over.")

    if len(rr) > len(surface):
        raise ValueError("Length of rr must not exceed the length of surface.")
    if len(pr) > len(surface):
        raise ValueError("Length of pr must not exceed the length of surface.")
    if type(z) != None and len(zr) > len(surface):
        raise ValueError("Length of zr must not exceed the length of surface.")

    result = []

    for i, surf in enumerate(surface):
        total_flux = 0
        sign = 1 if not surf.startswith("-") else -1
        surf_dim = surf.replace("-", "")

        boundaries = {"min": 0, "max": -1}

        # Similar to your Cartesian version but adapted for polar coordinates
        if surf_dim == "r":
            boundary = rr[i] if i < len(rr) else "both"
            phi_vals = (
                get_indices_for_ranges(pr[i], phi)
                if i < len(pr) and len(pr[i]) > 0
                else []
            )
            z_vals = (
                get_indices_for_ranges(zr[i], z)
                if type(z) != None and i < len(zr) and len(zr[i]) > 0
                else []
            )
            if phi_vals == z_vals and phi_vals == []:
                phi_vals.append(range(len(phi) + 1))
                if f.ndim == 3:
                    for j in phi_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(phi_vals)):
                        z_vals.append(zr[i][j])
            elif phi_vals == []:
                for j in z_vals:
                    phi_vals.append(range(len(phi) + 1))
            elif z_vals == []:
                if f.ndim == 3:
                    for j in phi_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(phi_vals)):
                        z_vals.append(zr[i][j])

            # ... Rest of the logic ...

        elif surf_dim == "phi":
            boundary = pr[i] if i < len(pr) else "both"
            r_vals = (
                get_indices_for_ranges(rr[i], r)
                if i < len(rr) and len(rr[i]) > 0
                else []
            )
            z_vals = (
                get_indices_for_ranges(zr[i], z)
                if type(z) != None and i < len(zr) and len(zr[i]) > 0
                else []
            )
            if r_vals == z_vals and r_vals == []:
                r_vals.append(range(len(r) + 1))
                if f.ndim == 3:
                    for j in r_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(r_vals)):
                        z_vals.append(zr[i][j])
            elif r_vals == []:
                for j in z_vals:
                    r_vals.append(range(len(r) + 1))
            elif z_vals == []:
                if f.ndim == 3:
                    for j in r_vals:
                        z_vals.append(range(len(z) + 1))
                elif len(zr) > i and len(zr[i]) > 0:
                    for j in range(len(r_vals)):
                        z_vals.append(zr[i][j])
            # ... Rest of the logic ...

        elif surf_dim == "z":
            boundary = zr[i] if i < len(zr) else "both"
            r_vals = (
                get_indices_for_ranges(rr[i], r)
                if i < len(rr) and len(rr[i]) > 0
                else []
            )
            phi_vals = (
                get_indices_for_ranges(pr[i], phi)
                if i < len(pr) and len(pr[i]) > 0
                else []
            )
            if r_vals == phi_vals and r_vals == []:
                r_vals.append(range(len(r) + 1))
                phi_vals.append(range(len(phi) + 1))
            elif r_vals == []:
                for j in phi_vals:
                    r_vals.append(range(len(r) + 1))
            elif phi_vals == []:
                for j in r_vals:
                    phi_vals.append(range(len(phi) + 1))
            # ... Rest of the logic ...

        if boundary == 0:
            boundary = "min"
        # Calculate flux based on explicit grid values
        if surf_dim == "r":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(phi_vals)):
                    slice_data = (
                        f[boundary_val, phi_vals[j][0] : phi_vals[j][-1]]
                        if f.ndim == 2
                        else f[boundary_val, phi_vals[j][0] : phi_vals[j][-1]][
                            :, z_vals[j][0] : z_vals[j][-1]
                        ]
                    )
                    tmpl = np.trapz(
                        slice_data * r[boundary_val],
                        phi[phi_vals[j][0] : phi_vals[j][-1]],
                        axis=0,
                    )
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, z[z_vals[j][0] : z_vals[j][-1]])
                    elif len(z_vals) > 0:
                        tmpl *= z_vals[j][-1] - z_vals[j][0]
                    total_flux += sign * tmpl

        elif surf_dim == "phi":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(r_vals)):
                    slice_data = (
                        f[r_vals[j][0] : r_vals[j][-1], boundary_val]
                        if f.ndim == 2
                        else f[r_vals[j][0] : r_vals[j][-1], boundary_val][
                            :, z_vals[j][0] : z_vals[j][-1]
                        ]
                    )
                    tmpl = np.trapz(slice_data, r[r_vals[j][0] : r_vals[j][-1]], axis=0)
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, z[z_vals[j][0] : z_vals[j][-1]])
                    elif len(z_vals) > 0:
                        tmpl *= z_vals[j][-1] - z_vals[j][0]
                    total_flux += sign * tmpl

        elif surf_dim == "z":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(r_vals)):
                    slice_data = f[r_vals[j][0] : r_vals[j][-1], :, boundary_val][
                        :, phi_vals[j][0] : phi_vals[j][-1]
                    ]
                    tmpl = np.trapz(
                        slice_data * r[r_vals[j][0] : r_vals[j][-1]],
                        r[r_vals[j][0] : r_vals[j][-1]],
                        axis=0,
                    )
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, phi[phi_vals[j][0] : phi_vals[j][-1]])
                    total_flux += sign * tmpl

        result.append(total_flux)
    return result


def integrate_sph_sur(f, r, th, phi=None, rr=(), tr=(), pr=(), surface=()):
    if not surface:
        raise ValueError("Please specify a surface to integrate over.")

    if len(rr) > len(surface):
        raise ValueError("Length of rr must not exceed the length of surface.")
    if len(tr) > len(surface):
        raise ValueError("Length of tr must not exceed the length of surface.")
    if type(phi) != None and len(pr) > len(surface):
        raise ValueError("Length of pr must not exceed the length of surface.")

    result = []

    for i, surf in enumerate(surface):
        total_flux = 0
        sign = 1 if not surf.startswith("-") else -1
        surf_dim = surf.replace("-", "")

        boundaries = {"min": 0, "max": -1}

        # Similar to your Cartesian version but adapted for polar coordinates
        if surf_dim == "r":
            boundary = rr[i] if i < len(rr) else "both"
            th_vals = (
                get_indices_for_ranges(tr[i], th)
                if i < len(tr) and len(tr[i]) > 0
                else []
            )
            phi_vals = (
                get_indices_for_ranges(pr[i], phi)
                if type(phi) != None and i < len(pr) and len(pr[i]) > 0
                else []
            )
            if th_vals == phi_vals and th_vals == []:
                th_vals.append(range(len(th) + 1))
                if f.ndim == 3:
                    for j in th_vals:
                        phi_vals.append(range(len(phi) + 1))
                elif len(pr) > i and len(pr[i]) > 0:
                    for j in range(len(th_vals)):
                        phi_vals.append(pr[i][j])
            elif th_vals == []:
                for j in r_vals:
                    th_vals.append(range(len(th) + 1))
            elif phi_vals == []:
                if f.ndim == 3:
                    for j in th_vals:
                        phi_vals.append(range(len(phi) + 1))
                elif len(pr) > i and len(pr[i]) > 0:
                    for j in range(len(th_vals)):
                        phi_vals.append(pr[i][j])

            # ... Rest of the logic ...

        elif surf_dim == "th":
            boundary = tr[i] if i < len(tr) else "both"
            r_vals = (
                get_indices_for_ranges(rr[i], r)
                if i < len(rr) and len(rr[i]) > 0
                else []
            )
            phi_vals = (
                get_indices_for_ranges(pr[i], phi)
                if type(phi) != None and i < len(pr) and len(pr[i]) > 0
                else []
            )
            if r_vals == phi_vals and r_vals == []:
                r_vals.append(range(len(r) + 1))
                if f.ndim == 3:
                    for j in r_vals:
                        phi_vals.append(range(len(phi) + 1))
                elif len(pr) > i and len(pr[i]) > 0:
                    for j in range(len(r_vals)):
                        phi_vals.append(pr[i][j])
            elif r_vals == []:
                for j in phi_vals:
                    r_vals.append(range(len(r) + 1))
            elif phi_vals == []:
                if f.ndim == 3:
                    for j in r_vals:
                        phi_vals.append(range(len(phi) + 1))
                elif len(pr) > i and len(pr[i]) > 0:
                    for j in range(len(r_vals)):
                        phi_vals.append(pr[i][j])
            # ... Rest of the logic ...

        elif surf_dim == "phi":
            boundary = pr[i] if i < len(pr) else "both"
            r_vals = (
                get_indices_for_ranges(rr[i], r)
                if i < len(rr) and len(rr[i]) > 0
                else []
            )
            th_vals = (
                get_indices_for_ranges(tr[i], th)
                if i < len(tr) and len(tr[i]) > 0
                else []
            )
            if r_vals == th_vals and r_vals == []:
                r_vals.append(range(len(r) + 1))
                th_vals.append(range(len(th) + 1))
            elif r_vals == []:
                for j in th_vals:
                    r_vals.append(range(len(r) + 1))
            elif th_vals == []:
                for j in r_vals:
                    th_vals.append(range(len(th) + 1))
            # ... Rest of the logic ...

        if boundary == 0:
            boundary = "min"
        # Calculate flux based on explicit grid values
        if surf_dim == "r":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(th_vals)):
                    slice_data = (
                        f[boundary_val, th_vals[j][0] : th_vals[j][-1]]
                        if f.ndim == 2
                        else f[boundary_val, th_vals[j][0] : th_vals[j][-1]][
                            :, phi_vals[j][0] : phi_vals[j][-1]
                        ]
                    )
                    tmpl = np.trapz(
                        slice_data
                        * r[boundary_val] ** 2
                        * np.sin(th[th_vals[j][0] : th_vals[j][-1]]),
                        th[th_vals[j][0] : th_vals[j][-1]],
                        axis=0,
                    )
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, phi[phi_vals[j][0] : phi_vals[j][-1]])
                    elif len(phi_vals) > 0:
                        tmpl *= phi_vals[j][-1] - phi_vals[j][0]
                    else:
                        tmpl *= 2 * np.pi
                    total_flux += sign * tmpl

        elif surf_dim == "th":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(r_vals)):
                    slice_data = (
                        f[r_vals[j][0] : r_vals[j][-1], boundary_val]
                        if f.ndim == 2
                        else f[r_vals[j][0] : r_vals[j][-1], boundary_val][
                            :, phi_vals[j][0] : phi_vals[j][-1]
                        ]
                    )
                    tmpl = np.trapz(
                        slice_data
                        * np.sin(th[boundary_val])
                        * r[r_vals[j][0] : r_vals[j][-1]],
                        r[r_vals[j][0] : r_vals[j][-1]],
                        axis=0,
                    )
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, phi[phi_vals[j][0] : phi_vals[j][-1]])
                    elif len(phi_vals) > 0:
                        tmpl *= phi_vals[j][-1] - phi_vals[j][0]
                    else:
                        tmpl *= 2 * np.pi
                    total_flux += sign * tmpl

        elif surf_dim == "phi":
            for boundary_val in (
                [boundaries[boundary]] if boundary != "both" else [0, -1]
            ):
                for j in range(len(r_vals)):
                    slice_data = f[r_vals[j][0] : r_vals[j][-1], :, boundary_val][
                        :, th_vals[j][0] : th_vals[j][-1]
                    ]
                    tmpl = np.trapz(
                        slice_data * r[r_vals[j][0] : r_vals[j][-1]],
                        r[r_vals[j][0] : r_vals[j][-1]],
                        axis=0,
                    )
                    if f.ndim == 3:
                        tmpl = np.trapz(tmpl, th[th_vals[j][0] : th_vals[j][-1]])
                    total_flux += sign * tmpl

        result.append(total_flux)
    return result


if __name__ == "__main__":
    # print("Testing Model:",__file__)
    # from TestData import TestData
    # TestData=gradient(TestData,"rho")
    # print("Testing Result:", TestData.quantities["Gradient_rho_x1"], TestData.quantities["Gradient_rho_x2"]) #update
    # TestData=divergence(TestData,"rho")
    # print("Testing Result:", TestData.quantities["Divergence_rho"]) #update
    """
    from matplotlib import pyplot as plt
    plt.figure("imshow",facecolor="lightgray")
    plt.imshow(TestData.quantities["Divergence_rho"],cmap="RdBu",extent=[TestData.grid["x1"][0],TestData.grid["x1"][-1],TestData.grid["x2"][0],TestData.grid["x2"][-1]])
    plt.colorbar()
    plt.xticks(TestData.grid["x1"])
    plt.yticks(TestData.grid["x2"])
    plt.show()
    """
    """
    r=np.arange(0,10,0.01)
    print(integrate_sph_body(1,r))
    """
    # print(integrate_body(np.arange(10),np.arange(0,1,0.1)))
    # f=np.full((512,256,128),(1,1,1))
    # f=np.random.random((512,256))
    # r=np.arange(2,200,198/512)
    # th=np.arange(0,np.pi,np.pi/256)
    # print(integrate_sph_body(f[:2],r[:2],th))
    lenr = 5000
    lent = 1000
    # f=np.array([np.full((lent,),1) for i in range(lenr)])
    f = np.full((lenr, lent), 1)
    r = np.arange(0, 1, 1 / lenr)
    th = np.arange(0, np.pi / 2, np.pi / 2 / lent)
    # th=np.arange(np.pi/3,np.pi*2/3,np.pi/3/lent)
    # print(integrate_sph_sur(f,r,th,rr=("max",),tr=(((np.pi/3,2*np.pi/3),),),surface=("r",)))
    # print(integrate_sph_sur(f,r,th,rr=("max",),surface=("r",)))
    print(integrate_sph_sur(f, r, th, rr=(((0, 0.5),),), tr=("max",), surface=("th",)))
