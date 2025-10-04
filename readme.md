# ImperishableGate

**ImperishableGate** 是一个轻量级、高效的链接管理与服务器交互工具，旨在帮助你轻松管理和查询各类网址、标签和备注信息，同时提供便捷的服务器通信接口。无论你是需要批量管理收藏链接、自动抓取元信息，还是想快速测试服务器连接状态，ImperishableGate 都能为你提供稳定而灵活的解决方案。

<img src="https://i0.hdslb.com/bfs/new_dyn/c4eb64ff9626bed575f01a70516ade26515860792.jpg" title="Ciallo～(∠・ω< )⌒☆" alt="一张平平无奇的图片" data-align="center">

通过ImperishableGate，你可以：

* **快速添加、删除和修改链接**：不仅能保存 URL，还可以附加名称、标签和备注信息。

* **智能标签管理**：对链接进行分类标记，支持特别关注标签（如 `starred`）的轮询与邮件提醒功能。

* **高效搜索与查询**：支持基于 URL、名称、标签或关键字的精准或模糊搜索。

* **服务器交互测试**：通过 `ping` 和 `pingtest` 命令检测服务器连接状态。

* **便捷的批量操作**：一次性打开多个链接，或为多个链接添加/移除标签（功能持续开发中）。
  
  

ImperishableGate 基于Python开发，采用简洁的命令行交互模式，每条命令对应明确的功能，响应数据采用 JSON 格式，方便程序化处理。



* * *

## 文件目录

```
└─ImperishableGate
    │  links.db                 # 数据库文件
    │  readme.md                # readme文档
    │
    ├─Client
    │  │  main.py               # CLI客户端主程序
    │  │  parser.py             # 解析命令
    │
    └─Server
        │  add.py               # 添加链接
        │  addname.py           # 添加链接别名
        │  addnote.py           # 添加链接备注
        │  addtag.py            # 添加链接标签
        │  db.py                # 数据处理函数
        │  editnote.py          # 编辑链接备注
        │  get.py               # 获取链接信息
        │  http_utils.py        # 检查链接可用性
        │  list1.py             # 列出所有链接信息
        │  main.py              # 服务端主程序
        │  metagrab.py          # 获取链接元数据
        │  opener.py            # 打开链接
        │  ping.py              # 测试连接
        │  pingtest.py          # 测试连接
        │  remove.py            # 删除链接
        │  removename.py        # 删除链接别名
        │  removenote.py        # 删除链接备注
        │  removetag.py         # 删除链接标签
        │  search.py            # 模糊搜索
        │  searchtag.py         # 搜索带某标签的链接
        │  send_email.py        # 发送提醒邮件
```

---

安装指南
----

1. 克隆仓库：

```
git clone https://github.com/JerryLiTT/ImperishableGate.git
cd ImperishableGate 
```

2. 安装依赖：

```
pip install requests fastapi uvicorn apscheduler bs4
```

3. 启动服务端：

```
python ./ImperishableGate/Server/main.py
```

4. 启动客户端：

```
python ./ImperishableGate/Client/main.py
```

> ⚡ 提示：部分功能（如 starred 标签轮询和邮件提醒）需要配置邮箱和查询频次，可在 `./ImperishableGate/Server/main.py` 中设置。

* * *

快速上手
----

