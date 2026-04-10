# App 全自动生产工作流

基于 CrewAI 的多 Agent 协作系统，实现从想法到部署的全自动 App 生产流程。

## 功能特性

- 🤖 8 个专业 Agent 协作
- 🔧 每个 Agent 可独立配置 LLM
- 📊 完整的 CLI 监控系统
- 💾 输出空间大小控制
- 📝 支持多种想法输入方式

## 工作流顺序

调研 → 产品 → 调研产品 → 设计 → 架构 → 开发 → 测试 → 部署

## 安装

### 系统要求

- **Python 版本**: 3.10 - 3.12（推荐 3.11）
- **注意**: Python 3.13 可能存在兼容性问题

### 安装步骤

```bash
# 创建虚拟环境（推荐使用 Python 3.11）
python3.11 -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API keys
```

## 使用方法

### 运行工作流

```bash
# 方式1: 直接输入想法
python src/main.py run --idea "我想做一个待办事项APP"

# 方式2: 从文件读取
python src/main.py run --idea-file idea.txt

# 方式3: 交互式输入
python src/main.py run
```

### 监控命令

```bash
# 查看状态
python src/main.py status

# 查看日志
python src/main.py logs --tail 50

# 查看指标
python src/main.py metrics
```

### 配置管理

```bash
# Agent LLM 配置
python src/main.py config agents list
python src/main.py config agents show research_agent
python src/main.py config agents set research_agent --llm openai --model gpt-4

# 输出配置
python src/main.py config output list
python src/main.py config output set --max-total-size 500MB
python src/main.py config output space
```

## 项目结构

```
appProduct/
├── config/              # 配置文件
├── src/
│   ├── agents/          # Agent 定义
│   ├── tasks/           # Task 定义
│   ├── workflow/        # Crew 编排
│   ├── monitoring/      # 监控系统
│   ├── cli/             # CLI 命令
│   ├── input/           # 输入处理
│   ├── output/          # 输出管理
│   ├── llm_config.py    # LLM 配置
│   ├── output_config.py # 输出配置
│   └── main.py          # 主入口
├── logs/                # 日志目录
└── output/              # 输出目录
```
