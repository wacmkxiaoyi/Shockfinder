# coding=utf-8
# File type: <Function> set
# By Junxiang H., 2023/07/5
# wacmk.com/cn Tech. Supp.
try:
    import ShockFinder.Addon.Time as Time
except:
    import datetime

    class Time:
        def now():
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


import numpy as np, pandas as pd, pymysql

Filetype = "sql"


def get_save_sql(data, index, tablename, *quantities_name):
    dt = {}
    sql = (
        "insert into `"
        + tablename
        + "` (`index`) values ("
        + str(index)
        + ");\nupdate `"
        + tablename
        + "` set "
    )
    for i in quantities_name:
        if i in data.quantities.keys():
            sql += "`" + i + '`="' + Formatdata(data.quantities[i]) + '",'
    sql = sql[:-1] + " where `index`=" + str(index) + ";\n"
    return sql


def PreSave(filename, *quantities_name, **databaseinfo):
    filename = filename.rsplit(".", 1)[0]
    sql = (
        "#■■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■\n#■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■■\n#■■■■■■■■■□△■■■■■■■■■■■■■■■■■■■■■\n#■■■■■■■■□■△■◁■■■■■■■ShockFinder v7.0■■■■\n#■■■■■■■□■■△■■■■■■■■■■■■■■■■■■■■■\n#■■■■◁■□■■■■■■■■■■Junxiang H. &  C. B. Singh■■\n#■■■■■■■□■■▽■■■■■■■■■■■■■■■■■■■■■\n#■■■■■■■■□■▽■◁■■■■■wacmk.com/cn Tech. Supp.■■\n#■■■■■■■■■□▽■■■■■■■■■■■■■■■■■■■■■\n#■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■■\n#■■■■■■■■■■■□■■■■■■■■■■■■■■■■■■■■\n\n#Project Name: "
        + filename
        + "\n#Build at: "
        + Time.now()
        + "\n"
    )
    sql += (
        'insert into `mapping_database`(`name`) values ("'
        + filename
        + '");\nupdate `mapping_database` set `parameters`="'
    )
    for i in databaseinfo.keys():
        sql += (
            i
            + "="
            + str(databaseinfo[i])
            .replace("[", "")
            .replace("]", "")
            .replace("(", "")
            .replace(")", "")
            .replace("\\", "\\\\")
            + ";"
        )
    sql = sql[:-1] + '" where `name`="' + filename + '"\n'
    sql += (
        "create table if not exists `"
        + filename
        + "`(`index` int NOT NULL, PRIMARY KEY (`index`));\n"
    )
    for i in quantities_name:
        sql += "alter table `" + filename + "` add column `" + i + "` longtext NULL;\n"
    file = open(filename, "w")
    file.writelines(sql)
    file.close()
    return sql  # debug


def Save(filename, data, index, *quantities_name):
    filename = filename.rsplit(".", 1)[0]
    sql = get_save_sql(data, index, filename, *quantities_name)
    file = open(filename, "a")
    file.writelines(sql)
    file.close()


def Load(filename, mysqlobj):
    pass


def Formatdata(dt):  # max 2d
    if dt.ndim == 1:  # grid or 1d data:
        strc = (
            str(tuple(dt.tolist())).replace(" ", "").replace('"', "").replace("'", "")
        )
    elif dt.ndim == 2:  # 2d data:
        strc = (
            str(tuple([tuple(i.tolist()) for i in dt]))
            .replace(" ", "")
            .replace('"', "")
            .replace("'", "")
        )
    elif dt.ndim == 3:  # 3d data:
        strc = (
            str(tuple([tuple([tuple(j.tolist()) for j in i]) for i in dt]))
            .replace(" ", "")
            .replace('"', "")
            .replace("'", "")
        )
    return strc


def Decodedata(strc):
    dt = str_to_array(strc)
    if dt.ndim == 1:  # 1d
        dt = np.array([float(i) for i in dt])
    elif dt.ndim == 2:
        dt = np.array([np.array([float(j) for j in i]) for i in dt])
    else:
        dt = np.array(
            [np.array([np.array([float(k) for k in j]) for j in i]) for i in dt]
        )
    return dt


def char_num(strc, char):
    num = 0
    for i in strc:
        if i == char:
            num += 1
    return num


