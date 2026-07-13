import request from '@/utils/request';

/**
 * 智能问数查询
 * @param {Object} data
 * @param {string} data.aicode - 智能体编码
 * @param {string} data.question - 用户问题
 * @param {string} [data.chatSessionId] - 会话ID，不传则新建会话
 */
export function sendChat(data) {
  return request({
    url: '/api/v1/chat-server/chat',
    method: 'post',
    data,
  });
}

/**
 * 获取某次对话的完整执行结果
 * @param {Object} params
 * @param {string} params.chatSessionId - 会话 ID
 * @param {string} params.chatId - 对话 ID
 */
export function getChatInfo(params) {
  return request({
    url: '/api/v1/chat/info',
    method: 'get',
    params,
  });
}

/**
 * 获取历史会话记录列表（按更新时间分组）
 * @returns {Promise<Object>} 分组 Map，key 为 today / yesterday / lastWeek 等
 */
export function getChatSessionList() {
  return request({
    url: '/api/v1/chat/session/list',
    method: 'get',
  });
}

/**
 * 获取会话历史记录详情
 * @param {Object} params
 * @param {string} params.chatSessionId - 会话 ID
 */
export function getChatSessionInfo(params) {
  return request({
    url: '/api/v1/chat/session/info',
    method: 'get',
    params,
  });
}

/**
 * 删除会话及其下所有问答记录
 * @param {string} sessionId - 会话 ID
 */
export function deleteChatSession(sessionId) {
  return request({
    url: `/api/v1/chat/session/del/${sessionId}`,
    method: 'get',
  });
}

/**
 * 查询/下载数据
 * @param {Object} data - GetData 入参
 */
export function getData(data) {
  return request({
    url: '/api/v1/chat-server/getdata',
    method: 'post',
    data,
  });
}
