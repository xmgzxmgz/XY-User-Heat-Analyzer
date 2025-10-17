<script setup>
import { ref, computed } from 'vue'
import { crawl, analyze, demoAnalyze } from './api'

const tab = ref('crawl')

// Crawl state
const keyword = ref('手机')
const maxPages = ref(3)
const useJsonApi = ref(true)
const loadingCrawl = ref(false)
const items = ref([])

// Analyze state
const topN = ref(10)
const loadingAnalyze = ref(false)
const topWords = ref([])

const maxCount = computed(() => {
  return topWords.value.reduce((m, x) => Math.max(m, x.count || 0), 0)
})

async function onCrawl() {
  loadingCrawl.value = true
  topWords.value = []
  try {
    const res = await crawl(keyword.value, Number(maxPages.value), useJsonApi.value)
    items.value = res.items || []
  } catch (e) {
    alert('爬取失败：' + e.message)
  } finally {
    loadingCrawl.value = false
  }
}

async function onAnalyze() {
  loadingAnalyze.value = true
  try {
    const res = await analyze(items.value, Number(topN.value))
    topWords.value = res.top || []
  } catch (e) {
    alert('分析失败：' + e.message)
  } finally {
    loadingAnalyze.value = false
  }
}

async function onAnalyzeDemo() {
  loadingAnalyze.value = true
  try {
    const res = await demoAnalyze(Number(topN.value))
    topWords.value = res.top || []
  } catch (e) {
    alert('演示分析失败：' + e.message)
  } finally {
    loadingAnalyze.value = false
  }
}
</script>

<template>
  <div class="container">
    <header>
      <h1>XY 用户关注度分析</h1>
      <nav>
        <button :class="{active: tab==='crawl'}" @click="tab='crawl'">爬取</button>
        <button :class="{active: tab==='analyze'}" @click="tab='analyze'">分析</button>
      </nav>
    </header>

    <section v-if="tab==='crawl'" class="card">
      <h2>爬取闲鱼商品</h2>
      <div class="form-row">
        <label>关键词</label>
        <input v-model="keyword" placeholder="例如：苹果 手机" />
      </div>
      <div class="form-row">
        <label>最大页数</label>
        <input type="number" v-model="maxPages" min="1" />
      </div>
      <div class="form-row">
        <label>
          <input type="checkbox" v-model="useJsonApi" /> 优先 JSON 接口
        </label>
      </div>
      <div class="actions">
        <button @click="onCrawl" :disabled="loadingCrawl">{{ loadingCrawl ? '爬取中...' : '开始爬取' }}</button>
      </div>
      <p class="hint">注意：若站点结构变化或触发反爬，可能导致结果为空。</p>

      <div v-if="items.length" class="table-wrap">
        <h3>结果（{{ items.length }} 条）</h3>
        <table>
          <thead>
            <tr>
              <th>标题</th>
              <th>价格</th>
              <th>链接</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(it, idx) in items" :key="idx">
              <td>{{ it.title }}</td>
              <td>{{ it.price || '-' }}</td>
              <td>
                <a v-if="it.url" :href="it.url" target="_blank">打开</a>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-else class="card">
      <h2>品类关注度分析</h2>
      <div class="form-row">
        <label>Top N</label>
        <input type="number" v-model="topN" min="1" />
      </div>
      <div class="actions">
        <button @click="onAnalyze" :disabled="loadingAnalyze || !items.length">{{ loadingAnalyze ? '分析中...' : '分析当前爬取结果' }}</button>
        <button @click="onAnalyzeDemo" :disabled="loadingAnalyze">{{ loadingAnalyze ? '分析中...' : '用演示数据分析' }}</button>
      </div>

      <div v-if="topWords.length" class="chart">
        <h3>Top 词频</h3>
        <div class="bar" v-for="(row, i) in topWords" :key="i">
          <span class="label">{{ row.word }}</span>
          <span class="bar-fill" :style="{width: ((row.count / (maxCount||1)) * 100) + '%'}"></span>
          <span class="count">{{ row.count }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.container { max-width: 1000px; margin: 0 auto; padding: 24px; font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }
header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
nav button { margin-left: 8px; padding: 8px 12px; border: 1px solid #ddd; background: #fff; cursor: pointer; }
nav button.active { background: #1f6feb; color: #fff; border-color: #1f6feb; }
.card { background: #fff; border: 1px solid #eee; padding: 16px; border-radius: 8px; }
.form-row { display: flex; align-items: center; gap: 12px; margin: 8px 0; }
.form-row label { width: 120px; color: #555; }
.form-row input[type="text"], .form-row input[type="number"] { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
.actions { display: flex; gap: 12px; margin: 12px 0; }
.actions button { padding: 8px 12px; border: none; background: #1f6feb; color: #fff; border-radius: 4px; cursor: pointer; }
.actions button:disabled { opacity: 0.6; cursor: not-allowed; }
.hint { color: #888; font-size: 12px; }
.table-wrap { margin-top: 12px; overflow: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid #eee; padding: 8px; text-align: left; }
th { background: #fafafa; }
.chart { margin-top: 16px; }
.bar { display: grid; grid-template-columns: 1fr 6fr 60px; align-items: center; gap: 8px; margin: 6px 0; }
.bar .label { color: #333; }
.bar .bar-fill { height: 16px; background: #10b981; border-radius: 4px; }
.bar .count { text-align: right; color: #555; }
</style>
