# 股票交易系统

这是一个基于 Flask 的股票交易系统，提供实时股票数据、交易记录管理和客服系统。

## 部署步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
- 复制 `.env.example` 为 `.env`
- 填入你的 Supabase 配置信息

3. 运行应用：
```bash
python app.py
```

## 部署到 Render

### 使用 Render Blueprints

1. Fork 这个仓库到你的 GitHub 账号
2. 登录 [Render](https://render.com)
3. 点击 "New +" 按钮，选择 "Blueprint"
4. 连接你的 GitHub 仓库
5. 点击 "Apply" 部署

### 手动部署

1. 在 Render 上创建新的 Web Service
2. 连接你的 GitHub 仓库
3. 配置以下设置：
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. 添加环境变量：
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
5. 点击 "Create Web Service"

## 功能特点

- 实时股票数据
- 交易记录管理
- 交易策略更新
- WhatsApp 客服系统
- 响应式设计 