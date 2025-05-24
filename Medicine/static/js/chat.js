document.addEventListener('DOMContentLoaded', function() {
    const chatList = document.getElementById('chat-list');
    const loadingIndicator = document.getElementById('loading-indicator');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    let currentPage = 1;
    const itemsPerPage = 10;
    let totalPages = 1;

    document.getElementById('chatreview-btn').addEventListener('click', function() {
    if (!confirm('确定要对所有用户问题进行安全审核吗？')) return;

    // 调用后端接口进行审核
    axios.post('/api/chatreview')
        .then(response => {
            alert('审核完成！');
            // 可以重新加载聊天记录，刷新状态列显示
            loadChatData();  // 你的已有函数，刷新表格
        })
        .catch(error => {
            alert('审核失败：' + (error.response?.data?.message || error.message));
        });
});


    // 加载提问数据
    async function loadQuestions(page = 1) {
        try {
            console.log('开始加载数据，页码:', page); // 调试日志
            loadingIndicator.style.display = 'block';
            chatList.innerHTML = '';

            const response = await axios.get('/api/chat', { // 假设API端点为 /api/chat
                params: { page, limit: itemsPerPage }
            });

            console.log('API响应数据:', response.data); // 调试日志

            // 确保响应数据包含chats字段
            if (!response.data || !response.data.chats) {
                throw new Error('响应数据格式不正确');
            }

            renderQuestions(response.data.chats);
            totalPages = response.data.total_pages || 1;
            updatePagination();

        } catch (error) {
            console.error('加载提问失败:', error);
            const errorMsg = error.response?.data?.error || error.message;
            alert(`加载提问数据失败: ${errorMsg}`);

            // 显示无数据状态
            chatList.innerHTML = `
                <tr>
                    <td colspan="7" class="error-message">
                        ${errorMsg || '无法加载数据，请稍后重试'}
                    </td>
                </tr>
            `;
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    // 渲染提问列表
    function renderQuestions(chats) {
        try {
            console.log('渲染提问数据:', chats); // 调试日志

            if (!chats || chats.length === 0) {
                chatList.innerHTML = `
                    <tr>
                        <td colspan="7" class="no-data">暂无提问数据</td>
                    </tr>
                `;
                return;
            }

            chatList.innerHTML = chats.map(chat => {
                // 处理日期格式
                const updatedAt = chat.updated_at ?
                    new Date(chat.updated_at).toLocaleString('zh-CN') :
                    '未知时间';

                return `
                    <tr data-id="${chat.id}">
                        <td>${chat.id}</td>
                        <td>${chat.user_name || '匿名'}</td>
                        <td>${chat.email || '未知邮箱'}</td>
                        <td class="content-cell">${chat.question}</td>
                        <td class="content-cell">${chat.answer || '暂无回答'}</td>
                        <td>
                            <select class="permission-select" 
                                    data-chat-id="${chat.id}">
                                <option value="0" ${chat.permission === 0 ? 'selected' : ''}>0</option>
                                <option value="1" ${chat.permission === 1 ? 'selected' : ''}>1</option>
                            </select>
                        </td>
                        <td><span class="status-${chat.flag}">${chat.flag !== undefined && chat.flag !== null ? chat.flag : ''}</span></td>
                    </tr>
                `;
            }).join('');

        } catch (error) {
            console.error('渲染数据时出错:', error);
            chatList.innerHTML = `
                <tr>
                    <td colspan="7" class="error-message">
                        渲染数据时出错: ${error.message}
                    </td>
                </tr>
            `;
        }
    }

    // 更新分页状态
    function updatePagination() {
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
        pageInfo.textContent = `第${currentPage}页 / 共${totalPages}页`;
    }

    // 修改权限更新函数
    async function updatePermission(selectElem) {
        const chatId = selectElem.getAttribute('data-chat-id');
        const newPermission = selectElem.value;

    //     try {
    //         const response = await axios.post(`/api/chat/${chatId}/permission`, {
    //             permission: newPermission
    //         });

    //         if (response.data.success) {
    //             alert('权限更新成功');
    //         } else {
    //             alert('权限更新失败: ' + (response.data.message || '未知错误'));
    //         }
    //     } catch (error) {
    //         console.error('更新权限失败:', error);
    //         const errorMsg = error.response?.data?.error || error.message;
    //         alert(`更新权限失败: ${errorMsg}`);
    //     }
       }

    // 初始化加载第一页数据
    loadQuestions();

    // 绑定分页按钮事件
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadQuestions(currentPage);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadQuestions(currentPage);
        }
    });

    // 绑定权限选择事件
    chatList.addEventListener('change', async (event) => {
        if (event.target.classList.contains('permission-select')) {
            await updatePermission(event.target);
        }
    });
});