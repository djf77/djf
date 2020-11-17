# controller/session.py

from flask import Blueprint, request, session
import database

session_bp = Blueprint('session', __name__, url_prefix='/session')


# 登录接口
@session_bp.route('', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    database.get_id(username, password)

    return '登录成功'


# 查看用户信息的接口
@session_bp.route('/get', methods=['GET'])
def get_session():
    return session.get('username')

