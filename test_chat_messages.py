"""
Dify 聊天消息 API 完整测试脚本
支持阻塞模式和流式模式
"""

import requests
import json
import time

# API 配置
API_BASE_URL = "https://api.dify.ai/v1"
API_KEY = "xxx"


def send_chat_message_blocking(query, conversation_id=None, inputs=None, user="test-user"):
    """
    发送聊天消息 - 阻塞模式
    
    参数:
        query: 用户输入/提问内容
        conversation_id: 可选，会话ID（用于继续之前的对话）
        inputs: 可选，App 定义的各变量值
        user: 用户标识
    
    返回:
        响应结果
    """
    url = f"{API_BASE_URL}/chat-messages"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "query": query,
        "inputs": inputs or {},
        "response_mode": "blocking",
        "user": user
    }
    
    # 如果有会话ID，添加到请求
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    try:
        print(f"正在发送消息: {query}")
        print(f"请求模式: 阻塞模式")
        print("-" * 60)
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print("✓ 请求成功!")
            print(f"耗时: {elapsed_time:.2f}秒\n")
            
            # 基本信息
            print(f"事件类型: {result.get('event', 'N/A')}")
            print(f"任务ID: {result.get('task_id', 'N/A')}")
            print(f"消息ID: {result.get('message_id', 'N/A')}")
            print(f"会话ID: {result.get('conversation_id', 'N/A')}")
            print(f"模式: {result.get('mode', 'N/A')}")
            print("-" * 60)
            
            # AI 回复
            print(f"\n【AI 回复】")
            answer = result.get('answer', '')
            print(answer)
            print()
            
            # 元数据和使用统计
            metadata = result.get('metadata', {})
            usage = metadata.get('usage', {})
            
            if usage:
                print("-" * 60)
                print(f"Token 使用情况:")
                print(f"  - 提示词 tokens: {usage.get('prompt_tokens', 0)}")
                print(f"  - 回复 tokens: {usage.get('completion_tokens', 0)}")
                print(f"  - 总计 tokens: {usage.get('total_tokens', 0)}")
                print(f"  - 提示词价格: {usage.get('prompt_price', 0)} {usage.get('currency', 'USD')}")
                print(f"  - 回复价格: {usage.get('completion_price', 0)} {usage.get('currency', 'USD')}")
                print(f"  - 总费用: {usage.get('total_price', 0)} {usage.get('currency', 'USD')}")
                print(f"  - 延迟: {usage.get('latency', 0):.2f}秒")
            
            # 检索资源（如果有）
            retriever_resources = metadata.get('retriever_resources', [])
            if retriever_resources:
                print(f"\n引用资源数量: {len(retriever_resources)}")
                for idx, resource in enumerate(retriever_resources, 1):
                    print(f"\n【资源 {idx}】")
                    print(f"  位置: {resource.get('position', 'N/A')}")
                    print(f"  数据集: {resource.get('dataset_name', 'N/A')}")
                    print(f"  文档: {resource.get('document_name', 'N/A')}")
                    print(f"  相关度: {resource.get('score', 0):.4f}")
                    content = resource.get('content', '')
                    print(f"  内容预览: {content[:100]}..." if len(content) > 100 else f"  内容: {content}")
            
            print("-" * 60)
            return result
        else:
            print(f"✗ 请求失败!")
            print(f"状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ 发生异常: {str(e)}")
        return None


