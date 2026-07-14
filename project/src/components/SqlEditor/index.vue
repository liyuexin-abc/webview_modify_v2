<template>
  <div class="sql-editor">
    <div class="sql-editor__header">
      <span class="sql-editor__badge">SQL</span>
      <span class="sql-editor__title">{{ title }}</span>
      <span class="sql-editor__meta">{{ lineCount }} 行 · {{ charCount }} 字符</span>
    </div>
    <div class="sql-editor__body">
      <div class="sql-editor__gutter" ref="gutter">
        <div v-for="n in lineCount" :key="n" class="sql-editor__lineno">
          {{ n }}
        </div>
      </div>
      <textarea
        ref="textarea"
        class="sql-editor__textarea"
        :value="value"
        :placeholder="placeholder"
        :rows="rows"
        spellcheck="false"
        @input="onInput"
        @scroll="syncScroll"
        @keydown.tab.prevent="onTab"
      ></textarea>
    </div>
  </div>
</template>

<script>
/**
 * 可编辑 SQL 编辑器(轻量):
 * - 行号槽 + 等宽字体 + 编辑器外壳,浅色主题
 * - 支持 v-model、Tab 键缩进(2 空格)
 * - 只做视觉增强,不改变绑定值语义
 */
export default {
  name: "SqlEditor",
  props: {
    value: { type: String, default: "" },
    title: { type: String, default: "SQL 编辑器" },
    placeholder: {
      type: String,
      default: "SELECT ... FROM ... JOIN ... WHERE ...",
    },
    rows: { type: Number, default: 8 },
  },
  computed: {
    lineCount() {
      const v = this.value || "";
      return Math.max(v.split("\n").length, 1);
    },
    charCount() {
      return (this.value || "").length;
    },
  },
  methods: {
    onInput(e) {
      this.$emit("input", e.target.value);
    },
    syncScroll() {
      if (this.$refs.gutter && this.$refs.textarea) {
        this.$refs.gutter.scrollTop = this.$refs.textarea.scrollTop;
      }
    },
    onTab(e) {
      const el = e.target;
      const start = el.selectionStart;
      const end = el.selectionEnd;
      const next = this.value.substring(0, start) + "  " + this.value.substring(end);
      this.$emit("input", next);
      this.$nextTick(() => {
        el.selectionStart = el.selectionEnd = start + 2;
      });
    },
  },
};
</script>

<style scoped lang="scss">
.sql-editor {
  border: 1px solid var(--border-color, #e5eaf1);
  border-radius: 10px;
  overflow: hidden;
  background: #fbfcfe;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  &:focus-within {
    border-color: var(--brand, #2b5cff);
    box-shadow: 0 0 0 3px rgba(43, 92, 255, 0.08);
  }
}

.sql-editor__header {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 34px;
  padding: 0 12px;
  background: #f4f7fb;
  border-bottom: 1px solid var(--border-color, #e5eaf1);
}

.sql-editor__badge {
  display: inline-flex;
  align-items: center;
  height: 18px;
  padding: 0 7px;
  border-radius: 4px;
  background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.sql-editor__title {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
}

.sql-editor__meta {
  margin-left: auto;
  font-size: 11px;
  color: #94a3b8;
}

.sql-editor__body {
  display: flex;
  align-items: stretch;
  max-height: 46vh;
}

.sql-editor__gutter {
  flex-shrink: 0;
  min-width: 40px;
  padding: 10px 0;
  background: #f4f7fb;
  border-right: 1px solid var(--border-color, #e5eaf1);
  overflow: hidden;
  user-select: none;
}

.sql-editor__lineno {
  padding: 0 10px 0 6px;
  font-family: var(--font-mono, "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace);
  font-size: 12.5px;
  line-height: 21px;
  color: #a8b4c4;
  text-align: right;
}

.sql-editor__textarea {
  flex: 1;
  min-width: 0;
  padding: 10px 14px;
  border: none;
  outline: none;
  resize: vertical;
  background: transparent;
  font-family: var(--font-mono, "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace);
  font-size: 12.5px;
  line-height: 21px;
  color: #1e293b;

  &::placeholder {
    color: #b6c2d2;
    font-family: inherit;
  }
}
</style>
