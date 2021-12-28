import os

from flask import Flask, jsonify
import mysql.connector as mydb


app = Flask(__name__)

# コネクションの作成
conn = mydb.connect(
    host=os.environ["host"],
    port="3306",
    user=os.environ["user"],
    password=os.environ["password"],
    database="metaverse"
)

# コネクションが切れた時に再接続してくれるよう設定
conn.ping(reconnect=True)
print(conn.is_connected())


def append(avt, advancements, ended, r, overwrite=False):
    ret = {}
    if not avt[0] in ended:
        ended.append(avt[0])
        tmp = []
        for i in avt[3]:
            if i != "":
                try:
                    r_f = append(advancements[list(map(lambda x: x[0], advancements)).index(i)], advancements, ended, r,
                                 True)
                    if r_f[0] != {}:
                        tmp.append(r_f[0])
                    ended = r_f[1]
                except ValueError:
                    pass
        ret = {"id": avt[0], "name": avt[1], "icon": avt[4], "type": avt[5], "children": tmp}
    elif overwrite:
        index = list(map(lambda x: x["id"], r)).index(avt[0])
        ret = r[index]
        del r[index]
    return ret, ended, r


@app.route('/')
def get_advancements(request):
    cur = conn.cursor()
    cur.execute("SELECT * FROM `advancement`")
    advancements = cur.fetchall()
    cur.close()
    ret = []
    ended = []
    advancements = list(map(lambda n: (n[0], n[1], n[2], n[3].split(","), n[4], n[5]), advancements))
    for i in advancements:
        r = append(i, advancements, ended, ret)
        ret = r[2]
        if r[0] != {}:
            ret.append(r[0])
        ended = r[1]
    return jsonify(ret)


if __name__ == '__main__':
    app.run()
