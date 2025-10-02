from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" addtag "ciallo" "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'addtag', 'payload1': 'ciallo', 'payload2': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/addtag")#这里要修改
async def addtag(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload2")
    tag = data.get("payload1")

    print("收到请求内容:", data)
    print(db.get_tags_by_url(url))

    if db.link_exists(url) == True:
        if tag in db.get_tags_by_url(url):
            return {
                "action": "addtag",
                "payload1": "tag " + str(tag) + " of " + str(url) + " already exists"
            }
        else:
            db.add_tag_to_url(url, tag)
            print("successfully added tag " + tag + " to " + url)
            return {
                "action": "addtag",
                "payload1": "successfully added tag " + tag + " to " + url
            }

    else:
        return {
            "action": "addtag",
            "payload1": "添加tag失败，链接不存在:  " + str(url) + " ，你可以试着用add命令创建一个"
        }










