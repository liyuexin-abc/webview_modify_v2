<!-- 对话输入框：固定在页面底部，用于发送智能问数问题 -->
<template>
  <div :class="['chat-input', {'chat-input--welcome': welcome}]">
    <div class="chat-input__box">
      <textarea
        ref="textareaRef"
        v-model="message"
        class="chat-input__textarea"
        :placeholder="placeholder"
        :disabled="loading"
        @keydown="handleEnter"
      />
      <div class="chat-input__bottom">
        <div class="chat-input__left" />
        <div class="chat-input__right">
          <div v-if="loading" class="chat-input__send is-loading">
            <i class="el-icon-loading" />
          </div>
          <div
            v-else
            :class="['chat-input__send', {'is-active': hasInput}]"
            @click="handleSend"
          >
            <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M915.515273 142.819385 98.213046 458.199122c-46.058539 17.772838-44.90475 43.601756 2.348455 57.622994l197.477685 58.594874 80.292024 238.91085c10.51184 31.277988 37.972822 37.873693 61.462483 14.603752l103.584447-102.611545 204.475018 149.840224c26.565749 19.467242 53.878547 9.222132 61.049613-23.090076l149.210699-672.34491C965.264096 147.505054 946.218922 130.971848 915.515273 142.819385zM791.141174 294.834331l-348.61988 310.610267c-6.268679 5.58499-11.941557 16.652774-12.812263 24.846818l-15.390659 144.697741c-1.728128 16.24808-7.330491 16.918483-12.497501 1.344894l-67.457277-203.338603c-2.638691-7.954906 0.975968-17.705389 8.022355-21.931178l442.114555-265.181253C812.67481 268.984974 815.674251 272.975713 791.141174 294.834331z"
                fill="#ffffff"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatInput',
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    welcome: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      message: '',
    };
  },
  computed: {
    placeholder() {
      return this.welcome
        ? '请输入您的问题，如：资产质量情况怎么样？'
        : '请输入您的问题，如：资产质量情况怎么样？';
    },
    hasInput() {
      return !!this.message.trim();
    },
  },
  methods: {
    handleEnter(e) {
      if (e.key !== 'Enter') return;
      if (e.shiftKey) return;
      e.preventDefault();
      this.handleSend();
    },
    handleSend() {
      if (this.loading || !this.hasInput) return;
      this.$emit('send', this.message.trim());
      this.message = '';
    },
  },
};
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.chat-input {
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  padding: 0 24px 16px;

  &.chat-input--welcome {
    width: 100%;
    max-width: 900px;
    padding: 0 24px;
  }

  &:not(.chat-input--welcome) {
    .chat-input__box {
      // max-width: 800px;
    }
  }

  .chat-input__box {
    width: 90%;
    height: 127px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    margin: 0 auto;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    box-shadow:
      0 0 2px 0 #00000005,
      0 0 4px 0 #0000000a,
      0 0 8px 0 #00000014;
    transition: all 0.3s ease-in-out;

    &:focus-within {
      border-color: $primary-color;
      box-shadow:
        0 0 2px 0 rgba(32, 76, 233, 0.06),
        0 0 4px 0 rgba(32, 76, 156, 0.1),
        0 0 8px 0 rgba(32, 76, 233, 0.18);
    }
  }

  .chat-input__textarea {
    width: 100%;
    flex: 1;
    outline: none;
    border: none;
    resize: none;
    padding: 20px 20px 8px;
    font-size: 16px;
    line-height: 1.5;
    color: $text-primary;
    background: transparent;
    font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;

    &::placeholder {
      color: $text-secondary;
    }

    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }
  }

  .chat-input__bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    flex-shrink: 0;
  }

  .chat-input__left {
    flex: 1;
    min-width: 0;
  }

  .chat-input__right {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    padding-left: 10px;
  }

  .chat-input__send {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: $primary-color;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.5;
    cursor: not-allowed;
    user-select: none;
    transition: opacity 0.2s ease, box-shadow 0.2s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &.is-active {
      opacity: 1;
      cursor: pointer;
      box-shadow: 0 0 2px 2px rgba(0, 72, 160, 0.2);
    }

    &.is-loading {
      opacity: 1;
      cursor: default;
    }
  }
}
</style>
