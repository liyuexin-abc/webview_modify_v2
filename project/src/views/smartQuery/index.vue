<!-- 智能问数仪表盘页面：编排侧边栏、查询面板与对话输入的整体交互逻辑 -->
<template>
  <div class="dashboard smart-query">
    <AgentSidebar
      ref="sidebar"
      :session-groups="sessionGroups"
      :active-session-id="activeSessionId"
      :active-agent-id="selectedAgent && selectedAgent.id"
      :session-loading="sessionLoading"
      @select-agent="handleSelectAgent"
      @select-session="handleSelectSession"
      @delete-session="handleDeleteSession"
      @add-agent="handleAddAgent"
      @edit-agent="handleEditAgent"
      @new-session="handleNewSession"
    />

    <div class="dashboard__body">
      <main ref="mainContent" v-loading="sessionDetailLoading" class="dashboard__main">
        <div v-if="showWelcome" class="dashboard__welcome-panel">
          <ChatWelcome :agent="selectedAgent" />
          <ChatInput welcome :loading="chatLoading" @send="handleChatSend" />
        </div>
        <QueryPanel
          v-else
          :agent="selectedAgent"
          :chat-rounds="chatRounds"
          :pending-query-text="pendingQueryText"
          :view-types="viewTypes"
          :filter-operators="filterOperators"
          :streaming-thinking="streamingThinking"
          :thinking-loading="chatLoading"
          :result-ready="resultReady"
          @remove-dimension="handleRemoveDimension"
          @remove-metric="handleRemoveMetric"
          @search="handleSearch"
          @download="handleDownload"
          @show-sql="handleShowSql"
          @change-view="handleChangeView"
        />
      </main>

      <ChatInput v-if="!showWelcome" :loading="chatLoading" @send="handleChatSend" />
    </div>

    <AgentConfigDialog
      :visible.sync="agentConfigVisible"
      :agent="editingAgent"
      @saved="handleAgentConfigSaved"
    />
  </div>
</template>

<script>
import AgentSidebar from './components/AgentSidebar.vue';
import AgentConfigDialog from './components/AgentConfigDialog.vue';
import QueryPanel from './components/QueryPanel.vue';
import ChatInput from './components/ChatInput.vue';
import ChatWelcome from './components/ChatWelcome.vue';
import {sendChat, getChatInfo, getChatSessionList, getChatSessionInfo, getData, deleteChatSession} from '@/api/smartQuery/chat';
import {connectChatWebSocket} from '@/views/smartQuery/utils/chatWebSocket.js';

/** 历史会话分组配置，key 与接口返回字段一致 */
const SESSION_GROUP_CONFIG = [
  {key: 'today', label: '今天'},
  {key: 'yesterday', label: '昨天'},
  {key: 'lastWeek', label: '近7天'},
  {key: 'lastMonth', label: '近30天'},
  {key: 'lastSixMonth', label: '近半年'},
  {key: 'moreThanSixMonth', label: '半年以上'},
];

/** 查询结果视图类型选项 */
const VIEW_TYPES = [
  {label: '表格', value: 'table'},
  // {label: '柱状图', value: 'bar'},
  // {label: '折线图', value: 'line'},
];

/** 筛选器运算符选项 */
const FILTER_OPERATORS = ['大于', '小于', '等于', '不等于', '包含'];

/** 接口 operator 枚举与展示文案映射 */
const FILTER_OPERATOR_MAP = {
  0: '大于',
  1: '小于',
  2: '等于',
  7: '不等于',
  8: '包含',
};

/** 展示文案与接口 operator 枚举反向映射 */
const FILTER_OPERATOR_REVERSE_MAP = {
  大于: 0,
  小于: 1,
  等于: 2,
  不等于: 7,
  包含: 8,
};

/** 视图类型与 chartType 枚举映射 */
const CHART_TYPE_MAP = {
  table: 1,
  bar: 2,
  line: 3,
};

