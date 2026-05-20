import { useState, useEffect } from 'react'
import { Table, Tag, Typography } from 'antd'
import { fetchAlerts } from '../api/client'

const { Title } = Typography
const LEVEL_MAP: Record<number, { color: string; text: string }> = {
  1: { color: 'red', text: '🔴 一级' },
  2: { color: 'orange', text: '🟠 二级' },
  3: { color: 'gold', text: '🟡 三级' },
}

export default function Alerts() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    fetchAlerts().then(d => { setData(d || []); setLoading(false) })
  }, [])

  const columns = [
    { title: '时间', dataIndex: 'alert_time', width: 170, render: (v: string) => v?.slice(0, 19) },
    { title: '级别', dataIndex: 'level', width: 90, render: (v: number) =>
        <Tag color={LEVEL_MAP[v]?.color}>{LEVEL_MAP[v]?.text}</Tag> },
    { title: '类别', dataIndex: 'category', width: 80 },
    { title: '内容', dataIndex: 'title', ellipsis: true },
  ]

  return (
    <div>
      <Title level={3} style={{ color: '#e0e0e0' }}>⚠️ 预警中心</Title>
      <Table columns={columns} dataSource={data} rowKey="id"
        loading={loading} pagination={{ pageSize: 20 }} size="small" />
    </div>
  )
}