def send_chat_message_streaming(query, conversation_id=None, inputs=None, user="test-user"):
    """
    发送聊天消息 - 流式模式
    
    参数:
        query: 用户输入/提问内容
        conversation_id: 可选，会话ID（用于继续之前的对话）
        inputs: 可选，App 定义的各变量值
        user: 用户标识
    
    返回:
        响应结果
    """
    url = f"{API_BASE_URL}/chat-messages"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "query": query,
        "inputs": inputs or {},
        "response_mode": "streaming",
        "user": user
    }
    
    # 如果有会话ID，添加到请求
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    try:
        print(f"正在发送消息: {query}")
        print(f"请求模式: 流式模式")
        print("-" * 60)
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload, stream=True)
        
        if response.status_code == 200:
            print("✓ 连接成功，开始接收流式响应...\n")
            print("【AI 回复】")
            
            full_answer = ""
            message_id = None
            conversation_id_result = None
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
                                # 收到消息块
                                answer_chunk = data.get('answer', '')
                                print(answer_chunk, end='', flush=True)
                                full_answer += answer_chunk
                                
                                # 保存 ID 信息
                                if not message_id:
                                    message_id = data.get('message_id')
                                if not conversation_id_result:
                                    conversation_id_result = data.get('conversation_id')
                                if not task_id:
                                    task_id = data.get('task_id')
                            
                            elif event == 'message_end':
                                # 消息结束
                                print("\n")
                                metadata = data.get('metadata', {})
                                message_id = data.get('message_id') or message_id
                                conversation_id_result = data.get('conversation_id') or conversation_id_result
                            
                            elif event == 'workflow_started':
                                print(f"\n[工作流开始] workflow_run_id: {data.get('workflow_run_id')}")
                            
                            elif event == 'node_started':
                                node_data = data.get('data', {})
                                print(f"[节点开始] {node_data.get('title', 'N/A')} ({node_data.get('node_type', 'N/A')})")
                            
                            elif event == 'node_finished':
                                node_data = data.get('data', {})
                                print(f"[节点完成] {node_data.get('title', 'N/A')} - 状态: {node_data.get('status', 'N/A')}")
                            
                            elif event == 'workflow_finished':
                                workflow_data = data.get('data', {})
                                print(f"[工作流完成] 状态: {workflow_data.get('status', 'N/A')}")
                            
                            elif event == 'message_file':
                                print(f"\n[文件] 类型: {data.get('type')}, URL: {data.get('url')}")
                            
                            elif event == 'message_replace':
                                print(f"\n[消息替换] {data.get('answer')}")
                                full_answer = data.get('answer', '')
                            
                            elif event == 'error':
                                print(f"\n✗ [错误] {data.get('message')}")
                            
                            elif event == 'ping':
                                # ping 事件，保持连接
                                pass
                        
                        except json.JSONDecodeError:
                            # 跳过无法解析的行
                            pass
            
            elapsed_time = time.time() - start_time
            
            # 显示统计信息
            print("-" * 60)
            print(f"任务ID: {task_id}")
            print(f"消息ID: {message_id}")
            print(f"会话ID: {conversation_id_result}")
            print(f"总耗时: {elapsed_time:.2f}秒")
            
            # 显示元数据
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
                
                # 检索资源
                retriever_resources = metadata.get('retriever_resources', [])
                if retriever_resources:
                    print(f"\n引用资源数量: {len(retriever_resources)}")
                    for idx, resource in enumerate(retriever_resources, 1):
                        print(f"\n【资源 {idx}】")
                        print(f"  数据集: {resource.get('dataset_name', 'N/A')}")
                        print(f"  文档: {resource.get('document_name', 'N/A')}")
                        print(f"  相关度: {resource.get('score', 0):.4f}")
            
            print("-" * 60)
            
            return {
                "message_id": message_id,
                "conversation_id": conversation_id_result,
                "task_id": task_id,
                "answer": full_answer,
                "metadata": metadata
            }
        else:
            print(f"✗ 请求失败!")
            print(f"状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ 发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_blocking_mode():
    """测试阻塞模式"""
    print("\n" + "=" * 60)
    print("测试 1: 阻塞模式 - 单次对话")
    print("=" * 60 + "\n")
    
    result = send_chat_message_blocking(
        query="你好，请简单介绍一下你自己"
    )
    return result


def test_streaming_mode():
    """测试流式模式"""
    print("\n" + "=" * 60)
    print("测试 2: 流式模式 - 单次对话")
    print("=" * 60 + "\n")
    
    result = send_chat_message_streaming(
        query="请用3句话介绍什么是人工智能"
    )
    return result


def test_multi_turn_conversation():
    """测试多轮对话"""
    print("\n" + "=" * 60)
    print("测试 3: 多轮对话 - 阻塞模式")
    print("=" * 60 + "\n")
    
    # 第一轮对话
    print("【第一轮对话】")
    result1 = send_chat_message_blocking(
        query="我想了解机器学习"
    )
    
    if result1:
        conversation_id = result1.get('conversation_id')
        
        # 等待一下
        time.sleep(1)
        
        # 第二轮对话（使用相同的 conversation_id）
        print("\n【第二轮对话 - 继续上次的话题】")
        result2 = send_chat_message_blocking(
            query="它有哪些应用场景？",
            conversation_id=conversation_id
        )
        
        return result2
    
    return None


def test_with_inputs():
    """测试带输入变量"""
    print("\n" + "=" * 60)
    print("测试 4: 带输入变量")
    print("=" * 60 + "\n")
    
    # 注意：这里的 inputs 需要根据你的 App 实际定义的变量来填写
    inputs = {
        # 示例变量，根据实际情况修改
        # "topic": "Python编程",
        # "level": "初级"
    }
    
    result = send_chat_message_blocking(
        query="请介绍一下相关内容",
        inputs=inputs
    )
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Dify 聊天消息 API 测试")
    print("=" * 60)
    print(f"API基础URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 60)
    
    # 运行测试
    # 你可以选择运行哪些测试
    
    # 测试1: 阻塞模式（最简单）
    test_blocking_mode()
    
    # 测试2: 流式模式
    test_streaming_mode()
    
    # 取消注释以下行来运行更多测试:
    
    # test_multi_turn_conversation()  # 多轮对话
    # test_with_inputs()  # 带输入变量
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

