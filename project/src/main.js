import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './permission'


import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import { download } from '@/utils/request'

import Pagination from "@/components/Pagination";
import BaseIcon from "@/components/BaseIcon";

import markdownitVue from 'markdown-it-vue';

// 设计令牌 + Element UI 全局覆盖（顺序：tokens -> element 覆盖 -> global 业务样式）
import "@/styles/design-tokens.scss";
import "@/styles/element-override.scss";
import "@/assets/css/global.scss";

// 开发环境 mock 数据层（仅 development 生效）
if (process.env.NODE_ENV === 'development') {
  require('@/mock');
}
import { messageDuration } from "@/utils/common.js";

import afTableColumn from 'af-table-column'

Vue.use(afTableColumn)


// 全局注册
Vue.component('markdown-it-vue', markdownitVue);

Vue.config.productionTip = false

Vue.prototype.download = download
Vue.prototype.$messageDuration = messageDuration
    

Vue.use(ElementUI);
Vue.component('Pagination', Pagination)
Vue.component('BaseIcon', BaseIcon)

new Vue({
  router,
 
  render: h => h(App),
}).$mount('#app')
