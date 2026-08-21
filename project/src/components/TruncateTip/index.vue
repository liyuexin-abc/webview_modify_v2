<template>
  <!-- 超长省略 + 仅在文字确实被截断时才显示 Tooltip -->
  <el-tooltip
    :content="text"
    :placement="placement"
    :open-delay="openDelay"
    :disabled="!truncated"
  >
    <div
      ref="el"
      class="truncate-tip"
      :style="maxWidth ? { maxWidth: maxWidth + 'px' } : null"
      @mouseenter="check"
    >
      {{ text }}
    </div>
  </el-tooltip>
</template>

<script>
export default {
  name: 'TruncateTip',
  props: {
    text: { type: [String, Number], default: '' },
    // 最大宽度(px)；传 0 表示由外部 CSS 控制宽度
    maxWidth: { type: Number, default: 0 },
    placement: { type: String, default: 'top' },
    openDelay: { type: Number, default: 150 },
  },
  data() {
    return { truncated: false }
  },
  methods: {
    check() {
      const el = this.$refs.el
      // scrollWidth > clientWidth 说明文字被截断了
      this.truncated = !!el && el.scrollWidth > el.clientWidth
    },
  },
}
</script>

<style scoped>
.truncate-tip {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}
</style>
