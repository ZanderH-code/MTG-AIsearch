import requests
import json

def test_models_api():
    """测试模型列表获取功能"""
    
    # 测试API基础URL
    base_url = "http://localhost:8000"
    
    print("=== 测试模型列表获取 ===")
    
    # 测试1: 获取Aihubmix模型列表
    print("\n--- 测试1: Aihubmix模型列表 ---")
    aihubmix_data = {
        "api_key": "test_key_123",
        "provider": "aihubmix"
    }
    
    try:
        response = requests.post(f"{base_url}/api/models", json=aihubmix_data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result.get('success')}")
            print(f"提供商: {result.get('provider')}")
            print(f"模型数量: {len(result.get('models', []))}")
            print("模型列表:")
            for model in result.get('models', []):
                print(f"  - {model.get('name')} ({model.get('id')})")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试2: 获取OpenAI模型列表
    print("\n--- 测试2: OpenAI模型列表 ---")
    openai_data = {
        "api_key": "test_key_123",
        "provider": "openai"
    }
    
    try:
        response = requests.post(f"{base_url}/api/models", json=openai_data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result.get('success')}")
            print(f"提供商: {result.get('provider')}")
            print(f"模型数量: {len(result.get('models', []))}")
            print("模型列表:")
            for model in result.get('models', []):
                print(f"  - {model.get('name')} ({model.get('id')})")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试3: 带模型参数的验证
    print("\n--- 测试3: 带模型参数的验证 ---")
    validate_data = {
        "api_key": "test_key_123",
        "provider": "aihubmix",
        "model": "gpt-4o-mini"
    }
    
    try:
        response = requests.post(f"{base_url}/api/validate-key", json=validate_data)
        print(f"验证状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"验证结果: {result}")
        else:
            print(f"验证错误: {response.text}")
    except Exception as e:
        print(f"验证失败: {e}")

if __name__ == "__main__":
    test_models_api()

