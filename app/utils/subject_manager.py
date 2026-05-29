"""
科目管理器 —— 从 subjects.json 动态读取/写入科目列表

支持运行时新增科目，自动持久化到 JSON 文件。
兼容 PyInstaller 打包：首次运行时从包内复制默认文件到用户数据目录。
"""

import json
import os
import sys
import shutil


def _get_data_dir():
    """
    获取可写数据目录（存放 subjects.json 等用户数据）
    - 开发模式：项目根目录 /database/
    - 打包 exe：exe 所在目录下的 _data/ 文件夹
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，数据存在 exe 旁边
        return os.path.join(os.path.dirname(sys.executable), '_data', 'database')
    else:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database')


def _get_bundled_file():
    """获取包内预置的 subjects.json（仅打包模式有效）"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'database', 'subjects.json')
    return None


_SUBJECTS_FILE = os.path.join(_get_data_dir(), 'subjects.json')

# 默认科目
_DEFAULT_SUBJECTS = [
    '模电', '数电',
    '数学', '英语', '政治', '专业课',
    '数据结构', '计算机组成原理', '操作系统', '计算机网络',
    '其他'
]


def _ensure_file():
    """确保 subjects.json 存在，不存在则从包内复制或创建默认"""
    if os.path.exists(_SUBJECTS_FILE):
        return

    os.makedirs(os.path.dirname(_SUBJECTS_FILE), exist_ok=True)

    # 优先从打包资源复制
    bundled = _get_bundled_file()
    if bundled and os.path.exists(bundled):
        shutil.copy2(bundled, _SUBJECTS_FILE)
        return

    # 否则创建默认
    save_subjects(_DEFAULT_SUBJECTS)


def load_subjects() -> list:
    """读取科目列表"""
    _ensure_file()
    try:
        with open(_SUBJECTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('subjects', _DEFAULT_SUBJECTS[:])
    except (json.JSONDecodeError, FileNotFoundError):
        return _DEFAULT_SUBJECTS[:]


def save_subjects(subjects: list):
    """保存科目列表到文件（去重、保留顺序）"""
    seen = set()
    unique = []
    for s in subjects:
        s = s.strip()
        if s and s not in seen:
            seen.add(s)
            unique.append(s)

    os.makedirs(os.path.dirname(_SUBJECTS_FILE), exist_ok=True)
    with open(_SUBJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'subjects': unique}, f, ensure_ascii=False, indent=2)


def add_subject(subject_name: str) -> bool:
    """新增一个科目，返回是否真正新增（去重）"""
    if not subject_name or not subject_name.strip():
        return False
    name = subject_name.strip()
    subjects = load_subjects()
    if name in subjects:
        return False
    subjects.append(name)
    save_subjects(subjects)
    return True
