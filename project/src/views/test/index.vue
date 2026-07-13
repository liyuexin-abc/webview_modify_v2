<template>
  <div
    class="login"
    v-loading="loading"
    element-loading-text="登录中,请稍等..."
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
  >
    



<markdown-it-vue :content="markdownText"></markdown-it-vue>


  </div>
</template>

<script>


export default {
  name: 'test',

   data() {
    return {
      markdownText: `
### 第一步：准备材料
### 第二步：开始制作
### 第三步：完成111
      `,


    }
   },

}



</script>


<style scoped>
/* 1. 在 .markdown-body 容器上重置计数器 */
::v-deep .markdown-body {
  counter-reset: step-counter;
}

/* 2. 为 h3 添加步骤条样式 */
::v-deep .markdown-body h3 {
  /* 触发计数器递增 */
  counter-increment: step-counter;
  
  /* 布局：为序号和竖线留出空间 */
  display: block;
  position: relative;
  padding-left: 40px;
  margin-bottom: 24px;
  
  /* 标题文字样式 */
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 3. 生成步骤序号（圆形数字） */
::v-deep .markdown-body h3::before {
  content: counter(step-counter);
  position: absolute;
  left: 0;
  top: 2px;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background: #409EFF;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
}

/* 4. 生成步骤之间的连接竖线 */
::v-deep .markdown-body h3::after {
  content: '';
  position: absolute;
  left: 11px;  /* 圆点中心位置 (24/2 - 1) */
  top: 28px;   /* 圆点底部 */
  width: 2px;
  height: calc(100% + 8px); /* 延伸到下一个步骤 */
  background: #dcdfe6;
}

/* 5. 最后一个步骤不需要竖线 */
::v-deep .markdown-body h3:last-child::after {
  display: none;
}
</style>