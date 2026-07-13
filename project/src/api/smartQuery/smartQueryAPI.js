import request from '@/utils/request'

// 获取历史记录
export function getChatHistoryListAPI() {
  return request({
    url: '/api/v1/chat/session/list',

    method: 'get',
    //params: query
  })
}

// 获取历史记录
export function getChatHistoryListDetailAPI(query) {
    return request({
      url: '/api/v1/chat/session/info',

      method: 'get',
      params: query
    })
  }
  
  export function saveAiBodyAPI(data) {
    return request({
      url: '/api/v1/aibody/save',
      method: 'POST',
      data: data
    });
  }

  //问数
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




  export function getAiBodyListAPI(params) {
    return request({
      url: '/api/v1/aibody/list',
      method: 'get',
      params: params
    });
  }

  export function getAiBodyDetailAPI(code) {
    return request({
      url: '/api/v1/aibody/info/' + code,
      method: 'get',
      //params: params
    });
  }

  export function getAiBodyCandidateTablesAPI(params) {
    return request({
      url: '/api/v1/aibody/candidate-tables',
      method: 'get',
      params: params
    });
  }


  export function deleteAiBodyAPI(code) {
    return request({
      url: '/api/v1/aibody/del/' + code,
      method: 'get',
      //params: params
    });
  }


