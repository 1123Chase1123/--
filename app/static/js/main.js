// 考研知识点复习系统 —— 前端脚本

document.addEventListener('DOMContentLoaded', function () {
    // Flash 消息自动消失
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.5s';
            el.style.opacity = '0';
            setTimeout(function () { el.remove(); }, 500);
        }, 4000);
    });

    // 删除确认
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.dataset.confirm || '确定要执行此操作吗？')) {
                e.preventDefault();
            }
        });
    });
});
