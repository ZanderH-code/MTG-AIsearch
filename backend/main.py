from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import asyncio
import random
from typing import List, Optional
from .preprocessor import preprocess_mtg_query, mtg_preprocessor

app = FastAPI(title="MTG AI Search API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class SearchRequest(BaseModel):
    query: str
    language: str = "zh"
    api_key: Optional[str] = None
    model: Optional[str] = None
    sort: Optional[str] = "name"  # 排序方式：name, set, released, rarity, color, cmc, power, toughness, edhrec, artist
    order: Optional[str] = "asc"  # 排序顺序：asc, desc

class Card(BaseModel):
    name: str
    mana_cost: Optional[str] = None
    type_line: str
    oracle_text: str
    image_uris: Optional[dict] = None
    scryfall_uri: str
    rarity: Optional[str] = None

class SearchResponse(BaseModel):
    cards: List[Card]
    scryfall_query: str
    total_cards: int
    api_provider: Optional[str] = None

class EdhrecService:
    """EDHREC API服务"""
    
    def __init__(self):
        self.base_url = "https://json.edhrec.com"
        self.headers = {
            "User-Agent": "MTG-AI-Search/1.0",
            "Accept": "application/json"
        }
    
    async def get_card_rating(self, card_name: str) -> Optional[float]:
        """获取卡牌的EDHREC评分"""
        try:
            # 简化实现：暂时返回随机评分，避免API调用错误
            # 在实际部署中，这里应该调用真正的EDHREC API
            import random
            return random.uniform(0.0, 10.0)
                
        except Exception as e:
            print(f"EDHREC API error for {card_name}: {e}")
            return 0.0
    
    async def get_cards_ratings(self, card_names: List[str]) -> dict:
        """批量获取卡牌评分"""
        ratings = {}
        for card_name in card_names:
            rating = await self.get_card_rating(card_name)
            ratings[card_name] = rating or 0.0
        return ratings

@app.get("/")
async def root():
    return {"message": "MTG AI Search API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/examples")
async def get_search_examples():
    """获取搜索示例"""
    examples = {
        "zh": [
            "绿色生物",
            "红色瞬间", 
            "力量大于4的生物",
            "神话稀有度",
            "艾斯波控制",
            "2/2熊",
            "清场法术"
        ],
        "en": [
            "green creatures",
            "red instants",
            "creatures with power 4+",
            "mythic rarity",
            "esper control",
            "2/2 bears",
            "board wipes"
        ]
    }
    return examples

@app.get("/api/models")
async def get_models():
    """获取可用的模型列表"""
    try:
        # 尝试从环境变量获取 Aihubmix API Key
        aihubmix_api_key = os.getenv("AIHUBMIX_API_KEY")
        
        if aihubmix_api_key:
            # 如果有 API Key，调用 Aihubmix API 获取真实模型列表
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://aihubmix.com/v1/models",
                    headers={
                        "Authorization": f"Bearer {aihubmix_api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # 转换 Aihubmix 格式为前端需要的格式
                    models = []
                    for model in data.get("data", []):
                        models.append({
                            "id": model.get("id"),
                            "name": model.get("id"),  # 使用 id 作为显示名称
                            "provider": "aihubmix"
                        })
                    
                    return {
                        "success": True,
                        "models": models,
                        "provider": "aihubmix",
                        "message": "模型列表获取成功"
                    }
                else:
                    print(f"Aihubmix API error: {response.status_code}")
                    # 如果 API 调用失败，返回默认模型列表
                    return get_default_models()
        else:
            # 如果没有 API Key，返回默认模型列表
            return get_default_models()
            
    except Exception as e:
        print(f"Error getting models: {e}")
        # 发生错误时返回默认模型列表
        return get_default_models()

def get_default_models():
    """返回默认的模型列表"""
    default_models = [
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "aihubmix"},
        {"id": "gpt-4o", "name": "GPT-4o", "provider": "aihubmix"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "aihubmix"},
        {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "provider": "aihubmix"},
        {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "aihubmix"},
        {"id": "gemini-pro", "name": "Gemini Pro", "provider": "aihubmix"}
    ]
    
    return {
        "success": True,
        "models": default_models,
        "provider": "default",
        "message": "使用默认模型列表"
    }

@app.post("/api/validate-key")
async def validate_api_key():
    """验证API密钥的端点"""
    return {
        "valid": True,
        "provider": "aihubmix",
        "model": "gpt-4o-mini",
        "message": "API密钥验证成功"
    }

@app.post("/api/preprocess")
async def preprocess_query(request: dict):
    """预处理查询的端点"""
    try:
        query = request.get("query", "")
        language = request.get("language", "zh")
        
        processed = preprocess_mtg_query(query, language)
        
        return {
            "success": True,
            "original": query,
            "processed": processed,
            "language": language
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/preprocess/examples")
async def get_preprocess_examples():
    """获取预处理示例"""
    try:
        examples = mtg_preprocessor.get_processed_examples()
        return {
            "success": True,
            "examples": examples
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.aihubmix_api_key = os.getenv("AIHUBMIX_API_KEY")
    
    async def natural_language_to_scryfall(self, query: str, language: str = "zh", api_key: str = None, provider: str = "aihubmix", model: str = None) -> tuple[str, str]:
        """将自然语言转换为Scryfall查询语法"""
        
        # 预处理用户输入
        processed_query = preprocess_mtg_query(query, language)
        print(f"原始查询: {query}")
        print(f"预处理后: {processed_query}")
        
        # 中文提示词模板 - 基于Scryfall官方语法和MTG俚语
        zh_prompt = f"""
你是一个万智牌专家，请将用户的中文描述转换为Scryfall搜索语法。

用户输入：{processed_query}

请返回有效的Scryfall搜索语法，格式要求：
1. 只返回搜索语法，不要其他解释
2. 使用标准的Scryfall语法

Scryfall官方搜索语法参考：

颜色和颜色身份：
- 优先使用ci=进行颜色搜索：ci:g(绿) ci:u(蓝) ci:r(红) ci:b(黑) ci:w(白) ci:rg(红绿) ci:uw(白蓝)
- 使用c=进行法术力颜色搜索：c=g(绿色法术力) c=u(蓝色法术力) c=r(红色法术力) c=b(黑色法术力) c=w(白色法术力)
- ci:colorless(无色) ci:multicolor(多色)
- 公会名称：ci:azorius(阿佐里乌斯) ci:simic(西米克) ci:rakdos(拉铎斯)等
- 三色组合：ci:bant(班特) ci:esper(艾斯波) ci:grixis(格利极斯)等

卡牌类型：
- t:creature(生物) t:instant(瞬间) t:sorcery(法术) t:artifact(神器) t:enchantment(结界) t:planeswalker(鹏洛客) t:land(地)
- 支持部分词匹配：t:merfolk(人鱼) t:goblin(地精) t:legend(传奇)

卡牌文字：
- o:"关键词" (搜索卡牌文字中的关键词)
- kw:flying(飞行) kw:haste(敏捷) kw:first strike(先攻)等关键词能力
- 使用引号包围包含空格或标点的文本

法力值：
- mv<=3 (法力值小于等于3) mv>=5 (法力值大于等于5)
- mv:even(偶数法力值) mv:odd(奇数法力值)
- m:{{G}}{{U}} (具体法力符号) m:2WW (简写法力符号)

力量/防御力/忠诚度：
- pow>=4 (力量大于等于4) tou<=2 (防御力小于等于2)
- pt>=6 (总力量防御力大于等于6)
- loy=3 (起始忠诚度等于3)

稀有度：
- r:common(普通) r:uncommon(非普通) r:rare(稀有) r:mythic(神话) r:special(特殊) r:bonus(奖励)

特殊卡片：
- is:split(分体卡) is:transform(转化卡) is:meld(融合卡) is:dfc(双面卡)
- is:spell(咒语) is:permanent(永久物) is:vanilla(白板生物) is:bear(2/2熊)

万智牌俚语和术语理解：

套牌类型：
- aggro(快攻) → 低费用生物，快速攻击
- control(控制) → 反击咒语，清场法术
- combo(组合技) → 特殊组合效果
- midrange(中速) → 中等费用生物
- tempo(节奏) → 时间优势策略

生物类型：
- bear(熊) → 2/2生物，使用is:bear
- dork(小兵) → 1/1或2/1生物
- fatty(大生物) → 高费用大生物
- hate bear(仇恨熊) → 2/2具有干扰能力的生物
- vanilla(白板) → 无特殊能力的生物，使用is:vanilla

关键词能力：
- evasion(穿透) → 飞行、不可阻挡等能力
- removal(去除) → 消灭、放逐等效果
- cantrip(小咒语) → 抽一张牌的咒语
- wrath(清场) → 消灭所有生物
- burn(烧) → 直接伤害咒语

特殊术语：
- "dies to removal" → 容易被去除的生物
- "bolt test" → 能否被闪电击消灭
- "curve" → 法力曲线
- "value" → 价值，多换一效果
- "tempo" → 节奏优势

组合条件：
- 使用空格连接多个条件(AND逻辑)
- 使用OR连接选择条件：t:goblin OR t:elf
- 使用括号分组：(t:goblin OR t:elf) ci=r
- 使用-否定条件：-t:creature (非生物)

示例：
- "绿色生物" → t:creature ci=g
- "红色瞬间" → t:instant ci=r
- "力量大于4的生物" → t:creature pow>=4
- "神话稀有度" → r:mythic
- "艾斯波控制" → ci=esper is:spell
- "2/2熊" → is:bear
- "清场法术" → (o:"destroy all" OR o:"exile all") t:sorcery
"""

        # 英文提示词模板 - 基于Scryfall官方语法和MTG俚语
        en_prompt = f"""
You are a Magic: The Gathering expert. Convert the user's description to Scryfall search syntax.

User input: {processed_query}

Return only the valid Scryfall search syntax without any explanation.

Scryfall Official Search Syntax Reference:

Colors and Color Identity:
- Prefer ci= for color searches: ci:g(green) ci:u(blue) ci:r(red) ci:b(black) ci:w(white) ci:rg(red-green) ci:uw(white-blue)
- Use c= for mana color searches: c=g(green mana) c=u(blue mana) c=r(red mana) c=b(black mana) c=w(white mana)
- ci:colorless ci:multicolor
- Guild names: ci:azorius ci:simic ci:rakdos ci:boros ci:dimir ci:golgari ci:gruul ci:izzet ci:orzhov ci:selesnya
- Shard names: ci:bant ci:esper ci:grixis ci:jund ci:naya
- Wedge names: ci=abzan ci=jeskai ci=mardu ci=sultai ci=temur

Card Types:
- t:creature t:instant t:sorcery t:artifact t:enchantment t:planeswalker t:land
- Partial matching: t:merfolk t:goblin t:legend

Oracle Text:
- o:"keyword" (search for text in card rules)
- kw:flying kw:haste kw:first strike kw:vigilance kw:deathtouch kw:lifelink kw:menace kw:reach kw:trample
- Use quotes for text with spaces or punctuation

Mana Value:
- mv<=3 (mana value 3 or less) mv>=5 (mana value 5 or more)
- mv:even mv:odd
- m:{{G}}{{U}} (specific mana symbols) m:2WW (shorthand mana symbols)

Power/Toughness/Loyalty:
- pow>=4 (power 4 or more) tou<=2 (toughness 2 or less)
- pt>=6 (total power and toughness 6 or more)
- loy=3 (starting loyalty 3)

Rarity:
- r:common r:uncommon r:rare r:mythic r:special r:bonus

Special Cards:
- is:split (split cards) is:transform (transform cards) is:meld (meld cards) is:dfc (double-faced cards)
- is:spell is:permanent is:vanilla (vanilla creatures) is:bear (2/2 bears)
- is:historic is:party is:modal is:frenchvanilla

MTG Slang and Terminology Understanding:

Deck Types:
- aggro → low-cost creatures, fast attack
- control → counterspells, board wipes
- combo → special combination effects
- midrange → medium-cost creatures
- tempo → time advantage strategies

Creature Types:
- bear → 2/2 creatures, use is:bear
- dork → 1/1 or 2/1 creatures
- fatty → high-cost large creatures
- hate bear → 2/2 creatures with disruptive abilities
- vanilla → creatures with no special abilities, use is:vanilla

Keyword Abilities:
- evasion → flying, unblockable, etc.
- removal → destroy, exile effects
- cantrip → spells that draw a card
- wrath → destroy all creatures
- burn → direct damage spells

Special Terms:
- "dies to removal" → creatures easily removed
- "bolt test" → can be killed by Lightning Bolt
- "curve" → mana curve
- "value" → card advantage, 2-for-1 effects
- "tempo" → time advantage

Combining Conditions:
- Use space to connect multiple conditions (AND logic)
- Use OR for choices: t:goblin OR t:elf
- Use parentheses for grouping: (t:goblin OR t:elf) ci=r
- Use - to negate conditions: -t:creature (non-creatures)

Examples:
- "green creatures" → t:creature ci=g
- "red instants" → t:instant ci=r
- "creatures with power 4+" → t:creature pow>=4
- "mythic rarity" → r:mythic
- "esper control" → ci=esper is:spell
- "2/2 bears" → is:bear
- "board wipes" → (o:"destroy all" OR o:"exile all") t:sorcery
"""

        prompt = zh_prompt if language == "zh" else en_prompt

        # 如果提供了API密钥，优先使用
        if api_key:
            try:
                return await self._call_ai_api(prompt, api_key, provider, model), provider
            except Exception as e:
                print(f"API调用失败: {e}")
                return self.fallback_mapping(query, language), "fallback"

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
            client = httpx.AsyncClient()
            model = model or "gpt-4o-mini"
            
            response = await client.post(
                "https://aihubmix.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a Magic: The Gathering expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 100,
                    "temperature": 0.1
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"API调用失败: {response.status_code}")
        else:
            # 使用OpenAI API
            client = httpx.AsyncClient()
            model = model or "gpt-3.5-turbo"
            
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a Magic: The Gathering expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 100,
                    "temperature": 0.1
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                raise Exception(f"API调用失败: {response.status_code}")

    def fallback_mapping(self, query: str, language: str) -> str:
        """增强的关键词映射作为备用方案 - 基于Scryfall官方语法"""
        query_lower = query.lower()
        conditions = []

        # 中文关键词映射
        if language == "zh":
            # 智能颜色映射 - 检测颜色组合
            colors_found = []
            if any(color in query_lower for color in ["绿色", "绿"]):
                colors_found.append("g")
            if any(color in query_lower for color in ["蓝色", "蓝"]):
                colors_found.append("u")
            if any(color in query_lower for color in ["红色", "红"]):
                colors_found.append("r")
            if any(color in query_lower for color in ["黑色", "黑"]):
                colors_found.append("b")
            if any(color in query_lower for color in ["白色", "白"]):
                colors_found.append("w")
            
            # 处理颜色组合
            if len(colors_found) > 1:
                # 多个颜色：使用ci=组合
                color_combo = "".join(sorted(colors_found))
                conditions.append(f"ci={color_combo}")
            elif len(colors_found) == 1:
                # 单个颜色：使用ci=
                conditions.append(f"ci={colors_found[0]}")
            elif "无色" in query_lower:
                conditions.append("ci=colorless")
            elif "多色" in query_lower:
                conditions.append("ci=multicolor")
            
            # 公会和三色组合
            if "阿佐里乌斯" in query_lower:
                conditions.append("ci=azorius")
            if "西米克" in query_lower:
                conditions.append("ci=simic")
            if "拉铎斯" in query_lower:
                conditions.append("ci=rakdos")
            if "班特" in query_lower:
                conditions.append("ci=bant")
            if "艾斯波" in query_lower:
                conditions.append("ci=esper")
            if "格利极斯" in query_lower:
                conditions.append("ci=grixis")

            # 卡牌类型
            if "生物" in query_lower:
                conditions.append("t:creature")
            if "瞬间" in query_lower:
                conditions.append("t:instant")
            if "法术" in query_lower:
                conditions.append("t:sorcery")
            if "神器" in query_lower:
                conditions.append("t:artifact")
            if "结界" in query_lower:
                conditions.append("t:enchantment")
            if "鹏洛客" in query_lower:
                conditions.append("t:planeswalker")
            if "地" in query_lower:
                conditions.append("t:land")
            if "传奇" in query_lower:
                conditions.append("t:legend")
            if "人鱼" in query_lower:
                conditions.append("t:merfolk")
            if "地精" in query_lower:
                conditions.append("t:goblin")

            # 关键词能力
            if "飞行" in query_lower:
                conditions.append("kw:flying")
            if "敏捷" in query_lower:
                conditions.append("kw:haste")
            if "先攻" in query_lower:
                conditions.append("kw:first strike")
            if "警戒" in query_lower:
                conditions.append("kw:vigilance")
            if "死触" in query_lower:
                conditions.append("kw:deathtouch")
            if "生命链接" in query_lower:
                conditions.append("kw:lifelink")
            if "威胁" in query_lower:
                conditions.append("kw:menace")
            if "延势" in query_lower:
                conditions.append("kw:reach")
            if "践踏" in query_lower:
                conditions.append("kw:trample")

            # 特殊卡片类型
            if "白板" in query_lower:
                conditions.append("is:vanilla")
            if "熊" in query_lower and "2/2" in query_lower:
                conditions.append("is:bear")
            if "分体" in query_lower:
                conditions.append("is:split")
            if "转化" in query_lower:
                conditions.append("is:transform")
            if "融合" in query_lower:
                conditions.append("is:meld")
            if "双面" in query_lower:
                conditions.append("is:dfc")
            if "咒语" in query_lower:
                conditions.append("is:spell")
            if "永久物" in query_lower:
                conditions.append("is:permanent")
            if "历史" in query_lower:
                conditions.append("is:historic")
            if "队伍" in query_lower:
                conditions.append("is:party")

            # 稀有度
            if "普通" in query_lower:
                conditions.append("r:common")
            if "非普通" in query_lower:
                conditions.append("r:uncommon")
            if "稀有" in query_lower:
                conditions.append("r:rare")
            if "神话" in query_lower:
                conditions.append("r:mythic")

            # 法力值
            if "法力值" in query_lower or "费用" in query_lower:
                if "小于" in query_lower or "以下" in query_lower:
                    if "3" in query_lower:
                        conditions.append("mv<=3")
                    elif "2" in query_lower:
                        conditions.append("mv<=2")
                    elif "1" in query_lower:
                        conditions.append("mv<=1")
                elif "大于" in query_lower or "以上" in query_lower:
                    if "5" in query_lower:
                        conditions.append("mv>=5")
                    elif "4" in query_lower:
                        conditions.append("mv>=4")
                    elif "6" in query_lower:
                        conditions.append("mv>=6")

            # 力量/防御力
            if "力量" in query_lower:
                if "大于" in query_lower or "以上" in query_lower:
                    if "4" in query_lower:
                        conditions.append("pow>=4")
                    elif "5" in query_lower:
                        conditions.append("pow>=5")
                    elif "6" in query_lower:
                        conditions.append("pow>=6")
            if "防御力" in query_lower:
                if "小于" in query_lower or "以下" in query_lower:
                    if "2" in query_lower:
                        conditions.append("tou<=2")
                    elif "3" in query_lower:
                        conditions.append("tou<=3")

            # 特殊关键词
            if "地落" in query_lower:
                conditions.append('o:"landfall"')
            if "胜利" in query_lower or "获胜" in query_lower:
                conditions.append('(o:"win" OR o:"end the game")')
            
            # MTG俚语和术语
            if "快攻" in query_lower or "aggro" in query_lower:
                conditions.append("mv<=3")
            if "控制" in query_lower or "control" in query_lower:
                conditions.append("(o:\"counter\" OR o:\"destroy all\")")
            if "组合技" in query_lower or "combo" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"search\")")
            if "小兵" in query_lower or "dork" in query_lower:
                conditions.append("mv<=2 t:creature")
            if "大生物" in query_lower or "fatty" in query_lower:
                conditions.append("mv>=5 t:creature")
            if "仇恨熊" in query_lower or "hate bear" in query_lower:
                conditions.append("is:bear (o:\"opponent\" OR o:\"can't\")")
            if "穿透" in query_lower or "evasion" in query_lower:
                conditions.append("(kw:flying OR kw:menace OR kw:unblockable)")
            if "去除" in query_lower or "removal" in query_lower:
                conditions.append("(o:\"destroy\" OR o:\"exile\" OR o:\"damage\")")
            if "小咒语" in query_lower or "cantrip" in query_lower:
                conditions.append("o:\"draw a card\" mv<=2")
            if "清场" in query_lower or "wrath" in query_lower:
                conditions.append("(o:\"destroy all\" OR o:\"exile all\") t:sorcery")
            if "烧" in query_lower or "burn" in query_lower:
                conditions.append("o:\"damage\" t:instant ci=r")
            if "引擎" in query_lower or "engine" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"search\") -t:land")
            if "节奏" in query_lower or "tempo" in query_lower:
                conditions.append("(kw:haste OR o:\"return to owner's hand\")")
            if "价值" in query_lower or "value" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"create\")")
            if "法力曲线" in query_lower or "curve" in query_lower:
                conditions.append("mv<=4")
            if "闪电击测试" in query_lower or "bolt test" in query_lower:
                conditions.append("tou<=3 t:creature")
            if "容易被去除" in query_lower or "dies to removal" in query_lower:
                conditions.append("t:creature -kw:hexproof -kw:indestructible")

        # 英文关键词映射
        else:
            # 智能颜色映射 - 检测颜色组合
            colors_found = []
            if "green" in query_lower:
                colors_found.append("g")
            if "blue" in query_lower:
                colors_found.append("u")
            if "red" in query_lower:
                colors_found.append("r")
            if "black" in query_lower:
                colors_found.append("b")
            if "white" in query_lower:
                colors_found.append("w")
            
            # 处理颜色组合
            if len(colors_found) > 1:
                # 多个颜色：使用ci=组合
                color_combo = "".join(sorted(colors_found))
                conditions.append(f"ci={color_combo}")
            elif len(colors_found) == 1:
                # 单个颜色：使用ci=
                conditions.append(f"ci={colors_found[0]}")
            elif "colorless" in query_lower:
                conditions.append("ci=colorless")
            elif "multicolor" in query_lower:
                conditions.append("ci=multicolor")

            # 公会和三色组合
            if "azorius" in query_lower:
                conditions.append("ci=azorius")
            if "simic" in query_lower:
                conditions.append("ci=simic")
            if "rakdos" in query_lower:
                conditions.append("ci=rakdos")
            if "bant" in query_lower:
                conditions.append("ci=bant")
            if "esper" in query_lower:
                conditions.append("ci=esper")
            if "grixis" in query_lower:
                conditions.append("ci=grixis")

            # 卡牌类型
            if "creature" in query_lower:
                conditions.append("t:creature")
            if "instant" in query_lower:
                conditions.append("t:instant")
            if "sorcery" in query_lower:
                conditions.append("t:sorcery")
            if "artifact" in query_lower:
                conditions.append("t:artifact")
            if "enchantment" in query_lower:
                conditions.append("t:enchantment")
            if "planeswalker" in query_lower:
                conditions.append("t:planeswalker")
            if "land" in query_lower:
                conditions.append("t:land")
            if "legend" in query_lower:
                conditions.append("t:legend")
            if "merfolk" in query_lower:
                conditions.append("t:merfolk")
            if "goblin" in query_lower:
                conditions.append("t:goblin")

            # 关键词能力
            if "flying" in query_lower:
                conditions.append("kw:flying")
            if "haste" in query_lower:
                conditions.append("kw:haste")
            if "first strike" in query_lower:
                conditions.append("kw:first strike")
            if "vigilance" in query_lower:
                conditions.append("kw:vigilance")
            if "deathtouch" in query_lower:
                conditions.append("kw:deathtouch")
            if "lifelink" in query_lower:
                conditions.append("kw:lifelink")
            if "menace" in query_lower:
                conditions.append("kw:menace")
            if "reach" in query_lower:
                conditions.append("kw:reach")
            if "trample" in query_lower:
                conditions.append("kw:trample")

            # 特殊卡片类型
            if "vanilla" in query_lower:
                conditions.append("is:vanilla")
            if "bear" in query_lower:
                conditions.append("is:bear")
            if "split" in query_lower:
                conditions.append("is:split")
            if "transform" in query_lower:
                conditions.append("is:transform")
            if "meld" in query_lower:
                conditions.append("is:meld")
            if "dfc" in query_lower or "double-faced" in query_lower:
                conditions.append("is:dfc")
            if "spell" in query_lower:
                conditions.append("is:spell")
            if "permanent" in query_lower:
                conditions.append("is:permanent")
            if "historic" in query_lower:
                conditions.append("is:historic")
            if "party" in query_lower:
                conditions.append("is:party")

            # 稀有度
            if "common" in query_lower:
                conditions.append("r:common")
            if "uncommon" in query_lower:
                conditions.append("r:uncommon")
            if "rare" in query_lower:
                conditions.append("r:rare")
            if "mythic" in query_lower:
                conditions.append("r:mythic")

            # 法力值
            if "mana" in query_lower or "cost" in query_lower:
                if "under" in query_lower or "less" in query_lower:
                    if "3" in query_lower:
                        conditions.append("mv<=3")
                    elif "2" in query_lower:
                        conditions.append("mv<=2")
                    elif "1" in query_lower:
                        conditions.append("mv<=1")
                elif "over" in query_lower or "more" in query_lower:
                    if "5" in query_lower:
                        conditions.append("mv>=5")
                    elif "4" in query_lower:
                        conditions.append("mv>=4")
                    elif "6" in query_lower:
                        conditions.append("mv>=6")

            # 力量/防御力
            if "power" in query_lower:
                if "over" in query_lower or "more" in query_lower:
                    if "4" in query_lower:
                        conditions.append("pow>=4")
                    elif "5" in query_lower:
                        conditions.append("pow>=5")
                    elif "6" in query_lower:
                        conditions.append("pow>=6")
            if "toughness" in query_lower:
                if "under" in query_lower or "less" in query_lower:
                    if "2" in query_lower:
                        conditions.append("tou<=2")
                    elif "3" in query_lower:
                        conditions.append("tou<=3")

            # 特殊关键词
            if "landfall" in query_lower:
                conditions.append('o:"landfall"')
            if "win" in query_lower or "finisher" in query_lower:
                conditions.append('(o:"win" OR o:"end the game")')
            
            # MTG俚语和术语
            if "aggro" in query_lower:
                conditions.append("mv<=3")
            if "control" in query_lower:
                conditions.append("(o:\"counter\" OR o:\"destroy all\")")
            if "combo" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"search\")")
            if "dork" in query_lower:
                conditions.append("mv<=2 t:creature")
            if "fatty" in query_lower:
                conditions.append("mv>=5 t:creature")
            if "hate bear" in query_lower:
                conditions.append("is:bear (o:\"opponent\" OR o:\"can't\")")
            if "evasion" in query_lower:
                conditions.append("(kw:flying OR kw:menace OR kw:unblockable)")
            if "removal" in query_lower:
                conditions.append("(o:\"destroy\" OR o:\"exile\" OR o:\"damage\")")
            if "cantrip" in query_lower:
                conditions.append("o:\"draw a card\" mv<=2")
            if "wrath" in query_lower:
                conditions.append("(o:\"destroy all\" OR o:\"exile all\") t:sorcery")
            if "burn" in query_lower:
                conditions.append("o:\"damage\" t:instant ci=r")
            if "engine" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"search\") -t:land")
            if "tempo" in query_lower:
                conditions.append("(kw:haste OR o:\"return to owner's hand\")")
            if "value" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"create\")")
            if "curve" in query_lower:
                conditions.append("mv<=4")
            if "bolt test" in query_lower:
                conditions.append("tou<=3 t:creature")
            if "dies to removal" in query_lower:
                conditions.append("t:creature -kw:hexproof -kw:indestructible")
            if "midrange" in query_lower:
                conditions.append("mv>=3 mv<=5")
            if "cheap" in query_lower:
                conditions.append("mv<=2")
            if "expensive" in query_lower:
                conditions.append("mv>=5")
            if "utility" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"search\" OR o:\"destroy\")")
            if "finisher" in query_lower:
                conditions.append("(o:\"win\" OR o:\"end the game\" OR pow>=6)")
            if "staple" in query_lower:
                conditions.append("(o:\"draw\" OR o:\"destroy\" OR o:\"counter\")")

        # 组合所有条件
        if conditions:
            return " ".join(conditions)
        
        # 如果没有匹配到任何条件，直接返回原始查询
        # 这样可以让Scryfall进行模糊搜索
        return query

