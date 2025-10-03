from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" list                                                                                
{'server': '100.92.189.86:9323', 'action': 'list'}

'''
router = APIRouter()

@router.post("/list")#这里要修改,而且list在python里被用过了，就改成list1
async def list1(request: Request):
    data = await request.json()
    #url = data.get("payload1")

    print("收到请求内容:", data)


    # 调用 db 获取所有链接
    urls = db.get_all_links()
    # 格式化返回，方便前端查看
    info_of_urls = []
    if urls:  # 如果非空
        for url in urls:
            info_of_urls.append(db.get_info_by_url(url[1]))
        print(info_of_urls)
        return {
            "action": "searchtag",
            "payload1": info_of_urls
        }
    else:
        return {
            "action": "list",
            "payload1": "还没有链接哦，快去添加吧！"
        }






