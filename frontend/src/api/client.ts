import axios from 'axios'

const api = axios.create({ baseURL: '/api', timeout: 15000 })
export default api

export async function fetchMainThread(window: number = 20) {
  const r = await api.get('/main-thread', { params: { window } })
  return r.data
}

export async function fetchSectorRanking(period = '1w', limit = 10) {
  const r = await api.get('/sectors/ranking', { params: { period, limit } })
  return r.data
}

export async function fetchSectorTrend(code: string, period = '1m') {
  const r = await api.get(`/sectors/${code}/trend`, { params: { period } })
  return r.data
}

export async function fetchNorthSummary(period = '1m') {
  const r = await api.get('/north/summary', { params: { period } })
  return r.data
}

export async function fetchSouthSummary(period = '1m') {
  const r = await api.get('/south/summary', { params: { period } })
  return r.data
}

export async function fetchMarginSummary(period = '1m') {
  const r = await api.get('/margin/summary', { params: { period } })
  return r.data
}

export async function fetchAlerts(level?: number) {
  const r = await api.get('/alerts', { params: level ? { level } : {} })
  return r.data
}
