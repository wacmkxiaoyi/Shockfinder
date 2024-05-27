# File type: <Function> set
# By Junxiang H., 2023/07/03
# wacmk.com/cn Tech. Supp.


import numpy as np
import math
from scipy.interpolate import griddata


def get_par(args, name, default=None):
    try:
        return args[name]
    except:
        return default


def set_None(string):
    return None if string == "None" else string


def CharUndecode(string):
    return string.replace("$", r"$")


def find_index(x, value):
    result = np.where(x < value)[0]
    if len(result) == 0:
        return 0
    elif len(x) == len(result):
        return None
    if value - x[result[-1]] > x[result[-1] + 1] - value:
        return result[-1] + 1
    return result[-1]


def clean_kwargs(dic, fun, exceptions=[]):
    dd = []
    for i in dic.keys():
        if i not in fun.__code__.co_varnames and i not in exceptions:
            dd.append(i)
    for i in dd:
        del dic[i]
    return dic


linekeys = [
    "linewidth",
    "color",
    "linestyle",
    "marker",
    "markersize",
    "solid_capstyle",
    "dash_capstyle",
    "dash_joinstyle",
    "solid_joinstyle",
    "markevery",
    "label",
]


def clean_keys(dic, valkeys=[]):
    dd = []
    for i in dic.keys():
        if i not in valkeys:
            dd.append(i)
    for i in dd:
        del dic[i]
    return dic


"""
def get_2drp_value(r,phi,x,y,v,default):
	tr=(x**2+y**2)**0.5
	tp=math.atan(y/x)
	if x<0:
		tp+=np.pi
	elif y<0:
		tp+=2*np.pi
	rind=find_index(r,tr)
	if rind==None:
		return default
	pind=find_index(phi,tp)
	if pind==None:
		return default
	return v[rind][pind]

def rop_to_xoy(r,phi,v=None):
	if type(v)==type(None):
		return (r*np.cos(phi),r*np.sin(phi))
	x=y=np.union1d(-r,r)
	newv=np.full((len(x),len(y)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([get_2drp_value(r,phi,x[i],y[j],v,newv[i][j]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,y,newv)


def get_2drt_value(r,theta,x,z,v,default):
	tr=(x**2+z**2)**0.5
	tt=math.acos(z/tr)
	rind=find_index(r,tr)
	if rind==None:
		return default
	tind=find_index(theta,tt)
	if tind==None:
		return default
	return v[rind][tind]
def rot_to_xoz(r,theta,v=None):
	if type(v)==type(None):
		return (r*np.sin(theta),r*np.cos(theta))
	x=z=np.union1d(-r,r)
	newv=np.full((len(x),len(z)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([get_2drt_value(r,theta,x[i],z[j],v,newv[i][j]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,z,newv)

def get_3drzp_value(r,phi,x,y,k,v,default):
	tr=(x**2+y**2)**0.5
	tp=math.atan(y/x)
	if x<0:
		tp+=np.pi
	elif y<0:
		tp+=2*np.pi
	rind=find_index(r,tr)
	if rind==None:
		return default
	pind=find_index(phi,tp)
	if pind==None:
		return default
	return v[rind][pind][k]

def rzp_to_xyz(r,z,phi,v=None):
	if type(v)==type(None):
		return (r*np.cos(phi),r*np.sin(phi),z)
	x=y=np.union1d(-r,r)
	newv=np.full((len(x),len(y),len(z)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([np.array([get_3drzp_value(r,phi,x[i],y[j],k,v,newv[i][j][k]) for k in range(len(newv[i][j]))]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,y,z,newv)

def get_3drtp_value(r,theta,phi,x,y,z,v,default):
	tr=(x**2+y**2+z**2)**0.5
	tt=math.acos(z/tr)
	tp=math.atan(y/x)
	if x<0:
		tp+=np.pi
	elif y<0:
		tp+=2*np.pi
	rind=find_index(r,tr)
	if rind==None:
		return default
	tind=find_index(theta,tt)
	if tind==None:
		return default
	pind=find_index(phi,tp)
	if pind==None:
		return default
	
	return v[rind][tind][pind]
	
def rtp_to_xyz(r,theta,phi,v=None):
	if type(v)==type(None):
		return (r*np.sin(theta)*np.cos(phi),r*np.sin(theta)*np.sin(phi),r*np.cos(theta))
	x=y=z=np.union1d(-r,r)
	newv=np.full((len(x),len(y),len(z)),0.5*np.min(v) if np.min(v)>0 else 1.5*np.min(v))
	newv=np.array([np.array([np.array([get_3drtp_value(r,theta,phi,x[i],y[j],z[k],v,newv[i][j][k]) for k in range(len(newv[i][j]))]) for j in range(len(newv[i]))]) for i in range(len(newv))])
	return (x,y,z,newv)
"""