```
# 测试服务器连接
gate "127.0.0.1:9323" ping "hello"

# 添加一个链接
gate "127.0.0.1:9323" add "bilibili.com"

# 给链接添加名称和标签
gate "127.0.0.1:9323" addname "B站" "bilibili.com"
gate "127.0.0.1:9323" addtag "ACG" "bilibili.com"

# 给链接添加备注
gate "127.0.0.1:9323" addnote "哔哩哔哩，干杯！" "bilibili.com"

# 查询链接信息
gate "127.0.0.1:9323" get "B站"

# 使用默认浏览器打开链接
gate "127.0.0.1:9323" open "B站"`
```

* * *

命令一览
----

接下来，你可以通过以下命令管理你的链接世界。



| 命令             | 用法                                  | 功能                                       |
| -------------- | ----------------------------------- | ---------------------------------------- |
| **ping**       | `gate ip ping "str"`                | 测试与服务器的连接状态                              |
| **pingtest**   | `gate ip pingtest "str"`            | 测试服务器连接，会重复输入字符串并返回时间                    |
| **list**       | `gate ip list`                      | 显示存储的所有链接及信息（url、name、note、tag、metadata） |
| **add**        | `gate ip add "url"`                 | 添加 URL 到数据库，自动抓取 metadata                |
| **remove**     | `gate ip remove "url"`              | 从数据库删除 URL 及其信息                          |
| **addtag**     | `gate ip addtag "tag" "url"`        | 为 URL 添加标签                               |
| **removetag**  | `gate ip removetag "tag" "url"`     | 移除 URL 标签                                |
| **addnote**    | `gate ip addnote "note" "url"`      | 给 URL 添加备注                               |
| **removenote** | `gate ip removenote "url"`          | 删除 URL 的备注                               |
| **editnote**   | `gate ip editnote "note" "url"`     | 修改 URL 的备注                               |
| **addname**    | `gate ip addname "name" "url"`      | 给 URL 添加名称，简化操作                          |
| **removename** | `gate ip removename "name"`         | 删除 URL 的名称                               |
| **searchtag**  | `gate ip searchtag "tag"`           | 查找标有指定 tag 的所有 URL 信息                    |
| **get**        | `gate ip get "url/name"`            | 获取指定 URL 或 name 的详细信息                    |
| **search**     | `gate ip search "str"`              | 模糊搜索 URL、name、metadata 等信息               |
| **open**       | `gate ip open "url/name/tag" [...]` | 使用默认浏览器打开指定 URL、name 或 tag 下的所有 URL      |
| 开发中......      |                                     |                                          |

> 小提示：即使你在输入 URL 或命令时出错，ImperishableGate 也会友好地给出提示信息，让你的操作无压力。



## ping

```
gate ip ping "str"
```

👉用于**测试与服务器的连接状态**，后面字符串可随便填

例如：

```
gate "127.0.0.1:9323" ping "ciallo"
```

会返回：

```
{"action":"ping","payload1":"ping test succeeded"}
```



---



## pingtest

```
gate ip pingtest "str"
```

👉用于**测试与服务器的连接状态**

会把你的输入的字符串重复两遍输出，并给出当前时间

例如：

```
gate "127.0.0.1:9323" pingtest "ciallo"
```

会返回：

```
{"action":"pingtest","payload1":"ciallociallo","time":"2025-10-02 21:05:28"}
```



---



## list

```
gate ip list
```

👉用于**显示你所储存的链接**，以及链接相关的**所有信息**，包括`url`、`name`、`note`、`tag`、`metadata`

例如：

```
gate "127.0.0.1:9323" list
```

会返回：

```
{"action":"searchtag","list":[
["https://www.bing.com",[],"",["starred"],{"title":"","description":"","keywords":"","og:site_name":""}],["https://www.google.com",[],"",[],{"title":"","description":"","keywords":"","og:site_name":""}],["https://www.bilibili.com",[],"",[],{"title":"哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","description":"因为内容太多了，所以略去","og:site_name":""}],["www.acfun.cn",[],"",["acg"],{"title":"AcFun弹幕视频网 - 认真你就输啦 (・ω・)ノ- ( ゜- ゜)つロ","description":"AcFun是国内首家弹幕视频网站，这里有全网独家动漫新番， 友好的弹幕氛围，有趣的UP主，好玩有科技感的虚拟偶像，年轻人都在用。","keywords":"A站 AcFun ACG 弹幕 视频 动画 漫画 游戏 新番 鬼畜 东方 初音 DOTA MUGEN","og:site_name":""}]]}
```

> 看起来人都麻了，对吧？别急，我会改的



---



## add

```
gate ip add "url"
```

👉用于**添加一个`url`到数据库**中，同时自动爬取该网址的`metadata`并记入数据库

若想查看，可以使用`get`命令

例如：

```
gate 127.0.0.1:9323 add "bilibili.com"
```

会返回：

```
 {"action":"pingtest","payload1":"已添加: bilibili.com"}
```

请注意，要输入一个`url`/`IP`地址，否则会告诉你：

```
 {"action":"pingtest","payload1":"That's not an url"}
