# ShockFinder

**ShockFinder** is an interactive scientic simulation data analysis software based on python and supports multi-process, multi-mode, I/O access and drawing.

Author Junxiang H. & C. B. Singh<br>
If you have any questions and suggestions<br>
Please contact: huangjunxiang@mail.ynu.edu.cn

You can download the **outdate** version at **"Releases"** in your right hand.

Latest Version: 7.0, date: 2023-07-11
\<Inner Version: XME 3.1, XUI 1.1\>

# Install

Please enter the following code on the command line to install **ShockFinder**

```shell
pip3 install ShockFinder
```

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

## GUI MODE

