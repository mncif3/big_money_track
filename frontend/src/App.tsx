import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ConfigProvider, Layout, Menu } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import {
  DashboardOutlined, StockOutlined, SwapOutlined,
  AlertOutlined, SettingOutlined,
} from '@ant-design/icons'
import Dashboard from './pages/Dashboard'
import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

const { Header, Content } = Layout

const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: '看板' },
  { key: '/sectors', icon: <StockOutlined />, label: '板块' },
  { key: '/north', icon: <SwapOutlined />, label: '北向' },
  { key: '/south', icon: <SwapOutlined />, label: '南向' },
  { key: '/margin', icon: <SwapOutlined />, label: '融资融券' },
  { key: '/alerts', icon: <AlertOutlined />, label: '预警' },
  { key: '/system', icon: <SettingOutlined />, label: '系统' },
]

function AppLayout() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center', padding: '0 24px' }}>
        <div style={{ color: '#fff', fontSize: 18, fontWeight: 'bold', marginRight: 32 }}>
          🔥 CapFlow
        </div>
        <Menu
          theme="dark" mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<div style={{ padding: 24 }}><h2>预警中心 (开发中)</h2></div>} />
          <Route path="/system" element={<div style={{ padding: 24 }}><h2>系统状态 (开发中)</h2></div>} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </ConfigProvider>
  )
}
