# 🎴 MTG AI 搜索工具

一个基于AI的万智牌卡牌搜索工具，支持自然语言查询和多种AI模型。

## ✨ 功能特点

- 🤖 **AI驱动搜索**：使用自然语言描述搜索卡牌
- 🔑 **多AI服务支持**：支持Aihubmix、OpenAI等AI服务
- 🎯 **模型选择**：动态获取和选择AI模型
- 🌐 **多语言支持**：支持中文和英文查询
- 📱 **PWA支持**：可安装为iOS应用
- 🎨 **响应式设计**：适配各种设备屏幕
- ⚡ **实时搜索**：快速获取卡牌信息

## 🚀 快速开始

### 本地开发

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/mtg-ai-search.git
   cd mtg-ai-search
   ```

2. **启动后端**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

3. **启动前端**
   ```bash
   cd frontend
   python -m http.server 8080
   ```

4. **访问应用**
   - 前端：http://localhost:8080
   - 后端API：http://localhost:8000
   - API文档：http://localhost:8000/docs

### 生产部署

使用Render一键部署：

```bash
# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

详细部署说明请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🏗️ 技术架构

### 后端技术栈
- **FastAPI**：现代、快速的Web框架
- **OpenAI**：AI服务集成
- **httpx**：异步HTTP客户端
- **Pydantic**：数据验证
- **Uvicorn**：ASGI服务器

### 前端技术栈
- **HTML5**：语义化标记
- **CSS3**：现代样式和动画
- **JavaScript ES6+**：交互逻辑
- **PWA**：渐进式Web应用

### 外部服务
- **Scryfall API**：万智牌卡牌数据
- **Aihubmix API**：AI服务（推荐）
- **OpenAI API**：AI服务

## 📖 使用指南

### 1. 配置AI服务

1. 访问登录页面
2. 选择AI服务提供商（推荐Aihubmix）
3. 输入API密钥
4. 选择AI模型
5. 验证并保存配置

### 2. 搜索卡牌

1. 在搜索框中输入自然语言描述
2. 选择语言（中文/英文）
3. 点击搜索按钮
4. 查看搜索结果

### 3. 搜索示例

**中文示例：**
- "地落卡组的强力终端"
- "绿色的生物卡"
- "费用在3点以下的瞬间"
- "力量大于4的红色生物"

**英文示例：**
- "landfall finisher"
- "green creatures"
- "instant spells under 3 mana"
- "red creatures with power 4+"

## 🔧 API接口

### 主要端点

- `POST /api/search`：搜索卡牌
- `POST /api/validate-key`：验证API密钥
- `POST /api/models`：获取模型列表
- `GET /api/health`：健康检查

### 请求示例

```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "地落卡组的强力终端",
    "language": "zh",
    "api_key": "your_api_key",
    "model": "gpt-4o-mini"
  }'
```

## 🎨 界面预览

- **登录页面**：API密钥配置界面
- **主页面**：搜索界面和结果展示
- **响应式设计**：适配手机、平板、桌面

## 🔒 安全特性

- API密钥本地存储
- CORS安全配置
- 请求验证和错误处理
- 环境变量管理

## 📱 iOS支持

### PWA安装
1. 在Safari中访问应用
2. 点击分享按钮
3. 选择"添加到主屏幕"
4. 应用将出现在主屏幕上

### 原生应用
- 支持React Native开发
- 可发布到App Store

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 🙏 致谢

- [Scryfall](https://scryfall.com/) - 万智牌卡牌数据
- [Aihubmix](https://aihubmix.com/) - AI服务支持
- [OpenAI](https://openai.com/) - AI模型服务

## 📞 支持

如有问题或建议，请：
- 提交 [Issue](../../issues)
- 发送邮件至：your-email@example.com
- 加入讨论群：[Discord链接]

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
