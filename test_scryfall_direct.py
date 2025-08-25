import httpx
import asyncio

async def test_scryfall_direct():
    """直接测试Scryfall API的排序功能"""
    base_url = "https://api.scryfall.com/cards/search"
    
    # 测试不同的排序方式
    test_cases = [
        {"query": "t:creature c:r", "description": "红色生物 - 默认排序"},
        {"query": "t:creature c:r order:name:asc", "description": "红色生物 - 按名称升序"},
        {"query": "t:creature c:r order:name:desc", "description": "红色生物 - 按名称降序"},
        {"query": "t:creature c:r order:cmc:asc", "description": "红色生物 - 按法力值升序"},
        {"query": "t:creature c:r order:cmc:desc", "description": "红色生物 - 按法力值降序"},
        {"query": "t:creature c:r order:power:desc", "description": "红色生物 - 按力量降序"},
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n测试 {i+1}: {test_case['description']}")
        print(f"查询: {test_case['query']}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    base_url,
                    params={
                        "q": test_case["query"],
                        "unique": "cards"
                    },
                    headers={
                        "User-Agent": "MTG-AI-Search/1.0",
                        "Accept": "application/json"
                    },
                    timeout=30.0
                )
                
                print(f"HTTP状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 成功 - 找到 {data.get('total_cards', 0)} 张卡牌")
                    
                    # 显示前5张卡牌的名称和相关信息
                    if data.get('data'):
                        print("前5张卡牌:")
                        for j, card in enumerate(data['data'][:5]):
                            name = card.get('name', 'Unknown')
                            cmc = card.get('cmc', 'N/A')
                            power = card.get('power', 'N/A')
                            toughness = card.get('toughness', 'N/A')
                            print(f"  {j+1}. {name} (CMC: {cmc}, P/T: {power}/{toughness})")
                else:
                    print(f"❌ 失败")
                    print(f"错误响应: {response.text}")
                    
        except Exception as e:
            print(f"❌ 异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_scryfall_direct())
