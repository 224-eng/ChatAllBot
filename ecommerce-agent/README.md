# 电商 AI Agent

面向电商场景的 AI Agent 系统，支持多角色（卖家、客服、买家）使用，通过自然语言交互完成数据分析、客服处理、选品推荐、内容创作等任务。

## 功能特性

- **数据分析 Agent**：自动查询销量、库存、退货率等数据
- **客服处理 Agent**：解答订单、物流、售后问题
- **选品推荐 Agent**：基于向量搜索推荐商品
- **内容创作 Agent**：生成商品文案和描述
- **知识问答 Agent**：基于 RAG 检索知识库回答问题

## 技术栈

- **Agent 框架**：LangChain + LangGraph
- **LLM**：DeepSeek V3 / Qwen 2.5
- **向量数据库**：Milvus
- **关系数据库**：PostgreSQL
- **缓存**：Redis
- **后端**：FastAPI

## 快速开始

### 1. 环境准备

```bash
# 复制环境变量配置
cp .env.example .env

# 编辑 .env 填写 API Key
```

### 2. 启动基础设施

```bash
# 使用你服务器上已有的服务，或者本地启动
docker compose -f docker-compose.yml up -d
```

### 3. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
# 创建数据库表
alembic upgrade head

# 生成模拟数据
python scripts/generate_mock_data.py
```

### 5. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

## 项目结构

```
ecommerce-agent/
├── app/                    # 应用代码
│   ├── agents/             # Agent 核心
│   ├── tools/              # 工具层
│   ├── memory/             # 记忆系统
│   ├── vector/             # 向量处理
│   ├── models/             # 数据模型
│   └── config/             # 配置
├── data/                   # 数据文件
├── scripts/                # 脚本
├── tests/                  # 测试
├── migrations/             # 数据库迁移
├── docker-compose.yml      # 基础设施
├── requirements.txt        # 依赖
└── README.md               # 项目说明
```

## 相关文档

- [系统设计文档](ecommerce-agent-design.md)
- [PR 拆分计划](ecommerce-agent-pr-plan.md)

## License

MIT
