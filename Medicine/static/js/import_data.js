document.addEventListener('DOMContentLoaded', function() {
    const importForm = document.querySelector('.import-container form');
    const fileInput = document.getElementById('file');
    const messageContainer = document.getElementById('message-container'); // 使用静态的消息容器

    if (importForm) {
        importForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const file = fileInput.files[0];
            if (!file) {
                showMessage('请选择要上传的文件', 'alert-warning');
                return;
            }

            // 检查文件类型
            if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
                showMessage('只支持Excel文件(.xlsx, .xls)', 'alert-danger');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            // 显示加载状态
            const submitButton = importForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 导入中...';
            submitButton.disabled = true;

            // 使用Axios发送请求
            axios.post('/import', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then(function(response) {
                // 成功响应处理
                const message = response.data.message || '导入成功';
                if (response.data.status === 'success') {
                    showMessage(message, 'alert-success');
                    importForm.reset(); // 清空表单
                } else {
                    // 如果 status 不是 success，但 message 存在
                    showMessage(message, 'alert-danger');
                }
            })
            .catch(function(error) {
                // 错误响应处理
                let errorMessage = '导入过程中发生错误';
                if (error.response) {
                    // 服务器返回了错误响应
                    // 从 error.response.data 中提取 message
                    errorMessage = error.response.data.message || errorMessage;
                } else if (error.request) {
                    // 请求已发出但没有收到响应
                    errorMessage = '服务器无响应，请稍后再试';
                } else {
                    // 设置请求时出错
                    errorMessage = error.message;
                }
                showMessage(errorMessage, 'alert-danger');
            })
            .finally(function() {
                // 恢复按钮状态
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            });
        });
    }

    function showMessage(message, alertClass) {
        // 清除之前的消息
        messageContainer.className = 'alert mt-3 ' + alertClass;
        messageContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // 显示消息
        messageContainer.style.display = 'block';

        // 自动隐藏消息（可选，5秒后隐藏）
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 5000);
    }
});