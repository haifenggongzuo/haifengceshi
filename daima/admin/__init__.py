from flask import Blueprint
from flask_login import LoginManager

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
login_manager = LoginManager()

def init_admin(app):
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = '请先登录'
    
    from . import views
    app.register_blueprint(admin_bp)
    
    return app 