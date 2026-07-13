<!-- 对话空状态：未开始问答时展示当前智能体欢迎语 -->
<template>
  <div class="chat-welcome">
    <h2 class="chat-welcome__title">
      你好欢迎使用
      <span class="chat-welcome__agent-wrap">
        <span class="chat-welcome__agent">{{ agentName }}</span>
        <i class="el-icon-info chat-welcome__info" :title="agentDesc" />
      </span>
      智能体
    </h2>
    <p v-if="agentDesc" class="chat-welcome__desc">{{ agentDesc }}</p>
  </div>
</template>

<script>
export default {
  name: 'ChatWelcome',
  props: {
    agent: {
      type: Object,
      default: null,
    },
  },
  computed: {
    agentName() {
      return this.agent?.name || '智能体';
    },
    agentDesc() {
      const agent = this.agent;
      if (!agent) return '';

      return agent.description || agent.intro || agent.remark || '';
    },
  },
};
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.chat-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 900px;
  padding: 0 24px;
  text-align: center;

  .chat-welcome__title {
    margin: 0 0 16px;
    font-size: 24px;
    font-weight: 600;
    line-height: 1.5;
    color: #000;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .chat-welcome__agent-wrap {
    display: inline-flex;
    align-items: flex-start;
    vertical-align: baseline;
  }

  .chat-welcome__agent {
    color: $primary-color;
  }

  .chat-welcome__info {
    margin-left: 2px;
    font-size: 14px;
    color: $primary-color;
    cursor: pointer;
    transform: translateY(-2px);
  }

  .chat-welcome__desc {
    margin: 0;
    width: 100%;
    max-width: 720px;
    font-size: 14px;
    line-height: 1.6;
    color: #000;
    text-align: center;
  }
}
</style>