/** AI 结果 stepType 与展示文案映射 */
const CONTENT_TYPE = {
  query: '查询',
  compute: '计算',
  analyze: '分析',
  summarize: '总结',
};

export default {
  name: 'DataDashboard',
  components: {
    AgentSidebar,
    AgentConfigDialog,
    QueryPanel,
    ChatInput,
    ChatWelcome,
  },
  data() {
    return {
      // 智能体
      selectedAgent: null,
      agentConfigVisible: false,
      editingAgent: null,

      // 历史会话
      sessionList: {},
      activeSessionId: null,
      sessionLoading: false,
      sessionDetailLoading: false,

      // 查询展示
      chatRounds: [],
      pendingQueryText: '',
      resultReady: false,

      // 对话会话
      chatSessionId: null,
      currentChatId: null,
      chatLoading: false,
      streamingThinking: '',
      chatWs: null,
      wsShouldFetchOnClose: false,

      // 静态配置
      viewTypes: VIEW_TYPES,
      filterOperators: FILTER_OPERATORS,
    };
  },
  computed: {
    sessionGroups() {
      return SESSION_GROUP_CONFIG.map(({key, label}) => ({
        key,
        label,
        sessions: this.sessionList[key] || [],
      }));
    },
    showWelcome() {
      return !this.chatRounds.length && !this.pendingQueryText && !this.streamingThinking && !this.chatLoading && !this.resultReady;
    },
  },
  mounted() {
    this.fetchChatSessionList();
  },
  beforeDestroy() {
    this.closeChatWebSocket();
  },
  methods: {
    // ---------- 智能体与侧边栏 ----------

    handleSelectAgent(agent) {
      this.selectedAgent = agent;
      this.activeSessionId = null;
      this.chatSessionId = null;
      this.clearDisplayState();
    },

    async fetchChatSessionList() {
      this.sessionLoading = true;
      try {
        this.sessionList = (await getChatSessionList()).data || {};
      } catch (e) {
        this.sessionList = {};
      } finally {
        this.sessionLoading = false;
      }
    },

    handleSelectSession(session) {
      this.activeSessionId = session.id;
      this.chatSessionId = session.chatSessionId;
      this.closeChatWebSocket();
      this.chatLoading = false;
      this.streamingThinking = '';
      this.clearDisplayState();
      this.fetchSessionDetail(session.chatSessionId);
    },

    handleDeleteSession(session) {
      this.$confirm(`确定删除会话「${session.chatName}」吗？该会话下的所有问答记录将一并删除。`, '删除会话', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(async () => {
          await deleteChatSession(session.chatSessionId);
          this.$message.success('删除成功');

          if (this.activeSessionId === session.id) {
            this.closeChatWebSocket();
            this.chatLoading = false;
            this.streamingThinking = '';
            this.activeSessionId = null;
            this.chatSessionId = null;
            this.currentChatId = null;
            this.clearDisplayState();
          }

          this.fetchChatSessionList();
        })
        .catch(() => {});
    },

    clearDisplayState() {
      this.chatRounds = [];
      this.pendingQueryText = '';
      this.resultReady = false;
    },

    async fetchSessionDetail(chatSessionId) {
      this.sessionDetailLoading = true;
      try {
        const data = await getChatSessionInfo({chatSessionId});
        if (!data) {
          this.$message.info('会话不存在');
          return;
        }
        this.applySessionDetail(data.data);
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.sessionDetailLoading = false;
      }
    },

    applySessionDetail(data) {
      if (data.aiBodyCode) {
        const agent = this.$refs.sidebar?.findAgentByCode(data.aiBodyCode);
        if (agent) {
          this.selectedAgent = agent;
        }
      }

      const chatInfo = data.chatInfo || [];
      this.chatRounds = chatInfo
        .map(chat => {
          const parsed = this.parseChatResult(chat);
          return {
            chatId: chat.chatId,
            queryText: parsed.queryText,
            thinkingMessage: parsed.thinkingMessage,
            resultItems: parsed.resultItems,
          };
        })
        .filter(round => round.queryText || round.resultItems.length);

      this.resultReady = this.chatRounds.some(round => round.resultItems.length);
    },

    handleAddAgent() {
      this.editingAgent = null;
      this.agentConfigVisible = true;
    },

    handleEditAgent(agent) {
      this.editingAgent = agent;
      this.agentConfigVisible = true;
    },

    handleAgentConfigSaved() {
      this.$refs.sidebar.refresh();
    },

    handleNewSession(agent) {
      this.closeChatWebSocket();
      this.chatLoading = false;
      this.streamingThinking = '';
      this.selectedAgent = agent;
      this.activeSessionId = null;
      this.chatSessionId = null;
      this.currentChatId = null;
      this.clearDisplayState();
    },

    // ---------- 查询配置 ----------

    handleRemoveDimension(roundIndex, resultIndex, tagIndex) {
      this.chatRounds[roundIndex].resultItems[resultIndex].dimensions.splice(tagIndex, 1);
    },

    handleRemoveMetric(roundIndex, resultIndex, tagIndex) {
      this.chatRounds[roundIndex].resultItems[resultIndex].metrics.splice(tagIndex, 1);
    },

    async handleSearch(roundIndex, resultIndex, filterData) {
      const item = this.chatRounds[roundIndex].resultItems[resultIndex];
      this.$set(item, 'filter', {...filterData});

      if (!item.dataRequest) {
        this.$message.warning('缺少查询配置，无法搜索');
        return;
      }

      this.$set(item, 'searchLoading', true);
      try {
        this.syncListsFromDisplay(item);
        const params = this.buildGetDataParams(item, filterData);
        const data = await getData(params);
        this.applyGetDataResult(item, data.data);
        this.$message.success('搜索完成');
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.$set(item, 'searchLoading', false);
      }
    },

    handleChangeView(roundIndex, resultIndex, type) {
      this.$set(this.chatRounds[roundIndex].resultItems[resultIndex], 'viewType', type);
    },

    handleDownload(roundIndex, resultIndex) {
      const item = this.chatRounds[roundIndex].resultItems[resultIndex];
      this.$message.info(`开始下载：${item.title || item.typeLabel}`);
    },

    handleShowSql(roundIndex, resultIndex) {
      const sql = this.chatRounds[roundIndex].resultItems[resultIndex]?.sql;
      if (!sql) {
        this.$message.info('暂无 SQL 语句');
        return;
      }
      this.$alert(sql, 'SQL 语句', {confirmButtonText: '确定'});
    },

    // ---------- 对话发送与 WebSocket ----------

    handleChatSend(text) {
      if (this.chatLoading) return;

      if (!this.selectedAgent) {
        this.$message.warning('请先选择智能体');
        return;
      }

      const aicode = this.selectedAgent.aicode || this.selectedAgent.code;
      if (!aicode) {
        this.$message.warning('当前智能体缺少编码');
        return;
      }

      this.resetChatState(text);

      sendChat({
        aicode,
        question: text,
        chatSessionId: this.chatSessionId || undefined,
      })
        .then(data => this.startChatSession(data.data))
        .catch(() => {
          this.chatLoading = false;
        });
    },

    resetChatState(text) {
      // 在历史会话中追加提问时，保留已有对话轮次
      if (!this.chatSessionId || !this.chatRounds.length) {
        this.clearDisplayState();
      }
      this.pendingQueryText = text;
      this.streamingThinking = '';
      this.chatLoading = true;
      this.closeChatWebSocket();
      this.scrollToBottom();
    },

    /** 主内容区滚动到底部 */
    scrollToBottom(smooth = true) {
      this.$nextTick(() => {
        this.$nextTick(() => {
          const el = this.$refs.mainContent;
          if (!el) return;
          el.scrollTo({
            top: el.scrollHeight,
            behavior: smooth ? 'smooth' : 'auto',
          });
        });
      });
    },

    startChatSession({chatSessionId, chatId, host}) {
      this.chatSessionId = chatSessionId;
      this.currentChatId = chatId;
      this.openThinkingWebSocket(chatSessionId, chatId, host);
    },

    openThinkingWebSocket(chatSessionId, chatId, host) {
      this.wsShouldFetchOnClose = true;

      this.chatWs = connectChatWebSocket({
        chatSessionId,
        chatId,
        host,
        onMessage: this.handleWsMessage,
        onClose: () => {
          this.chatWs = null;
          if (this.wsShouldFetchOnClose) {
            this.wsShouldFetchOnClose = false;
            this.fetchChatResult(chatSessionId, chatId);
          }
        },
        onError: () => {
          this.$message.error('思考过程连接异常');
          this.chatWs = null;
        },
      });
    },

    handleWsMessage(msg) {
      const text = this.extractThinkingText(msg);
      if (text) {
        this.streamingThinking = this.streamingThinking ? `${this.streamingThinking}\n${text}` : text;
        this.scrollToBottom(false);
      }
    },

    closeChatWebSocket() {
      this.wsShouldFetchOnClose = false;
      if (this.chatWs) {
        this.chatWs.close();
        this.chatWs = null;
      }
    },

    extractThinkingText(msg) {
      if (!msg || typeof msg !== 'object') return null;
      if (msg.metadata && msg.metadata.close) return null;

      const candidates = [msg.content, msg.text, msg.message, msg.thinking, msg.data && typeof msg.data === 'string' ? msg.data : null, msg.data && msg.data.content, msg.data && msg.data.text];

      return candidates.find(item => typeof item === 'string' && item.trim())?.trim() || null;
    },

    // ---------- 查询结果获取与解析 ----------

    async fetchChatResult(chatSessionId, chatId) {
      try {
        const data = await getChatInfo({chatSessionId, chatId});
        this.applyChatResult(data.data);
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.chatLoading = false;
        this.fetchChatSessionList();
      }
    },

    applyChatResult(data) {
      const parsed = this.parseChatResult(data);

      this.streamingThinking = '';
      const newRound = {
        chatId: data.chatId,
        queryText: parsed.queryText || this.pendingQueryText,
        thinkingMessage: parsed.thinkingMessage,
        resultItems: parsed.resultItems,
      };
      this.pendingQueryText = '';

      const existingIndex = this.chatRounds.findIndex(round => round.chatId === data.chatId);
      if (existingIndex >= 0) {
        this.$set(this.chatRounds, existingIndex, newRound);
      } else {
        this.chatRounds = [...this.chatRounds, newRound];
      }
      this.resultReady = this.chatRounds.some(round => round.resultItems.length);
      this.scrollToBottom();
    },

    /** 取 chatItemInfo 中最后一个 AI 条目的 think.message 作为最终思考过程 */
    extractFinalThinkMessage(data) {
      const items = data?.chatItemInfo || [];
      const aiItems = items.filter(item => item.type === 'ai');
      const lastAiItem = aiItems[aiItems.length - 1];
      return lastAiItem?.think?.message?.trim() || '';
    },

    parseChatResult(data) {
      const items = data?.chatItemInfo || [];
      const userItem = items.find(item => item.type === 'user');
      const aiItems = items.filter(item => item.type === 'ai');

      const resultItems = aiItems.map(item => this.parseAiItem(item)).filter(item => item && item.hasContent);

      return {
        queryText: userItem?.question || '',
        thinkingMessage: this.extractFinalThinkMessage(data),
        resultItems,
        hasResult: resultItems.length > 0,
      };
    },

    parseAiItem(aiItem) {
      const stepType = aiItem.stepType || 'query';
      const typeLabel = CONTENT_TYPE[stepType] || stepType;

      if (stepType === 'summarize') {
        const tablePayload = aiItem.chartData?.dataVO?.data || aiItem.chartData?.dataVO;
        const summaryText = this.extractSummaryText(tablePayload);

        return {
          itemId: aiItem.itemId,
          stepType,
          typeLabel,
          title: aiItem.question || '',
          summaryText,
          hasContent: Boolean(summaryText),
        };
      }

      const result = {
        itemId: aiItem.itemId,
        stepType,
        typeLabel,
        title: aiItem.question || '',
        dimensions: [],
        metrics: [],
        filter: {},
        filterFields: [],
        tableColumns: [],
        tableData: [],
        sql: '',
        viewType: 'table',
        dataRequest: null,
        searchLoading: false,
        hasContent: false,
      };

      const chartData = aiItem.chartData;
      if (!chartData || typeof chartData !== 'object') {
        return result;
      }

      const requestDTO = chartData.dataRequestDTO;
      const tablePayload = chartData.dataVO?.data || chartData.dataVO;

      if (requestDTO) {
        this.fillRequestConfig(result, requestDTO);
        result.dataRequest = JSON.parse(JSON.stringify(requestDTO));
      }

      if (tablePayload) {
        this.fillTableFromPayload(result, tablePayload);
        result.sql = tablePayload.sql || result.sql;
      }

      if (!result.sql && aiItem.think?.message) {
        result.sql = this.extractSqlFromThink(aiItem.think.message);
      }

      if (chartData.total !== undefined && chartData.total !== null && !result.tableData.length) {
        result.tableColumns = [{prop: 'total', label: '结果'}];
        result.tableData = [{total: chartData.total}];
      }

      result.hasContent = Boolean(result.tableColumns.length || result.tableData.length || result.dimensions.length || result.metrics.length || result.sql);

      return result;
    },

    fillRequestConfig(result, requestDTO) {
      if (Array.isArray(requestDTO.dimList)) {
        result.dimensions = requestDTO.dimList.map(item => item.dimName || item.dimKey);
      }

      if (Array.isArray(requestDTO.indexList)) {
        result.metrics = requestDTO.indexList.map(item => item.indName || item.indKey);
      }

      const fieldNames = [...(requestDTO.dimList || []).map(item => item.dimName || item.dimKey), ...(requestDTO.indexList || []).map(item => item.indName || item.indKey)];
      result.filterFields = [...new Set(fieldNames.filter(Boolean))];

      result.filter = this.buildFilterFromRequest(requestDTO);
    },

    buildFilterFromRequest(requestDTO) {
      const filter = {};
      const timeRange = requestDTO.timeRange;

      if (timeRange?.start && timeRange?.end) {
        filter.dateField = requestDTO.dimList?.[0]?.dimName || '日期';
        filter.dateRange = [timeRange.start, timeRange.end];
      }

      const firstFilter = requestDTO.filters?.[0];
      if (firstFilter) {
        filter.field = firstFilter.filterField?.name || firstFilter.filterField?.key || '';
        filter.operator = FILTER_OPERATOR_MAP[firstFilter.operator] || FILTER_OPERATORS[0];
        filter.value = firstFilter.filterValue ?? '';
      }

      return filter;
    },

    /** 同步 UI 上维度/指标变更到 dataRequest */
    syncListsFromDisplay(item) {
      const req = item.dataRequest;
      if (!req) return;

      req.dimList = (req.dimList || []).filter(dim => item.dimensions.includes(dim.dimName || dim.dimKey));
      req.indexList = (req.indexList || []).filter(ind => item.metrics.includes(ind.indName || ind.indKey));
    },

    buildGetDataParams(item, filterData) {
      const base = item.dataRequest || {};
      const params = {
        dimList: base.dimList || [],
        indexList: base.indexList || [],
        dateGranularity: base.dateGranularity || 'day',
        filters: [],
        orderList: base.orderList || [],
        downloadFlag: 0,
        chartType: CHART_TYPE_MAP[item.viewType] || base.chartType || 1,
        pageNo: base.pageNo || base.page || 1,
        pageSize: base.pageSize || 20,
      };

      if (base.top) {
        params.top = base.top;
      }

      if (filterData.dateRange?.length === 2) {
        params.timeRange = {
          start: filterData.dateRange[0],
          end: filterData.dateRange[1],
        };
      } else if (base.timeRange) {
        params.timeRange = {...base.timeRange};
      }

      if (filterData.field && filterData.value !== undefined && filterData.value !== '') {
        params.filters = [
          {
            filterField: this.findFilterField(base, filterData.field),
            operator: FILTER_OPERATOR_REVERSE_MAP[filterData.operator] ?? 0,
            filterValue: String(filterData.value),
            logicType: 0,
          },
        ];
      } else if (Array.isArray(base.filters) && base.filters.length) {
        params.filters = base.filters.map(filter => ({...filter}));
      }

      return params;
    },

    findFilterField(dataRequest, fieldName) {
      const dim = (dataRequest.dimList || []).find(item => item.dimName === fieldName || item.dimKey === fieldName);
      if (dim) {
        return {
          fieldClazz: 0,
          id: dim.id,
          key: dim.dimKey,
          name: dim.dimName,
        };
      }

      const index = (dataRequest.indexList || []).find(item => item.indName === fieldName || item.indKey === fieldName);
      if (index) {
        return {
          fieldClazz: 1,
          id: index.id,
          key: index.indKey,
          name: index.indName,
        };
      }

      const existing = dataRequest.filters?.[0]?.filterField;
      if (existing && (existing.name === fieldName || existing.key === fieldName)) {
        return {...existing};
      }

      return {
        fieldClazz: 0,
        key: fieldName,
        name: fieldName,
      };
    },

    applyGetDataResult(item, data) {
      if (!data) return;

      item.tableColumns = (data.columns || []).map(this.normalizeColumn);
      item.tableData = data.records || [];
      if (data.sql) {
        item.sql = data.sql;
      }

      if (item.dataRequest) {
        if (data.page) item.dataRequest.pageNo = data.page;
        if (data.pageSize) item.dataRequest.pageSize = data.pageSize;
      }
    },

    fillTableFromPayload(result, payload) {
      if (Array.isArray(payload.columns) && Array.isArray(payload.records)) {
        result.tableColumns = payload.columns.map(this.normalizeColumn);
        result.tableData = payload.records;
        return;
      }

      if (Array.isArray(payload.columns) && Array.isArray(payload.rows)) {
        result.tableColumns = payload.columns.map(this.normalizeColumn);
        result.tableData = payload.rows;
      }
    },

    extractSqlFromThink(message) {
      if (!message || typeof message !== 'string') return '';
      const sqlMatch = message.match(/select[\s\S]+?(?:\nlimit|$)/i);
      return sqlMatch ? sqlMatch[0].trim() : '';
    },

    extractSummaryText(payload) {
      if (!payload) return '';

      const rows = payload.rows || payload.records;
      if (!Array.isArray(rows) || !rows.length) return '';

      const row = rows[0];
      if (typeof row === 'string') return row;

      return row.answer || row.summary || row.content || Object.values(row)[0] || '';
    },

    normalizeColumn(col) {
      if (typeof col === 'string') {
        return {prop: col, label: col};
      }
      const prop = col.key || col.field || col.prop || col.name || '';
      const label = col.name || col.title || col.label || prop;
      return {prop, label};
    },
  },
};
</script>

<style lang="scss" scoped>
@use './styles/variables.scss' as *;

.dashboard {
  display: flex;
  width: 100%;
  height: 100%;
  min-height: 0;
  overflow: hidden;
  background-image: radial-gradient(ellipse at 15% 30%, rgba(248, 234, 252, .8) 0%, transparent 45%), radial-gradient(ellipse at 85% 70%, rgba(32, 76, 233, .12) 0%, transparent 45%), radial-gradient(ellipse at 50% 10%, rgba(255, 255, 255, .9) 0%, transparent 50%);

  .dashboard__body {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .dashboard__main {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    padding: 20px 24px;
    scrollbar-width: none;
    -ms-overflow-style: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  .dashboard__welcome-panel {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 74px;
    padding-top: 18vh;
    overflow-y: auto;
  }
}
</style>

<style lang="scss">
@use './styles/theme.scss';
</style>
