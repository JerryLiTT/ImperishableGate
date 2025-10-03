from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" searchtag "ciallo"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'searchtag', 'payload1': 'ciallo'}#这里要修改

'''
router = APIRouter()

@router.post("/searchtag")#这里要修改
async def searchtag(request: Request):#这里要修改
    data = await request.json()
    tag = data.get("payload1")
    

    print("收到请求内容:", data)

    urls = db.get_urls_by_tag(tag)
    info_of_urls = []

    if urls:  # 如果非空
        for url in urls:
            info_of_urls.append(db.get_info_by_url(url))
        return {
            "action": "searchtag",
            "payload1": info_of_urls
        }

    else:
        return {
            "action": "searchtag",
            "payload1": "找不到  " + str(tag) + " ，换个tag试试吧"
        }














