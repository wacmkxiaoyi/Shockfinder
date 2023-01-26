# Shockfinder

Author Junxiang H. & C. B. Singh<br>
If you have any questions and suggestions<br>
Please contact: huangjunxiang@mail.ynu.edu.cn

## 0° Update infomation:

Shockfinder v3.5 (build 2022.06.30), upload: 2023.01.25<br>
Feature:<br>
|----PLUTO data reader<br>
|--------Update PyPLUTO (see http://plutocode.ph.unito.it/userguide.pdf) to support Python>3.7<br>
|--------Quadrant self-replication support (First or first&fourth quadrant support)<br>
|--------Computing complexity support<br>
|--------Multi-mode preset data processing<br>
|--------Advanced quantity support<br>
|--------2D (R)HD/(R)MHD SPH support<br>
|--------Original data output support<br>
|----Shock locator<br>
|--------Interval data selection support<br>
|--------Tolerance value calculation support<br>
|--------Tolerance transonic point auxiliary locating support<br>
|--------Logarithmic analysis support<br>
|--------Multi-data source support<br>
|--------Multi-shock detection<br>
|--------Newtonian star and black hole support<br>
|----Luminosity calculator<br>
|--------Bremsstrahlung calculation support<br>
|--------Luminosity spatial distribution support<br>
|----Multi-process optimizer (v2.3)<br>
|--------Data splitter<br>
|--------Data Integrator<br>
|--------Data accessor<br>
|------------DBMS controller<br>
|------------CSV file controller<br>
|--------Time control support<br>
|--------Luminosity calculation controller<br>
|--------Data analysis environment controller<br>
|--------Logical analysis of depth array<br>
|--------Post-processing dataset generator (v1.0)<br>
|--------Post update support<br>
|--------Multi-functional figuring support<br>
|----Drawing module based on matplotlib<br>
|--------Picture access support<br>
|--------Curve operation support<br>
|--------Curve crossing support<br>
|----Interactive interface<br>
|--------Command tool and pre-command processing<br>
|--------Data pre-analysis parameters error checking<br>
|--------Dataset interaction tools<br>
|--------Dynamic equilibrium calculator<br>
|--------PLUTO grid optimizer<br>
|--------Automatic input check<br>
|--------SQL Interactive<br>
|--------Multi-process data analysis interaction and drawing module interaction<br>
|----Other<br>
|--------Non-matrix divergence calculation<br>
|--------Non-matrix array operation<br>
|--------Text and array conversion support<br>
|--------Data source selector<br>
|--------Command abbreviation recovery<br>
|--------Log Exporter and printer<br>

# User Guide

## 1° Environment and installing

###  1.1° Enviorment
You must install python (>3.7) in your computer (or in high-performance server cluster), some basic modules need to be used. Please ensure that they have been installed:

**sys<br>
math<br>
numpy<br>
scipy<br>
datetime<br>
time<br>
csv<br>
pymysql<br>
matplotlib<br>
mpl_toolkits<br>
random<br>
os<br>
multiprocessing**

### 1.2° Installing
Download and decompress Shockfinder to your computer<br>
(the .tar.gz compression version will be put in the future update)

### 1.3° Enter Shockfinder environment and pre-command

#### 1.3.1° Shockfinder environment

```shell
python (Shockfinder directory)/shock_finder.py [pre-command [pre-command-value]]
```

For example in Linux, Shockfinder is installed in your home directory<br>
```shell
python ~/shock_finder.py
```
(This command can be added in your .bashrc with a alian command which is easier used for future.)

For Windows is similar to Linux, and a quick operation .bat file in the directory, you can run Shockfinder in one of two<br>
```shell
D:
cd Shockfinder
python shock_finder.py
```

#### 1.3.2° Pre-command:

**[r|-r|read]**: Read the command set from a file, which is used for non-interactive platforms or batch processing<br>
**[cv|-cv|curve]**: Load curve from csv file(s)<br>
**[o|-o|log]**: Log file, used for non-interactive processing<br>
**[l|-l|load]**: Load a post-analysis result from a csv file<br>
**[t|-t|test]**: Debug mode (default False), software will crash when is meeting an exception error in debug mode.

E.g., set log file: ~/test_log_file.log, set commands files: ~/command1 and ~/command2<br>
```shell
python ~/shock_finder.py o=~/test_log_file.log, r=(~/command1,~/command2)
```
load a result file ~/result.csv and a curve ~/curve.csv<br>
```shell
python ~/shock_finder.py l=~/result.csv cv=~/curve.csv
```
Debug mode, parameter 't' is abbreviation of 'True'<br>
```shell
python ~/shock_finder.py t=t
```

## 2° Command line

After entering the Shockfinder environment, all operations can be executed with commands in command line. By the way, you can do data analysis and other operations without touching any source code<br>

### 2.1° Command format

The command line provides some basic commands that can be executed directly in Shockfinder. Detailed descriptions of these commands will be released later. Some commands also require special parameters, but rest assured that most of these parameters are rewritable and contain error checking functions. You don't need to worry about incorrect input during use. However, **as a researcher, it is very necessary to put caution at first**:

Command format
```shell
Basic_command [parameter[-parameter_type][=[datasource[@datamodel]]]]
```

Basic_command:
**set**: set parameter before data analysis<br>
**update**: update parameter after analysis<br>
**curve**: curve operation<br>
**sql**: DBMS operation<br>
**save**: save current dataset<br>
**load**: load a dataset<br>
**delete**: delete a dataset or a curve from DBMS<br>
**read**: read command set<br>
**connect**: do analysis<br>
**close**: close DBMS<br>
**exit**: exit environment<br>
**show**: show parameters<br>
**reset**: reset parameters<br>
**draw**: draw a figure<br>
**help**: print help

Spaces are used to separate commands and parameters. However, it is reassuring that Shockfinder integrates redundant space clearing function (if you have spaces in unnecessary places or multiple spaces between commands and parameters, these spaces will be cleared), so there **is no need to worry about the impact of redundant spaces**.

### 2.2° Annotation

Shockfinder allows users to enter some commands that do not need to be executed, including wrong or illegal commands, empty commands (which can be composed of pure spaces) and commented commands.

Shockfinder supports line comments starting with # and//<br>
```shell
#Command....
//Command....
```

### 2.3° Command abbreviation

In order to avoid the use of lengthy names as command names in Shockfinder, "general_parameters. py" is responsible for defining the aliases (or abbreviations) of commands. Users can modify them according to their personal preferences. The data dictionary "g_command_trans" describes the abbreviations of basic commands.

The relevant command abbreviations can be viewed through the help command. For details, see 3 °.
```shell
help
```

## 3° Help
