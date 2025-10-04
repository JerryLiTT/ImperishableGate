from fastapi import APIRouter, Request
import db

'''
gate "127.0.0.1:9323" search "ciallo"                         #这里要修改                                                      
{'server': '100.92.189.86:9323', 'action': 'search', 'payload1': 'ciallo'}#这里要修改





返回
{"action":"search","payload1":[{"info":["https://www.bilibili.com",[],"",[],{"title":"哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","description":"哔哩哔哩（bilibili.com)是国内知名的视频弹幕网站，这里有及时的动漫新番，活跃的ACG氛围，有创意的Up主。大家可以在这里找到许多欢乐。","keywords":"bilibili,哔哩哔哩,哔哩哔哩动画,哔哩哔哩弹幕网,弹幕视频,B站,弹幕,字幕,AMV,MAD,MTV,ANIME,动漫,动漫音乐,游戏,游戏解说,二次元,游戏视频,ACG,galgame,动画,番组,新番,初音,洛天依,vocaloid,日本动漫,国产动漫,手机游戏,网络游戏,电子竞技,ACG燃曲,ACG神曲,追新番,新番动漫,新番吐槽,巡音,镜音双子,千本樱,初音MIKU,舞蹈MMD,MIKUMIKUDANCE,洛天依原创曲,洛天依翻唱曲,洛天依投食歌,洛天依MMD,vocaloid家族,OST,BGM,动漫歌曲,日本动漫音乐,宫崎骏动漫音乐,动漫音乐推荐,燃系mad,治愈系mad,MAD MOVIE,MAD高燃","og:site_name":""}],"matched_fields":["url","metainfo"]},{"info":["bilibili.com",[],"",["starred"],{"title":"哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","description":"哔哩哔哩（bilibili.com)是国内知名的视频弹幕网站，这里有及时的动漫新番，活跃的ACG氛围，有创意的Up主。大家可以在这里找到许多欢乐。","keywords":"bilibili,哔哩哔哩,哔哩哔哩动画,哔哩哔哩弹幕网,弹幕视频,B站,弹幕,字幕,AMV,MAD,MTV,ANIME,动漫,动漫音乐,游戏,游戏解说,二次元,游戏视频,ACG,galgame,动画,番组,新番,初音,洛天依,vocaloid,日本动漫,国产动漫,手机游戏,网络游戏,电子竞技,ACG燃曲,ACG神曲,追新番,新番动漫,新番吐槽,巡音,镜音双子,千本樱,初音MIKU,舞蹈MMD,MIKUMIKUDANCE,洛天依原创曲,洛天依翻唱曲,洛天依投食歌,洛天依MMD,vocaloid家族,OST,BGM,动漫歌曲,日本动漫音乐,宫崎骏动漫音乐,动漫音乐推荐,燃系mad,治愈系mad,MAD MOVIE,MAD高燃","og:site_name":""}],"matched_fields":["url","metainfo"]}]}

'''
router = APIRouter()

@router.post("/search")#这里要修改
async def search(request: Request):#这里要修改
    data = await request.json()
    search_thing = data.get("payload1")
    search_result = db.search_all(search_thing)

    print("收到请求内容:", data)

    

    if search_result:  # 如果非空
        return {
            "action": "search",
            "payload1": search_result
        }

    else:
        return {
            "action": "search",
            "payload1": "找不到  " + str(search_thing) + " ，换个内容试试吧"
        }














