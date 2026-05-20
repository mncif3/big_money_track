import { useState, useEffect } from 'react'
import { Table, Tag, Typography } from 'antd'
import api from '../api/client'

const { Title } = Typography

const STATUS_COLOR: Record<string, string> = {
  success: 'green', failed: 'red', running: 'blue', partial: 'orange',
}

export default function System() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    api.get('/system/etl-status').then(r => { setData(r.data || []); setLoading(false) }).catch(() => setLoading(false))
  }, [])

  const columns = [
    { title: '任务名', dataIndex: 'job_name' },
    { title: '状态', dataIndex: 'status', render: (v: string) => <Tag color={STATUS_COLOR[v] || 'default'}>{v}</Tag> },
    { title: '开始时间', dataIndex: 'start_time', width: 170 },
    { title: '结束时间', dataIndex: 'end_time', width: 170 },
    { title: '处理行数', dataIndex: 'rows_processed' },
  ]

  return (
    <div>
      <Title level={3} style={{ color: '#e0e0e0' }}>⚙️ 系统状态</Title>
      <Table columns={columns} dataSource={data} rowKey="job_name"
        loading={loading} pagination={false} size="small" />
    </div>
  )
}
