import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from charset_normalizer import from_bytes
from urllib.parse import urlparse

'''
from metagrab import get_page_metadata  

url = "https://www.python.org"
metadata = get_page_metadata(url)
print(metadata)
'''


'''
{
  "title": "Search - Microsoft Bing",
  "description": "Search with Microsoft Bing and use the power of AI to find information, explore webpages, images, videos, maps, and more. A smart search engine for the forever curious.",
  "keywords": null,
  "og:site_name": "Search - Microsoft Bing"
}
'''





DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

def get_page_metadata(url: str, timeout: int = 10) -> Dict[str, str]:
    """
    获取网页元数据
    返回 dict，包含: title, description, keywords, og:site_name
    - URL 无协议自动加 https://
    - 请求失败或字段缺失时返回空字符串
    """
    # 自动补全协议
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url

    # 初始化返回值
    result = {
        "title": "",
        "description": "",
        "keywords": "",
        "og:site_name": "",
    }

    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout, allow_redirects=True, verify=False)
        resp.raise_for_status()

        # 自动检测编码
        if not resp.encoding or resp.encoding.lower() == "iso-8859-1":
            resp.encoding = resp.apparent_encoding

        # 解析 HTML
        try:
            soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            soup = BeautifulSoup(resp.text, "html.parser")

        # title
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            result["title"] = title_tag.string.strip()

        # description
        desc = soup.find("meta", attrs={"name": "description"})
        if desc and desc.get("content"):
            result["description"] = desc["content"].strip()

        # keywords
        kw = soup.find("meta", attrs={"name": "keywords"})
        if kw and kw.get("content"):
            result["keywords"] = kw["content"].strip()

        # og:site_name
        og = soup.find("meta", attrs={"property": "og:site_name"})
        if og and og.get("content"):
            result["og:site_name"] = og["content"].strip()

    except requests.exceptions.RequestException as e:
        # 网络错误、SSL 错误、超时等
        print(f"[Warning] 请求失败: {e}. 返回空结果。")

    return result


# 示例调用
if __name__ == "__main__":
    urls = [
        "acfun.com",  # 没协议
        "https://example.com",
        "https://不存在的域名.test"
    ]

    for url in urls:
        meta = get_page_metadata(url)
        print(f"URL: {url}")
        print(meta)
        print("-" * 50)