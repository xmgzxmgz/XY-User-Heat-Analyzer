from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .crawler import XianyuCrawler
from .analysis import analyze_items, analyze_csv


class CrawlRequest(BaseModel):
    keyword: str
    max_pages: int = 3
    use_json_api: bool = True


class AnalyzeRequest(BaseModel):
    items: List[dict]
    top_n: int = 10
    stopwords_path: Optional[str] = "data/stopwords.txt"


class AnalyzeCSVRequest(BaseModel):
    input_csv: str = "xianyu_items.csv"
    top_n: int = 10
    stopwords_path: Optional[str] = "data/stopwords.txt"


app = FastAPI(title="XY User Heat Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/crawl")
def crawl(req: CrawlRequest):
    crawler = XianyuCrawler(keyword=req.keyword, max_pages=req.max_pages, use_json_api=req.use_json_api)
    items = crawler.crawl()
    return {"count": len(items), "items": items}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    result = analyze_items(req.items, stopwords_path=req.stopwords_path, top_n=req.top_n)
    # 将 Series 转为 [{word, count}] 列表
    payload = [{"word": str(idx), "count": int(val)} for idx, val in result.items()]
    return {"top": payload}


@app.post("/analyze-csv")
def analyze_csv_endpoint(req: AnalyzeCSVRequest):
    result = analyze_csv(req.input_csv, stopwords_path=req.stopwords_path, top_n=req.top_n)
    payload = [{"word": str(idx), "count": int(val)} for idx, val in result.items()]
    return {"top": payload}


@app.get("/demo/analyze")
def demo_analyze(top_n: int = 10, stopwords_path: Optional[str] = "data/stopwords.txt"):
    result = analyze_csv("data/demo_xianyu_items.csv", stopwords_path=stopwords_path, top_n=top_n)
    payload = [{"word": str(idx), "count": int(val)} for idx, val in result.items()]
    return {"top": payload}