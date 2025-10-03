from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" addname "B站" "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'addname', 'payload1': 'B站', 'payload2': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/addname")#这里要修改
async def addname(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload2")
    name = data.get("payload1")

    print("收到请求内容:", data)
    print(db.get_names_by_url(url))

    if db.link_exists(url) == True:
        if name in db.get_all_names():
            return {
                "action": "addname",
                "payload1": "failed to add name " + name + " to " + url + " , because name " + name +  " already exists"
            }
        else:
            db.add_name_to_url(url, name)
            print("successfully added name " + name + " to " + url)
            return {
                "action": "addname",
                "payload1": "successfully added name " + name + " to " + url
            }

    else:
        return {
            "action": "addname",
            "payload1": "添加name失败，链接不存在:  " + str(url) + " ，你可以试着用add命令创建一个"
        }










