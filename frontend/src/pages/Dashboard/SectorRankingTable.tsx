import { useState, useEffect } from 'react';
import { Table, Radio, Tag } from 'antd';
import { fetchSectorRanking } from '../../api/client';

export default function SectorRankingTable() {
  const [period, setPeriod] = useState('1w');
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchSectorRanking(period, 10).then(d => { setData(d.ranking || []); setLoading(false); });
  }, [period]);

  const fmt = (v: number) => (v / 1e8).toFixed(1) + '亿';

  const columns = [
    { title: '#', dataIndex: '__idx', width: 40, render: (_: any, __: any, i: number) => i + 1 },
    { title: '板块', dataIndex: 'sector_name', ellipsis: true },
    { title: '净流入', dataIndex: 'total_inflow', render: (v: number) =>
        <span style={{ color: v >= 0 ? '#cf1322' : '#3f8600' }}>{fmt(v)}</span> },
    { title: '强度', dataIndex: 'avg_ratio', render: (v: number) => `${(v * 100).toFixed(1)}%` },
  ];

  return (
    <div>
      <Radio.Group value={period} onChange={e => setPeriod(e.target.value)} size="small"
        style={{ marginBottom: 8 }}
        options={[
          { label: '1日', value: '1d' }, { label: '1周', value: '1w' },
          { label: '1月', value: '1m' }, { label: '3月', value: '3m' },
        ]} optionType="button" />
      <Table columns={columns} dataSource={data} rowKey="sector_code"
        loading={loading} pagination={false} size="small" />
    </div>
  );
}
