from fastapi import FastAPI
import uvicorn
import sqlite3

'''
如果你使用
data = await request.json()
print(data)

则输出如下
{'server': '127.0.0.1:9323', 
'action': 'pingtest', 
'payload1': 'konpaku youmu', 
'payload2': '1', 
'payload3': '1', 
'payload4': '1', 
'payload5': '1', 
'payload6': '12', 
'payload7': '2', 
'payload8': '2', 
'payload9': '2'}

要开发新action，只需新建一个 xxx.py，
再from pingtest import router as pingtest_router；
 app.include_router(xxx_router) 即可
'''




# 导入功能模块
from ping import router as ping_router
from pingtest import router as pingtest_router

from add import router as add_router
from remove import router as remove_router
from list1 import router as list_router

from addtag import router as addtag_router
from removetag import router as removetag_router

from addnote import router as addnote_router
from removenote import router as removenote_router
from editnote import router as editnote_router



import db

app = FastAPI()

# 初始化数据库
conn = sqlite3.connect("links.db", check_same_thread=False)  # FastAPI 要加 check_same_thread=False
db.init_db(conn)

# 注册路由
app.include_router(ping_router)
app.include_router(pingtest_router)

app.include_router(add_router)
app.include_router(remove_router)
app.include_router(list_router)

app.include_router(addtag_router)
app.include_router(removetag_router)

app.include_router(addnote_router)
app.include_router(removenote_router)
app.include_router(editnote_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9323)
