## 目录说明
* app：后端路径
* app/api：API文件路径
* app/data：数据路径，通常保存一些配置文件、日志等，应该添加到`.gitignore`
* app/middleware：中间件
* app/utils：常用函数
* app/config.py：配置类
* app/main.py：程序入口、主函数

## 使用

```
git clone https://github.com/helloxz/fastinit.git
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r app/requirements.txt
```

## 命名规范
* app/api中，命名统一：FileNameHandler
* app/model中，命名统一：FileNameModel