# File type: <Function> set
# By Junxiang H., 2023/07/4
# wacmk.com/cn Tech. Supp.
import math

def str_clean(strc):
    if strc[-1] == "\n":
        strc = strc[:-1]
    result = ""
    while len(strc) > 1 and strc[0] == " ":
        strc = strc[1:]
    for i in ("#", "//"):
        strc = strc.split(i)[0]
    stat = False
    for i in strc:
        if i == " ":
            if not stat:
                stat = True
                result += i
        else:
            stat = False
            result += i
    return result if result != "" else None


def str_to_float(strc):
    try:
        return float(strc)
    except:
        if strc[-2:].lower() == "pi":
            try:
                return float(strc[:-2]) * math.pi
            except:
                return strc
        return strc


def retype_string(string):
    if "." in string or "e" in string or "pi" == string[-2:]:
        string = str_to_float(string)
        if type(string) == str:
            if string == "None":
                string = None
            elif string == "True":
                string = True
            elif string == "False":
                string = False
    else:
        try:
            string = int(string)
        except:
            pass
    return (
        string
        if type(string) != str or len(string.split(",")) == 1
        else [retype_string(i) for i in string.split(",")]
    )


def remove_empty(array):
    return [i for i in array if i != ""]


def get_config(config_file):
    file = open(config_file, "r")
    commands = {}
    for line in file.readlines():
        result = str_clean(line)
        if result:
            tt = remove_empty(result.split(";"))
            if len(tt) == 1 and "=" in tt[0]:
                ts = tt[0].split("=")
                if len(ts) == 2:
                    key, value = ts
                    commands[key] = retype_string(value)
                else:
                    print("Unknow configuration:", tt[0])
            else:
                key = tt[0]
                subcommands = {}
                for subcmd in tt[1:]:
                    ss = subcmd.split("=")
                    if len(ss) != 2:
                        print("Unknow configuration:", subcmd)
                        continue
                    subkey, value = ss
                    subcommands[subkey] = retype_string(value)
                commands[key] = subcommands
    file.close()
    return commands
