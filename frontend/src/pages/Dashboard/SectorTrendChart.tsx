import { useState, useEffect } from 'react'
import ReactECharts from 'echarts-for-react'
import { Spin, Empty } from 'antd'
import { fetchMainThread, fetchSectorTrend } from '../../api/client'

const COLORS = ['#4f8cff', '#fa8c16', '#52c41a']

export default function SectorTrendChart() {
  const [loading, setLoading] = useState(true)
  const [series, setSeries] = useState<any[]>([])
  const [dates, setDates] = useState<string[]>([])

  useEffect(() => {
    (async () => {
      setLoading(true)
      const main = await fetchMainThread(20)
      const top3 = (main?.top_sectors || []).slice(0, 3)
      if (!top3.length) { setLoading(false); return }
      const allDates = new Set<string>()
      const allSeries = []
      for (let i = 0; i < top3.length; i++) {
        const s = top3[i]
        const trend = await fetchSectorTrend(s.sector_code, '1m')
        const data = (trend?.trend || []).map((p: any) => {
          allDates.add(p.date)
          return [p.date, p.main_net_inflow / 1e8]
        })
        allSeries.push({
          name: s.sector_name || s.sector_code, type: 'line', data,
          smooth: true, symbol: 'none',
          lineStyle: { color: COLORS[i], width: 2 },
          itemStyle: { color: COLORS[i] },
        })
      }
      setDates(Array.from(allDates).sort())
      setSeries(allSeries)
      setLoading(false)
    })()
  }, [])

  if (loading) return <Spin />
  if (!series.length) return <Empty description={<span style={{ color: '#8890a0' }}>暂无趋势数据</span>} />

  const option = {
    grid: { top: 30, right: 20, bottom: 30, left: 50 },
    legend: { top: 0, textStyle: { color: '#8890a0' } },
    xAxis: { type: 'category', data: dates, axisLabel: { rotate: 45, fontSize: 10, color: '#8890a0' }, axisLine: { lineStyle: { color: '#2a2d3a' } } },
    yAxis: { type: 'value', name: '净流入(亿)', nameTextStyle: { color: '#8890a0' }, axisLabel: { fontSize: 10, color: '#8890a0' }, splitLine: { lineStyle: { color: '#2a2d3a' } } },
    tooltip: { trigger: 'axis' },
    series,
  }

  return <ReactECharts option={option} style={{ height: 320 }} theme="dark" />
}
