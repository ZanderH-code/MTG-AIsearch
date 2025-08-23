from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import List, Optional
import asyncio
from functools import lru_cache
from openai import OpenAI

app = FastAPI(title="MTG AI Search API", version="1.0.0")

# CORS配置，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # 本地开发
        "http://localhost:3000",  # 本地开发备用端口
        "https://mtg-ai-frontend.onrender.com",  # Render前端域名
        "https://your-frontend-domain.com",  # 你的自定义域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class SearchRequest(BaseModel):
    query: str
    language: str = "zh"  # 支持中文和英文
    api_key: Optional[str] = None  # 可选的API密钥
    model: Optional[str] = None  # 可选的模型名称

class ApiKeyRequest(BaseModel):
    api_key: str
    provider: str = "aihubmix"  # aihubmix 或 openai
    model: Optional[str] = None  # 可选的模型名称

class ModelListRequest(BaseModel):
    api_key: str
    provider: str = "aihubmix"

class Card(BaseModel):
    name: str
    mana_cost: Optional[str] = None
    type_line: str
    oracle_text: str
    image_uris: Optional[dict] = None
    scryfall_uri: str

class SearchResponse(BaseModel):
    cards: List[Card]
    scryfall_query: str
    total_cards: int
    api_provider: Optional[str] = None  # 显示使用的API提供商

