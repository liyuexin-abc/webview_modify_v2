<!-- 数据表格：展示查询结果，支持列排序与分页 -->
<template>
  <div class="data-table">
    <el-table
      :data="paginatedData"
      border
      stripe
      size="small"
      class="data-table__inner"
      @sort-change="handleSortChange"
    >
      <el-table-column
        v-for="col in displayColumns"
        :key="col.prop"
        :prop="col.prop"
        :label="col.label"
        sortable="custom"
        :min-width="col.minWidth || 120"
        :align="col.align || 'left'"
      />
    </el-table>

    <div class="data-table__pagination">
      <el-pagination
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :page-sizes="[10, 20, 50]"
        :total="total"
        layout="sizes, total, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    data: {
      type: Array,
      default: () => [],
    },
    columns: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      sortedData: [],
    };
  },
  computed: {
    displayColumns() {
      return this.columns;
    },
    total() {
      return this.sortedData.length;
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      return this.sortedData.slice(start, start + this.pageSize);
    },
  },
  watch: {
    data: {
      immediate: true,
      handler(val) {
        this.sortedData = [...val];
        this.currentPage = 1;
      },
    },
  },
  methods: {
    handleSortChange({ prop, order }) {
      if (!order) {
        this.sortedData = [...this.data];
        return;
      }
      const dir = order === 'ascending' ? 1 : -1;
      this.sortedData = [...this.data].sort((a, b) => {
        const va = a[prop];
        const vb = b[prop];
        if (typeof va === 'number') return (va - vb) * dir;
        return String(va).localeCompare(String(vb), 'zh-CN') * dir;
      });
    },
    handleSizeChange() {
      this.currentPage = 1;
    },
    handlePageChange() {},
  },
};
</script>

<style lang="scss" scoped>
.data-table {
  padding-top: 10px;

  .data-table__inner {
    width: 100%;

    ::v-deep {
      &.el-table {
        border-color: #e8ecf2;
        color: #0b0b0b;
        font-size: 13px;

        &::before {
          background-color: #e8ecf2;
        }
      }

      .el-table__header-wrapper th {
        background: #fafbfe;
        color: #0b0b0b;
        font-weight: 500;
        border-color: #e8ecf2;
      }

      .el-table__body-wrapper td {
        border-color: #e8ecf2;
      }

      .el-table--striped .el-table__body tr.el-table__row--striped td {
        background: #fafbfe;
      }

      .el-table__body tr:hover > td {
        background: #f0f5ff;
      }
    }
  }

  .data-table__pagination {
    display: flex;
    justify-content: flex-end;
    padding-top: 16px;

    ::v-deep .el-pagination {
      color: #5f6674;
      font-weight: 400;

      .el-pagination__total,
      .el-pagination__jump {
        color: #5f6674;
      }

      .btn-prev,
      .btn-next,
      .el-pager li {
        background: #fff;
        border: 1px solid #e8ecf2;
        color: #0b0b0b;

        &:hover {
          color: #204ce9;
        }

        &.active {
          background: #204ce9;
          border-color: #204ce9;
          color: #fff;
        }
      }
    }
  }
}
</style>
