import { useState, useEffect } from 'react';
import { Table, Tag } from 'antd';
import { fetchAlerts } from '../../api/client';

const LEVEL_TAG: Record<number, { color: string; text: string }> = {
  1: { color: 'red', text: '🔴 一级' },
  2: { color: 'orange', text: '🟠 二级' },
  3: { color: 'gold', text: '🟡 三级' },
};

export default function AlertPanel() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchAlerts().then(d => { setData(d || []); setLoading(false); });
  }, []);

  const columns = [
    { title: '时间', dataIndex: 'alert_time', width: 160, render: (v: string) => v?.slice(0, 16) },
    { title: '级别', dataIndex: 'level', width: 80, render: (v: number) => {
      const t = LEVEL_TAG[v] || { color: 'default', text: String(v) };
      return <Tag color={t.color}>{t.text}</Tag>;
    }},
    { title: '类别', dataIndex: 'category', width: 80 },
    { title: '内容', dataIndex: 'title', ellipsis: true },
  ];

  return <Table columns={columns} dataSource={data} rowKey="id"
    loading={loading} pagination={{ pageSize: 10 }} size="small" />;
}
