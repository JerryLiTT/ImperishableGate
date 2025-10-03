from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" addnote "哔哩哔哩，干杯！" "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'addnote', 'payload1': '哔哩哔哩，干杯！', 'payload2': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/addnote")#这里要修改
async def addnote(request: Request):#这里要修改
    data = await request.json()
    url = data.get("payload2")
    note = data.get("payload1")

    print("收到请求内容:", data)
    print(db.get_note_by_url(url))

    if db.link_exists(url) == True:
        if db.has_note(url)==True:
            return {
                "action": "addnote",
                "payload1": "failed to add note " + note + " to " + url + " , because note " + db.get_note_by_url(url) + " of " + str(url) + " already exists, you can try to edit it"
            }
        else:
            db.add_note_to_url(url, note)
            print("successfully added note " + note + " to " + url)
            return {
                "action": "addnote",
                "payload1": "successfully added note " + note + " to " + url
            }

    else:
        return {
            "action": "addnote",
            "payload1": "添加note失败，链接不存在:  " + str(url) + " ，你可以试着用add命令创建一个"
        }










