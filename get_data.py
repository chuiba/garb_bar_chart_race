# 这个文件用于读取所有的装扮信息
# Warning: 由于获取前百信息的 API 已失效, 所以该功能已无法使用, 这里保留了当时测试时的数据 test.csv, 用于测试

garb_nums = [
1062,
1123,
1140,
1157,
1174,
1205,
1222,
1410,
1431,
1463,
1498,
1648,
1685,
1704,
1710,
1751,
1855,
1911,
1919,
1938,
1988,
2010,
2059,
2063,
2097,
2109,
2156,
2180,
2239,
2268,
2301,
2413,
2415,
2452,
2479,
2503,
2505,
2554,
2575,
2595,
2621,
2646,
2670,
2699,
2725,
2750,
2774,
2794,
2845,
2890,
2954,
2979,
2981,
3001,
3054,
3055,
3085,
3116,
3139,
3186,
3242,
3243,
3371,
3372,
3373,
3376,
3379,
3407,
3433,
3468,
3496,
3500,
3554,
3556,
3582,
3637,
3638,
3660,
3696,
3717,
3741,
3745,
3796,
3855,
3898,
3908,
3952,
4001,
4002,
4019,
4035,
4089,
4148,
4150,
4200,
4228,
4259,
4290,
4336,
4389,
4411,
4447,
4555,
4664,
4666,
4696,
4718,
4749,
4755,
4756,
4800,
4873,
4874,
4978,
5081,
5128,
5235,
5267,
5301,
5327,
5333,
5359,
5392,
#5424,
]

import sqlite3
import requests
import json

def create():
    conn = sqlite3.connect('./test.db')
    cursor = conn.cursor()
    sql = '''create table garb_top (
            garb_id int,
            user_id int,
            nickname text,
            number int)'''

    cursor.execute(sql)
    cursor.close()

def update(garb_id, user_id, nickname, number):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("INSERT INTO garb_top (garb_id,user_id,nickname,number) \
          VALUES (?, ?, ?, ?)", (garb_id, user_id, nickname, number))

    conn.commit()
    conn.close()

def get_users():
    ret = []
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    cursor = c.execute(
        "select user_id from garb_top group by user_id")
    for row in cursor:
        ret.append(row[0])

    conn.close()
    return ret

def get_nickname(_has_header):
    ret = []
    if True == _has_header:
        ret = ["Data"]

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    cursor = c.execute(
        "select nickname from garb_top group by user_id")
    for row in cursor:
        ret.append(row[0])

    conn.close()
    return ret


def get_count_by_garb_num(garb_id):
    _users = init_user_dict()
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    cursor = c.execute("select user_id, nickname, count(*) from (select * from garb_top where garb_id <= " + str(garb_id) + "  and number <= 10 ) group by user_id order by count(*) desc")
    for row in cursor:
        _users[row[0]] = row[2]

    conn.close()
    return _users

# 获取数据
def parse():
    for num in garb_nums:
        print(num)
        response = requests.get("https://api.bilibili.com/x/garb/rank/fan?item_id="+str(num))
        res = json.loads(response.text)['data']['rank']
        for info in res:
            print(info)
            update(num, info["mid"], info["nickname"], info["number"])

def init_user_dict():
    _user_count = {}
    for user in user_list:
        _user_count[user] = 0

    return _user_count


# 创建数据用
#create()
#parse()

import pandas as pd

# 统计用
# id: count, id: count
user_list = get_users()
user_dict = init_user_dict()

contents = []
for num in garb_nums:
    r = get_count_by_garb_num(num)
    line = [num]
    for k in r:
        line.append(r[k])

    contents.append(line)
    print(line)

df = pd.DataFrame(contents)
df.columns = get_nickname(True)
# df.to_csv(Csv_path, header=False)           # 不添加表头
#df.columns = ["Source", "Target", "Type", "Path"]  # 添加表头

df.to_csv("test.csv", header=True, index=False)

