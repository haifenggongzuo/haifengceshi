from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .. import admin_bp
from ..models.user import AdminUser

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 在实际应用中，这里应该从 Supabase 验证用户
        if username == 'admin' and password == 'admin123':  # 临时测试用
            user = AdminUser(1, username, 'admin@example.com')
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        
        flash('用户名或密码错误', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html') 