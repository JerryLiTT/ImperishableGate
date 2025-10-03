from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" get "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'get', 'payload1': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/get")#这里要修改
async def get(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload1")
    
    #把name变成url
    if (db.link_exists(url) == False) and (url in db.get_all_names()):
        url = db.get_url_by_name(url)

    print("收到请求内容:", data)


    

    if db.link_exists(url) ==True :  # 如果非空
        
        return {
            "action": "get",
            "payload1": db.get_info_by_url(url)
        }

    else:
        return {
            "action": "get",
            "payload1": "找不到  " + str(url) + " ，换一个试试吧"
        }














