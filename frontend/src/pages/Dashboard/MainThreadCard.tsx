import { useState, useEffect } from 'react'
import { Card, Radio, Tag, Spin, Empty } from 'antd'
import { fetchMainThread } from '../../api/client'

const PERIODS = [
  { label: '5日', value: 5 },
  { label: '1月', value: 20 },
  { label: '3月', value: 60 },
]

const TAG_COLORS = ['gold', 'cyan', 'geekblue']

export default function MainThreadCard() {
  const [window, setWindow] = useState(20)
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    fetchMainThread(window).then(d => { setData(d); setLoading(false) })
  }, [window])

  const cardStyle = { background: '#161822', borderColor: '#2a2d3a', borderRadius: 8, marginBottom: 16 }

  return (
    <Card
      title={<span style={{ color: '#e0e0e0' }}>🔥 当前主线</span>}
      extra={<Radio.Group options={PERIODS} value={window} onChange={e => setWindow(e.target.value)} optionType="button" size="small" />}
      size="small" style={cardStyle} styles={{ header: { borderBottom: '1px solid #2a2d3a' } }}
    >
      <Spin spinning={loading}>
        {data?.top_sectors?.length > 0 ? (
          <div>
            {data.top_sectors.map((s: any, i: number) => (
              <div key={s.sector_code} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '10px 0', borderBottom: i < data.top_sectors.length - 1 ? '1px solid #2a2d3a' : 'none'
              }}>
                <span>
                  <Tag color={TAG_COLORS[i]}>TOP{i + 1}</Tag>
                  <strong style={{ color: '#e0e0e0' }}>{s.sector_name || s.sector_code}</strong>
                </span>
                <span style={{ color: '#8890a0', fontSize: 13 }}>
                  评分 <strong style={{ color: '#4f8cff' }}>{s.score}</strong> | 流入 <strong style={{ color: '#ff4d4f' }}>{(s.amount_sum / 1e8).toFixed(1)}亿</strong> | 连续 {s.persist_days} 日
                </span>
              </div>
            ))}
            <div style={{ marginTop: 8, fontSize: 12, color: '#555' }}>计算时间: {data.computed_at}</div>
          </div>
        ) : (
          <Empty description={<span style={{ color: '#8890a0' }}>暂无主线数据，等待数据采集</span>} />
        )}
      </Spin>
    </Card>
  )
}
