from functools import wraps
from flask import jsonify, request, current_app
from flask_login import current_user
from ..models.user import AdminUser

def admin_required(f):
    """要求管理员权限的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, AdminUser):
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    """要求特定角色的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role):
                return jsonify({'error': f'需要{role}角色权限'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def json_required(f):
    """要求JSON请求的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': '需要JSON格式的请求'}), 400
        return f(*args, **kwargs)
    return decorated_function

def cache_control(max_age=3600):
    """设置缓存控制的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            response.headers['Cache-Control'] = f'public, max-age={max_age}'
            return response
        return decorated_function
    return decorator 