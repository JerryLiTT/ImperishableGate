from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" editnote "哔哩哔哩，干杯！" "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'editnote', 'payload1': '哔哩哔哩，干杯！', 'payload2': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/editnote")#这里要修改
async def editnote(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload2")
    note = data.get("payload1")

    print("收到请求内容:", data)
    print(db.get_note_by_url(url))

    if db.link_exists(url) == True:
        if db.has_note(url)==True:
            db.update_note_of_url(url, note)
            return {
                "action": "editnote",
                "payload1": "successfully edited note as " + note + " to " + url
            }
        else:
            db.add_note_to_url(url, note)
            print("successfully added note " + note + " to " + url)
            return {
                "action": "editnote",
                "payload1": "修改note失败，因为note不存在，所以帮你创建了个：successfully added note " + note + " to " + url
            }

    else:
        return {
            "action": "editnote",
            "payload1": "修改note失败，链接不存在:  " + str(url) + " ，你可以试着用add命令创建一个"
        }










