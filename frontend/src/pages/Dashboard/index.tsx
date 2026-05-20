import { useState, useEffect } from 'react';
import { Row, Col, Card, Typography } from 'antd';
import MainThreadCard from './MainThreadCard';
import SectorRankingTable from './SectorRankingTable';
import SectorTrendChart from './SectorTrendChart';
import AlertPanel from './AlertPanel';

const { Title } = Typography;

export default function Dashboard() {
  return (
    <div style={{ padding: 24, background: '#f0f2f5', minHeight: '100vh' }}>
      <Title level={3} style={{ marginBottom: 16 }}>
        🔥 CapFlow — 资金流向看板
      </Title>

      {/* Top: Main Thread */}
      <MainThreadCard />

      <Row gutter={16} style={{ marginTop: 16 }}>
        {/* Left: Sector Ranking */}
        <Col span={12}>
          <Card title="📊 板块资金流入 TOP10" size="small">
            <SectorRankingTable />
          </Card>
        </Col>
        {/* Right: Trend Chart */}
        <Col span={12}>
          <Card title="📈 主线板块资金趋势" size="small">
            <SectorTrendChart />
          </Card>
        </Col>
      </Row>

      {/* Bottom: Alerts */}
      <Card title="⚠️ 最近预警" size="small" style={{ marginTop: 16 }}>
        <AlertPanel />
      </Card>
    </div>
  );
}
