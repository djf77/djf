# database.py
from flask import session
from mysql.connector import connect
from werkzeug.security import generate_password_hash, check_password_hash
from utils import HttpError
import config


# 与MySQL建立连接
def get_connection():
    conn = connect(user=config.database.get('user'), password=config.database.get('password'),
                   database=config.database.get('database'))
    cursor = conn.cursor()

    return conn, cursor


# 判断用户名是否存在
def username_is_exist(username):
    # 获取数据库连接
    conn, cursor = get_connection()

    cursor.execute('select count(*) from `users` where `username`=%s', (username,))
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count


# 将用户存入数据库
def save_user(username, password):
    count = username_is_exist(username)

    if count >= 1:
        raise HttpError(409, '用户名已存在')

    # 获取数据库连接
    conn, cursor = get_connection()

    # 将用户信息存入数据库中，对于密码这一涉及到用户隐私的信息我们需要加密后再存储
    # 这里直接使用werkzeug网络包中的generate_password_hash函数进行加密
    cursor.execute('insert into `users`(`username`, `password`) values (%s, %s)',
                   (username, generate_password_hash(password)))

    conn.commit()

    cursor.close()
    conn.close()


def get_id(username, password):
    # 获取数据库连接
    conn, cursor = get_connection()
    cursor.execute('select `id`, `password` from `users` where `username`=%s', (username,))
    values = cursor.fetchone()
    # 如果数据库中没有这个用户，则fetchone函数会返回None
    if values is None:
        raise HttpError(400, '用户名或密码错误')

    user_id = values[0]  # 用户的id
    pwd = values[1]  # 数据库中的密码

    # 因为数据库中的密码已被加密，无法直接和传入的密码相比较，我们可以使用check_password_hash来判断
    # 它接收两个参数，第一个是已加密的密码，第二个是未加密的，如果未加密的密码和已加密的密码被加密前相同，则返回 Ture，否则返回 False
    if not check_password_hash(pwd, password):  # 如果密码不同
        raise HttpError(400, '用户名或密码错误')  # 错误信息都统一返回“用户名或密码错误”，防止别人试出数据库中有没有这个用户名

    # 登录成功，将用户名存入session中，供第四个任务使用
    session['username'] = username
    # 同时将用户在数据库中的id也存入session中，我们将在第三个任务中用到
    session['user_id'] = user_id


def change_username(username):
    # 获取数据库连接
    conn, cursor = get_connection()

    # 如果session中没有user_id，说明用户未登录，返回401错误
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')

    # 判断用户名是否存在
    cursor.execute('select count(*) from `users` where `username`=%s', (username,))
    count = cursor.fetchone()[0]
    # 如果用户名已存在则返回409错误
    if count >= 1:
        raise HttpError(409, '用户名已存在')

    # 根据登录时储存的user_id在where子句中定位到具体的用户并更新他的用户名
    cursor.execute('update `users` set `username`=%s where id=%s', (username, session.get('user_id')))

    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()


def change_password(password):
    # 获取数据库连接
    conn, cursor = get_connection()

    # 如果session中没有user_id，说明用户未登录，返回401错误
    if session.get('user_id') is None:
        raise HttpError(401, '请先登录')

    # 根据登录时储存的user_id在where子句中定位到具体的用户并更新他的密码（注意密码还是要加密）
    cursor.execute('update `users` set `password`=%s where id=%s',
                   (generate_password_hash(password), session.get('user_id')))

    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()
