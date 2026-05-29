"""文件上传处理工具"""

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', set())


def save_upload(file_storage, subdir: str = 'images') -> tuple[bool, str]:
    """保存上传文件，返回 (成功, 存储路径/错误信息)"""
    if not file_storage or not file_storage.filename:
        return False, '未选择文件'

    if not allowed_file(file_storage.filename):
        return False, f'不支持的文件类型'

    # UUID 重命名防止冲突
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    safe_name = f'{uuid.uuid4().hex}.{ext}'

    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subdir)
    os.makedirs(upload_dir, exist_ok=True)

    save_path = os.path.join(upload_dir, safe_name)
    file_storage.save(save_path)

    # 返回相对路径（用于数据库存储和模板渲染）
    relative_path = os.path.join('uploads', subdir, safe_name).replace('\\', '/')
    return True, relative_path
