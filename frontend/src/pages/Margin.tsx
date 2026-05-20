import { useState, useEffect } from 'react'
import { Typography, Spin } from 'antd'
import ReactECharts from 'echarts-for-react'
import { fetchMarginSummary } from '../api/client'

const { Title } = Typography

export default function Margin() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMarginSummary('3m').then(d => { setData(d); setLoading(false) })
  }, [])

  if (loading) return <Spin />
  if (!data?.trend?.length) return <Title level={4} style={{ color: '#8890a0' }}>暂无融资融券数据</Title>

  const dates = data.trend.map((p: any) => p.date)
  const balance = data.trend.map((p: any) => (p.margin_balance / 1e8))
  const netBuy = data.trend.map((p: any) => (p.margin_net_buy / 1e8))

  const option = {
    grid: { top: 40, right: 30, bottom: 40, left: 60 },
    title: { text: '融资融券趋势', textStyle: { color: '#e0e0e0' } },
    legend: { textStyle: { color: '#8890a0' } },
    xAxis: { type: 'category', data: dates, axisLabel: { rotate: 45, color: '#8890a0', fontSize: 10 } },
    yAxis: { type: 'value', name: '余额(亿)', nameTextStyle: { color: '#8890a0' }, axisLabel: { color: '#8890a0' } },
    tooltip: { trigger: 'axis' },
    series: [
      { name: '融资余额', type: 'line', data: balance, smooth: true, areaStyle: { opacity: 0.1 }, lineStyle: { color: '#4f8cff' } },
      { name: '融资净买入', type: 'bar', data: netBuy, itemStyle: { color: '#fa8c16' } },
    ],
  }

  return (
    <div>
      <Title level={3} style={{ color: '#e0e0e0' }}>💰 融资融券</Title>
      <ReactECharts option={option} style={{ height: 400 }} theme="dark" />
    </div>
  )
}
