/**
 * 连接思考过程 WebSocket
 * @param {Object} options
 * @param {string} options.chatSessionId
 * @param {string} options.chatId
 * @param {Function} [options.onMessage]
 * @param {Function} [options.onClose]
 * @param {Function} [options.onError]
 * @returns {{ close: Function }}
 */
export function connectChatWebSocket({chatSessionId, chatId, host, onMessage, onClose, onError}) {

  //const wsBase = 'ws://47.111.6.75:8090';
  const wsBase = ''//process.env.VUE_APP_WS_API

  const path = `/api/websocket/${chatSessionId}@${chatId}`;
  const url = `${wsBase}${path}?host=${host}`;

  const ws = new WebSocket(url);
  let closed = false;

  const close = () => {
    if (closed) return;
    closed = true;
    if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
      ws.close();
    }
  };

  ws.onmessage = event => {
    let data;
    try {
      data = JSON.parse(event.data);
    } catch {
      data = {raw: event.data};
    }

    onMessage && onMessage(data);

    if (data.metadata && data.metadata.close) {
      close();
      onClose && onClose(data);
    }
  };

  ws.onerror = event => {
    onError && onError(event);
  };

  ws.onclose = () => {
    if (!closed) {
      closed = true;
      onClose && onClose();
    }
  };

  return {close};
}
