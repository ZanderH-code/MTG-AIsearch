import httpx
import asyncio
import json

async def test_edhrec_data():
    """测试Scryfall API是否包含EDHRec评分数据"""
    base_url = "https://api.scryfall.com/cards/search"
    
    # 测试一些知名的EDH卡牌
    test_cards = [
        "Sol Ring",
        "Cyclonic Rift", 
        "Swords to Plowshares",
        "Counterspell",
        "Lightning Bolt"
    ]
    
    print("检查Scryfall API中的EDHRec数据...")
    print("=" * 50)
    
    for card_name in test_cards:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    base_url,
                    params={
                        "q": f'!"{card_name}"',
                        "unique": "cards"
                    },
                    headers={
                        "User-Agent": "MTG-AI-Search/1.0",
                        "Accept": "application/json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('data'):
                        card = data['data'][0]
                        print(f"\n卡牌: {card.get('name', 'Unknown')}")
                        print(f"  所有字段: {list(card.keys())}")
                        
                        # 检查是否有EDHRec相关字段
                        edhrec_fields = [key for key in card.keys() if 'edhrec' in key.lower()]
                        if edhrec_fields:
                            print(f"  ✅ 找到EDHRec相关字段: {edhrec_fields}")
                            for field in edhrec_fields:
                                print(f"    {field}: {card.get(field)}")
                        else:
                            print(f"  ❌ 没有找到EDHRec相关字段")
                        
                        # 检查其他可能的评分字段
                        rating_fields = [key for key in card.keys() if 'rating' in key.lower() or 'score' in key.lower()]
                        if rating_fields:
                            print(f"  📊 找到评分相关字段: {rating_fields}")
                            for field in rating_fields:
                                print(f"    {field}: {card.get(field)}")
                        
                        # 显示一些重要字段的值
                        important_fields = ['name', 'cmc', 'power', 'toughness', 'rarity', 'set_name']
                        print(f"  重要字段:")
                        for field in important_fields:
                            if field in card:
                                print(f"    {field}: {card.get(field)}")
                        
                else:
                    print(f"❌ 获取 {card_name} 失败: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ 异常: {e}")

if __name__ == "__main__":
    asyncio.run(test_edhrec_data())
