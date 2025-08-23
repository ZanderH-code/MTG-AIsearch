import requests
import json

def test_api_with_key():
    """测试带API密钥的搜索功能"""
    
    # 测试API基础URL
    base_url = "http://localhost:8000"
    
    # 测试1: 验证API密钥端点
    print("=== 测试1: API密钥验证 ===")
    validate_data = {
        "api_key": "test_key_123",
        "provider": "aihubmix"
    }
    
    try:
        response = requests.post(f"{base_url}/api/validate-key", json=validate_data)
        print(f"验证状态码: {response.status_code}")
        print(f"验证结果: {response.json()}")
    except Exception as e:
        print(f"验证失败: {e}")
    
    print("\n=== 测试2: 演示模式搜索 ===")
    # 测试2: 演示模式搜索（无API密钥）
    demo_data = {
        "query": "绿色的生物卡",
        "language": "zh"
    }
    
    try:
        response = requests.post(f"{base_url}/api/search", json=demo_data)
        print(f"演示模式状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Scryfall查询: {result.get('scryfall_query')}")
            print(f"找到卡牌数量: {result.get('total_cards')}")
            print(f"AI提供商: {result.get('api_provider')}")
            print(f"返回卡牌数量: {len(result.get('cards', []))}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"演示模式搜索失败: {e}")
    
    print("\n=== 测试3: 带API密钥搜索 ===")
    # 测试3: 带API密钥搜索
    api_data = {
        "query": "地落卡组的强力终端",
        "language": "zh",
        "api_key": "test_key_123"  # 这里使用测试密钥
    }
    
    try:
        response = requests.post(f"{base_url}/api/search", json=api_data)
        print(f"API模式状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Scryfall查询: {result.get('scryfall_query')}")
            print(f"找到卡牌数量: {result.get('total_cards')}")
            print(f"AI提供商: {result.get('api_provider')}")
            print(f"返回卡牌数量: {len(result.get('cards', []))}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"API模式搜索失败: {e}")

if __name__ == "__main__":
    test_api_with_key()

