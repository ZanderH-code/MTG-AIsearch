import httpx
import asyncio

async def test_sorting_fix():
    """测试修复后的排序功能"""
    url = "https://mtg-ai-backend.onrender.com/api/search"
    
    # 测试不同的排序方式
    test_cases = [
        {"sort": "name", "order": "asc", "description": "按名称升序"},
        {"sort": "name", "order": "desc", "description": "按名称降序"},
        {"sort": "cmc", "order": "asc", "description": "按法力值升序"},
        {"sort": "cmc", "order": "desc", "description": "按法力值降序"},
        {"sort": "power", "order": "desc", "description": "按力量降序"},
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n测试 {i+1}: {test_case['description']}")
        print(f"排序参数: {test_case['sort']}:{test_case['order']}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json={
                        "query": "red creatures",
                        "language": "en",
                        "sort": test_case["sort"],
                        "order": test_case["order"]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 成功 - 找到 {data['total_cards']} 张卡牌")
                    print(f"   Scryfall查询: {data['scryfall_query']}")
                    
                    # 显示前5张卡牌的名称和相关信息
                    if data['cards']:
                        print("   前5张卡牌:")
                        for j, card in enumerate(data['cards'][:5]):
                            print(f"     {j+1}. {card['name']}")
                else:
                    print(f"❌ 失败 - HTTP {response.status_code}")
                    print(f"   错误: {response.text}")
                    
        except Exception as e:
            print(f"❌ 异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_sorting_fix())