def str_to_array(strc):
    if type(strc) is not str:
        return strc
    strc = strc.replace(" ", "")
    if (
        strc == ""
        or not char_num(strc, "]") == char_num(strc, "[")
        or not char_num(strc, ")") == char_num(strc, "(")
        or not (
            strc[0] == "[" and strc[-1] == "]" or strc[0] == "(" and strc[-1] == ")"
        )
    ):
        return strc
    pt = 0
    ptb = []
    pte = []
    ptstr = ""
    anb = ""
    ane = ""
    tmpresult = []
    result = []
    tmp = strc.split(",")
    for i in tmp:
        if pt <= 1 and (
            i[0] == "["
            and i[-1] == "]"
            and char_num(i, "]") == char_num(i, "[")
            or i[0] == "("
            and i[-1] == ")"
            and char_num(i, "(") == char_num(i, ")")
        ):
            sttp = str_to_array(i[1:-1])
            if len(tmp) == 1:
                anb = i[0]
                ane = i[-1]
                if sttp != "":
                    result.append(sttp)
            else:
                if i[0] == "[":
                    if sttp != "":
                        result.append([str_to_array(i[1:-1])])
                    else:
                        result.append([])
                else:
                    if sttp != "":
                        result.append((str_to_array(i[1:-1]),))
                    else:
                        result.append(())
        else:
            for j in i:
                if j == "[":
                    ptb.append(j)
                    if anb == "":
                        anb = j
                        ane = "]"
                    pte.append("]")
                    pt += 1
                    if pt > 1:
                        ptstr += j
                elif j == "(":
                    ptb.append(j)
                    if anb == "":
                        anb = j
                        ane = ")"
                    pte.append(")")
                    pt += 1
                    if pt > 1:
                        ptstr += j
                elif j == pte[pt - 1]:
                    del pte[pt - 1]
                    del ptb[pt - 1]
                    pt -= 1
                    if pt > 0:
                        ptstr += j
                else:
                    ptstr += j
            if pt > 1:
                ptstr += ","
            elif pt <= 1 and ptstr != "":
                result.append(str_to_array(ptstr))
                ptstr = ""
    if anb == "(" and ane == ")":
        return np.array(result)
    return result


class MySQL:
    host = "127.0.0.1"
    user = "pluto_data_stream_1"
    password = "xx1234"
    port = 3306
    database = "data_stream_1"
    charset = "utf8"
    conn = 0
    cursor = 0
    is_connect = False

    def connect(self):
        if not self.is_connect:
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.password,
                    port=self.port,
                    db=self.database,
                    charset=self.charset,
                )
                self.cursor = self.conn.cursor()
                self.build_mapping_tables()
                self.is_connect = True
                return True
            except Exception as err:
                print(err)
                self.is_connect = False
                return False
        return True

    def reconnect(self):
        self.close()
        return self.connect()

    def close(self):
        if self.is_connect:
            self.conn.close()
            self.is_connect = False

    def execute(self, sql):
        try:
            result = self.cursor.execute(sql.replace("\\", "\\\\"))
            if int(result) > 0:
                return True
            return False
        except Exception as err:
            print(err)
            return err

    def get_result(self, sql):
        status = self.execute(sql)
        if str(status) == "True":
            return self.cursor.fetchall()
        elif str(status) == "False":
            return None
        return None

    def build_mapping_tables(self):
        sql = "create table if not exists `mapping_database`(  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, `parameters` longtext NULL, `time` datetime NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`name`) USING BTREE) engine=innodb CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;\n"
        sql += "create table if not exists `mapping_figure`(  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL, `time` datetime NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`name`) USING BTREE) engine=innodb CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;\n"
        if exce:
            self.execute(sql)
        return sql

    def savefigure(self, fig, figinfo):
        # use pd
        pass

    def load(self, tablename):
        pass


if __name__ == "__main__":
    """
    import time
    dt=np.random.random((512,280))
    print(PreSave("testtb","test1","test2","test3","test4"))
    t1=time.time()
    dst=Formatdata(dt)
    t2=time.time()
    print(dt,"\nFormattime=",t2-t1)
    t1=time.time()
    dt=Decodedata(dst)
    t2=time.time()
    print(dt,"\nDecodeTime=",t2-t1)
    """
    pass
