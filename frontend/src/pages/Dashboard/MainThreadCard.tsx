import { useState, useEffect } from 'react';
import { Card, Radio, Tag, Spin, Empty } from 'antd';
import { fetchMainThread } from '../../api/client';

const PERIODS = [
  { label: '5日', value: 5 },
  { label: '1月', value: 20 },
  { label: '3月', value: 60 },
];

export default function MainThreadCard() {
  const [window, setWindow] = useState(20);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchMainThread(window).then(d => { setData(d); setLoading(false); });
  }, [window]);

  return (
    <Card
      title="🔥 当前主线"
      extra={<Radio.Group options={PERIODS} value={window} onChange={e => setWindow(e.target.value)}
        optionType="button" size="small" />}
      size="small"
    >
      <Spin spinning={loading}>
        {data?.top_sectors?.length > 0 ? (
          <div>
            {data.top_sectors.map((s: any, i: number) => (
              <div key={s.sector_code} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '8px 0', borderBottom: i < data.top_sectors.length - 1 ? '1px solid #f0f0f0' : 'none'
              }}>
                <span>
                  <Tag color={['gold', 'cyan', 'geekblue'][i]}>TOP{i + 1}</Tag>
                  <strong>{s.sector_name || s.sector_code}</strong>
                </span>
                <span style={{ color: '#666' }}>
                  评分 <strong>{s.score}</strong> | 流入 <strong style={{ color: '#cf1322' }}>{(s.amount_sum / 1e8).toFixed(1)}亿</strong> | 连续 {s.persist_days} 日
                </span>
              </div>
            ))}
            <div style={{ marginTop: 8, fontSize: 12, color: '#999' }}>
              计算时间: {data.computed_at}
            </div>
          </div>
        ) : (
          <Empty description="暂无主线数据，等待数据采集" />
        )}
      </Spin>
    </Card>
  );
}
