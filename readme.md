helloworld

# 命令一览

## ping

`gate ip ping "str"`

用于测试与服务器的连接状态，后面字符串可随便填

例如`gate "127.0.0.1:9323" ping "ciallo"`

会返回`{"action":"ping","payload1":"ping test succeeded"}`



## pingtest

`gate ip pingtest "str"`

用于测试与服务器的连接状态，会把你的输入的字符串重复两遍输出，并给出当前时间

例如`gate "127.0.0.1:9323" pingtest "ciallo"`
会返回`{"action":"pingtest","payload1":"ciallociallo","time":"2025-10-02 21:05:28"}`



## list

`gate ip list`

用于显示你所储存的链接

例如`gate "127.0.0.1:9323" list`

会返回`{"action":"list","payload1":[{"id":2,"url":"https://openai.com","note":null}，{"id":4,"url":"www.bilibili.com","note":null}]}`



## add

`gate ip add "url"`

用于添加一个url到数据库中

例如`gate 127.0.0.1:9323 add "bilibili.com"`

会返回` {"action":"pingtest","payload1":"已添加: bilibili.com"}`

请注意，要输入一个url/IP地址，否则会告诉你

 `{"action":"pingtest","payload1":"That's not an url"}`

如果数据库里已经有了相应的url了，那会告诉你

`{"action":"pingtest","payload1":"链接已存在: bilibili.com"}`





## remove

`gate ip remove "url"`

用于从数据库中移除一个url

例如`gate 127.0.0.1:9323 remove "bilibili.com"`

会返回`  {"action":"remove","payload1":"已删除: bilibili.com"}`

输错或者重复删除也没有关系啦，会告诉你

` {"action":"remove","payload1":"删除失败，链接不存在: bilibili.com"}`





# 将开发命令一览

## addtag

`gate ip addtag "tag" "url"`

为你的url添加tag

例如`gate "127.0.0.1:9323" addtag "ciallo" "bilibili.com"`

会返回`{"action":"addtag","payload1":"successfully added tag ciallo to bilibili.com"}`

如果没有url的话，会提示你

`{"action":"remove","payload1":"添加tag失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}`

重复输入的话，会告诉你

`{"action":"addtag","payload1":"tag ciallo of bilibili.com already exists"}`





PS.后续会开发一次性给多个链接添加tag，一次性给链接添加多个tag的功能



## removetag

`gate ip removetag "tag" "url"`

为你的url移除tag

例如`gate "127.0.0.1:9323" removetag "ciallo" "bilibili.com"`

会返回`{"action":"removetag","payload1":"successfully removed tag ciallo from bilibili.com"}`

如果没有url的话，会提示你

`{"action":"removetag","payload1":"删除tag失败，链接不存在: bilibili.com"}`

如果tag本身不是属于url的话，会告诉你

`{"action":"removetag","payload1":"tag ciallo doesn't exist or belong to bilibili.com"}`





PS.后续会开发一次性给多个链接移除tag，一次性给链接移除多个tag的功能



## addnote

`gate ip addnote "note" "url"`

用于给指定的url添加一条备注

例如`gate 127.0.0.1:9323 addnote "哔哩哔哩，干杯！" "bilibili.com"`

会返回` {"action":"addnote","payload1":"successfully added note 哔哩哔哩，干杯！ to bilibili.com"}`

如果没有url的话，会提示你

`{"action":"addnote","payload1":"添加note失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}`

如果note已经存在的话，会提示你

`{"action":"addnote","payload1":"添加note失败，note已经存在，你可以试着用editnote命令修改它}`



## removenote

`gate ip removenote "url"`

用于给指定的url删除备注

例如`gate 127.0.0.1:9323 removenote "bilibili.com"`

会返回` {"action":"removenote","payload1":"successfully removed note 哔哩哔哩，干杯！ from bilibili.com"}`

如果没有url的话，会提示你

`{"action":"removenote","payload1":"删除note失败，链接不存在: bilibili.com"}`

如果note不存在的话，会提示你

`{"action":"removenote","payload1":"删除note失败，note不存在}`



PS.写给开发：删除url的时候，需要删除其note



## editnote

`gate ip editnote "note" "url"`

用于给指定的url修改备注

例如`gate 127.0.0.1:9323 editnote "哔哩哔哩" "bilibili.com"`

会返回` {"action":"editnote","payload1":"successfully edited note as 哔哩哔哩 to bilibili.com"}`

如果没有url的话，会提示你

`{"action":"editnote","payload1":"修改note失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}`

如果note已经存在的话，会提示你

`{"action":"editnote","payload1":"修改note失败，因为note不存在，所以帮你创建了个：successfully added note 哔哩哔哩 to bilibili.com}`







## addname

`gate ip add "name" "url"`

用于从数据库给一个url添加一个name，可用于替代url

例如`gate 127.0.0.1:9323 addname "B站" "bilibili.com"`

会返回` {"action":"addname","payload1":"successfully added name B站 to bilibili.com"}`

如果没有url的话，会提示你

`{"action":"addname","payload1":"添加name失败，链接不存在: bilibili.com"，你可以试着用add命令创建一个}`

如果name已经存在的话，会提示你

`{"action":"addname","payload1":"添加name失败，该name已经存在}`



PS.写给开发，以后需要维护name2url的映射关系，即修改和url有关的所有操作





## removename

`gate ip removename "name"`

用于给指定的url删除name

例如`gate 127.0.0.1:9323 removename "B站"`

会返回` {"action":"removename","payload1":"successfully removed name B站 from bilibili.com"}`

如果没有name的话，会提示你

`{"action":"removenote","payload1":"删除name失败，name不存在"}`



PS.写给开发：删除url的时候，需要删除其name





## searchtag

`gate ip searchtag "tag"`

用于给找出标有指定tag的url的所有信息，包括url、name、note、tag

例如`gate 127.0.0.1:9323 searchtag "ciallo"`

会返回` {"action":"searchtag","payload1":"["bilibili.com",["B站","bilibili"],"哔哩哔哩，干杯！",["ciallo","acg"]],["acfun.com",["A站","acfun"],"这是acfun",["ciallo","acg"]]"}`

如果没有tag或tag无对应的名字的话，会提示你

`{"action":"searchnote","payload1":"找不到，换个tag试试吧"}`



## get

`gate ip get "url/name"`

用于给找出标有指定name的url的所有信息，包括url、name、note、tag

例如`gate 127.0.0.1:9323 get "B站"`

会返回` {"action":"searchtag","payload1":"["bilibili.com",["B站","bilibili"],"哔哩哔哩，干杯！",["ciallo","acg"]]}`

如果找不到name或url的话，会提示你

`{"action":"searchnote","payload1":"找不到，换个name/url试试吧"}`




