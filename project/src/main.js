import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './permission'


import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import { download } from '@/utils/request'

import Pagination from "@/components/Pagination";

import markdownitVue from 'markdown-it-vue';


import "@/assets/css/global.scss";
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

new Vue({
  router,
 
  render: h => h(App),
}).$mount('#app')
