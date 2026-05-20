import { useState, useEffect } from 'react'
import { Typography, Spin } from 'antd'
import ReactECharts from 'echarts-for-react'
import { fetchSouthSummary } from '../api/client'

const { Title } = Typography

export default function South() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSouthSummary('3m').then(d => { setData(d); setLoading(false) })
  }, [])

  if (loading) return <Spin />
  if (!data?.trend?.length) return <Title level={4} style={{ color: '#8890a0' }}>暂无南向数据</Title>

  const dates = data.trend.map((p: any) => p.date)
  const total = data.trend.map((p: any) => (p.total_net / 1e8))
  const sh = data.trend.map((p: any) => (p.sh_net / 1e8))
  const sz = data.trend.map((p: any) => (p.sz_net / 1e8))

  const option = {
    grid: { top: 40, right: 30, bottom: 40, left: 60 },
    title: { text: '南向资金净流入趋势 (港股通)', textStyle: { color: '#e0e0e0' } },
    legend: { textStyle: { color: '#8890a0' } },
    xAxis: { type: 'category', data: dates, axisLabel: { rotate: 45, color: '#8890a0', fontSize: 10 } },
    yAxis: { type: 'value', name: '净流入(亿港元)', nameTextStyle: { color: '#8890a0' }, axisLabel: { color: '#8890a0' } },
    tooltip: { trigger: 'axis' },
    series: [
      { name: '合计', type: 'bar', data: total, itemStyle: { color: '#fa8c16' } },
      { name: '港股通(沪)', type: 'line', data: sh, smooth: true, symbol: 'none', lineStyle: { color: '#ff4d4f' } },
      { name: '港股通(深)', type: 'line', data: sz, smooth: true, symbol: 'none', lineStyle: { color: '#52c41a' } },
    ],
  }

  return (
    <div>
      <Title level={3} style={{ color: '#e0e0e0' }}>🟠 南向资金</Title>
      <ReactECharts option={option} style={{ height: 400 }} theme="dark" />
    </div>
  )
}
