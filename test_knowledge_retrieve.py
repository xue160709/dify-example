"""
Dify 知识库检索 API 测试脚本
"""

import requests
import json

# API 配置
API_BASE_URL = "https://api.dify.ai/v1"
DATASET_ID = "ff09e8db-836d-4375-ae98-fa40228b967f"
API_KEY = "xxx"


def retrieve_from_knowledge_base(query, retrieval_config=None):
    """
    从知识库检索相关块
    
    参数:
        query: 搜索查询字符串
        retrieval_config: 可选的检索配置
    
    返回:
        检索结果
    """
    url = f"{API_BASE_URL}/datasets/{DATASET_ID}/retrieve"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "query": query
    }
    
    # 如果提供了检索配置，添加到请求体
    if retrieval_config:
        payload["retrieval_model"] = retrieval_config
    
    try:
        print(f"正在发送请求到: {url}")
        print(f"查询内容: {query}")
        print(f"请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        print("-" * 60)
        
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ 请求成功!")
            print(f"\n查询内容: {result.get('query', {}).get('content', '')}")
            print(f"检索到的记录数: {len(result.get('records', []))}")
            print("\n" + "=" * 60)
            
            # 打印检索结果
            for idx, record in enumerate(result.get('records', []), 1):
                segment = record.get('segment', {})
                score = record.get('score', 0)
                
                print(f"\n【结果 {idx}】")
                print(f"相关度分数: {score}")
                print(f"段落ID: {segment.get('id', 'N/A')}")
                print(f"文档ID: {segment.get('document_id', 'N/A')}")
                print(f"位置: {segment.get('position', 'N/A')}")
                print(f"字数: {segment.get('word_count', 'N/A')}")
                print(f"Token数: {segment.get('tokens', 'N/A')}")
                
                # 打印文档信息
                document = segment.get('document', {})
                if document:
                    print(f"\n文档信息:")
                    print(f"  - 文档名称: {document.get('name', 'N/A')}")
                    print(f"  - 数据源类型: {document.get('data_source_type', 'N/A')}")
                
                # 打印内容（截取前200字符）
                content = segment.get('content', '')
                print(f"\n内容预览:")
                print(f"  {content[:200]}{'...' if len(content) > 200 else ''}")
                
                # 如果有关键词，打印关键词
                keywords = segment.get('keywords', [])
                if keywords:
                    print(f"\n关键词: {', '.join(keywords)}")
                
                print("-" * 60)
            
            return result
        else:
            print(f"✗ 请求失败!")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ 发生异常: {str(e)}")
        return None


def test_basic_search():
    """测试基本搜索"""
    print("\n" + "=" * 60)
    print("测试 1: 基本搜索")
    print("=" * 60)
    
    result = retrieve_from_knowledge_base(
        query="什么是人工智能?"
    )
    return result


def test_advanced_search():
    """测试高级搜索（带检索配置）"""
    print("\n" + "=" * 60)
    print("测试 2: 高级搜索（混合搜索 + 重排序）")
    print("=" * 60)
    
    retrieval_config = {
        "search_method": "hybrid_search",  # 混合搜索
        "reranking_enable": True,  # 启用重排序
        "reranking_mode": {
            "reranking_provider_name": "cohere",
            "reranking_model_name": "rerank-multilingual-v2.0"
        },
        "top_k": 5,  # 返回前5个结果
        "score_threshold_enabled": True,  # 启用分数阈值
        "score_threshold": 0.5,  # 最低分数0.5
        "weights": 0.7  # 语义搜索权重
    }
    
    result = retrieve_from_knowledge_base(
        query="机器学习算法",
        retrieval_config=retrieval_config
    )
    return result


def test_semantic_search():
    """测试语义搜索"""
    print("\n" + "=" * 60)
    print("测试 3: 语义搜索")
    print("=" * 60)
    
    retrieval_config = {
        "search_method": "semantic_search",  # 语义搜索
        "top_k": 3  # 返回前3个结果
    }
    
    result = retrieve_from_knowledge_base(
        query="深度学习",
        retrieval_config=retrieval_config
    )
    return result


def test_full_text_search():
    """测试全文搜索"""
    print("\n" + "=" * 60)
    print("测试 4: 全文搜索")
    print("=" * 60)
    
    retrieval_config = {
        "search_method": "full_text_search",  # 全文搜索
        "top_k": 3
    }
    
    result = retrieve_from_knowledge_base(
        query="神经网络",
        retrieval_config=retrieval_config
    )
    return result


def test_with_metadata_filtering():
    """测试带元数据过滤的搜索"""
    print("\n" + "=" * 60)
    print("测试 5: 带元数据过滤的搜索")
    print("=" * 60)
    
    retrieval_config = {
        "search_method": "hybrid_search",
        "top_k": 5,
        "metadata_filtering_conditions": {
            "logical_operator": "and",
            "conditions": [
                {
                    "name": "category",
                    "comparison_operator": "equals",
                    "value": "AI"
                }
            ]
        }
    }
    
    result = retrieve_from_knowledge_base(
        query="自然语言处理",
        retrieval_config=retrieval_config
    )
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Dify 知识库检索 API 测试")
    print("=" * 60)
    print(f"API基础URL: {API_BASE_URL}")
    print(f"知识库ID: {DATASET_ID}")
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 60)
    
    # 运行测试
    # 你可以选择运行哪些测试
    
    # 测试1: 基本搜索（最简单）
    test_basic_search()
    
    # 取消注释以下行来运行更多测试:
    
    # test_advanced_search()
    # test_semantic_search()
    # test_full_text_search()
    # test_with_metadata_filtering()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

