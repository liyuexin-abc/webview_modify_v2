import request from '@/utils/request'

// 获取组合列表 -- 31-组合列表
export function getPortfolioDataListAPI(query) {
  return request({
    url: '/api/v1/indicator-groups/list',

    method: 'get',
    params: query
  })
}


// 获取指标组合详情 -- 32-组合详情
export function getPortfolioDataDetailAPI(id) {
  return request({
    url: '/api/v1/indicator-groups/' + id + '/detail',

    method: 'get',
    //params: query
  })
}

//保存组合 -- 33-保存组合
export function savePortfolioDataAPI(data) {
  return request({
    //url: '/indicator-groups',
    url:'/api/v1/indicator-groups/save',

    method: 'POST',
    data: data
  })
}

// 下线组合 -- 34-下线组合
export function offlineCandidatesAPI(id) {
  return request({
    url: '/api/v1/indicator-groups/'+id+'/offline',

    method: 'POST',
    //params: query
  })
}

// 上线组合 -- 35-上线组合
export function onlineCandidatesAPI(id) {
  return request({
    url: '/api/v1/indicator-groups/'+id+'/online',
    method: 'POST',
    //params: query
  })
}


//删除组合 -- 36-删除组合
export function deletePortfolioDataAPI(id,data) {
  return request({
    url: '/api/v1/indicator-groups/' + id,

    method: 'DELETE',
    data: data
  })
}



// 获取指标组合详情 -- 37-字段候选列表
export function getCandidatesAPI(query) {
  return request({
    url: '/api/v1/indicator-groups/candidates',

    method: 'get',
    params: query
  })
}


export const itemTypeEnum = {
  DIMENSION: {value: 'dimension',name: '维度' },
  ATOMICMETRIC: {value: 'atomic_metric',name: '原子指标'},
  CALCULATEDMETRIC: {value: 'calculated_metric',name: '计算指标'},
  DERIVEDMETRIC: {value: 'derived_metric',name: '派生指标'},
  INDICATORGROUP: {value: 'indicator_group',name: '指标组合'},
}

export const statusEnum = {
  DIMENSION: {value: 0,name: '草稿' },
  ATOMICMETRIC: {value: 1,name: '审批中'},
  CALCULATEDMETRIC: {value: 2,name: '已上线'},
  DERIVEDMETRIC: {value: 3,name: '已下线'},
}


export const orderEnum = [
  {value: 'ASC',name: '升序' },
  {value: 'DESC',name: '降序'},
]