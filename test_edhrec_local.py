#!/usr/bin/env python3
"""
本地测试EDHREC排序功能
"""

import asyncio
import random
from typing import List, Optional

# 模拟卡牌数据
sample_cards = [
    {"name": "Lightning Bolt", "cmc": 1, "power": None, "toughness": None},
    {"name": "Sol Ring", "cmc": 1, "power": None, "toughness": None},
    {"name": "Counterspell", "cmc": 2, "power": None, "toughness": None},
    {"name": "Swords to Plowshares", "cmc": 1, "power": None, "toughness": None},
    {"name": "Cyclonic Rift", "cmc": 7, "power": None, "toughness": None},
    {"name": "Demonic Tutor", "cmc": 2, "power": None, "toughness": None},
    {"name": "Mana Crypt", "cmc": 0, "power": None, "toughness": None},
    {"name": "Force of Will", "cmc": 5, "power": None, "toughness": None},
]

async def sort_cards_with_edhrec(cards: list, order: str) -> list:
    """使用EDHREC评分对卡牌进行排序"""
    try:
        # 简化实现：使用随机评分进行排序演示
        random.seed(42)  # 固定种子，确保结果一致
        
        # 为每张卡牌生成随机评分
        card_ratings = {}
        for card in cards:
            card_name = card.get('name', '')
            if card_name:
                card_ratings[card_name] = random.uniform(0.0, 10.0)
        
        # 根据评分排序
        reverse = order == "desc"
        
        def get_edhrec_rating(card):
            card_name = card.get('name', '')
            return card_ratings.get(card_name, 0.0)
        
        sorted_cards = sorted(cards, key=get_edhrec_rating, reverse=reverse)
        
        print(f"EDHREC排序完成: {order}")
        return sorted_cards
        
    except Exception as e:
        print(f"EDHREC排序错误: {e}")
        return cards  # 如果排序失败，返回原始列表

def sort_cards(cards: list, sort: str, order: str) -> list:
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
            "edhrec": "edhrec",
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
        elif sort_field == "edhrec":
            # 处理EDHREC评分字段 - 需要从EDHREC API获取数据
            print("EDHREC排序需要从外部API获取数据，暂时使用默认排序")
            # 这里可以扩展为真正的EDHREC评分排序
            sorted_cards = cards  # 暂时返回原始顺序
        else:
            # 其他字段直接按字符串排序
            sorted_cards = sorted(cards, key=lambda x: x.get(sort_field, ''), reverse=reverse)
        
        print(f"排序完成: {sort_field}:{order}")
        return sorted_cards
        
    except Exception as e:
        print(f"排序错误: {e}")
        return cards  # 如果排序失败，返回原始列表

async def test_sorting():
    """测试排序功能"""
    print("=== 本地排序功能测试 ===")
    
    # 测试1: 按名称排序
    print("\n1. 测试按名称排序 (升序):")
    sorted_cards = sort_cards(sample_cards, "name", "asc")
    for i, card in enumerate(sorted_cards[:5]):
        print(f"  {i+1}. {card['name']}")
    
    # 测试2: 按CMC排序
    print("\n2. 测试按CMC排序 (降序):")
    sorted_cards = sort_cards(sample_cards, "cmc", "desc")
    for i, card in enumerate(sorted_cards[:5]):
        print(f"  {i+1}. {card['name']} (CMC: {card['cmc']})")
    
    # 测试3: EDHREC排序
    print("\n3. 测试EDHREC排序 (降序):")
    sorted_cards = await sort_cards_with_edhrec(sample_cards, "desc")
    for i, card in enumerate(sorted_cards[:5]):
        print(f"  {i+1}. {card['name']}")
    
    # 测试4: EDHREC排序 (升序)
    print("\n4. 测试EDHREC排序 (升序):")
    sorted_cards = await sort_cards_with_edhrec(sample_cards, "asc")
    for i, card in enumerate(sorted_cards[:5]):
        print(f"  {i+1}. {card['name']}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(test_sorting())
