/**
 * 开发环境 Mock 数据层（仅 development 引入，见 main.js）
 * - 通过 axios 请求拦截器 + 自定义 adapter 拦截匹配的 URL，返回演示数据
 * - 同时 stub /api/websocket/ 的 WebSocket，模拟"思考过程"推送
 * - 不影响生产构建；未匹配的请求仍走真实后端
 */
import service from '@/utils/request'

// ---------- 演示数据 ----------

const AGENTS = [
  { code: 'agent_sales', name: '销售分析智能体', description: '销售域指标问答' },
  { code: 'agent_finance', name: '财务洞察智能体', description: '财务域指标问答' },
  { code: 'agent_user', name: '用户增长智能体', description: '用户域指标问答' },
]

// 模拟后端返回的"未排版单行 SQL"(与生产环境一致),用于验证前端自动格式化
const SQL_DEMO = "select f.`ptdate` as `ptdate`, f.`org` as `org`, sum(f.`fadianliang`) as `fadianliang` from (select DATE_FORMAT(mainsrc.`data_time`, '%Y-%m-%d') as `ptdate`, mainsrc.`org_name` as `org`, mainsrc.`day_power` as `fadianliang` from `analysis`.`power_org_data` mainsrc) f where 1=1 and f.`ptdate` >= '2024-01-03' and f.`ptdate` <= '2024-01-05' group by f.`ptdate`, f.`org` limit 10 offset 90"

const QUERY_COLUMNS = [
  { key: 'region', name: '地区', unit: '' },
  { key: 'sales_amount', name: '销售额', unit: '万元' },
  { key: 'order_cnt', name: '订单数', unit: '笔' },
]

const REGIONS = ['华东', '华南', '华北', '西南', '华中', '东北', '西北']
const QUERY_RECORDS = REGIONS.map((r, i) => ({
  region: r,
  sales_amount: (9800 - i * 1130 + (i % 3) * 210).toFixed(2),
  order_cnt: 12400 - i * 1500,
}))

function chatInfoPayload(chatId, question) {
  return {
    chatId,
    chatItemInfo: [
      { type: 'user', question },
      {
        type: 'ai',
        stepType: 'query',
        itemId: '查数',
        question: '各地区销售额与订单数（近半年）',
        think: {
          speed: 3.2,
          message:
            '1. 解析问题：识别指标「销售额」「订单数」，维度「地区」，时间范围近半年\n2. 匹配语义模型：dws_sales_order_df\n3. 生成查询 SQL 并执行\n4. 汇总结果并进行归因分析',
        },
        chartData: {
          dataVO: {
            code: 200,
            data: {
              records: QUERY_RECORDS.map((r) => ({ ...r })),
              columns: QUERY_COLUMNS,
              total: QUERY_RECORDS.length,
              sql: SQL_DEMO,
            },
          },
          dataRequestDTO: {
            chartType: 1,
            timeRange: { start: '2026-01-01', end: '2026-06-30' },
            dateGranularity: 'month',
            indexList: [
              { indKey: 'sales_amount', indName: '销售额', id: 101 },
              { indKey: 'order_cnt', indName: '订单数', id: 102 },
            ],
            dimList: [{ dimKey: 'region', dimName: '地区', id: 201 }],
            filters: [],
          },
        },
      },
      {
        type: 'ai',
        stepType: 'analyze',
        itemId: '分析',
        question: '数据归因分析',
        think: {
          speed: 3.2,
          message:
            '1. 解析问题：识别指标「销售额」「订单数」，维度「地区」，时间范围近半年\n2. 匹配语义模型：dws_sales_order_df\n3. 生成查询 SQL 并执行\n4. 汇总结果并进行归因分析',
        },
        chartData: {
          dataVO: {
            columns: [{ name: 'entity' }, { name: 'analysis_result' }],
            rows: [
              {
                entity: '华东地区',
                analysis_result:
                  '销售额 **9800 万元** 居首，占整体约 23%，主要由新品上市带动，环比增长 12.4%。',
              },
              {
                entity: '西北地区',
                analysis_result:
                  '销售额偏低，订单转化率较均值低 3.1pct，建议关注渠道覆盖率。',
              },
            ],
          },
        },
      },
      {
        type: 'ai',
        stepType: 'summarize',
        itemId: '总结',
        question: '结论总结',
        think: {
          speed: 3.2,
          message:
            '1. 解析问题：识别指标「销售额」「订单数」，维度「地区」，时间范围近半年\n2. 匹配语义模型：dws_sales_order_df\n3. 生成查询 SQL 并执行\n4. 汇总结果并进行归因分析',
        },
        chartData: {
          dataVO: {
            rows: [
              {
                answer:
                  '近半年整体销售呈稳步上升趋势：华东、华南贡献了近 45% 的销售额；订单数与销售额走势基本一致。建议加大西北区域渠道投入，并持续跟踪新品复购率。',
              },
            ],
          },
        },
      },
    ],
  }
}

