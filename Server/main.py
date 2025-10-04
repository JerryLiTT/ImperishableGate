from fastapi import FastAPI
import uvicorn
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


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
from get import router as get_router

from addtag import router as addtag_router
from removetag import router as removetag_router
from searchtag import router as searchtag_router

from addnote import router as addnote_router
from removenote import router as removenote_router
from editnote import router as editnote_router

from addname import router as addname_router
from removename import router as removename_router


from http_utils import get_status_code
from send_email import send_email


import db
import metagrab

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
app.include_router(get_router)

app.include_router(addtag_router)
app.include_router(removetag_router)
app.include_router(searchtag_router)

app.include_router(addnote_router)
app.include_router(removenote_router)
app.include_router(editnote_router)

app.include_router(addname_router)
app.include_router(removename_router)




def meta_refresh():
    # 用于每24小时更新一次所有网址的meta信息
    urls=[item[1] for item in db.get_all_links()]
    for url_in_urls in urls:
        metadata = metagrab.get_page_metadata(url_in_urls)
        db.update_metainfo_by_url(url_in_urls, metadata)
    print('all metadata refreshed')




def test_website():
    starred_urls = db.get_urls_by_tag("starred")
    
    bad_urls = []

    for starred_url in starred_urls:
        code, err = get_status_code(starred_url)
        if err:
            print(f"[失败] {starred_url} -> {err}")
        else:
            print(f"[成功] {starred_url} -> 状态码 {code}")
            if code != 200:
            #if 1==1:
                bad_urls.append(f"[有情况] {starred_url} -> 状态码 {code}")
    if bad_urls != []:
        send_email('f9126042@gmail.com', 'jccy anov yygy gcif', 'jerrylitt2022@outlook.com', "Website Status", str(bad_urls))
    else:
        print('everything is ok')

    #print(f"[{datetime.now()}] 每分钟执行一次的任务！")


scheduler = BackgroundScheduler()
# 每24小时执行一次任务，从程序启动时开始计算
scheduler.add_job(meta_refresh, 'interval', hours=24)
scheduler.add_job(test_website, 'interval', minutes=240, next_run_time=datetime.now())

scheduler.start()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9323)
