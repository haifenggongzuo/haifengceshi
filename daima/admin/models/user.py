from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login_manager

class AdminUser(UserMixin):
    def __init__(self, id, username, email, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.is_active = is_active
        self.last_login = None

    def set_password(self, password):
        # 在实际应用中，这里应该调用 Supabase 更新密码
        pass

    def check_password(self, password):
        # 在实际应用中，这里应该调用 Supabase 验证密码
        pass

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.is_active

@login_manager.user_loader
def load_user(user_id):
    # 在实际应用中，这里应该从 Supabase 加载用户信息
    return None 