```

如果数据库里已经有了相应的`url`了，那会告诉你：

```
{"action":"pingtest","payload1":"链接已存在: bilibili.com"}
```



---



## remove

```
gate ip remove "url"
```

👉用于从数据库中**移除一个`url`**，同时抹去它的`name`、`note`和`metadata`

例如：

```
gate 127.0.0.1:9323 remove "bilibili.com"
```

会返回：

```
{"action":"remove","payload1":"已删除: bilibili.com"}
```

输错或者重复删除也没有关系啦，会告诉你：

```
{"action":"remove","payload1":"删除失败，链接不存在: bilibili.com"}
```



---



## addtag

```
gate ip addtag "tag" "url"
```

**👉为你的`url`添加`tag`**

例如：

```
gate "127.0.0.1:9323" addtag "ciallo" "bilibili.com"
```

会返回：

```
{"action":"addtag","payload1":"successfully added tag ciallo to bilibili.com"}
```

如果没有`url`的话，会提示你：

```
{"action":"remove","payload1":"添加tag失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}
```

重复输入的话，会告诉你：

```
{"action":"addtag","payload1":"tag ciallo of bilibili.com already exists"}
```



> PS.特别地，如果你的`url`有一个`tag`名为`starred`**，那么这个`url`会被列入**特别关注列表，将有轮询机制查询这些`url`的状态，如果有异常将会发邮件提醒你（收件邮箱、发件邮箱、密码、查询频次均可调，具体见`./ImperishableGate/Server/main.py`，可能我哪天想起来的话会加个`conf`文件吧）

> PS.后续会开发一次性给多个`url`添加`tag`，一次性给`url`添加多个`tag`的功能



---



## removetag

```
gate ip removetag "tag" "url"
```

**👉为你的`url`移除`tag`**

例如：

```
gate "127.0.0.1:9323" removetag "ciallo" "bilibili.com"
```

会返回：

```
{"action":"removetag","payload1":"successfully removed tag ciallo from bilibili.com"}
```

如果没有`url`的话，会提示你：

```
{"action":"removetag","payload1":"删除tag失败，链接不存在: bilibili.com"}
```

如果`tag`本身不是属于`url`的话，会告诉你：

```
{"action":"removetag","payload1":"tag ciallo doesn't exist or belong to bilibili.com"}
```



> PS.后续会开发一次性给多个链接移除`tag`，一次性给链接移除多个`tag`的功能



---



## addnote

```
gate ip addnote "note" "url"
```

👉用于**给指定的`url`添加一条备注**

例如：

```
gate 127.0.0.1:9323 addnote "哔哩哔哩，干杯！" "bilibili.com"
```

会返回：

```
 {"action":"addnote","payload1":"successfully added note 哔哩哔哩，干杯！ to bilibili.com"}
```

如果没有`url`的话，会提示你：

```
{"action":"addnote","payload1":"添加note失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}
```

如果`note`已经存在的话，会提示你：

```
{"action":"addnote","payload1":"添加note失败，note已经存在，你可以试着用editnote命令修改它}
```



---



## removenote

```
gate ip removenote "url"
```

👉用于**给指定的`url`删除备注**

例如：

```
gate 127.0.0.1:9323 removenote "bilibili.com"
```

会返回：

```
 {"action":"removenote","payload1":"successfully removed note 哔哩哔哩，干杯！ from bilibili.com"}
```

如果没有`url`的话，会提示你：

```
{"action":"removenote","payload1":"删除note失败，链接不存在: bilibili.com"}
```

如果`note`不存在的话，会提示你：

```
{"action":"removenote","payload1":"删除note失败，note不存在}
```



---



## editnote

```
gate ip editnote "note" "url"
```

👉用于**给指定的`url`修改备注**

例如：

```
gate 127.0.0.1:9323 editnote "哔哩哔哩" "bilibili.com"
```

会返回：

```
 {"action":"editnote","payload1":"successfully edited note as 哔哩哔哩 to bilibili.com"}
```

如果没有`url`的话，会提示你：

```
{"action":"editnote","payload1":"修改note失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}
```

如果`note`已经存在的话，会提示你：

```
{"action":"editnote","payload1":"修改note失败，因为note不存在，所以帮你创建了个：successfully added note 哔哩哔哩 to bilibili.com}
```



---



## addname

```
gate ip addname "name" "url"
```

👉用于从数据库**给一个`url`添加一个name**

在`get`、`open`、`remove`、`addnote`、`editnote`、`removenote`、`addtag`、`removetag`命令中，你可以使用`name`替代`url`，简化繁琐的输入

例如：

```
gate 127.0.0.1:9323 addname "B站" "bilibili.com"
```

会返回：

```
 {"action":"addname","payload1":"successfully added name B站 to bilibili.com"}
```

如果没有`url`的话，会提示你：

```
{"action":"addname","payload1":"添加name失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}
```

如果`name`已经存在的话，会提示你：

```
{"action":"addname","payload1":"添加name失败，该name已经存在}
```



---



## removename

```
gate ip removename "name"
```

👉用于**给指定的`url`删除`name`**

例如：

```
gate 127.0.0.1:9323 removename "B站"
```

会返回：

```
 {"action":"removename","payload1":"successfully removed name B站 from bilibili.com"}
```

如果没有`name`的话，会提示你：

```
{"action":"removenote","payload1":"删除name失败，name B站 不存在"}
```



---



## searchtag

```
gate ip searchtag "tag"
```

👉用于**找出标有指定`tag`的`url`的所有信息**，包括`url`、`name`、`note`、`tag`、`metadata`

例如：

```
gate 127.0.0.1:9323 searchtag "ciallo"
```

会返回：

```
{"action":"searchtag","payload1":"["bilibili.com",["B站","bilibili"],"哔哩哔哩，干杯！",["ciallo","acg"],["metadata部分略去"],["acfun.com",["A站","acfun"],"这是acfun",["ciallo","acg"],["metadata部分略去"]]"}
```

如果没有`tag`或`tag`无对应的名字的话，会提示你：

```
{"action":"searchnote","payload1":"找不到ciallo，换个tag试试吧"}
```



---



## get

```
gate ip get "url/name"
```

👉用于给**找出**标有指定`name`（或者直接输入`url`也行）的`url`的**所有信息**，包括`url`、`name`、`note`、`tag`、`metadata`

例如：

```
gate 127.0.0.1:9323 get "B站"
```

会返回：

```
 {"action":"get","payload1":"["bilibili.com",["B站","bilibili"],"哔哩哔哩，干杯！",["ciallo","acg"],["metadata部分略去"]]}
```

如果找不到`name`或`url`的话，会提示你：

```
{"action":"searchnote","payload1":"找不到，换个name/url试试吧"}
```

---

## search

```
gate ip search "str"
```

**👉模糊搜索**功能，输入任意字符，返回与之有关的`url`及其所有信息，以及匹配之处

例如：

```
gate 127.0.0.1:9323 search 二次元
```

会返回：

```
 {"action":"search","payload1":[{"info":["https://www.bilibili.com",[],"",[],{"title":"哔哩哔哩 (゜-゜)つロ 干杯~-bilibili","description":"哔哩哔哩（bilibili.com)是国内知名的视频弹幕网站，这里有及时的动漫新番，活跃的ACG氛围，有创意的Up主。大家可以在这里找到许多欢乐。","keywords":"bilibili,哔哩哔哩,哔哩哔哩动画,哔哩哔哩弹幕网,弹幕视频,B站,弹幕,字幕,AMV,MAD,MTV,ANIME,动漫,动漫音乐,游戏,游戏解说,二次元,游戏视频,ACG,galgame,动画,番组,新番,初音,洛天依,vocaloid,日本动漫,国产动漫,手机游戏,网络游戏,电子竞技,ACG燃曲,ACG神曲,追新番,新番动漫,新番吐槽,巡音,镜音双子,千本樱,初音MIKU,舞蹈MMD,MIKUMIKUDANCE,洛天依原创曲,洛天依翻唱曲,洛天依投食歌,洛天依MMD,vocaloid家族,OST,BGM,动漫歌曲,日本动漫音乐,宫崎骏动漫音乐,动漫音乐推荐,燃系mad,治愈系mad,MAD MOVIE,MAD高燃","og:site_name":""}],"matched_fields":["metainfo"]}]}
```

当然，如果真的找不到，会返回：

```
{"action":"search","payload1":"找不到  hduawkbefkue ，换个内容试试吧"}
```



---



## open

```
gate ip open "url1/name1/tag1" "url2/name2/tag2" "url3/name3/tag3"
```

👉⽤默认浏览器打开给出的⽹址

可以一次性打开多个，`url`/`name`之间用空格隔开即可。如果输入的是`tag`的话，会一次性打开标有该`tag`的所有`url`

例如：

```
gate 127.0.0.1:9323 open aaa.com acg B站
```

会返回：

```
{"action":"open","payload1":["aaa.com","bilibili.com","www.acfun.cn","bilibili.com"]}
```

并且帮你打开以上网站

如果你给出的`url`/`name`/`tag`并不在数据库中，会告诉你：

```
{"action":"open","payload1":"不是吧，你输入的urls/names/tags我一个也找不到？！换个吧"}
```







![](https://i0.hdslb.com/bfs/new_dyn/8ea939441347fb849b71113ea3332393515860792.jpg)


