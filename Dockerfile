FROM docker.m.daocloud.io/library/python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml uv.lock README.md ./
COPY chewy_notification ./chewy_notification
COPY example_project ./example_project

# 安装 uv
RUN pip install uv

# 安装 Python 依赖
RUN uv sync --frozen

# 收集静态文件
WORKDIR /app/example_project
RUN uv run python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8002

# 启动命令
CMD ["uv", "run", "gunicorn", "example_project.wsgi:application", \
     "--bind", "0.0.0.0:8002", \
     "--workers", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