# 缓存热门搜索
@lru_cache(maxsize=1000)
def get_cached_search(query: str):
    # 这里可以实现本地缓存逻辑
    return None

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.aihubmix_api_key = os.getenv("AIHUBMIX_API_KEY")
        # 如果没有API密钥，使用演示模式
        self.demo_mode = not (self.openai_api_key or self.aihubmix_api_key)
        if self.demo_mode:
            print("⚠️  运行在演示模式 - 使用本地关键词映射")
    
    async def natural_language_to_scryfall(self, query: str, language: str = "zh", api_key: str = None, provider: str = "aihubmix", model: str = None) -> tuple[str, str]:
        """
        将自然语言转换为Scryfall查询语法
        返回: (scryfall_query, api_provider)
        """
        
        # 中文提示词模板
        zh_prompt = f"""
你是一个万智牌专家，请将用户的中文描述转换为Scryfall搜索语法。

用户输入：{query}

请返回有效的Scryfall搜索语法，格式要求：
1. 只返回搜索语法，不要其他解释
2. 使用标准的Scryfall语法

Scryfall搜索语法参考：
- 颜色：c:g(绿) c:u(蓝) c:r(红) c:b(黑) c:w(白) c:rg(红绿) c:uw(白蓝)
- 卡牌类型：t:creature(生物) t:instant(瞬间) t:sorcery(法术) t:artifact(神器) t:enchantment(结界) t:planeswalker(鹏洛客) t:land(地)
- 卡牌文字：o:"关键词" (搜索卡牌文字中的关键词)
- 法力值：cmc<=3 (法力值小于等于3) cmc>=5 (法力值大于等于5)
- 力量/防御力：pow>=4 (力量大于等于4) tou<=2 (防御力小于等于2)
- 稀有度：r:rare(稀有) r:mythic(神话) r:common(普通)
- 组合条件：使用 AND 或空格连接多个条件
- 或条件：使用 OR 连接多个选择

示例：
- "地落卡组的强力终端" → o:"landfall" t:creature (o:"win" OR o:"end the game")
- "绿色的生物卡" → t:creature c:g
- "费用在3点以下的瞬间" → t:instant cmc<=3
- "力量大于4的红色生物" → t:creature c:r pow>=4
- "神器结界卡" → (t:artifact OR t:enchantment)
- "地落或进场触发" → (o:"landfall" OR o:"enters the battlefield")
"""

        # 英文提示词模板
        en_prompt = f"""
You are a Magic: The Gathering expert. Convert the user's description to Scryfall search syntax.

User input: {query}

Return only the valid Scryfall search syntax without any explanation.

Scryfall Search Syntax Reference:
- Colors: c:g(green) c:u(blue) c:r(red) c:b(black) c:w(white) c:rg(red-green) c:uw(white-blue)
- Card Types: t:creature t:instant t:sorcery t:artifact t:enchantment t:planeswalker t:land
- Oracle Text: o:"keyword" (search for text in card rules)
- Mana Value: cmc<=3 (mana value 3 or less) cmc>=5 (mana value 5 or more)
- Power/Toughness: pow>=4 (power 4 or more) tou<=2 (toughness 2 or less)
- Rarity: r:rare r:mythic r:common
- Combine conditions: Use AND or space to connect multiple conditions
- OR conditions: Use OR to connect multiple choices

Examples:
- "landfall finisher" → o:"landfall" t:creature (o:"win" OR o:"end the game")
- "green creatures" → t:creature c:g
- "instant spells under 3 mana" → t:instant cmc<=3
- "red creatures with power 4+" → t:creature c:r pow>=4
- "artifacts or enchantments" → (t:artifact OR t:enchantment)
- "landfall or ETB triggers" → (o:"landfall" OR o:"enters the battlefield")
"""

        prompt = zh_prompt if language == "zh" else en_prompt
        
        # 如果提供了API密钥，优先使用
        if api_key:
            try:
                return await self._call_ai_api(prompt, api_key, provider, model), provider
            except Exception as e:
                print(f"API调用失败: {e}")
                return self.fallback_mapping(query, language), "fallback"
        
        # 如果是演示模式，直接使用关键词映射
        if self.demo_mode:
            return self.fallback_mapping(query, language), "demo"
        
        # 优先使用Aihubmix API
        if self.aihubmix_api_key:
            try:
                return await self._call_ai_api(prompt, self.aihubmix_api_key, "aihubmix", model), "aihubmix"
            except Exception as e:
                print(f"Aihubmix API error: {e}")
        
        # 使用OpenAI API
        if self.openai_api_key:
            try:
                return await self._call_ai_api(prompt, self.openai_api_key, "openai", model), "openai"
            except Exception as e:
                print(f"OpenAI API error: {e}")
        
        # 如果都失败，使用本地关键词映射
        return self.fallback_mapping(query, language), "fallback"
    
    async def _call_ai_api(self, prompt: str, api_key: str, provider: str, model: str = None) -> str:
        """调用AI API"""
        if provider == "aihubmix":
            # 使用Aihubmix API
            client = OpenAI(
                api_key=api_key,
                base_url="https://aihubmix.com/v1"
            )
            model = model or "gpt-4o-mini"
        else:
            # 使用OpenAI API
            client = OpenAI(api_key=api_key)
            model = model or "gpt-3.5-turbo"
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[
                {"role": "system", "content": "You are a Magic: The Gathering expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def fallback_mapping(self, query: str, language: str) -> str:
        """简单的关键词映射作为备用方案"""
        query_lower = query.lower()
        
        # 中文关键词映射
        if language == "zh":
            if "地落" in query_lower:
                return 'o:"landfall"'
            elif "神器" in query_lower:
                return 't:artifact'
            elif "生物" in query_lower:
                return 't:creature'
            elif "瞬间" in query_lower:
                return 't:instant'
            elif "法术" in query_lower:
                return 't:sorcery'
            elif "绿色" in query_lower or "绿" in query_lower:
                return 'c:g'
            elif "蓝色" in query_lower or "蓝" in query_lower:
                return 'c:u'
            elif "红色" in query_lower or "红" in query_lower:
                return 'c:r'
            elif "黑色" in query_lower or "黑" in query_lower:
                return 'c:b'
            elif "白色" in query_lower or "白" in query_lower:
                return 'c:w'
        
        # 英文关键词映射
        else:
            if "landfall" in query_lower:
                return 'o:"landfall"'
            elif "artifact" in query_lower:
                return 't:artifact'
            elif "creature" in query_lower:
                return 't:creature'
            elif "instant" in query_lower:
                return 't:instant'
            elif "sorcery" in query_lower:
                return 't:sorcery'
            elif "green" in query_lower:
                return 'c:g'
            elif "blue" in query_lower:
                return 'c:u'
            elif "red" in query_lower:
                return 'c:r'
            elif "black" in query_lower:
                return 'c:b'
            elif "white" in query_lower:
                return 'c:w'
        
        # 默认返回空字符串，让Scryfall返回所有卡牌
        return ""

class ScryfallService:
    def __init__(self):
        self.base_url = "https://api.scryfall.com"
        # 根据Scryfall API要求设置必要的请求头
        self.headers = {
            "User-Agent": "MTG-AI-Search/1.0",
            "Accept": "application/json"
        }
    
    async def search_cards(self, query: str, page: int = 1) -> dict:
        """搜索卡牌"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/cards/search",
                    params={
                        "q": query,
                        "page": page,
                        "unique": "cards"
                    },
                    headers=self.headers,
                    timeout=30.0
                )
                
                print(f"Scryfall API 请求: {query}")
                print(f"Scryfall API 状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"找到 {result.get('total_cards', 0)} 张卡牌")
                    return result
                elif response.status_code == 404:
                    # 没有找到卡牌
                    print("没有找到匹配的卡牌")
                    return {"data": [], "total_cards": 0}
                else:
                    print(f"Scryfall API 错误: {response.status_code}")
                    raise HTTPException(status_code=response.status_code, detail="Scryfall API error")
                    
        except Exception as e:
            print(f"Scryfall API error: {e}")
            raise HTTPException(status_code=500, detail="Failed to search cards")

# 初始化服务
ai_service = AIService()
scryfall_service = ScryfallService()

@app.get("/")
async def root():
    return {"message": "MTG AI Search API", "version": "1.0.0"}

@app.post("/api/search", response_model=SearchResponse)
async def search_cards(request: SearchRequest):
    """搜索卡牌的主要API"""
    try:
        # 1. 将自然语言转换为Scryfall查询语法
        scryfall_query, api_provider = await ai_service.natural_language_to_scryfall(
            request.query, 
            request.language,
            request.api_key,
            "aihubmix" if request.api_key else "demo",
            request.model
        )
        
        if not scryfall_query:
            raise HTTPException(status_code=400, detail="无法解析搜索查询")
        
        # 2. 调用Scryfall API搜索卡牌
        scryfall_result = await scryfall_service.search_cards(scryfall_query)
        
        # 3. 转换响应格式
        cards = []
        for card_data in scryfall_result.get("data", []):
            card = Card(
                name=card_data.get("name", ""),
                mana_cost=card_data.get("mana_cost"),
                type_line=card_data.get("type_line", ""),
                oracle_text=card_data.get("oracle_text", ""),
                image_uris=card_data.get("image_uris"),
                scryfall_uri=card_data.get("scryfall_uri", "")
            )
            cards.append(card)
        
        return SearchResponse(
            cards=cards,
            scryfall_query=scryfall_query,
            total_cards=scryfall_result.get("total_cards", 0),
            api_provider=api_provider
        )
        
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="搜索失败")

@app.post("/api/validate-key")
async def validate_api_key(request: ApiKeyRequest):
    """验证API密钥"""
    try:
        # 测试API密钥是否有效
        test_prompt = "测试连接"
        if request.provider == "aihubmix":
            client = OpenAI(
                api_key=request.api_key,
                base_url="https://aihubmix.com/v1"
            )
            model = request.model or "gpt-4o-mini"
        else:
            client = OpenAI(api_key=request.api_key)
            model = request.model or "gpt-3.5-turbo"
        
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
            temperature=0.1
        )
        
        return {
            "valid": True,
            "provider": request.provider,
            "model": model,
            "message": "API密钥验证成功"
        }
        
    except Exception as e:
        return {
            "valid": False,
            "provider": request.provider,
            "message": f"API密钥验证失败: {str(e)}"
        }

@app.post("/api/models")
async def get_models(request: ModelListRequest):
    """获取可用的模型列表"""
    try:
        if request.provider == "aihubmix":
            client = OpenAI(
                api_key=request.api_key,
                base_url="https://aihubmix.com/v1"
            )
        else:
            client = OpenAI(api_key=request.api_key)
        
        # 获取模型列表
        models_response = await asyncio.to_thread(
            client.models.list
        )
        
        # 过滤出聊天模型
        chat_models = []
        for model in models_response.data:
            if model.id.startswith(('gpt-', 'claude-', 'gemini-')):
                chat_models.append({
                    "id": model.id,
                    "name": model.id,
                    "provider": request.provider
                })
        
        return {
            "success": True,
            "models": chat_models,
            "provider": request.provider
        }
        
    except Exception as e:
        # 如果获取模型列表失败，返回默认模型列表
        default_models = {
            "aihubmix": [
                {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "aihubmix"},
                {"id": "gpt-4o", "name": "GPT-4o", "provider": "aihubmix"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "aihubmix"},
                {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "provider": "aihubmix"},
                {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "aihubmix"},
                {"id": "gemini-pro", "name": "Gemini Pro", "provider": "aihubmix"}
            ],
            "openai": [
                {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "openai"},
                {"id": "gpt-4o", "name": "GPT-4o", "provider": "openai"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"}
            ]
        }
        
        return {
            "success": False,
            "models": default_models.get(request.provider, []),
            "provider": request.provider,
            "message": f"获取模型列表失败，使用默认列表: {str(e)}"
        }

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
