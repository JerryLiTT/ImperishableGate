# http_utils.py
from typing import Optional, Tuple
import requests

def get_status_code(
    url: str,
    timeout: float = 5.0,
    allow_redirects: bool = True,
    verify_ssl: bool = True,
    headers: Optional[dict] = None,
) -> Tuple[Optional[int], Optional[str]]:
    """
    获取给定 URL 的 HTTP 状态码。

    返回:
        (status_code, error_message)
        - status_code: 成功时返回整数（如 200, 404）
        - error_message: 出错时返回错误描述，否则为 None
    """
    # 如果没有协议头，默认加上 https://
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = headers or {"User-Agent": "status-checker/1.0"}
    try:
        # 尝试 HEAD
        resp = requests.head(
            url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            verify=verify_ssl
        )
        # 如果服务器不支持 HEAD，回退 GET
        if resp.status_code in (405, 501):
            resp = requests.get(
                url,
                timeout=timeout,
                allow_redirects=allow_redirects,
                headers=headers,
                stream=True,
                verify=verify_ssl
            )
            resp.close()
        return resp.status_code, None
    except requests.exceptions.RequestException as e:
        return None, str(e)
