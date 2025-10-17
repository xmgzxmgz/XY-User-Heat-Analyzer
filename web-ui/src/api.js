const BASE_URL = "http://localhost:8000";

export async function crawl(keyword, maxPages = 3, useJsonApi = true) {
  const resp = await fetch(`${BASE_URL}/crawl`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ keyword, max_pages: maxPages, use_json_api: useJsonApi }),
  });
  if (!resp.ok) throw new Error(`crawl failed: ${resp.status}`);
  return await resp.json();
}

export async function analyze(items, topN = 10, stopwordsPath = "data/stopwords.txt") {
  const resp = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items, top_n: topN, stopwords_path: stopwordsPath }),
  });
  if (!resp.ok) throw new Error(`analyze failed: ${resp.status}`);
  return await resp.json();
}

export async function demoAnalyze(topN = 10) {
  const resp = await fetch(`${BASE_URL}/demo/analyze?top_n=${topN}`);
  if (!resp.ok) throw new Error(`demo analyze failed: ${resp.status}`);
  return await resp.json();
}