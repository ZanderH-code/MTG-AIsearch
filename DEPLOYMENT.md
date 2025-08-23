# 🚀 MTG AI 搜索工具部署指南

## Render 部署方案

### 方案1：分离部署（推荐）

#### 1. 后端部署

1. **创建GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/mtg-ai-backend.git
   git push -u origin main
   ```

2. **在Render上部署后端**
   - 访问 [Render Dashboard](https://dashboard.render.com/)
   - 点击 "New +" → "Web Service"
   - 连接你的GitHub仓库
   - 配置：
     - **Name**: `mtg-ai-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: `Free`

3. **设置环境变量**
   - 在Render Dashboard中找到你的服务
   - 进入 "Environment" 标签
   - 添加以下环境变量：
     ```
     OPENAI_API_KEY=your_openai_api_key
     AIHUBMIX_API_KEY=your_aihubmix_api_key
     ```

#### 2. 前端部署

1. **创建前端仓库**
   ```bash
   cd frontend
   git init
   git add .
   git commit -m "Initial frontend commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/mtg-ai-frontend.git
   git push -u origin main
   ```

2. **在Render上部署前端**
   - 访问 [Render Dashboard](https://dashboard.render.com/)
   - 点击 "New +" → "Static Site"
   - 连接你的前端GitHub仓库
   - 配置：
     - **Name**: `mtg-ai-frontend`
     - **Build Command**: `echo "Static site - no build needed"`
     - **Publish Directory**: `.` (根目录)
     - **Plan**: `Free`

### 方案2：统一部署（单仓库）

如果你想要一个仓库包含前后端：

1. **创建统一仓库结构**
   ```
   mtg-ai-app/
   ├── backend/
   │   ├── main.py
   │   ├── requirements.txt
   │   └── ...
   ├── frontend/
   │   ├── index.html
   │   ├── login.html
   │   └── ...
   ├── render.yaml
   └── README.md
   ```

2. **使用render.yaml自动部署**
   - 将整个仓库推送到GitHub
   - 在Render Dashboard中选择 "New +" → "Blueprint"
   - 连接你的仓库
   - Render会自动根据`render.yaml`创建两个服务

## 🔧 部署后配置

### 1. 更新CORS设置

部署完成后，需要更新后端的CORS配置：

```python
# 在 backend/main.py 中更新
allow_origins=[
    "http://localhost:8080",
    "https://your-frontend-domain.onrender.com",  # 你的实际前端域名
]
```

### 2. 更新前端API地址

部署完成后，需要更新前端的API地址：

```javascript
// 在 frontend/index.html 和 frontend/login.html 中更新
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? "http://localhost:8000" 
  : "https://your-backend-domain.onrender.com";  // 你的实际后端域名
```

### 3. 环境变量设置

确保在Render后端服务中设置了正确的环境变量：
- `OPENAI_API_KEY`
- `AIHUBMIX_API_KEY`

## 🌐 自定义域名

### 1. 后端自定义域名
- 在Render后端服务设置中添加自定义域名
- 更新前端代码中的API地址

### 2. 前端自定义域名
- 在Render前端服务设置中添加自定义域名
- 更新后端CORS配置

## 📱 PWA支持

为了支持iOS发布，可以添加PWA配置：

1. **创建manifest.json**
   ```json
   {
     "name": "MTG AI 搜索工具",
     "short_name": "MTG AI",
     "description": "用自然语言搜索万智牌卡牌",
     "start_url": "/",
     "display": "standalone",
     "background_color": "#667eea",
     "theme_color": "#2c3e50",
     "icons": [
       {
         "src": "icon-192.png",
         "sizes": "192x192",
         "type": "image/png"
       },
       {
         "src": "icon-512.png",
         "sizes": "512x512",
         "type": "image/png"
       }
     ]
   }
   ```

2. **添加Service Worker**
   - 创建`sw.js`文件
   - 在HTML中注册Service Worker

## 🔍 测试部署

部署完成后，测试以下功能：

1. **API健康检查**
   ```
   GET https://your-backend-domain.onrender.com/api/health
   ```

2. **前端访问**
   ```
   https://your-frontend-domain.onrender.com
   ```

3. **功能测试**
   - API密钥配置
   - 模型列表获取
   - 卡牌搜索功能

## 💡 优化建议

1. **缓存策略**
   - 添加Redis缓存热门搜索
   - 实现CDN加速静态资源

2. **监控和日志**
   - 添加错误监控
   - 实现请求日志记录

3. **安全性**
   - 添加API速率限制
   - 实现请求验证

4. **性能优化**
   - 图片懒加载
   - 代码压缩和优化
