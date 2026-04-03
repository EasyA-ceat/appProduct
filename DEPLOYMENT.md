# 部署文档

## Docker 部署

### 前置要求
- Docker 20.10+
- Docker Compose 2.0+

### 快速开始

1. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API keys
```

2. **构建镜像**
```bash
# Linux/Mac
./scripts/build.sh

# Windows
scripts\build.bat
```

3. **运行工作流**
```bash
# Linux/Mac
./scripts/run.sh

# Windows
scripts\run.bat
```

4. **查看日志**
```bash
docker-compose logs -f
```

5. **停止工作流**
```bash
# Linux/Mac
./scripts/stop.sh

# Windows
scripts\stop.bat
```

6. **清理资源**
```bash
# Linux/Mac
./scripts/clean.sh

# Windows
scripts\clean.bat
```

## 手动运行工作流

### 在容器内运行
```bash
docker exec -it app-product-workflow python -m src.main run --idea "我想做一个待办事项APP"
```

### 查看状态
```bash
docker exec -it app-product-workflow python -m src.main status
```

### 查看日志
```bash
docker exec -it app-product-workflow python -m src.main logs --tail 50
```

## 本地开发

### 安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 运行
```bash
python -m src.main run --idea "我想做一个待办事项APP"
```

## 配置说明

### Agent LLM 配置
编辑 `config/agents.yaml` 来配置每个 Agent 使用的 LLM。

### 输出配置
编辑 `config/output.yaml` 来配置输出空间限制和文件类型限制。

## 数据持久化

- `./logs` - 日志文件
- `./output` - 生成的项目输出

这些目录通过 Docker volumes 挂载，数据会持久化到宿主机。
