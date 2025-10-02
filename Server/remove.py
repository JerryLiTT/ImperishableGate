from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" remove "www.github.com"                                                                                
{'server': '100.92.189.86:9323', 'action': 'remove', 'payload1': 'www.github.com'}

'''
router = APIRouter()

@router.post("/remove")#这里要修改
async def remove(request: Request):
    data = await request.json()
    url = data.get("payload1")

    print("收到请求内容:", data)

    # 检查是否是 url
    if db.link_exists(url):
        db.delete_link(url)
        print(f"已删除: {url}")
        return {
            "action": "remove",
            "payload1": f"已删除: {url}"
        }
    else:
        print(f"删除失败，链接不存在: {url}")
        return {
            "action": "remove",
            "payload1": f"删除失败，链接不存在: {url}"
        }





