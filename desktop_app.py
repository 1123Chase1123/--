"""
考研知识点复习系统 —— 桌面应用启动器（无控制台模式）
"""

import threading
import sys
import os
import time
import urllib.request
import webbrowser
import traceback

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

HOST = '127.0.0.1'


def _get_exe_dir():
    """获取 exe 所在目录（用于写日志文件）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))


def _log_error(msg):
    """写错误日志到 exe 旁边的 debug_log.txt"""
    log_path = os.path.join(_get_exe_dir(), 'debug_log.txt')
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f'\n[{time.strftime("%Y-%m-%d %H:%M:%S")}] {msg}\n')
    except Exception:
        pass
    return log_path


def _find_free_port(start=5000, end=5010):
    """从 start 到 end 找第一个可用端口"""
    import socket
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, port))
                return port
            except OSError:
                continue
    return None


def _msgbox(title, text):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, text, title, 0)
    except Exception:
        pass


def start_flask(port):
    from app import create_app
    flask_app = create_app()
    flask_app.run(host=HOST, port=port, debug=False, use_reloader=False)


def wait_for_flask(url, timeout=15):
    for _ in range(timeout * 2):
        try:
            urllib.request.urlopen(f'{url}/auth/login', timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def keep_alive():
    while threading.active_count() > 1:
        time.sleep(1)


def main():
    # ===== 找可用端口 =====
    port = _find_free_port()
    if port is None:
        _msgbox('启动失败', '端口 5000-5010 全部被占用，无法启动')
        _log_error('All ports 5000-5010 are occupied')
        return

    server_url = f'http://{HOST}:{port}'

    # ===== 启动 Flask =====
    def start_with_log():
        try:
            start_flask(port)
        except Exception as e:
            tb = traceback.format_exc()
            log_path = _log_error(f'Flask crashed:\n{tb}')
            _msgbox('启动失败', f'Flask 内部错误\n\n日志已保存至:\n{log_path}')
            # 强退进程，避免卡死
            os._exit(1)

    flask_thread = threading.Thread(target=start_with_log, daemon=True)
    flask_thread.start()

    if not wait_for_flask(server_url):
        _log_error(f'Flask did not respond at {server_url} within timeout')
        _msgbox('启动失败',
                f'Flask 服务器无响应\n\n'
                f'可尝试手动运行:\n'
                f'    python run.py\n'
                f'然后浏览器访问 http://127.0.0.1:5000\n\n'
                f'日志已保存至 exe 所在目录下的 debug_log.txt')
        return

    _log_error(f'Flask started OK at {server_url}')

    # ===== 桌面窗口 =====
    try:
        import webview
        window = webview.create_window(
            title='考研复习系统',
            url=server_url,
            width=1200,
            height=800,
            min_size=(900, 600),
            resizable=True,
            fullscreen=False,
            text_select=True,
        )

        # 关闭窗口时中文确认对话框
        def on_closing():
            import ctypes
            ret = ctypes.windll.user32.MessageBoxW(
                0, '确定要退出考研复习系统吗？', '确认关闭', 4  # 4 = 是/否
            )
            return ret == 6  # 6 = 是

        window.events.closing += on_closing
        webview.start()

    except Exception as e:
        tb = traceback.format_exc()
        _log_error(f'WebView failed, fallback to browser:\n{tb}')
        webbrowser.open(server_url)
        _msgbox(
            '提示',
            f'桌面窗口启动失败，已自动打开浏览器。\n\n'
            f'关闭此窗口即可停止服务器。\n\n'
            f'详情请查看 debug_log.txt'
        )
        keep_alive()


if __name__ == '__main__':
    main()
