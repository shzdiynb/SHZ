document.addEventListener('DOMContentLoaded', function() {
    // 登录表单处理
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    // 显示错误消息
    function showError(message, duration = 3000) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';

            // 自动隐藏错误信息
            if (duration > 0) {
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, duration);
            }
        }
    }

    // 清除错误消息
    function clearError() {
        if (errorMessage) {
            errorMessage.style.display = 'none';
            errorMessage.textContent = '';
        }
    }

    // 表单提交处理
    if (loginForm) {
        // 输入框获取焦点时清除错误
        usernameInput.addEventListener('focus', clearError);
        passwordInput.addEventListener('focus', clearError);

        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // 获取表单数据
            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            // 前端验证
            if (!username || !password) {
                showError('用户名和密码不能为空');
                return;
            }

            try {
                // 显示加载状态
                const submitBtn = loginForm.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.textContent = '登录';

                // 发送登录请求
                const response = await axios.post('/login', {
                    username: username,
                    password: password
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                // 处理响应
                if (response.data.success) {
                    // 登录成功，跳转
                    window.location.href = response.data.redirect || '/dashboard';
                } else {
                    showError(response.data.message || '登录失败');
                }
            } catch (error) {
                // 错误处理
                if (error.response) {
                    // 服务器返回的错误
                    const errorData = error.response.data;
                    showError(errorData.message || `错误: ${error.response.status}`);

                    // 特定错误处理
                    if (errorData.error === 'invalid_credentials') {
                        passwordInput.value = '';
                        passwordInput.focus();
                    }
                } else {
                    // 网络或其他错误
                    showError('网络错误，请稍后重试');
                    console.error('Login error:', error);
                }
            } finally {
                // 恢复按钮状态
                const submitBtn = loginForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                }
            }
        });
    }

    // 导航栏交互逻辑（保持不变）
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