#!/bin/bash

# 🚀 MTG AI 搜索工具部署脚本

echo "🎴 MTG AI 搜索工具部署脚本"
echo "================================"

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

# 检查Python是否安装
if ! command -v python &> /dev/null; then
    echo "❌ Python未安装，请先安装Python"
    exit 1
fi

echo "✅ 环境检查通过"

# 创建Git仓库
echo "📦 初始化Git仓库..."
git init
git add .
git commit -m "Initial commit: MTG AI Search Tool"

echo "🌐 部署选项："
echo "1. 分离部署（推荐）- 前后端分别部署"
echo "2. 统一部署 - 使用render.yaml自动部署"
echo "3. 仅部署后端"
echo "4. 仅部署前端"

read -p "请选择部署方式 (1-4): " choice

case $choice in
    1)
        echo "🚀 开始分离部署..."
        
        # 创建后端仓库
        echo "📦 创建后端仓库..."
        cd backend
        git init
        git add .
        git commit -m "Backend: MTG AI Search API"
        echo "✅ 后端代码已准备就绪"
        echo "📝 请手动创建GitHub仓库并推送代码"
        echo "🔗 然后在Render上创建Web Service"
        
        cd ..
        
        # 创建前端仓库
        echo "📦 创建前端仓库..."
        cd frontend
        git init
        git add .
        git commit -m "Frontend: MTG AI Search UI"
        echo "✅ 前端代码已准备就绪"
        echo "📝 请手动创建GitHub仓库并推送代码"
        echo "🔗 然后在Render上创建Static Site"
        
        cd ..
        ;;
        
    2)
        echo "🚀 开始统一部署..."
        echo "📝 请将整个项目推送到GitHub"
        echo "🔗 然后在Render上使用Blueprint部署"
        echo "📄 系统会自动根据render.yaml创建服务"
        ;;
        
    3)
        echo "🚀 仅部署后端..."
        cd backend
        git init
        git add .
        git commit -m "Backend: MTG AI Search API"
        echo "✅ 后端代码已准备就绪"
        echo "📝 请手动创建GitHub仓库并推送代码"
        cd ..
        ;;
        
    4)
        echo "🚀 仅部署前端..."
        cd frontend
        git init
        git add .
        git commit -m "Frontend: MTG AI Search UI"
        echo "✅ 前端代码已准备就绪"
        echo "📝 请手动创建GitHub仓库并推送代码"
        cd ..
        ;;
        
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎉 部署准备完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在GitHub上创建仓库"
echo "2. 推送代码到GitHub"
echo "3. 在Render上创建服务"
echo "4. 配置环境变量"
echo "5. 更新域名配置"
echo ""
echo "📖 详细说明请查看 DEPLOYMENT.md"

