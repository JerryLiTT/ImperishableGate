from fastapi import APIRouter, Request
import db
import metagrab

'''
gate "127.0.0.1:9323" add "www.github.com"                                                                                
{'server': '100.92.189.86:9323', 'action': 'add', 'payload1': 'www.github.com'}

'''
router = APIRouter()

@router.post("/add")#这里要修改
async def add(request: Request):
    data = await request.json()
    url = data.get("payload1")

    print("收到请求内容:", data)

    # 检查是否是 url
    if url and len(url) >= 3 and '.' in url[1:-1]:
        success = db.add_link(url)
        if success:
            print("That's an url, 已存入数据库")
            metadata = metagrab.get_page_metadata(url)
            print(metadata)
            db.update_metainfo_by_url(url, metadata)
            print(db.update_metainfo_by_url(url, metadata))
            return {
                "action": "add",
                "payload1": f"已添加: {url}"
            }
        else:
            return {
                "action": "add",
                "payload1": f"链接已存在: {url}"
            }
    else:
        print("That's not an url")
        return {
            "action": "add",
            "payload1": "That's not an url"
        }