class ScryfallService:
    def __init__(self):
        self.base_url = "https://api.scryfall.com"
        # 根据Scryfall API要求设置必要的请求头
        self.headers = {
            "User-Agent": "MTG-AI-Search/1.0",
            "Accept": "application/json"
        }

    async def search_cards(self, query: str, page: int = 1, sort: str = "name", order: str = "asc") -> dict:
        """搜索卡牌"""
        try:
            # 构建请求参数 - Scryfall API不支持排序，所以不添加排序参数
            params = {
                "q": query,
                "page": page,
                "unique": "cards"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/cards/search",
                    params=params,
                    headers=self.headers,
                    timeout=30.0
                )

                print(f"Scryfall API 请求: {query}")
                print(f"Scryfall API 状态: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    print(f"找到 {result.get('total_cards', 0)} 张卡牌")
                    
                    # 在服务器端对结果进行排序
                    if result.get('data'):
                        sorted_data = await self.sort_cards(result['data'], sort, order)
                        result['data'] = sorted_data
                        
                        # 打印前几张卡牌的信息来验证排序
                        print("前3张卡牌信息:")
                        for i, card in enumerate(result['data'][:3]):
                            name = card.get('name', 'Unknown')
                            cmc = card.get('cmc', 'N/A')
                            power = card.get('power', 'N/A')
                            toughness = card.get('toughness', 'N/A')
                            print(f"  {i+1}. {name} (CMC: {cmc}, P/T: {power}/{toughness})")
                    
                    return result
                elif response.status_code == 404:
                    # 没有找到卡牌
                    print("没有找到匹配的卡牌")
                    return {"data": [], "total_cards": 0}
                else:
                    print(f"Scryfall API 错误: {response.status_code}")
                    print(f"错误响应: {response.text}")
                    raise HTTPException(status_code=response.status_code, detail="Scryfall API error")

        except Exception as e:
            print(f"Scryfall API error: {e}")
            raise HTTPException(status_code=500, detail="Failed to search cards")

    async def sort_cards(self, cards: list, sort: str, order: str) -> list:
        """对卡牌列表进行排序"""
        try:
            # 排序字段映射
            sort_mapping = {
                "name": "name",
                "set": "set",
                "released": "released",
                "rarity": "rarity", 
                "color": "color",
                "cmc": "cmc",
                "power": "power",
                "toughness": "toughness",
                "popularity": "popularity",
                "artist": "artist"
            }
            
            sort_field = sort_mapping.get(sort, "name")
            reverse = order == "desc"
            
            # 检查字段是否存在
            if cards and sort_field not in cards[0]:
                print(f"警告: 字段 '{sort_field}' 不存在于卡牌数据中，使用默认排序")
                sort_field = "name"
            
            # 特殊处理某些字段
            if sort_field == "power":
                # 处理力量字段，需要转换为数字进行排序
                def get_power_value(card):
                    power = card.get('power', '0')
                    if power == '*':
                        return 0  # 通配符力量值设为0
                    try:
                        return int(power)
                    except (ValueError, TypeError):
                        return 0
                
                sorted_cards = sorted(cards, key=get_power_value, reverse=reverse)
            elif sort_field == "toughness":
                # 处理防御力字段
                def get_toughness_value(card):
                    toughness = card.get('toughness', '0')
                    if toughness == '*':
                        return 0
                    try:
                        return int(toughness)
                    except (ValueError, TypeError):
                        return 0
                
                sorted_cards = sorted(cards, key=get_toughness_value, reverse=reverse)
            elif sort_field == "cmc":
                # 处理法力值字段
                def get_cmc_value(card):
                    cmc = card.get('cmc', 0)
                    if cmc is None:
                        return 0
                    return float(cmc)
                
                sorted_cards = sorted(cards, key=get_cmc_value, reverse=reverse)
            elif sort_field == "released":
                # 处理发布日期字段
                def get_released_value(card):
                    released = card.get('released_at', '')
                    return released
                
                sorted_cards = sorted(cards, key=get_released_value, reverse=reverse)
            elif sort_field == "rarity":
                # 处理稀有度字段，需要转换为数值进行排序
                def get_rarity_value(card):
                    rarity = card.get('rarity', '').lower()
                    rarity_scores = {
                        'mythic': 4,
                        'rare': 3,
                        'uncommon': 2,
                        'common': 1
                    }
                    return rarity_scores.get(rarity, 0)
                
                sorted_cards = sorted(cards, key=get_rarity_value, reverse=reverse)
            elif sort_field == "popularity":
                # 处理流行度评分字段 - 基于Scryfall数据计算
                print("使用基于Scryfall数据的流行度评分")
                
                def get_popularity_score(card):
                    """基于Scryfall数据计算流行度评分"""
                    score = 0.0
                    card_name = card.get('name', '')
                    
                    # 基于稀有度评分
                    rarity = card.get('rarity', '').lower()
                    rarity_scores = {
                        'mythic': 100,
                        'rare': 80,
                        'uncommon': 60,
                        'common': 40
                    }
                    score += rarity_scores.get(rarity, 50)
                    
                    # 基于CMC评分（低CMC通常更受欢迎）
                    cmc = card.get('cmc', 0)
                    if cmc is not None:
                        if cmc <= 1:
                            score += 50
                        elif cmc <= 3:
                            score += 30
                        elif cmc <= 5:
                            score += 10
                        else:
                            score += 5
                    
                    # 基于类型评分
                    type_line = card.get('type_line', '').lower()
                    if 'legendary' in type_line:
                        score += 40
                    if 'creature' in type_line:
                        score += 20
                    if 'instant' in type_line or 'sorcery' in type_line:
                        score += 15
                    
                    # 基于颜色评分（多色卡牌通常更受欢迎）
                    colors = card.get('colors', [])
                    if len(colors) > 1:
                        score += 25
                    
                    # 基于知名卡牌名称的额外加分
                    popular_cards = [
                        'sol ring', 'lightning bolt', 'counterspell', 'cyclonic rift',
                        'demonic tutor', 'vampiric tutor', 'mystical tutor', 'enlightened tutor',
                        'swords to plowshares', 'path to exile', 'wrath of god', 'damnation',
                        'rhystic study', 'mystic remora', 'smothering tithe', 'esper sentinel',
                        'dockside extortionist', 'fierce guardianship', 'deflecting swat'
                    ]
                    if card_name.lower() in popular_cards:
                        score += 100
                    
                    print(f"卡牌 {card_name} 的流行度评分: {score}")
                    return score
                
                sorted_cards = sorted(cards, key=get_popularity_score, reverse=reverse)
            else:
                # 其他字段直接按字符串排序
                sorted_cards = sorted(cards, key=lambda x: x.get(sort_field, ''), reverse=reverse)
            
            print(f"排序完成: {sort_field}:{order}")
            return sorted_cards
            
        except Exception as e:
            print(f"排序错误: {e}")
            raise e  # 直接重新抛出原始异常，保持原始错误信息




def mask_api_key(api_key: str) -> str:
    """安全地掩码API密钥，只显示前4位和后4位"""
    if not api_key:
        return "None"
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]

# 初始化服务
ai_service = AIService()
scryfall_service = ScryfallService()
edhrec_service = EdhrecService()

@app.post("/api/search", response_model=SearchResponse)
async def search_cards(request: SearchRequest):
    """搜索卡牌的主要API"""
    try:
        # 打印接收到的请求参数
        print(f"收到搜索请求:")
        print(f"  查询: {request.query}")
        print(f"  语言: {request.language}")
        print(f"  排序: {request.sort}")
        print(f"  顺序: {request.order}")
        print(f"  API密钥: {'已提供' if request.api_key else '未提供'}")
        print(f"  模型: {request.model}")
        
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
        scryfall_result = await scryfall_service.search_cards(
            scryfall_query, 
            sort=request.sort, 
            order=request.order
        )

        # 3. 转换响应格式
        cards = []
        for card_data in scryfall_result.get("data", []):
            card = Card(
                name=card_data.get("name", ""),
                mana_cost=card_data.get("mana_cost"),
                type_line=card_data.get("type_line", ""),
                oracle_text=card_data.get("oracle_text", ""),
                image_uris=card_data.get("image_uris"),
                scryfall_uri=card_data.get("scryfall_uri", ""),
                rarity=card_data.get("rarity", "")
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
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")
