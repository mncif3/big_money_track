import { useState, useEffect } from 'react'
import { Table, Radio, Typography } from 'antd'
import { fetchSectorRanking } from '../api/client'

const { Title } = Typography

export default function Sectors() {
  const [period, setPeriod] = useState('1m')
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    fetchSectorRanking(period, 50).then(d => { setData(d.ranking || []); setLoading(false) })
  }, [period])

  const columns = [
    { title: '#', width: 50, render: (_: any, __: any, i: number) => <span style={{ color: '#8890a0' }}>{i + 1}</span> },
    { title: '板块', dataIndex: 'sector_name', ellipsis: true },
    { title: '净流入', dataIndex: 'total_inflow', render: (v: number) =>
        <span style={{ color: v >= 0 ? '#ff4d4f' : '#52c41a', fontWeight: 600 }}>
          {(v / 1e8).toFixed(1)}亿
        </span> },
    { title: '强度', dataIndex: 'avg_ratio', render: (v: number) =>
        <span style={{ color: '#8890a0' }}>{(v * 100).toFixed(1)}%</span> },
  ]

  return (
    <div>
      <Title level={3} style={{ color: '#e0e0e0' }}>📊 板块资金排名</Title>
      <Radio.Group value={period} onChange={e => setPeriod(e.target.value)} size="small"
        style={{ marginBottom: 12 }}
        options={[{ label: '1日', value: '1d' }, { label: '1周', value: '1w' }, { label: '1月', value: '1m' }, { label: '3月', value: '3m' }]}
        optionType="button" />
      <Table columns={columns} dataSource={data} rowKey="sector_code"
        loading={loading} pagination={{ pageSize: 31 }} size="small" />
    </div>
  )
}
