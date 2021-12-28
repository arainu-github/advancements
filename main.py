from fastapi import FastAPI
import mysql.connector as mydb
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

# コネクションの作成
conn = mydb.connect(
    host="localhost",
    port="3306",
    user="root",
    password="test",
    database="metaverse"
)

# コネクションが切れた時に再接続してくれるよう設定
conn.ping(reconnect=True)
print(conn.is_connected())


@app.get("/get/{uuid}")
async def root(uuid: str):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM `advancement` WHERE `id` LIKE '{uuid}'")
    ret = cur.fetchall()
    cur.close()
    return ret


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


@app.get("/advancements")
async def advancement():
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
    return JSONResponse(ret)
