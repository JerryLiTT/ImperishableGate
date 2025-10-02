import requests
from parser import parse_command

'''
客户端的主程序
主要用于发送用户命令、显示服务端的输出
后面改进的话可以试试输出标颜色、或者做一个GUI
'''

def main():
    # 模拟用户输入
    user_input = input("请输入指令: ")

    # 调用解析器
    parsed = parse_command(user_input)

    print(parsed)

    if "error" in parsed:
        print("解析失败:", parsed["error"])
        return

    # 拼接 URL
    url = f"http://{parsed['server']}/{parsed['action']}"

    try:
        # 发送 POST 请求
        response = requests.post(url, json=parsed, timeout=5)

        # 打印返回结果
        print("状态码:", response.status_code)
        print("响应内容:", response.text)

    except requests.exceptions.RequestException as e:
        print("请求失败:", e)


if __name__ == "__main__":
    while True:

        main()
