# controller/users.py

from flask import Blueprint, request
import database

# 设置url_prefix，这样所有注册在该蓝图下的视图函数对应的URL都会自动在前面加上'/users'，就不需要每个接口都重复写了
users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
def register():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    database.save_user(username, password)

    return '创建成功'


# 修改用户名
@users_bp.route('/username', methods=['PUT'])
def change_username():
    data = request.get_json(force=True)
    username = data.get('username')

    database.change_username(username)

    return '修改用户名成功'


# 修改密码
@users_bp.route('/password', methods=['PUT'])
def change_password():
    data = request.get_json(force=True)
    password = data.get('password')

    database.change_password(password)

    return '修改密码成功'
