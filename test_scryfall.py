import httpx
import asyncio

async def test_scryfall_api():
    """测试Scryfall API调用"""
    
    # 根据Scryfall API文档设置必要的请求头
    headers = {
        "User-Agent": "MTG-AI-Search/1.0",
        "Accept": "application/json"
    }
    
    # 测试查询
    test_queries = [
        "o:\"landfall\"",
        "t:creature c:g",
        "t:instant cmc<=3"
    ]
    
    async with httpx.AsyncClient() as client:
        for query in test_queries:
            print(f"\n测试查询: {query}")
            try:
                response = await client.get(
                    "https://api.scryfall.com/cards/search",
                    params={"q": query, "page": 1, "unique": "cards"},
                    headers=headers,
                    timeout=30.0
                )
                
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"找到 {data.get('total_cards', 0)} 张卡牌")
                    
                    # 显示前3张卡牌的信息
                    cards = data.get('data', [])[:3]
                    for i, card in enumerate(cards, 1):
                        print(f"  {i}. {card.get('name', 'Unknown')} - {card.get('type_line', 'Unknown')}")
                        
                elif response.status_code == 404:
                    print("没有找到匹配的卡牌")
                else:
                    print(f"API错误: {response.status_code}")
                    
            except Exception as e:
                print(f"请求错误: {e}")
            
            # 根据Scryfall API要求，在请求之间添加延迟
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(test_scryfall_api())

