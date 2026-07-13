<!-- 筛选条件栏：日期范围、字段、运算符与筛选值配置 -->
<template>
  <div class="filter-bar">
    <span class="filter-bar__label">筛选器</span>
    <div class="filter-bar__content">
      <div class="filter-bar__row">
        <div class="filter-bar__group filter-bar__group--date">
          <el-select v-model="localFilter.dateField" size="small" class="filter-bar__group-prefix">
            <el-option v-for="item in filterFields" :key="item" :label="item" :value="item" />
          </el-select>

          <el-date-picker
            v-model="localFilter.dateRange"
            type="daterange"
            size="small"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            class="filter-bar__date-picker"
          />
        </div>
      </div>

      <div class="filter-bar__row filter-bar__row--action">
        <div class="filter-bar__group filter-bar__group--filter">
          <el-select v-model="localFilter.field" size="small" class="filter-bar__group-prefix">
            <el-option v-for="item in filterFields" :key="item" :label="item" :value="item" />
          </el-select>

          <el-select v-model="localFilter.operator" size="small" class="filter-bar__group-operator">
            <el-option v-for="item in filterOperators" :key="item" :label="getOperatorSymbol(item)" :value="item" />
          </el-select>

          <el-input v-model="localFilter.value" size="small" placeholder="请输入" clearable class="filter-bar__group-value" />
        </div>

        <el-button type="primary" size="small" icon="el-icon-search" :loading="searchLoading" class="filter-bar__search-btn" @click="handleSearch">搜索</el-button>
      </div>
    </div>
  </div>
</template>

<script>
/** 运算符展示符号 */
const OPERATOR_SYMBOL_MAP = {
  大于: '>',
  小于: '<',
  等于: '=',
  不等于: '!=',
  包含: 'like',
};

export default {
  name: 'FilterBar',
  props: {
    filter: {
      type: Object,
      default: () => ({}),
    },
    filterFields: {
      type: Array,
      default: () => [],
    },
    filterOperators: {
      type: Array,
      default: () => [],
    },
    searchLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      localFilter: {...this.filter, dateField: '日期'},
    };
  },
  watch: {
    filter: {
      deep: true,
      handler(val) {
        this.localFilter = {...val, dateField: this.localFilter.dateField || '日期'};
      },
    },
  },
  methods: {
    getOperatorSymbol(operator) {
      return OPERATOR_SYMBOL_MAP[operator] || operator;
    },
    handleSearch() {
      this.$emit('search', {...this.localFilter});
    },
  },
};
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.filter-bar {
  display: flex;
  align-items: flex-start;
  padding: 8px 0;

  .filter-bar__label {
    width: 56px;
    flex-shrink: 0;
    font-size: 13px;
    color: $text-secondary;
    line-height: 32px;
  }

  .filter-bar__content {
    flex: 1;
    min-width: 0;
  }

  .filter-bar__row {
    margin-bottom: 8px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .filter-bar__row--action {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .filter-bar__group {
    display: inline-flex;
    align-items: stretch;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    vertical-align: top;

    .filter-bar__group-prefix {
      width: 88px;
      flex-shrink: 0;

      ::v-deep .el-input__inner {
        border: none;
        border-radius: 0;
        border-right: 1px solid #dcdfe6;
        background: #f5f7fa;
        color: $text-regular;
        padding-right: 24px;
      }
    }

    .filter-bar__date-picker {
      flex: 1;
      min-width: 240px;
    }

    .filter-bar__group-operator {
      width: 56px;
      flex-shrink: 0;

      ::v-deep .el-input__inner {
        border: none;
        border-radius: 0;
        border-right: 1px solid #dcdfe6;
        text-align: center;
        padding: 0 20px 0 8px;
      }
    }

    .filter-bar__group-value {
      width: 59%;
      flex-shrink: 0;

      ::v-deep .el-input__inner {
        border: none;
        border-radius: 0;
      }
    }
  }

  .filter-bar__group--date {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 400px;

    ::v-deep .filter-bar__date-picker.el-range-editor.el-input__inner {
      display: flex;
      align-items: center;
      line-height: normal;
      overflow: visible;
      border: none;
      border-radius: 0;
      box-shadow: none;
    }

    ::v-deep .filter-bar__date-picker .el-range-separator {
      width: auto;
      min-width: 20px;
      line-height: 1;
      height: auto;
      padding: 0 4px;
      overflow: visible;
      flex-shrink: 0;
    }

    ::v-deep .filter-bar__date-picker .el-range-input {
      line-height: 1;
    }
  }

  .filter-bar__group--filter {
    flex: 1;
    max-width: 360px;
  }

  .filter-bar__search-btn {
    flex-shrink: 0;
    padding: 8px 16px;
  }
}
</style>
