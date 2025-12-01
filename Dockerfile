FROM debian:12-slim
# 工作目录
WORKDIR /opt/fastinit
# 把当前目录下的所有文件拷贝到工作目录
COPY *.sh .
COPY app/requirements.txt .
# 执行安装脚本
RUN bash install.sh
# 暴露端口和目录
EXPOSE 2080
# VOLUME /opt/fastinit/app/data
# 启动命令
CMD ["bash", "run.sh"]