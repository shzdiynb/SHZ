document.addEventListener('DOMContentLoaded', function() {
    const feedbackList = document.getElementById('feedback-list');
    const loadingIndicator = document.getElementById('loading-indicator');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    let currentPage = 1;
    const itemsPerPage = 10;
    let totalPages = 1;

    // 加载反馈数据
    async function loadFeedbacks(page = 1) {
        try {
            console.log('开始加载数据，页码:', page); // 调试日志
            loadingIndicator.style.display = 'block';
            feedbackList.innerHTML = '';

            const response = await axios.get('/api/feedback', {
                params: { page, limit: itemsPerPage }
            });

            console.log('API响应数据:', response.data); // 调试日志

            // 确保响应数据包含feedbacks字段
            if (!response.data || !response.data.feedbacks) {
                throw new Error('响应数据格式不正确');
            }

            renderFeedbacks(response.data.feedbacks);
            totalPages = response.data.total_pages || 1;
            updatePagination();

        } catch (error) {
            console.error('加载反馈失败:', error);
            const errorMsg = error.response?.data?.error || error.message;
            alert(`加载反馈数据失败: ${errorMsg}`);

            // 显示无数据状态
            feedbackList.innerHTML = `
                <tr>
                    <td colspan="6" class="error-message">
                        ${errorMsg || '无法加载数据，请稍后重试'}
                    </td>
                </tr>
            `;
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    // 渲染反馈列表
    function renderFeedbacks(feedbacks) {
        try {
            console.log('渲染反馈数据:', feedbacks); // 调试日志

            if (!feedbacks || feedbacks.length === 0) {
                feedbackList.innerHTML = `
                    <tr>
                        <td colspan="6" class="no-data">暂无反馈数据</td>
                    </tr>
                `;
                return;
            }

            feedbackList.innerHTML = feedbacks.map(feedback => {
                // 处理日期格式
                const updatedAt = feedback.updated_at ?
                    new Date(feedback.updated_at).toLocaleString('zh-CN') :
                    '未知时间';

                return `
                    <tr data-id="${feedback.id}">
                        <td>${feedback.id}</td>
                        <td>${feedback.user_name || '匿名'}</td>
                        <td class="content-cell">${feedback.content}</td>
                        <td>
                            <span class="status-badge ${feedback.status}">
                                ${getStatusText(feedback.status)}
                            </span>
                        </td>
                        <td>
                            <select class="status-select" 
                                    data-feedback-id="${feedback.id}"
                                    onchange="updateFeedbackStatus(this)">
                                <option value="pending" ${feedback.status === 'pending' ? 'selected' : ''}>待处理</option>
                                <option value="approved" ${feedback.status === 'approved' ? 'selected' : ''}>已通过</option>
                                <option value="rejected" ${feedback.status === 'rejected' ? 'selected' : ''}>已拒绝</option>
                            </select>
                        </td>
                        <td>${updatedAt}</td>
                    </tr>
                `;
            }).join('');

        } catch (error) {
            console.error('渲染数据时出错:', error);
            feedbackList.innerHTML = `
                <tr>
                    <td colspan="6" class="error-message">
                        渲染数据时出错: ${error.message}
                    </td>
                </tr>
            `;
        }
    }

    // 修改状态更新函数
    window.updateFeedbackStatus = async function(selectElement) {
        const feedbackId = selectElement.dataset.feedbackId;
        const newStatus = selectElement.value;
        selectElement._previousValue = selectElement.value; // 保存原值用于错误恢复

        try {
            // 修改为请求新的API端点
            const response = await axios.patch(`/api/feedback/${feedbackId}`, {
                status: newStatus
            });

            // 更新UI
            const row = document.querySelector(`tr[data-id="${feedbackId}"]`);
            if (row) {
                const statusBadge = row.querySelector('.status-badge');
                statusBadge.className = `status-badge ${newStatus}`;
                statusBadge.textContent = getStatusText(newStatus);

                // 使用API返回的更新时间
                const timeCell = row.querySelector('td:last-child');
                if (response.data.feedback && response.data.feedback.updated_at) {
                    timeCell.textContent = formatDate(response.data.feedback.updated_at);
                }
            }
        } catch (error) {
            console.error('更新状态失败:', error);
            alert('更新状态失败，请稍后重试');
            // 恢复原值
            selectElement.value = selectElement._previousValue;
        }
    };

    // 分页控制
    function updatePagination() {
        pageInfo.textContent = `第${currentPage}页/共${totalPages}页`;
        prevPageBtn.disabled = currentPage <= 1;
        nextPageBtn.disabled = currentPage >= totalPages;
    }

    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadFeedbacks(currentPage);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadFeedbacks(currentPage);
        }
    });

    // 辅助函数
    function getStatusText(status) {
        const statusMap = {
            pending: '待处理',
            approved: '已通过',
            rejected: '已拒绝'
        };
        return statusMap[status] || status;
    }

    function formatDate(date) {
        if (!date) return '';
        const d = new Date(date);
        return d.toLocaleString('zh-CN');
    }

    // 初始化加载
    loadFeedbacks();
});