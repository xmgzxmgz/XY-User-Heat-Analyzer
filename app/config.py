import os

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

HTML_SEARCH_URL = "https://s.2.taobao.com/list/?q={keyword}&catid=0&ist=1"
JSON_API_URL = "https://s.2.taobao.com/list/waterfall?q={keyword}&start={page}"

REQUEST_TIMEOUT = 15
DEFAULT_DELAY_RANGE = (2.0, 5.0)

def get_proxies_from_env():
    http = os.environ.get("HTTP_PROXY")
    https = os.environ.get("HTTPS_PROXY")
    proxies = {}
    if http:
        proxies["http"] = http
    if https:
        proxies["https"] = https
    return proxies or None