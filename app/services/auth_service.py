"""用户认证业务逻辑"""

from app import db
from app.models.user import User
from app.utils.security import validate_username, validate_password
from flask_login import login_user, logout_user


class AuthService:
    """处理注册、登录、登出、密码修改"""

    @staticmethod
    def register(username: str, password: str, email: str = None) -> tuple[bool, str]:
        """用户注册"""
        # 验证输入
        valid, msg = validate_username(username)
        if not valid:
            return False, msg
        valid, msg = validate_password(password)
        if not valid:
            return False, msg

        # 检查重名
        if User.query.filter_by(username=username).first():
            return False, '用户名已存在'

        # 创建用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True, '注册成功'

    @staticmethod
    def login(username: str, password: str, remember: bool = False) -> tuple[bool, str]:
        """用户登录"""
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return False, '用户名或密码错误'

        login_user(user, remember=remember)
        return True, '登录成功'

    @staticmethod
    def logout() -> tuple[bool, str]:
        """用户登出"""
        logout_user()
        return True, '已退出登录'

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> tuple[bool, str]:
        """修改密码"""
        if not user.check_password(old_password):
            return False, '原密码错误'

        valid, msg = validate_password(new_password)
        if not valid:
            return False, msg

        user.set_password(new_password)
        db.session.commit()
        return True, '密码修改成功'
