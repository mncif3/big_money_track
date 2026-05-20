import { Card, Typography, Row, Col } from 'antd'
import MainThreadCard from './MainThreadCard'
import SectorRankingTable from './SectorRankingTable'
import SectorTrendChart from './SectorTrendChart'
import AlertPanel from './AlertPanel'

const { Title } = Typography

export default function Dashboard() {
  return (
    <div>
      <Title level={3} style={{ color: '#e0e0e0', marginBottom: 12 }}>🔥 资金流向看板</Title>
      <MainThreadCard />
      <Row gutter={12} style={{ marginTop: 12 }}>
        <Col span={12}>
          <Card title="📊 板块资金流入 TOP10" size="small" style={{ background: '#161822', borderColor: '#2a2d3a' }}>
            <SectorRankingTable />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="📈 主线板块资金趋势" size="small" style={{ background: '#161822', borderColor: '#2a2d3a' }}>
            <SectorTrendChart />
          </Card>
        </Col>
      </Row>
      <Card title="⚠️ 最近预警" size="small" style={{ marginTop: 12, background: '#161822', borderColor: '#2a2d3a' }}>
        <AlertPanel />
      </Card>
    </div>
  )
}
