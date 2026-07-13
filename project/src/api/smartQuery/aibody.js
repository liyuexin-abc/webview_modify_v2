import request from '@/utils/request'

/**
 * 智能体分页列表
 * @param {Object} params
 * @param {string} [params.keyword] - 名称模糊搜索
 * @param {number} params.page - 页码（min=1）
 * @param {number} params.pageSize - 每页条数（min=1）
 */
export function getAibodyList(params) {
  return request({
    url: '/api/v1/aibody/list',
    method: 'get',
    params
  })
}

/**
 * 智能体详情
 * @param {string} code - 智能体编码
 */
export function getAibodyInfo(code) {
  return request({
    url: `/api/v1/aibody/info/${code}`,
    method: 'get'
  })
}

/**
 * 获取数据源下可选表
 * @param {Object} params
 * @param {number} params.sourceId - 数据源 ID
 * @param {string} [params.keyword] - 表名/注释模糊搜索
 */
export function getCandidateTables(params) {
  return request({
    url: '/api/v1/aibody/candidate-tables',
    method: 'get',
    params
  })
}

/**
 * 新增/编辑智能体（aicode 为空时创建，非空时编辑）
 * @param {Object} data - AiBodySaveDTO
 * @param {string} data.name - 智能体名称
 * @param {string} [data.description] - 描述
 * @param {string} [data.aicode] - 智能体编码（非空=编辑）
 * @param {Array} [data.tableRelations] - 关联数据表
 * @param {Array} [data.knowledgeList] - 知识库条目
 */
export function saveAibody(data) {
  return request({
    url: '/api/v1/aibody/save',
    method: 'post',
    data
  })
}
