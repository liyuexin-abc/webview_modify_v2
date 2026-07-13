<!-- 思考过程展示：流式显示 AI 推理步骤，支持 Markdown 渲染与折叠 -->
<template>
  <div v-if="visible" class="answer-think">
    <div class="think-header">
      <button type="button" class="think-toggle" @click="toggleCollapse">
        <img v-if="loading" src="/img/GBI/loading.gif" alt="loading" class="loading-img" />
        <span v-else class="think-icon-wrap think-icon-wrap--done">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="think-icon" aria-hidden="true">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </span>
        <span class="think-status">{{ loading ? '思考中...' : '已推理思考' }}</span>
        <i
          v-if="displayContent"
          :class="['think-arrow', collapsed ? 'el-icon-arrow-down' : 'el-icon-arrow-up']"
        />
      </button>
    </div>

    <el-collapse-transition>
      <div v-show="!collapsed && displayContent" ref="thinkContentRef" class="think-content">
        <div class="think-markdown" v-html="renderedContent" />
      </div>
    </el-collapse-transition>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it';

const markdown = new MarkdownIt({
  breaks: true,
  linkify: true,
  html: true,
});

export default {
  name: 'ThinkingProcess',
  props: {
    content: {
      type: String,
      default: '',
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      collapsed: false,
      /** 思考进行中自动滚到底部，思考结束后关闭 */
      autoScroll: false,
    };
  },
  computed: {
    displayContent() {
      return this.content?.trim() || '';
    },
    visible() {
      return this.loading || Boolean(this.displayContent);
    },
    renderedContent() {
      if (!this.displayContent) return '';
      return markdown.render(this.displayContent);
    },
  },
  watch: {
    loading(val, oldVal) {
      if (val) {
        this.collapsed = false;
        this.autoScroll = true;
        this.scrollToBottom();
        return;
      }
      this.autoScroll = false;
      if (oldVal && this.displayContent) {
        this.collapsed = true;
      }
    },
    content() {
      if (this.autoScroll && this.loading) {
        this.scrollToBottom();
        return;
      }
      if (!this.loading && this.displayContent) {
        this.collapsed = true;
      }
    },
    collapsed(val) {
      if (!val && this.autoScroll && this.loading) {
        this.scrollToBottom();
      }
    },
  },
  mounted() {
    if (this.loading) {
      this.autoScroll = true;
      this.scrollToBottom();
    } else if (this.displayContent) {
      this.collapsed = true;
    }
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        this.$nextTick(() => {
          const el = this.$refs.thinkContentRef;
          if (!el || this.collapsed) return;
          el.scrollTop = el.scrollHeight;
        });
      });
    },
    toggleCollapse() {
      if (!this.displayContent) return;
      this.collapsed = !this.collapsed;
    },
  },
};
</script>

<style lang="scss" scoped>
.answer-think {
  width: 100%;
  font-size: 14px;
  color: #5f6674;
  line-height: 24px;
  background: #f1f4f9;
  border-radius: 8px;
  border: 1px solid #e8eaed;
  overflow: hidden;
  // padding: 10px 0 0;
  margin-bottom: 12px;

  &:hover {
    border-color: #bfdbfe;
    box-shadow: 0 2px 12px rgba(59, 130, 246, 0.06);
  }

  .think-header {
    padding: 0 14px;
  }

  .think-toggle {
    display: flex;
    align-items: center;
    width: 100%;
    height: 44px;
    // padding: 0 16px;
    // margin-bottom: 10px;
    border: none;
    border-radius: 0;
    background: transparent;
    color: #333;
    font-size: 14px;
    cursor: pointer;
    text-align: left;
  }

  .loading-img {
    animation: loading 3s linear infinite;
    width: 30px;
    height: 30px;
    margin-right: 8px;
    flex-shrink: 0;
  }

  .think-icon-wrap {
    margin-right: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &--done {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background-color: #204ce9;

      .think-icon {
        width: 14px;
        height: 14px;
        color: #fff;
      }
    }
  }

  .think-status {
    flex: 1;
  }

  .think-arrow {
    flex-shrink: 0;
    color: #94a3b8;
    font-size: 14px;
  }

  .think-content {
    padding: 12px 16px;
    background: #fff;
    max-height: 300px;
    overflow-y: auto;
    scrollbar-gutter: stable;
    box-sizing: border-box;
  }

  .think-markdown {
    font-size: 14px;
    line-height: 1.6;
    color: #5f6674;
    word-break: break-word;

    ::v-deep {
      p {
        padding-left: 16px;
        position: relative;
        margin: 10px 0;

        &::before {
          position: absolute;
          content: '';
          height: 100%;
          width: 1px;
          background: #ddd;
          left: 2px;
          top: 0;
        }
      }

      h1,
      h2,
      h3,
      h4,
      h5,
      h6 {
        font-weight: 500;
        font-size: 16px;
        color: #0b0b0b;
        position: relative;
        padding-left: 16px;
        line-height: 24px;
        margin: 10px 0;

        &::before {
          content: '';
          position: absolute;
          width: 6px;
          height: 6px;
          background: #666;
          border-radius: 50%;
          top: 50%;
          left: 0;
          margin-top: -3px;
        }
      }

      ul,
      ol {
        margin: 0 0 8px;
        padding-left: 18px;
        list-style: auto;
      }

      li {
        margin-bottom: 4px;
      }

      code {
        padding: 1px 4px;
        background: #f5f7fa;
        border-radius: 2px;
        font-family: Consolas, Monaco, monospace;
        font-size: 11px;
      }

      pre {
        margin: 0 0 8px;
        padding: 8px 10px;
        background: #f5f7fa;
        border-radius: 4px;
        overflow-x: auto;

        code {
          padding: 0;
          background: transparent;
        }
      }

      strong {
        color: #0b0b0b;
        font-weight: 600;
      }

      blockquote {
        margin: 0 0 8px;
        padding-left: 10px;
        border-left: 3px solid #e8ecf2;
        color: #5f6674;
      }

      a {
        color: #204ce9;
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}

@keyframes loading {
  0% {
    transform: scale(0.7);
  }

  50% {
    transform: scale(1);
  }

  100% {
    transform: scale(0.7);
  }
}
</style>
