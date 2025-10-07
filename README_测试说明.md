# Dify API 测试工具集

本项目包含 Dify 平台的各种 API 测试脚本，方便开发者快速接入和测试。

## 📋 文件说明

### 知识库检索 API
- **`test_simple.py`** - 简单版知识库检索测试脚本
- **`test_knowledge_retrieve.py`** - 完整版知识库检索测试脚本，包含多种检索模式

### 聊天消息 API
- **`test_chat_simple.py`** - 简单版聊天消息测试脚本（流式模式）
- **`test_chat_messages.py`** - 完整版聊天消息测试脚本（支持阻塞和流式模式）

### 其他
- **`requirements.txt`** - Python依赖包

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行知识库检索测试

**简单测试：**
```bash
python test_simple.py
```

**完整测试：**
```bash
python test_knowledge_retrieve.py
```

### 3. 运行聊天消息测试

**简单测试（阻塞模式）：**
```bash
python test_chat_simple.py
```

**完整测试（支持流式和阻塞模式）：**
```bash
python test_chat_messages.py
```

## 📝 配置信息

### 知识库检索 API
- **API Base URL**: `https://api.dify.ai/v1`
- **Dataset ID**: `ff09e8db-836d-4375-ae98-fa40228b967f`
- **API Key**: `xxx`

### 聊天消息 API
- **API Base URL**: `https://api.dify.ai/v1`
- **API Key**: `xxx`

## 🎯 测试用例说明

## 一、知识库检索 API 测试

### 测试 1: 基本搜索
最简单的检索方式，只需要提供查询字符串。

```python
retrieve_from_knowledge_base(query="什么是人工智能?")
```

### 测试 2: 高级搜索（混合搜索 + 重排序）
使用混合搜索方法，结合重排序模型提升结果质量。

```python
retrieval_config = {
    "search_method": "hybrid_search",
    "reranking_enable": True,
    "top_k": 5,
    "score_threshold": 0.5
}
```

### 测试 3: 语义搜索
基于语义理解的搜索，适合理解用户意图。

```python
retrieval_config = {
    "search_method": "semantic_search",
    "top_k": 3
}
```

### 测试 4: 全文搜索
基于关键词的全文检索。

```python
retrieval_config = {
    "search_method": "full_text_search",
    "top_k": 3
}
```

### 测试 5: 带元数据过滤
根据元数据条件过滤检索结果。

```python
retrieval_config = {
    "search_method": "hybrid_search",
    "metadata_filtering_conditions": {
        "logical_operator": "and",
        "conditions": [...]
    }
}
```

---

## 二、聊天消息 API 测试

### 测试 1: 阻塞模式 - 单次对话
最简单的对话方式，等待完整响应后一次性返回。

```python
send_chat_message_blocking(
    query="你好，请简单介绍一下你自己"
)
```

**特点：**
- 等待完整回复后返回
- 实现简单，适合对实时性要求不高的场景
- 返回完整的响应数据

### 测试 2: 流式模式 - 单次对话
类似打字机效果的流式返回，实时显示 AI 回复。

```python
send_chat_message_streaming(
    query="请用3句话介绍什么是人工智能"
)
```

**特点：**
- 实时返回回复内容，用户体验更好
- 基于 SSE（Server-Sent Events）实现
- 支持实时显示回复进度

**流式事件类型：**
- `message` - LLM 返回的文本块
- `message_end` - 消息结束事件
- `message_file` - 文件事件
- `message_replace` - 消息内容替换事件
- `workflow_started` - 工作流开始
- `node_started` - 节点开始执行
- `node_finished` - 节点执行完成
- `workflow_finished` - 工作流完成
- `error` - 错误事件
- `ping` - 保持连接的心跳事件

### 测试 3: 多轮对话
支持上下文的连续对话。

```python
# 第一轮对话
result1 = send_chat_message_blocking(
    query="我想了解机器学习"
)

# 第二轮对话（使用相同的 conversation_id）
result2 = send_chat_message_blocking(
    query="它有哪些应用场景？",
    conversation_id=result1.get('conversation_id')
)
```

**特点：**
- 保持对话上下文
- 通过 `conversation_id` 关联多轮对话
- AI 能理解之前的对话内容

### 测试 4: 带输入变量
传入 App 定义的变量值。

```python
inputs = {
    "topic": "Python编程",
    "level": "初级"
}

send_chat_message_blocking(
    query="请介绍一下相关内容",
    inputs=inputs
)
```

### 响应模式对比

| 特性 | 阻塞模式（blocking） | 流式模式（streaming） |
|------|---------------------|---------------------|
| 响应方式 | 一次性返回完整结果 | 分块实时返回 |
| 用户体验 | 需要等待完整响应 | 打字机效果，实时显示 |
| 实现复杂度 | 简单 | 需要处理 SSE 流 |
| 超时风险 | 长流程可能超时（100秒） | 通过流式传输避免超时 |
| 适用场景 | 短对话、批量处理 | 长对话、需要实时反馈 |

