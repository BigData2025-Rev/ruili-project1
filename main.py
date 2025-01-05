from app import app
import controller.Controller  # 导入路由逻辑以注册到 app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
