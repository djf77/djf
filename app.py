# app.py

from flask import Flask, jsonify
from controller.users import users_bp
from controller.session import session_bp
from utils import HttpError

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(session_bp)

app.config['SECRET_KEY'] = '123456'


# 注册一个错误处理器
@app.errorhandler(HttpError)
def handle_http_error(error):
    response = jsonify(error.to_dict())  # 创建一个Response实例
    response.status_code = error.status_code  # 修改HTTP状态码
    return response


if __name__ == '__main__':
    app.run(debug=True)