### 聊天消息 API 响应数据

**阻塞模式响应：**
```json
{
    "event": "message",
    "task_id": "任务ID",
    "message_id": "消息ID",
    "conversation_id": "会话ID",
    "mode": "chat",
    "answer": "AI的完整回复",
    "metadata": {
        "usage": {
            "prompt_tokens": 1033,
            "completion_tokens": 128,
            "total_tokens": 1161,
            "total_price": "0.0012890",
            "currency": "USD"
        },
        "retriever_resources": [...]
    },
    "created_at": 1705407629
}
```

**流式模式响应：**
每个事件以 `data:` 开头，事件之间用两个换行符分隔：
```
data: {"event": "message", "answer": "Hi", ...}

data: {"event": "message_end", "metadata": {...}}
```

---

## 🔧 自定义查询

### 知识库检索 - 修改查询内容

在 `test_simple.py` 中修改这一行：

```python
payload = {
    "query": "你的查询内容"  # 修改这里
}
```

### 聊天消息 - 修改对话内容

在 `test_chat_simple.py` 中修改这一行：

```python
payload = {
    "query": "你想说的话",  # 修改这里
    "response_mode": "blocking",  # 或 "streaming"
    "user": "your-user-id"
}
```

### 调整检索参数

在 `test_knowledge_retrieve.py` 中可以自定义以下参数：

- **`search_method`**: 搜索方法
  - `hybrid_search` - 混合搜索
  - `semantic_search` - 语义搜索
  - `full_text_search` - 全文搜索
  - `keyword_search` - 关键词搜索

- **`top_k`**: 返回结果数量（默认：3）

- **`score_threshold`**: 最低相关度分数（0-1之间）

- **`reranking_enable`**: 是否启用重排序

- **`weights`**: 混合搜索中语义搜索的权重（0-1之间）

## 📊 响应结果说明

API 返回的每个结果包含：

- **`score`**: 相关度分数（越高越相关）
- **`segment`**: 段落信息
  - `id`: 段落ID
  - `content`: 段落内容
  - `word_count`: 字数
  - `tokens`: Token数量
  - `keywords`: 关键词列表
  - `document`: 文档信息
    - `name`: 文档名称
    - `data_source_type`: 数据源类型

## ❗ 常见问题

### 知识库检索 API

#### 1. 401 Unauthorized
检查 Dataset API Key 是否正确。

#### 2. 404 Not Found
检查 Dataset ID 是否正确。

#### 3. 返回结果为空
- 知识库可能没有相关内容
- 尝试调整 `score_threshold` 阈值
- 尝试不同的搜索方法

### 聊天消息 API

#### 1. 400 invalid_param
- 检查请求参数是否正确
- 确认 `response_mode` 是 "blocking" 或 "streaming"

#### 2. 400 app_unavailable
- App 配置不可用
- 检查 App 是否已发布

#### 3. 400 provider_not_initialize
- 无可用模型凭据配置
- 在 Dify 控制台配置模型

#### 4. 400 provider_quota_exceeded
- 模型调用额度不足
- 检查账户额度

#### 5. 400 conversation_id_not_exist
- 会话 ID 不存在
- 检查 conversation_id 是否正确

#### 6. 流式模式接收不完整
- 确保正确处理 SSE 流
- 检查网络连接稳定性

### 通用问题

#### 1. 连接超时
- 检查网络连接，确保可以访问 `api.dify.ai`
- 流式模式可以避免长请求超时问题

#### 2. 字符编码问题
- 确保使用 UTF-8 编码
- 正确处理中文字符

## 💡 使用建议

### 知识库检索 API
1. **快速测试**: 使用 `test_simple.py`
2. **详细调试**: 使用 `test_knowledge_retrieve.py`
3. **性能优化**: 根据实际需求调整 `top_k` 和 `score_threshold`

### 聊天消息 API
1. **快速测试**: 使用 `test_chat_simple.py`（阻塞模式）
2. **详细调试**: 使用 `test_chat_messages.py`（支持流式和阻塞）
3. **生产推荐**: 优先使用流式模式，用户体验更好
4. **多轮对话**: 保存并复用 `conversation_id`
5. **错误处理**: 捕获并处理各种 event 类型，特别是 `error` 事件

### 通用建议
1. **安全性**: 将 API Key 存储在环境变量中，不要硬编码
2. **错误处理**: 添加适当的异常处理和重试机制
3. **日志记录**: 记录关键操作和错误信息
4. **成本控制**: 注意 token 使用量和费用

## 🔒 安全提示

⚠️ **重要**: 不要将API Key提交到版本控制系统中！

建议使用环境变量：

```python
import os
API_KEY = os.getenv('DIFY_API_KEY')
```

然后在命令行中设置：

```bash
# Windows PowerShell
$env:DIFY_API_KEY="your-api-key"

# Windows CMD
set DIFY_API_KEY=your-api-key

# Linux/Mac
export DIFY_API_KEY=your-api-key
```

