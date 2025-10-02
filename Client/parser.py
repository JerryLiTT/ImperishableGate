import shlex

def parse_command(command: str) -> dict:
    """
    解析用户输入的命令，如:
    gate "127.0.0.1:9323" ping "konpaku youmu" "extra data"

    返回一个 dict，包含:
    - server: 服务器地址
    - action: 请求的接口（如 ping）
    - payload1, payload2, ...: 携带的参数
    """
    try:
        # 使用 shlex 拆分，支持引号
        tokens = shlex.split(command)

        if len(tokens) < 4:
            raise ValueError("命令格式不正确，至少需要 gate 服务器IP及端口 action 以及至少一个payload")

        if tokens[0] != "gate":
            raise ValueError("命令必须以 gate 开头")

        server = tokens[1]          # 服务器地址
        action = tokens[2]          # 接口名（如 ping）
        payloads = tokens[3:]       # 传递的数据payload（可能多个）

        result = {
            "server": server,
            "action": action,
        }

        # 动态生成 payload1, payload2...，遍历的
        for i, payload in enumerate(payloads, start=1):
            result[f"payload{i}"] = payload

        return result

    except Exception as e:
        return {"error": str(e)}


# 测试
if __name__ == "__main__":
    cmd = 'gate "127.0.0.1:1270" ping "konpaku youmu" "extra arg" "third arg"'
    result = parse_command(cmd)
    print(result)
