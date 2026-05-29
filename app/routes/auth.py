"""用户认证路由"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        success, message = AuthService.login(username, password, remember)
        if success:
            flash(message, 'success')
            return redirect(url_for('notes.dashboard'))
        flash(message, 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        email = request.form.get('email', '').strip() or None

        if password != confirm_password:
            flash('两次密码输入不一致', 'danger')
            return render_template('register.html')

        success, message = AuthService.register(username, password, email)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        flash(message, 'danger')

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """登出"""
    AuthService.logout()
    flash('已退出登录', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    if request.method == 'POST':
        old_pwd = request.form.get('old_password', '')
        new_pwd = request.form.get('new_password', '')
        confirm_pwd = request.form.get('confirm_password', '')

        if new_pwd != confirm_pwd:
            flash('两次新密码输入不一致', 'danger')
            return render_template('change_password.html')

        success, message = AuthService.change_password(current_user, old_pwd, new_pwd)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.logout'))
        flash(message, 'danger')

    return render_template('change_password.html')
