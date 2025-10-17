import argparse
import os
from typing import Optional

from .crawler import XianyuCrawler
from .analysis import analyze_csv


def run_crawl(keyword: str, max_pages: int, use_json_api: bool, output: str) -> str:
    crawler = XianyuCrawler(keyword=keyword, max_pages=max_pages, use_json_api=use_json_api)
    items = crawler.crawl()
    if not items:
        print("[warn] 未获取到任何商品数据，可能站点结构变化或触发反爬。")
    crawler.save_to_csv(items, output)
    print(f"[ok] 已导出 {len(items)} 条到: {output}")
    return output


def run_analyze(input_csv: str, stopwords_path: Optional[str], top_n: int, save_top: Optional[str] = None) -> None:
    result = analyze_csv(input_csv, stopwords_path=stopwords_path, top_n=top_n)
    print("\n[Top 词频]")
    print(result)
    if save_top:
        result.to_csv(save_top, encoding="utf-8-sig")
        print(f"\n[ok] 词频TopN已导出: {save_top}")


def run_demo(top_n: int, stopwords_path: Optional[str], save_top: Optional[str] = None) -> None:
    demo_csv = os.path.join("data", "demo_xianyu_items.csv")
    if not os.path.exists(demo_csv):
        print("[err] 演示数据不存在")
        return
    run_analyze(demo_csv, stopwords_path=stopwords_path, top_n=top_n, save_top=save_top)


def parse_args():
    p = argparse.ArgumentParser("闲鱼商品名录爬取与品类关注度分析")
    p.add_argument("--mode", choices=["crawl", "analyze", "all", "demo"], default="all")
    p.add_argument("--keyword", default="手机")
    p.add_argument("--max-pages", type=int, default=5)
    p.add_argument("--use-json-api", action="store_true", default=True)
    p.add_argument("--output", default="xianyu_items.csv")
    p.add_argument("--top-n", type=int, default=10)
    p.add_argument("--stopwords", default=os.path.join("data", "stopwords.txt"))
    p.add_argument("--input", help="analyze模式指定输入CSV")
    p.add_argument("--save-top", help="词频TopN导出路径")
    return p.parse_args()


def main():
    args = parse_args()
    if args.mode == "crawl":
        run_crawl(args.keyword, args.max_pages, args.use_json_api, args.output)
    elif args.mode == "analyze":
        if not args.input:
            print("[err] analyze模式需要 --input 指定输入CSV")
            return
        run_analyze(args.input, stopwords_path=args.stopwords, top_n=args.top_n, save_top=args.save_top)
    elif args.mode == "all":
        csv_path = run_crawl(args.keyword, args.max_pages, args.use_json_api, args.output)
        run_analyze(csv_path, stopwords_path=args.stopwords, top_n=args.top_n, save_top=args.save_top)
    elif args.mode == "demo":
        run_demo(args.top_n, stopwords_path=args.stopwords, save_top=args.save_top)


if __name__ == "__main__":
    main()