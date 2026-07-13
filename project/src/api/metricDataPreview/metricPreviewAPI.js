import request from '@/utils/request'

// 登录方法
export function getMetricsTreeAPI(data) {
  return request({
    //url: '/report-preview/field-tree',
    url: '/api/v1/report-preview/dim-metric',

    method: 'post',
    data: data
  })
}

//获取指标预览
/*export function getMetricsPreviewAPI(data) {
    return request({
      url: '/report-preview/query',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
  }*/


//获取指标预览
export function getMetricsPreviewAPI(data) {
  return request({
    url: '/api/v1/chat-server/group/preview',

    method: 'POST',
    data: data
  })
}


//指标数据预览中的预览
export function getMetricsDataPreviewAPI(data) {
  return request({
    url: '/api/v1/chat-server/getdata',
    // headers: {
    //   isToken: false
    // },
    method: 'POST',
    data: data
  })
}




export const granularityEnum = {
  DAY: {value: 'day',name: '日期' },
  WEEK: {value: 'week',name: '自然周'},
  MONTH: {value: 'month',name: '月份'},
  QUARTER: {value: 'quarter',name: '季度'},
  YEAR: {value: 'year',name: '年'},
}


export const operatorEnum = {
   0:{value: 0,name: '>' },
   1:{value: 1,name: '<' },
   2:{value: 2,name: '=' },
   3:{value: 3,name: '>=' },
   4:{value: 4,name: '<=' },
   5:{value: 5,name: 'in' },
   6:{value: 6,name: 'not in' },
   7:{value: 7,name: '!=' },
   8:{value: 8,name: 'like' },
   9:{value: 9,name: 'not like' },
   10:{value: 10,name: '包含' },
   //11:{value: 11,name: '不包含' },
}

export const chartTypeEnum = {
  1:{value: 1,name: '表格' },
  2: {value: 2,name: '柱状图' },
  3: {value: 3,name: '折线图' },
  4:{value: 4,name: '饼图' },
  5: {value: 5,name: '指标卡' },
  6: {value: 6,name: '交叉表' },
}



export const orderEnum = [
  {value: 'desc',name: '倒序DESC'},
  {value: 'asc',name: '正序ASC' },
]

export const filterTypeEnum = {
  'dim': {value: 0,name: '维度'},
  'metric':{value: 1,name: '指标' },
}