def pol_to_xoy(r, phi, v=None):
    # Convert the r and phi grids to 1D
    r = np.asarray(r).flatten()
    phi = np.asarray(phi).flatten()

    # Create a meshgrid for r and phi
    R, Phi = np.meshgrid(r, phi, indexing="ij")

    # Convert polar to Cartesian coordinates
    X = R * np.cos(Phi)
    Y = R * np.sin(Phi)

    # Flatten the Cartesian coordinates for griddata
    points = np.c_[X.flatten(), Y.flatten()]

    # Create a new grid in Cartesian space
    grid_x = np.linspace(-np.max(r), np.max(r), len(r))
    grid_y = np.linspace(-np.max(r), np.max(r), len(r))

    grid_X, grid_Y = np.meshgrid(grid_x, grid_y, indexing="ij")

    if v is not None:
        values = v.flatten()
        grid_V = griddata(
            points,
            values,
            (grid_X, grid_Y),
            method="linear",
            fill_value=0.1 * np.min(v),
        )
        return grid_x, grid_y, grid_V

    return grid_x, grid_y


def rot_to_xoz(r, theta, v=None):
    # Convert the r and phi grids to 1D
    r = np.asarray(r).flatten()
    theta = np.asarray(theta).flatten()

    # Create a meshgrid for r and phi
    R, Th = np.meshgrid(r, theta, indexing="ij")

    # Convert polar to Cartesian coordinates
    X = R * np.sin(theta)
    Z = R * np.cos(theta)

    # Flatten the Cartesian coordinates for griddata
    points = np.c_[X.flatten(), Z.flatten()]

    # Create a new grid in Cartesian space
    grid_x = np.linspace(-np.max(r), np.max(r), len(r))
    grid_z = np.linspace(-np.max(r), np.max(r), len(r))

    grid_X, grid_Z = np.meshgrid(grid_x, grid_z, indexing="ij")

    if v is not None:
        values = v.flatten()
        grid_V = griddata(
            points,
            values,
            (grid_X, grid_Z),
            method="linear",
            fill_value=0.1 * np.min(v),
        )
        return grid_x, grid_z, grid_V

    return grid_x, grid_z


def rzp_to_xyz(r, z, phi, v=None):
    # Convert the r, z, and phi grids to 1D
    r = np.asarray(r).flatten()
    z = np.asarray(z).flatten()
    phi = np.asarray(phi).flatten()

    # Create a meshgrid for r, z, and phi
    R, Z, Phi = np.meshgrid(r, z, phi, indexing="ij")

    # Convert cylindrical to Cartesian coordinates
    X = R * np.cos(Phi)
    Y = R * np.sin(Phi)

    # Flatten the Cartesian coordinates for griddata
    points = np.c_[X.flatten(), Y.flatten(), Z.flatten()]

    # Create a new grid in Cartesian space
    grid_x = np.linspace(-np.max(r), np.max(r), len(r))
    grid_y = np.linspace(-np.max(r), np.max(r), len(r))
    grid_z = np.linspace(-np.max(z), np.max(z), len(z))

    grid_X, grid_Y, grid_Z = np.meshgrid(grid_x, grid_y, grid_z, indexing="ij")

    if v is not None:
        values = v.flatten()
        grid_V = griddata(
            points,
            values,
            (grid_X, grid_Y, grid_Z),
            method="linear",
            fill_value=0.1 * np.min(v),
        )
        return grid_x, grid_y, grid_z, grid_V

    return grid_x, grid_y, grid_z


def rtp_to_xyz(r, theta, phi, v=None):
    # Convert the r, theta, phi grids to 1D
    r = np.asarray(r).flatten()
    theta = np.asarray(theta).flatten()
    phi = np.asarray(phi).flatten()

    # Create a meshgrid for r, theta, phi
    R, Theta, Phi = np.meshgrid(r, theta, phi, indexing="ij")

    # Convert spherical to Cartesian coordinates
    X = R * np.sin(Theta) * np.cos(Phi)
    Y = R * np.sin(Theta) * np.sin(Phi)
    Z = R * np.cos(Theta)

    # Flatten the Cartesian coordinates for griddata
    points = np.c_[X.flatten(), Y.flatten(), Z.flatten()]

    # Create a new grid in Cartesian space
    grid_r = np.linspace(0, np.max(r), len(r))
    grid_theta = np.linspace(0, np.pi, len(theta))
    grid_phi = np.linspace(0, 2 * np.pi, len(phi))

    grid_x = np.linspace(-np.max(r), np.max(r), len(r))
    grid_y = np.linspace(-np.max(r), np.max(r), len(r))
    grid_z = np.linspace(-np.max(r), np.max(r), len(r))

    grid_X, grid_Y, grid_Z = np.meshgrid(grid_x, grid_y, grid_z, indexing="ij")

    if v is not None:
        values = v.flatten()
        grid_V = griddata(
            points,
            values,
            (grid_X, grid_Y, grid_Z),
            method="linear",
            fill_value=0.1 * np.min(v),
        )
        return grid_X, grid_Y, grid_Z, grid_V

    return grid_x, grid_x, grid_x


def _3D_to_2D(x, y, z, v, cx=None, cy=None, cz=None):
    def closest_index(arr, value):
        """Get the index of the closest value in arr to the specified value."""
        return np.argmin(np.abs(arr - value))

    results = []

    if cx is not None:
        for c in cx:
            ix = closest_index(x, c)
            results.append((y, z, v[ix, :, :]))

    if cy is not None:
        for c in cy:
            iy = closest_index(y, c)
            results.append((x, z, v[:, iy, :]))

    if cz is not None:
        for c in cz:
            iz = closest_index(z, c)
            results.append((x, y, v[:, :, iz]))

    return results[0]


def info():
    print("Module:", __file__)


if __name__ == "__main__":
    info()
