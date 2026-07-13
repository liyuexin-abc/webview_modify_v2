<template>
  <div :class="{'hidden':hidden}" class="pagination-container">

<div style="display: flex;justify-content: space-between;align-items: center;">
  <div style="font-size:14px;"> 
  共{{ total }}条数据
</div> 

<div>
    <el-pagination
      :background="background"
      :current-page.sync="currentPage"
      :page-size.sync="pageSize"
      :layout="layout"
      :page-sizes="pageSizes"
      :pager-count="pagerCount"
      :total="total"
      v-bind="$attrs"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :style="{ fontSize: '34px' }"
    />

</div>

  </div>
    </div>
</template>

<script>
import { scrollTo } from '@/utils/scroll-to'


export default {
  name: 'Pagination',
  props: {
    total: {
      required: true,
      type: Number
    },
    page: {
      type: Number,
      default: 1
    },
    limit: {
      type: Number,
      default: 20
    },
    pageSizes: {
      type: Array,
      default() {
        return [10, 20, 30, 50]
      }
    },
    // 移动端页码按钮的数量端默认值5
    pagerCount: {
      type: Number,
      default: document.body.clientWidth < 992 ? 5 : 7
    },
    layout: {
      type: String,
      default: 'prev, pager, next, sizes, jumper'
    },
    background: {
      type: Boolean,
      default: true
    },
    autoScroll: {
      type: Boolean,
      default: true
    },
    hidden: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    currentPage: {
      get() {
        return this.page
      },
      set(val) {
        this.$emit('update:page', val)
      }
    },
    pageSize: {
      get() {
        return this.limit
      },
      set(val) {
        this.$emit('update:limit', val)
      }
    }
  },
  methods: {

    handleSizeChange(val) {
      this.$emit('pagination', { page: this.currentPage, limit: val })
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    },
    handleCurrentChange(val) {
      this.$emit('pagination', { page: val, limit: this.pageSize })
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    }
  }
}
</script>

<style scoped>
.pagination-container {
  background: #fff;
  padding: 8px 16px;

}
.pagination-container.hidden {
  display: none;
}

.el-pagination {
align-items: center;
    display: flex;
        flex-wrap: wrap;
}


 ::v-deep .el-pagination__editor.el-input,
 ::v-deep .el-select .el-input .el-input__inner,

::v-deep .el-pagination .btn-next,
::v-deep .el-pagination__sizes.el-input .el-input__inner,
::v-deep .el-pagination .btn-prev,
::v-deep .el-pagination .el-pager li,
::v-deep .el-pagination button,
::v-deep .el-pagination span:not([class*=suffix]),
::v-deep .el-pagination__editor.el-input .el-input__inner {
  font-size: 14px; /* 修改为你想要的字体大小 */
}



</style>
