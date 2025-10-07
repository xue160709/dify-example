"""
Dify 知识库检索 API - 简单测试示例
"""

import requests

# 配置
API_BASE_URL = "https://api.dify.ai/v1"
DATASET_ID = "ff09e8db-836d-4375-ae98-fa40228b967f"
API_KEY = "xxx"

# 构建请求
url = f"{API_BASE_URL}/datasets/{DATASET_ID}/retrieve"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 请求体 - 修改这里的查询内容
payload = {
    "query": "什么是生成式UI?"  # 在这里输入你想要搜索的内容
}

# 发送请求
print(f"正在搜索: {payload['query']}")
response = requests.post(url, headers=headers, json=payload)

# 处理响应
if response.status_code == 200:
    result = response.json()
    print(f"\n✓ 搜索成功! 找到 {len(result.get('records', []))} 条结果\n")
    
    # 显示结果
    for idx, record in enumerate(result.get('records', []), 1):
        segment = record.get('segment', {})
        score = record.get('score', 0)
        content = segment.get('content', '')
        
        print(f"【结果 {idx}】- 相关度: {score:.4f}")
        print(f"{content[:150]}...\n")
else:
    print(f"✗ 请求失败: {response.status_code}")
    print(response.text)

