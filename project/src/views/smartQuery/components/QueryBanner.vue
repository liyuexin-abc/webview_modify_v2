<!-- 用户问题气泡：在查询区域顶部展示当前提问内容 -->
<template>
  <div class="query-banner">
    <div class="query-banner__inner">
      <span class="query-banner__text">{{ text }}</span>
      <span class="query-banner__avatar">{{ avatarText }}</span>
    </div>
  </div>
</template>

<script>
import {getUserInfo} from '@/utils/auth';

export default {
  name: 'QueryBanner',
  props: {
    text: {
      type: String,
      default: '',
    },
  },
  computed: {
    displayName() {
      const userInfo = getUserInfo() || {};
      return userInfo.name || userInfo.username || '用户';
    },
    avatarText() {
      const name = this.displayName.trim();
      if (!name) return '?';
      return name.charAt(0).toUpperCase();
    },
  },
};
</script>

<style lang="scss" scoped>
.query-banner {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;

  .query-banner__inner {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    max-width: 80%;
  }

  .query-banner__text {
    display: inline-block;
    padding: 10px 16px;
    background: #e3e7fc;
    color: #53555e;
    font-size: 14px;
    line-height: 1.5;
    border-radius: 14px 14px 0 14px;
    word-break: break-all;
  }

  .query-banner__avatar {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
    font-size: 14px;
    font-weight: 500;
    line-height: 32px;
    text-align: center;
  }
}
</style>
