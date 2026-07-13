<!-- 查询配置区：维度、指标、筛选器配置及下载、SQL、视图切换操作 -->
<template>
  <div class="query-config">
    <div class="query-config__toolbar">
      <div class="query-config__actions">
        <el-button size="small" icon="el-icon-download" @click="$emit('download')">
          下载
        </el-button>
        <el-button size="small" @click="$emit('show-sql')">
          SQL
        </el-button>
      </div>
      <el-select
        v-model="localViewType"
        size="small"
        class="query-config__view-type"
        @change="handleViewChange"
      >
        <el-option
          v-for="item in viewTypes"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>

    <ConfigTagRow
      label="维度"
      :tags="dimensions"
      @remove="handleRemoveDimension"
      @add="$emit('add-dimension')"
    />

    <ConfigTagRow
      label="指标"
      :tags="metrics"
      @remove="handleRemoveMetric"
      @add="$emit('add-metric')"
    />

    <FilterBar
      :filter="filter"
      :filter-fields="filterFields"
      :filter-operators="filterOperators"
      :search-loading="searchLoading"
      @search="$emit('search', $event)"
      @add-filter="$emit('add-filter')"
    />
  </div>
</template>

<script>
import ConfigTagRow from './ConfigTagRow.vue';
import FilterBar from './FilterBar.vue';

export default {
  name: 'QueryConfig',
  components: {
    ConfigTagRow,
    FilterBar,
  },
  props: {
    dimensions: {
      type: Array,
      default: () => [],
    },
    metrics: {
      type: Array,
      default: () => [],
    },
    filter: {
      type: Object,
      default: () => ({}),
    },
    viewTypes: {
      type: Array,
      default: () => [],
    },
    filterFields: {
      type: Array,
      default: () => [],
    },
    filterOperators: {
      type: Array,
      default: () => [],
    },
    viewType: {
      type: String,
      default: 'table',
    },
    searchLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      localViewType: this.viewType,
    };
  },
  watch: {
    viewType(val) {
      this.localViewType = val;
    },
  },
  methods: {
    handleRemoveDimension(index) {
      this.$emit('remove-dimension', index);
    },
    handleRemoveMetric(index) {
      this.$emit('remove-metric', index);
    },
    handleViewChange(val) {
      this.$emit('change-view', val);
    },
  },
};
</script>

<style lang="scss" scoped>
.query-config {
  .query-config__toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: #fafbfe;
    border-bottom: 1px solid #e8ecf2;
    margin: 0 -10px 0;
  }

  .query-config__actions {
    display: flex;
    gap: 8px;

    ::v-deep .el-button {
      border-color: #e8ecf2;
      color: #0b0b0b;

      &:hover {
        color: #204ce9;
        border-color: #bfdbfe;
        background: #f0f5ff;
      }
    }
  }

  .query-config__view-type {
    width: 100px;
  }
}
</style>
