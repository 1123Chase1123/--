"""
考研知识点复习系统 —— 启动入口

使用方法：
    python run.py                      # 网页模式（浏览器访问 http://localhost:5000）
    python run.py --desktop            # 桌面模式（弹出原生窗口）
    python desktop_app.py              # 同上，桌面模式
"""

import sys

if __name__ == '__main__':
    # 桌面模式
    if '--desktop' in sys.argv:
        from desktop_app import main
        main()
    # 网页模式（默认）
    else:
        from app import create_app
        app = create_app()
        print('🌐 网页模式已启动')
        print('📌 打开浏览器访问: http://127.0.0.1:5000')
        print('💡 提示: 使用 python run.py --desktop 可启动桌面窗口模式')
        app.run(debug=True, host='0.0.0.0', port=5000)
