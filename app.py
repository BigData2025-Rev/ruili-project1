from flask_cors import CORS
from flask import Flask

# 创建 Flask 实例
app = Flask(
    __name__,
    template_folder='templates',  # 模板文件夹
    static_folder='static'        # 静态资源文件夹
)
CORS(app) # allow cors request, otherwise I cannot access any non-static request