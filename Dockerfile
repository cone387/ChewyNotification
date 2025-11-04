FROM docker.m.daocloud.io/library/python:3.11-slim

# 设置工作目录
WORKDIR /app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && echo "" > /etc/apt/sources.list.d/debian.sources \
    && echo "deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list \
    && apt-get update


# 复制项目文件
COPY pyproject.toml uv.lock README.md ./
COPY chewy_notification ./chewy_notification
COPY example_project ./example_project

# 安装 uv
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
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
