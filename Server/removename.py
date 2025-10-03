from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" removename "B站"                        #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'removename', 'payload1': 'B站'}#这里要修改

'''
router = APIRouter()

@router.post("/removename")#这里要修改
async def removename(request: Request):#这里要修改
    data = await request.json()
    name = data.get("payload1")
    

    print("收到请求内容:", data)
    print(db.get_all_names())

    if name in db.get_all_names():
        url = db.get_url_by_name(name)
        db.remove_name(name)
        
        
        print("successfully removed name " + name + " from " + str(url))
        return {
            "action": "removename",
            "payload1": "successfully removed name " + name + " from " + str(url)
        }

    else:
        return {
            "action": "removename",
            "payload1": "删除name失败，name " + name + "不存在"
        }

