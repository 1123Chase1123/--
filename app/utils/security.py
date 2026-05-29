"""安全工具函数"""

import re


def validate_username(username: str) -> tuple[bool, str]:
    """验证用户名：3-20位字母数字下划线"""
    if not username or len(username) < 3 or len(username) > 20:
        return False, '用户名长度需在 3-20 个字符之间'
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
        return False, '用户名仅支持字母、数字、下划线和中文'
    return True, ''


def validate_password(password: str) -> tuple[bool, str]:
    """验证密码强度：至少6位"""
    if not password or len(password) < 6:
        return False, '密码长度至少 6 位'
    if len(password) > 128:
        return False, '密码长度不能超过 128 位'
    return True, ''
