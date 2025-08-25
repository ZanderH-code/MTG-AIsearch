# 🎴 MTG AI 搜索工具

一个基于AI的万智牌卡牌搜索工具，支持自然语言搜索和智能排序。

## ✨ 功能特点

- **🤖 AI智能搜索**：使用自然语言描述搜索卡牌
- **🌙 深色主题**：现代化的深色界面设计
- **🌍 多语言支持**：中文和英文界面
- **📊 智能排序**：支持多种排序方式（名称、稀有度、法力值等）
- **💡 搜索示例**：提供常用搜索示例
- **🔗 直接链接**：点击卡牌直接跳转到Scryfall

## 🚀 在线体验

- **前端应用**：https://mtg-ai-frontend.onrender.com
- **后端API**：https://mtg-ai-backend.onrender.com

## 📁 项目结构

```
MTG-AIsearch/
├── mtg-ai-frontend/    # 前端项目（React/HTML/CSS/JS）
└── mtg-ai-backend/     # 后端项目（Python FastAPI）
```

## 🛠️ 技术栈

### 前端
- HTML5 + CSS3 + JavaScript
- 响应式设计
- 深色主题UI

### 后端
- Python FastAPI
- Scryfall API 集成
- OpenAI/AIHubMix API 支持

## 🔧 本地开发

### 前端开发
```bash
cd mtg-ai-frontend
# 前端是静态文件，直接打开 build/index.html 即可
```

### 后端开发
```bash
cd mtg-ai-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📖 使用示例

### 搜索示例
- "绿色生物" → 搜索绿色生物卡牌
- "红色烧牌" → 搜索红色伤害法术
- "艾斯波控制" → 搜索艾斯波色组的控制卡牌
- "力量大于4的生物" → 搜索力量大于4的生物

### 排序功能
- **按名称**：字母顺序排序
- **按稀有度**：神话 → 稀有 → 非普通 → 普通
- **按法力值**：按法术力费用排序
- **按颜色**：按颜色身份排序
- **按力量/防御力**：按生物属性排序

## 🔑 API配置

1. 访问前端应用
2. 点击"设置"按钮
3. 配置你的AI API密钥（OpenAI或AIHubMix）
4. 开始使用AI搜索功能

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**享受你的万智牌搜索体验！** 🎴✨
