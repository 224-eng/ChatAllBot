# 数据目录

## 目录结构

```
data/
├── mock/           # 模拟数据
├── knowledge/      # 知识库文档
│   ├── products/   # 商品知识
│   ├── faq/        # FAQ
│   └── policy/     # 政策规则
└── embeddings/     # 预计算的向量缓存
```

## 模拟数据

使用 `scripts/generate_mock_data.py` 生成模拟数据。

## 知识库

知识库文档使用 Markdown 格式，按主题分类存放。
