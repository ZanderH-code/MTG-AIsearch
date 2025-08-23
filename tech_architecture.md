# 轻量化技术架构：AI万智牌搜索工具

## 推荐技术栈

### 后端：Python + FastAPI
```python
# 核心依赖
fastapi==0.104.1
uvicorn==0.24.0
openai==1.3.0
httpx==0.25.2
pydantic==2.5.0
```

### 前端：React + Vite
```bash
# 轻量级前端
npm create vite@latest mtg-ai-frontend -- --template react-ts
```

### 部署：Railway/Render (免费层)
- 自动部署
- 免费SSL证书
- 自定义域名支持

## 项目结构

```
mtg-ai-search/
├── backend/
│   ├── main.py              # FastAPI主应用
│   ├── api/
│   │   ├── search.py        # 搜索API
│   │   └── chat.py          # 对话API
│   ├── services/
│   │   ├── ai_service.py    # AI处理逻辑
│   │   └── scryfall.py      # Scryfall API调用
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## iOS发布策略

### 方案1：PWA (Progressive Web App)
**优势：**
- 无需App Store审核
- 跨平台兼容
- 可添加到主屏幕
- 离线缓存支持

**实现：**
```javascript
// manifest.json
{
  "name": "MTG AI Search",
  "short_name": "MTG AI",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [...]
}
```

### 方案2：React Native + FastAPI
**优势：**
- 原生性能
- App Store发布
- 更好的用户体验

**技术栈：**
```
前端：React Native + Expo
后端：FastAPI (部署到Railway)
状态管理：Zustand
网络请求：Axios
```

### 方案3：Flutter + FastAPI
**优势：**
- 真正的跨平台
- 优秀的性能
- 丰富的UI组件

## 轻量化实现要点

### 1. 最小化依赖
```python
# backend/requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
openai==1.3.0
httpx==0.25.2
python-dotenv==1.0.0
```

### 2. 缓存策略
```python
# 本地缓存热门搜索
from functools import lru_cache
import json

@lru_cache(maxsize=1000)
def get_cached_search(query: str):
    # 缓存常用搜索，减少API调用
    pass
```

### 3. 异步处理
```python
# 并发处理多个API请求
async def search_cards(query: str):
    async with httpx.AsyncClient() as client:
        # 并发调用AI和Scryfall API
        ai_task = process_natural_language(query)
        scryfall_task = fetch_cards(query)
        results = await asyncio.gather(ai_task, scryfall_task)
```

## 部署流程

### 1. 后端部署 (Railway)
```bash
# 1. 创建Railway项目
railway login
railway init

# 2. 设置环境变量
railway variables set OPENAI_API_KEY=your_key

# 3. 部署
railway up
```

### 2. 前端部署 (Vercel)
```bash
# 1. 构建
npm run build

# 2. 部署到Vercel
vercel --prod
```

### 3. PWA配置
```javascript
// 注册Service Worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

## 成本估算

### 免费层资源
- **Railway**: $5/月 (免费额度)
- **Vercel**: 免费 (个人项目)
- **OpenAI API**: $0.002/1K tokens
- **Scryfall API**: 完全免费

### 月成本预估
- 小规模使用: $10-20/月
- 中等规模: $50-100/月

## 开发时间线

### 第1周：MVP
- FastAPI后端基础架构
- 基础搜索功能
- 简单前端界面

### 第2周：AI集成
- OpenAI API集成
- 自然语言处理
- 错误处理

### 第3周：优化
- 缓存机制
- 性能优化
- PWA配置

### 第4周：发布
- 部署到生产环境
- 测试和调试
- 文档完善

## 总结

**Python + FastAPI** 是理想的轻量化方案：
- ✅ 开发速度快
- ✅ 部署简单
- ✅ 成本低廉
- ✅ iOS兼容性好 (PWA方案)
- ✅ 易于维护和扩展

对于iOS发布，推荐先使用PWA方案快速验证产品，后续可考虑React Native或Flutter开发原生应用。