let chatSeq = 0
const pendingQuestions = {}

const HISTORY_GROUPS = {
  today: [
    { aiBodyCode: 'agent_sales', chatSessionId: 'sess_demo_1', chatName: '各地区销售额对比' },
    { aiBodyCode: 'agent_sales', chatSessionId: 'sess_demo_2', chatName: '近半年订单趋势' },
  ],
  yesterday: [
    { aiBodyCode: 'agent_sales', chatSessionId: 'sess_demo_3', chatName: '华东销售额归因' },
    { aiBodyCode: 'agent_finance', chatSessionId: 'sess_demo_4', chatName: '毛利率月度分析' },
  ],
  lastWeek: [
    { aiBodyCode: 'agent_sales', chatSessionId: 'sess_demo_5', chatName: 'TOP10 城市销售排行' },
  ],
  lastMonth: [],
  lastSixMonth: [],
  moreThanSixMonth: [],
}

function pageList(list, params = {}) {
  const page = Number(params.page || 1)
  const pageSize = Number(params.pageSize || 10)
  return {
    page,
    pageSize,
    total: list.length,
    list: list.slice((page - 1) * pageSize, page * pageSize),
  }
}

const now = '2026-07-10 14:32:00'

const DATA_SOURCES = [
  { id: 1, name: '生产集市-MySQL', dbType: 'MySQL', host: '10.20.1.15', port: 3306, displayDbSchema: 'dws_mart' },
  { id: 2, name: '分析仓-Doris', dbType: 'Doris', host: '10.20.1.32', port: 9030, displayDbSchema: 'ads' },
]
const DATA_MODELS = [
  { id: 1, name: '销售订单模型', factTableName: 'dws_sales_order_df', sourceName: '生产集市-MySQL', dimTableCount: 4, updatedAt: now },
  { id: 2, name: '用户行为模型', factTableName: 'dws_user_action_df', sourceName: '分析仓-Doris', dimTableCount: 3, updatedAt: now },
]
const DIMENSIONS = [
  { id: 201, chineseName: '地区', englishName: 'region', updatedAt: now },
  { id: 202, chineseName: '渠道', englishName: 'channel', updatedAt: now },
  { id: 203, chineseName: '商品类目', englishName: 'category', updatedAt: now },
]
const METRICS = [
  { id: 101, chineseName: '销售额', englishName: 'sales_amount', unit: '万元', type: '原子指标', status: 1, caliber: '订单实付金额汇总', principalName: '张敏', updatedAt: now },
  { id: 102, chineseName: '订单数', englishName: 'order_cnt', unit: '笔', type: '原子指标', status: 1, caliber: '去重订单号计数', principalName: '李航', updatedAt: now },
]
const GROUPS = [
  { id: 1, groupCode: 'G_SALES', groupName: '销售核心指标组', subjectDomain: '销售域', fieldCount: 6, statusName: '已上线' },
]
const MAPPING_TABLES = [
  { id: 1, tbName: 'dws_sales_order_df', cnName: '销售订单宽表', sourceName: '生产集市-MySQL', tbTypeName: '物理表', typeKey: 'physical', mappedCount: 12, statusName: '已注册' },
]
const TREE_DIM = DIMENSIONS.map((d) => ({ id: d.id, key: d.englishName, name: d.chineseName }))
const TREE_METRIC = METRICS.map((m) => ({ id: m.id, key: m.englishName, name: m.chineseName }))

// ---------- 路由表 ----------

function ok(data) { return { code: 200, message: 'success', data } }

