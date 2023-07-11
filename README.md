# ShockFinder

**ShockFinder** is an interactive scientic simulation data analysis software based on python and supports multi-process, multi-mode, I/O access and drawing.

Author Junxiang H. & C. B. Singh<br>
If you have any questions and suggestions<br>
Please contact: huangjunxiang@mail.ynu.edu.cn

You can download the **outdate** version at **"Releases"** in your right hand.

Latest Version: 7.0, date: 2023-07-11
\<Inner Version: XME 3.1, XUI 1.1\>

# Install

Please follow one of the ways to install **ShockFinder**


```shell
pip3 install ShockFinder
```

And then download and release the zip (XUI libraries for Shockfinder) into the **folder** you would like to use ShockFinder (e.g., same folder with the ***shockfinder.py*** shown in **Useage**)

Link see https://github.com/wacmkxiaoyi/Shockfinder/releases

# Useage

Enter the following code and save it into a file (like ***shockfind.py***)

```python
import ShockFinder
from ShockFinder.Update import Update_all
import sys
def drop_bk(strc):
	if strc!="" and (strc[0]=="'" and strc[-1]=="'" or strc[0]=='"' and strc[-1]=='"'):
		strc=strc[1:-1]
	return strc
if __name__=="__main__":#windows support
	gui=True
	for i in sys.argv[1:]:
		if i.split("=")[0] in ("f","-f","file"):
			ShockFinder.ShockFinder(drop_bk(i.split("=")[1]))
			gui=False
		elif i.split("=")[0] in ("u","-u","update"):
			Update_all()
			gui=False
	if gui:
		ShockFinder.ShockFinder()
```

# GUI MODE

GUI Mode is used to **generate analysis configuration file** and **visualize analysis results**!

Entry GUI Mode:

```shell
python shockfind.py
```

The GUI engine for the ShockFinder is **XUI** (see https://github.com/wacmkxiaoyi/Xenon-UI). (This libraries is only used to **GUI mode**, the **PAM Mode** does not require)

Four pages can be used: **Analyze**, **Figure**, **Help** and **Exit**

Page **Exit** used to interrupt multithreading monitoring and exit the Shockfinder, and **Help** shown some basic information of ShockFinder (e.g., version, author)

## Page Analyze

Page **Analyze** has Three Menus, **Save Configuration**, **Global Settings** and **Analysis**

### Global Settings

Menu **Global Settings** has three sub-menus:

1. **Multi-process** : the configuration about multiprocessing analysis, default multiprocessing engine is **XME** (see https://github.com/wacmkxiaoyi/Xenon-Multiprocessing-Engine, some advanced optiones can follow this link).

2. **Database Storage**: the configuration about storing the after-analyzing data, default engine is **HDF5**, default project name (saving target file name) is **current timestampe** and Drop Buffer is the buffer cleared during the analysis process (default and recommend **True**)

3. **Simulation Data Loader**: in this submenu, you have to define which type of simulation data you used.

### Analysis

Menu **Analysis** has two sub-menus:

1. **Parameters**: in here you can define the global variable during the analyzing

2. **Quantities**: in here you can define which analysis approch will be used during the analyzing

### Save Configurations:

1. Button **Test**: to test cn the analysis process proceed normally

2. Button **Save**: save the analysis configuration file

## Page Figure

Page **Figure** has Two Menus, **Database**, and **Figure**

### Database

Menu **Database** has two sub-menus:

1. **Load**: before you figure the picture you like, you should load the **after-analyzing data** firstly. In this menu, data reading, browsing, and other functions can be performed

2. **Global Settings**: the configuration of loader of **after-analyzing data**

### Figure

Menu **Figure** has three sub-menus: **Set unit**, **2d** and **3d** (easy to understand without additional explanation)

# Parallel analysis mode (PAM)

After producing the analysis configration file (e.g., config1.ini, config2.ini), you can start to analyze:

```shell
python shockfinder.py -f=config1.ini -f=config2.ini ...
```

# How to add a new type of simulation or an analysis approach:

There are two model file in ShockFinder's source code: **

1. **LoaderModel.py** in **ShockFinder\\Addon\\Loader**
2. **AnalysisToolModel.py** in **ShockFinder\Addon\AnalysisTool**

Firstly, you have to copy it in the same folder and modified the contend, and then type 

```shell
python shockfinder.py update
```

in the DOC window. Then the new simulation Data type or analysis approach will be shown in **GUI** mode
