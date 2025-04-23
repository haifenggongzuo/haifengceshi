from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from flask_caching import Cache
from flask_mail import Mail

# 初始化扩展
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
babel = Babel()
cache = Cache()
mail = Mail()

def init_extensions(app):
    """初始化所有扩展"""
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    babel.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    
    # 配置登录视图
    login_manager.login_view = 'admin.login'
    login_manager.login_message = '请先登录'
    
    return app 