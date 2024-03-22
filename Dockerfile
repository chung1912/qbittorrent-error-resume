FROM python:3.11.7

# 设置环境变量
ENV QB_HOST="" \
    QB_PORT="" \
    QB_USERNAME="" \
    QB_PASSWORD=""

# 非必要步骤，更换pip源
RUN echo '[global]' > /etc/pip.conf && \
    echo 'index-url = https://mirrors.aliyun.com/pypi/simple/' >> /etc/pip.conf && \
    echo 'trusted-host = mirrors.aliyun.com' >> /etc/pip.conf


# 设置工作目录文件夹
WORKDIR /app
# 将当前目录下的文件都添加到工作目录文件夹
ADD ./main.py /app/
ADD ./requirements.txt /app/
ADD ./config.yml /app/

# # 移除部分文件夹和文件
# RUN rm -f /app/.gitignore && \
#     rm -rf /app/logs && \
#     rm -rf /app/.venv


# 安装依赖
RUN pip3 install -r requirements.txt


# 当启动容器时候，启动
CMD ["python3", "-u", "main.py"]
