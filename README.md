# big_money_track — 股市资金流向监控系统

Web 看板 + 飞书预警的 A 股全市场资金流向监控。

## 快速启动

```bash
cp .env.example .env  # 填写 PG_PASSWORD 和 FEISHU_WEBHOOK
docker compose up -d --build
# 浏览器打开 http://187:6666
```

## 技术栈

- **后端**: Python 3.12 + FastAPI + SQLAlchemy 2.0 + APScheduler
- **前端**: React 18 + TypeScript + Ant Design 5 + ECharts 5
- **存储**: PostgreSQL 16 + Redis 7
- **数据源**: akshare / efinance
- **部署**: docker-compose

## 文档

- [设计方案 v1.1](./docs/设计方案_v1.1.md)
- [开发方案 v2.1](./docs/开发方案_v2.1.md)
