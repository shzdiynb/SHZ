document.addEventListener('DOMContentLoaded', function() {
    // 可以在这里添加交互逻辑
    console.log('Admin system loaded');

    // 示例：导航栏hover效果
    const sidebar = document.querySelector('.sidebar');
    const navLinks = document.querySelectorAll('.nav a');

    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            if (window.innerWidth <= 768) {
                sidebar.style.width = '250px';
            }
        });

        link.addEventListener('mouseleave', function() {
            if (window.innerWidth <= 768) {
                sidebar.style.width = '60px';
            }
        });
    });
});