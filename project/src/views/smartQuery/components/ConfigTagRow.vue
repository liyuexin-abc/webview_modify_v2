<!-- 标签配置行：用于维度或指标的可增删标签列表 -->
<template>
  <div class="config-tag-row">
    <span class="config-tag-row__label">{{ label }}</span>
    <div class="config-tag-row__content">
      <el-tag
        v-for="(tag, index) in tags"
        :key="`${tag}-${index}`"
        closable
        size="small"
        class="config-tag-row__tag"
        @close="handleRemove(index)"
      >
        {{ tag }}
      </el-tag>
      <el-button
        type="text"
        icon="el-icon-plus"
        class="config-tag-row__add"
        @click="$emit('add')"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfigTagRow',
  props: {
    label: {
      type: String,
      required: true
    },
    tags: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    handleRemove(index) {
      this.$emit('remove', index)
    }
  }
}
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.config-tag-row {
  display: flex;
  align-items: flex-start;
  padding: 8px 0;

  .config-tag-row__label {
    width: 56px;
    flex-shrink: 0;
    font-size: 13px;
    color: $text-secondary;
    line-height: 28px;
  }

  .config-tag-row__content {
    flex: 1;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
  }

  .config-tag-row__tag {
    border-radius: 2px;
  }

  .config-tag-row__add {
    padding: 4px;
    font-size: 14px;
    color: $text-secondary;

    &:hover {
      color: $primary-color;
    }
  }
}
</style>
