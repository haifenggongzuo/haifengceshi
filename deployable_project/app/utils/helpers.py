import os
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

def generate_password_hash(password):
    """生成密码哈希"""
    return generate_password_hash(password)

def check_password_hash(password_hash, password):
    """验证密码哈希"""
    return check_password_hash(password_hash, password)

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, folder, filename=None):
    """保存上传的文件"""
    if not filename:
        filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    file.save(file_path)
    return file_path

def format_datetime(dt):
    """格式化日期时间"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def generate_token():
    """生成随机令牌"""
    return hashlib.sha256(os.urandom(32)).hexdigest() 