import json
import time
import random
import urllib.parse
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .config import (
    DEFAULT_HEADERS,
    HTML_SEARCH_URL,
    JSON_API_URL,
    REQUEST_TIMEOUT,
    DEFAULT_DELAY_RANGE,
    get_proxies_from_env,
)


class XianyuCrawler:
    def __init__(
        self,
        keyword: str,
        max_pages: int = 5,
        use_json_api: bool = True,
        delay_range: tuple = DEFAULT_DELAY_RANGE,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
    ) -> None:
        self.keyword = keyword
        self.max_pages = max_pages
        self.use_json_api = use_json_api
        self.delay_range = delay_range
        self.headers = headers or DEFAULT_HEADERS
        self.proxies = proxies or get_proxies_from_env()

    def crawl(self) -> List[Dict]:
        items: List[Dict] = []
        for page in range(1, self.max_pages + 1):
            time.sleep(random.uniform(*self.delay_range))
            page_items = []
            if self.use_json_api:
                page_items = self._fetch_json_items(page)
            if not page_items:
                html = self._fetch_html_page(page)
                page_items = self._parse_html_items(html)
            if not page_items:
                continue
            items.extend(page_items)
        return items

    def _fetch_json_items(self, page: int) -> List[Dict]:
        encoded_keyword = urllib.parse.quote(self.keyword)
        url = JSON_API_URL.format(keyword=encoded_keyword, page=page)
        try:
            resp = requests.get(
                url, headers=self.headers, timeout=REQUEST_TIMEOUT, proxies=self.proxies
            )
            if resp.status_code != 200:
                return []
            data = None
            try:
                data = resp.json()
            except Exception:
                try:
                    data = json.loads(resp.text)
                except Exception:
                    return []
            return self._extract_items_from_json(data)
        except requests.RequestException:
            return []

    def _extract_items_from_json(self, data) -> List[Dict]:
        items: List[Dict] = []

        def add(title: Optional[str], price: Optional[str], url: Optional[str]):
            if not title:
                return
            title = str(title).strip()
            if not title:
                return
            items.append({"title": title, "price": price, "url": url})

        def try_list(lst):
            if not isinstance(lst, list):
                return
            for it in lst:
                if not isinstance(it, dict):
                    continue
                title = (
                    it.get("title")
                    or it.get("name")
                    or it.get("itemName")
                    or it.get("raw_title")
                )
                price = it.get("price") or it.get("itemPrice") or it.get("sellingPrice")
                url = it.get("view_url") or it.get("itemUrl") or it.get("url")
                add(title, price, url)

        if isinstance(data, dict):
            for key in ("items", "result", "list", "data", "rows"):
                try_list(data.get(key))
        elif isinstance(data, list):
            try_list(data)

        return items

    def _fetch_html_page(self, page: int) -> str:
        encoded_keyword = urllib.parse.quote(self.keyword)
        url = HTML_SEARCH_URL.format(keyword=encoded_keyword)
        try:
            resp = requests.get(
                url, headers=self.headers, timeout=REQUEST_TIMEOUT, proxies=self.proxies
            )
            if resp.status_code != 200:
                return ""
            return resp.text
        except requests.RequestException:
            return ""

    def _parse_html_items(self, html: str) -> List[Dict]:
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        items: List[Dict] = []

        selectors = [
            "a.item-title",
            "h4.item-title a",
            "div.item-info a",
            "a[class*='title']",
        ]

        links = []
        for sel in selectors:
            found = soup.select(sel)
            if found:
                links = found
                break
        if not links:
            links = soup.find_all("a")

        for a in links:
            title = a.get_text(strip=True) if a else None
            href = a.get("href") if a else None
            if not title or len(title) < 2:
                continue
            price = None
            price_span = None
            parent = a.parent if a else None
            if parent:
                price_span = parent.select_one("span.price") or parent.select_one(
                    "span.item-price"
                )
            price = price_span.get_text(strip=True) if price_span else None
            items.append({"title": title, "price": price, "url": href})

        return items

    @staticmethod
    def save_to_csv(items: List[Dict], output_path: str) -> None:
        import pandas as pd

        df = pd.DataFrame(items)
        if "title" in df.columns:
            df = df.dropna(subset=["title"])  # 保证标题存在
        df.to_csv(output_path, index=False, encoding="utf-8-sig")