from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" removetag "ciallo" "bilibili.com"                                                     #这里要修改                          
{'server': '100.92.189.86:9323', 'action': 'removetag', 'payload1': 'ciallo', 'payload2': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/removetag")#这里要修改
async def removetag(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload2")
    tag = data.get("payload1")

    print("收到请求内容:", data)
    print(db.get_tags_by_url(url))

    if db.link_exists(url) == True:
        if tag in db.get_tags_by_url(url):
            db.remove_tag_from_url(url, tag)
            print("successfully removed tag " + tag + " from " + url)
            return {
                "action": "removetag",
                "payload1": "successfully removed tag " + tag + " from " + url
            }
            
        else:
            return {
                "action": "removetag",
                "payload1": "tag " + str(tag) + " doesn't exist or belong to " + str(url)
            }

    else:
        return {
            "action": "removetag",
            "payload1": "删除tag失败，链接不存在:  " + str(url)
        }