const routes = [
  {
    match: (u, m) => m === 'post' && u.includes('/upc/user/login'),
    handle: () => ({
      code: 1,
      message: 'success',
      data: {
        token: 'mock-token-demo',
        user: { userId: 1, name: 'demo', userName: 'demo', nickName: '演示用户' },
      },
    }),
  },
  { match: (u) => u.includes('/api/v1/aibody/list'), handle: (u, m, p) => ok(pageList(AGENTS, p)) },
  {
    match: (u) => u.includes('/api/v1/aibody/info/'),
    handle: (u) => {
      const code = u.split('/api/v1/aibody/info/')[1].split('?')[0]
      const a = AGENTS.find((x) => x.code === code) || AGENTS[0]
      return ok({ ...a, aicode: a.code, tableRelations: [], knowledgeList: [] })
    },
  },
  {
    match: (u) => u.includes('/api/v1/aibody/candidate-tables'),
    handle: (u) => {
      const sid = /sourceId=(\d+)/.test(u) ? Number(RegExp.$1) : 1
      return ok([
        { relationId: sid * 10 + 1, sourceId: sid, tableName: 'dws_sales_order_df', tableComment: '销售订单宽表' },
        { relationId: sid * 10 + 2, sourceId: sid, tableName: 'dim_region', tableComment: '区域维表' },
        { relationId: sid * 10 + 3, sourceId: sid, tableName: 'dim_product', tableComment: '商品维表' },
        { relationId: sid * 10 + 4, sourceId: sid, tableName: 'dws_user_action_df', tableComment: '用户行为宽表' },
      ])
    },
  },
  {
    match: (u) => u.includes('/api/v1/field-mappings/data-sources'),
    handle: () => ok(DATA_SOURCES),
  },
  {
    match: (u, m) => m === 'post' && u.includes('/api/v1/field-mappings/tables/parse'),
    handle: () =>
      ok([
        { fieldKey: 'patient_id', fieldType: 'BIGINT', fieldName: '患者ID', compareStatus: 0 },
        { fieldKey: 'patient_name', fieldType: 'VARCHAR', fieldName: '患者姓名', compareStatus: 0 },
        { fieldKey: 'visit_cnt', fieldType: 'INT', fieldName: '就诊次数', compareStatus: 1 },
        { fieldKey: 'total_fee', fieldType: 'DECIMAL', fieldName: '总费用', compareStatus: 1 },
      ]),
  },
  {
    match: (u, m) => m === 'post' && u.includes('/api/v1/field-mappings/tables/register-view'),
    handle: () => ok(true),
  },
  { match: (u) => u.includes('/api/v1/aibody/save'), handle: () => ok(true) },
  { match: (u) => u.includes('/api/v1/aibody/del/'), handle: () => ok(true) },

  { match: (u) => u.includes('/api/v1/chat/session/list'), handle: () => ok(HISTORY_GROUPS) },
  {
    match: (u) => u.includes('/api/v1/chat/session/info'),
    handle: (u) => {
      const sid = (u.split('chatSessionId=')[1] || 'sess_demo_1').split('&')[0]
      return ok({
        chatSessionId: sid,
        chatInfo: [chatInfoPayload('chat_hist_1', '近半年各地区的销售额和订单数是多少？')],
      })
    },
  },
  { match: (u) => u.includes('/api/v1/chat/session/del/'), handle: () => ok(true) },
  {
    match: (u, m) => m === 'post' && u.includes('/api/v1/chat-server/chat'),
    handle: (u, m, p, data) => {
      chatSeq += 1
      const chatId = `chat_${chatSeq}`
      pendingQuestions[chatId] = (data && data.question) || '数据查询'
      return ok({
        chatSessionId: (data && data.chatSessionId) || `sess_${Date.now()}`,
        chatId,
        host: 'mock',
      })
    },
  },
  {
    match: (u) => u.includes('/api/v1/chat/info'),
    handle: (u) => {
      const chatId = (u.split('chatId=')[1] || 'chat_1').split('&')[0]
      return ok(chatInfoPayload(chatId, pendingQuestions[chatId] || '近半年各地区的销售额和订单数是多少？'))
    },
  },
  {
    match: (u, m) => m === 'post' && (u.includes('/api/v1/chat-server/getdata') || u.includes('/api/v1/chat-server/group/preview')),
    handle: (u, m, p, data) => ok({
      page: (data && data.page) || 1,
      pageSize: (data && data.pageSize) || 10,
      total: QUERY_RECORDS.length,
      columns: QUERY_COLUMNS,
      records: QUERY_RECORDS.map((r) => ({ ...r })),
      sql: SQL_DEMO,
    }),
  },
  {
    match: (u, m) => m === 'post' && u.includes('/api/v1/report-preview/dim-metric'),
    handle: (u, m, p, data) => ok((data && data.type) === 'metric' ? TREE_METRIC : TREE_DIM),
  },

  { match: (u, m) => m === 'get' && /\/api\/v1\/data-sources(\?|$)/.test(u), handle: (u, m, p) => ok(pageList(DATA_SOURCES, p)) },
  { match: (u, m) => m === 'get' && /\/api\/v1\/data-models(\?|$)/.test(u), handle: (u, m, p) => ok(pageList(DATA_MODELS, p)) },
  {
    match: (u) => u.includes('/api/v1/dimensions/page'),
    handle: (u, m, p) => ok({ ...pageList(DIMENSIONS, p), records: DIMENSIONS }),
  },
  { match: (u, m) => m === 'get' && /\/api\/v1\/metrics(\?|$)/.test(u), handle: (u, m, p) => ok({ ...pageList(METRICS, p), records: METRICS }) },
  { match: (u) => u.includes('/api/v1/indicator-groups/list'), handle: (u, m, p) => ok(pageList(GROUPS, p)) },
  { match: (u, m) => m === 'get' && /\/api\/v1\/field-mappings\/tables(\?|$)/.test(u), handle: (u, m, p) => ok(pageList(MAPPING_TABLES, p)) },
  { match: (u) => u.includes('/api/v1/meta/collect-log/page'), handle: (u, m, p) => ok(pageList([], p)) },
  { match: (u) => u.includes('/api/v1/meta/db-type/list'), handle: () => ok(['MySQL', 'Doris', 'PostgreSQL']) },
]

