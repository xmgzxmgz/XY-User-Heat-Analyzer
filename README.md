[![License: MIT](https://img.shields.io/badge/License-MIT-2bbc8a.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Stars](https://img.shields.io/github/stars/xmgzxmgz/XY-User-Heat-Analyzer?style=social)
![Last Commit](https://img.shields.io/github/last-commit/xmgzxmgz/XY-User-Heat-Analyzer)

# 闲鱼商品名录爬取与品类关注度分析（XY User Heat Analyzer）

本项目实现：爬取闲鱼网页版商品信息（重点是商品名称），并通过中文分词与词频统计，输出用户关注度最高的品类关键词。

## 功能概览
- 爬取：支持尝试闲鱼搜索页的 JSON 接口（优先），失败则回退到 HTML 解析
- 反爬缓解：随机延迟、可自定义请求头与代理
- 持久化：导出为 `CSV`（UTF-8 BOM，方便中文）
- 分析：中文分词（jieba）、停用词过滤、词频统计、TopN 输出
- 命令行：`crawl`、`analyze`、`all`、`demo` 四种模式

## 环境准备
- Python 3.9+（推荐）
- 安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 快速上手
- 全流程：爬取并分析

```bash
python3 app/main.py --mode all --keyword "苹果 手机" --max-pages 3 --top-n 20
```

- 仅爬取：

```bash
python3 app/main.py --mode crawl --keyword "华为" --max-pages 2 --output xianyu_items.csv
```

- 仅分析（基于已生成的 `xianyu_items.csv`）：

```bash
python3 app/main.py --mode analyze --top-n 15 --input xianyu_items.csv
```

- 演示分析（不联网，使用内置示例数据）：

```bash
python3 app/main.py --mode demo --top-n 10
```

## 使用说明
- 关键参数：
  - `--keyword`：搜索关键词（中文可用）
  - `--max-pages`：最大页数（按站点实际分页策略，JSON 接口使用 `start` 递增）
  - `--use-json-api`：尝试使用瀑布流 JSON 接口（默认开启）
  - `--output`：爬取导出的 CSV 文件名（默认 `xianyu_items.csv`）
  - `--top-n`：输出前 N 个高频词
  - `--stopwords`：停用词文件路径（默认 `data/stopwords.txt`）
  - `--input`：分析时指定输入 CSV（仅在 `analyze` 模式生效）

- 代理设置（可选）：
  - 通过环境变量配置：`HTTP_PROXY`、`HTTPS_PROXY`

## 重要提示与策略
- 闲鱼网页可能通过 JavaScript 动态加载数据；本项目优先尝试其瀑布流 JSON 接口（`/list/waterfall`），若结构变化或不可用则自动回退到 HTML 解析。
- 若遇到强反爬：
  - 提高随机延迟范围
  - 更换或轮换 User-Agent
  - 使用代理池
- HTML 结构可能频繁更新，解析器实现了多选择器与鲁棒回退，核心目标是尽可能获取标题用于分析。

## 输出
- 爬取数据：`xianyu_items.csv`
  - 字段：`title`、`price`、`url`
- 分析结果：终端打印 TopN 词频，并可通过 `--save-top` 导出 `analysis_top_words.csv`

## 许可证
- 仅用于学习与研究目的。请遵守目标网站的使用条款与相关法律法规。