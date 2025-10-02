from fastapi import FastAPI
import uvicorn

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

要开发新action，只需新建一个 xxx.py，再 app.include_router(xxx_router) 即可
'''




# 导入功能模块
from ping import router as ping_router
from pingtest import router as pingtest_router

app = FastAPI()

# 注册路由
app.include_router(ping_router)
app.include_router(pingtest_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9323)
