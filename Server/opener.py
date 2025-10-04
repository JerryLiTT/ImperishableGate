from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" open "bilibili.com"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'open', 'payload1': 'bilibili.com'}#这里要修改

'''
router = APIRouter()

@router.post("/open")#这里要修改
async def opener(request: Request):#这里要修改
    data = await request.json()
    urls_tested = []
    urls = [v for k, v in sorted(data.items()) if k.startswith("payload")]


    for url_in_urls in urls:

        #把name变成url
        if (db.link_exists(url_in_urls) == False) and (url_in_urls in db.get_all_names()):
            url_in_urls = db.get_url_by_name(url_in_urls)
            urls_tested.append(url_in_urls)

        #本来就是url的不用变了
        elif db.link_exists(url_in_urls) == True:
            urls_tested.append(url_in_urls)

        elif url_in_urls in db.get_all_tags():
            for url_of_tag in db.get_urls_by_tag(url_in_urls):
                urls_tested.append(url_of_tag)
    #把urls_tested搞定，里面全是有效的链接

    print(urls_tested)

    


    print("收到请求内容:", data)


    

    if urls_tested != []:  # 如果非空
        
        return {
            "action": "open",
            "payload1": urls_tested
        }

    else:
        return {
            "action": "open",
            "payload1": "不是吧，你输入的urls/names/tags我一个也找不到？！换个吧"
        }