// ---------- axios adapter 注入 ----------

function parseQuery(url) {
  const q = url.split('?')[1]
  if (!q) return {}
  const out = {}
  q.split('&').forEach((kv) => {
    const [k, v] = kv.split('=')
    if (k) out[decodeURIComponent(k)] = decodeURIComponent(v || '')
  })
  return out
}

service.interceptors.request.use((config) => {
  const url = config.url || ''
  const method = (config.method || 'get').toLowerCase()
  const route = routes.find((r) => r.match(url, method))
  if (route) {
    config.adapter = () => {
      let body = config.data
      if (typeof body === 'string') {
        try { body = JSON.parse(body) } catch (e) { /* ignore */ }
      }
      const data = route.handle(url, method, parseQuery(url), body)
      return new Promise((resolve) => {
        setTimeout(() => resolve({
          data,
          status: 200,
          statusText: 'OK',
          headers: {},
          config,
          request: { responseType: config.responseType },
        }), 120)
      })
    }
  }
  return config
})

// ---------- WebSocket stub（思考过程流式推送） ----------

const NativeWebSocket = window.WebSocket
const THINK_LINES = [
  '正在理解您的问题…',
  '已识别指标：销售额、订单数；维度：地区',
  '已匹配语义模型 dws_sales_order_df，正在生成 SQL',
  '查询执行完成，正在进行数据分析与总结',
]

class MockWebSocket {
  constructor(url) {
    this.url = url
    this.readyState = 0
    setTimeout(() => {
      this.readyState = 1
      this.onopen && this.onopen()
      THINK_LINES.forEach((line, i) => {
        setTimeout(() => {
          if (this.readyState !== 1) return
          this.onmessage && this.onmessage({ data: JSON.stringify({ content: line }) })
          if (i === THINK_LINES.length - 1) {
            this.onmessage && this.onmessage({ data: JSON.stringify({ metadata: { close: true } }) })
            this.close()
          }
        }, 450 * (i + 1))
      })
    }, 200)
  }
  send() {}
  close() {
    if (this.readyState === 3) return
    this.readyState = 3
    this.onclose && this.onclose()
  }
}
MockWebSocket.OPEN = 1
MockWebSocket.CONNECTING = 0

window.WebSocket = function (url, protocols) {
  if (typeof url === 'string' && url.includes('/api/websocket/')) {
    return new MockWebSocket(url)
  }
  return protocols ? new NativeWebSocket(url, protocols) : new NativeWebSocket(url)
}
window.WebSocket.prototype = NativeWebSocket.prototype
window.WebSocket.OPEN = NativeWebSocket.OPEN
window.WebSocket.CONNECTING = NativeWebSocket.CONNECTING
window.WebSocket.CLOSING = NativeWebSocket.CLOSING
window.WebSocket.CLOSED = NativeWebSocket.CLOSED

// eslint-disable-next-line no-console
console.info('[mock] 开发环境 Mock 数据层已启用')
