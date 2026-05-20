import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ConfigProvider, Layout as AntLayout, Menu } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { antdTheme } from './theme'
import {
  DashboardOutlined, StockOutlined, SwapOutlined,
  AlertOutlined, SettingOutlined, FundOutlined,
} from '@ant-design/icons'
import Dashboard from './pages/Dashboard'
import Sectors from './pages/Sectors'
import North from './pages/North'
import South from './pages/South'
import Margin from './pages/Margin'
import Alerts from './pages/Alerts'
import System from './pages/System'
import { useNavigate, useLocation } from 'react-router-dom'

const { Header, Content } = AntLayout

const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: '看板' },
  { key: '/sectors', icon: <StockOutlined />, label: '板块' },
  { key: '/north', icon: <SwapOutlined />, label: '北向' },
  { key: '/south', icon: <SwapOutlined />, label: '南向' },
  { key: '/margin', icon: <FundOutlined />, label: '融资融券' },
  { key: '/alerts', icon: <AlertOutlined />, label: '预警' },
  { key: '/system', icon: <SettingOutlined />, label: '系统' },
]

function AppLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center', padding: '0 16px',
        background: '#161822', borderBottom: '1px solid #2a2d3a' }}>
        <div style={{ color: '#4f8cff', fontSize: 18, fontWeight: 'bold', marginRight: 24, whiteSpace: 'nowrap' }}>
          🔥 CapFlow
        </div>
        <Menu theme="dark" mode="horizontal" selectedKeys={[location.pathname]}
          items={menuItems} onClick={({ key }) => navigate(key)}
          style={{ flex: 1, minWidth: 0, background: 'transparent', borderBottom: 'none' }} />
      </Header>
      <Content style={{ padding: 16, background: '#0f1119' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sectors" element={<Sectors />} />
          <Route path="/north" element={<North />} />
          <Route path="/south" element={<South />} />
          <Route path="/margin" element={<Margin />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/system" element={<System />} />
        </Routes>
      </Content>
    </AntLayout>
  )
}

export default function App() {
  return (
    <ConfigProvider locale={zhCN} theme={antdTheme}>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </ConfigProvider>
  )
}
