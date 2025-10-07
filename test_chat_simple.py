"""
Dify 聊天消息 API - 简单测试示例
"""

import requests
import json

# 配置
API_BASE_URL = "https://api.dify.ai/v1"
API_KEY = "xxx"

# 构建请求
url = f"{API_BASE_URL}/chat-messages"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 请求体 - 阻塞模式（简单测试）
payload = {
    "query": "生成式UI",  # 在这里输入你想要发送的消息
    "inputs": {},
    "response_mode": "streaming",  # 使用流式模式
    "user": "test-user-001"  # 用户标识
}

# 发送请求
print(f"正在发送消息: {payload['query']}")
print("-" * 60)

response = requests.post(url, headers=headers, json=payload, stream=True)

# 处理响应
if response.status_code == 200:
    print(f"✓ 连接成功，开始接收流式响应...\n")
    print("【AI 回复】")
    
    full_answer = ""
    message_id = None
    conversation_id = None
    task_id = None
    metadata = None
    
    # 处理 SSE 流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8')
            
            # SSE 格式：data: {...}
            if line_text.startswith('data: '):
                data_str = line_text[6:]  # 去掉 "data: " 前缀
                
                try:
                    data = json.loads(data_str)
                    event = data.get('event', '')
                    
                    if event == 'message':
                        # 收到消息块，实时打印
                        answer_chunk = data.get('answer', '')
                        print(answer_chunk, end='', flush=True)
                        full_answer += answer_chunk
                        
                        # 保存 ID 信息
                        if not message_id:
                            message_id = data.get('message_id')
                        if not conversation_id:
                            conversation_id = data.get('conversation_id')
                        if not task_id:
                            task_id = data.get('task_id')
                    
                    elif event == 'message_end':
                        # 消息结束
                        print("\n")
                        metadata = data.get('metadata', {})
                        message_id = data.get('message_id') or message_id
                        conversation_id = data.get('conversation_id') or conversation_id
                    
                    elif event == 'error':
                        print(f"\n✗ [错误] {data.get('message')}")
                
                except json.JSONDecodeError:
                    # 跳过无法解析的行
                    pass
    
    # 显示统计信息
    print("-" * 60)
    print(f"任务ID: {task_id}")
    print(f"消息ID: {message_id}")
    print(f"会话ID: {conversation_id}")
    
    # 显示使用统计
    if metadata:
        usage = metadata.get('usage', {})
        if usage:
            print("-" * 60)
            print(f"Token 使用情况:")
            print(f"  - 提示词 tokens: {usage.get('prompt_tokens', 0)}")
            print(f"  - 回复 tokens: {usage.get('completion_tokens', 0)}")
            print(f"  - 总计 tokens: {usage.get('total_tokens', 0)}")
            print(f"  - 总费用: {usage.get('total_price', 0)} {usage.get('currency', 'USD')}")
            print(f"  - 延迟: {usage.get('latency', 0):.2f}秒")
else:
    print(f"✗ 请求失败: {response.status_code}")
    print(response.text)

