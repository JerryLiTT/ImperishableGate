from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" removenote "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'removenote', 'payload1': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/removenote")#这里要修改
async def removenote(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload1")
    

    print("收到请求内容:", data)
    print(db.get_note_by_url(url))

    if db.link_exists(url) == True:
        if db.has_note(url) == False:
            return {
                "action": "removenote",
                "payload1": "failed to remove note from " + url + " , because the note of " + str(url) + " doesn't exist"
            }
        else:
            note = db.get_note_by_url(url)
            result_of_delete_note_of_url = db.delete_note_of_url(url)
            if result_of_delete_note_of_url == True:
            
                print("successfully removeed note " + note + " from " + url)
                return {
                    "action": "removenote",
                    "payload1": "successfully removed note " + note + " from " + url
                }
            else:
                print("发生未知错误")

    else:
        return {
            "action": "removenote",
            "payload1": "删除note失败，链接不存在:  " + str(url)
        }










