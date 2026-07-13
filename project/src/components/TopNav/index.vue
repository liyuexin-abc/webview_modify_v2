<template>
  <div class="top-nav">
    <div class="top-nav__brand">
      <img class="top-nav__logo" src="@/assets/logo.png" alt="logo" />
      <span class="top-nav__title">数据分析平台</span>
    </div>


    <div class="top-nav__actions">
      <div >
        <el-button type="text" style="font-size:14px;" @click="showAgent"> 应用端 </el-button>
      </div>
      <div style="margin-right:50px;">
        <el-button type="text" style="font-size:14px;" @click="showManager"> 管理端 </el-button>
      </div>

      <el-dropdown trigger="click" @command="handleCommand">
        <div class="top-nav__user">
          <el-avatar :size="24" :style="{ backgroundColor: '#0073FF', color: 'white' }">
            {{ avatarText }}
          </el-avatar>
          <span class="top-nav__username">{{ displayName }}</span>
          <i class="el-icon-arrow-down top-nav__arrow" />
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="logout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { getUserInfo, clearAuth } from '@/utils/auth'

export default {
  data() {
    return {
      userInfo: getUserInfo() || {},
    }
  },
  computed: {
    displayName() {     
      return this.userInfo.name || this.userInfo.username || '用户'
    },

    avatarText() {
      const name = this.displayName.trim()
      if (!name) {
        return '?'
      }
      return name.charAt(0).toUpperCase()
    },
  },

  watch: {
    // 监听路由对象的变化
    $route: {
      handler(to, from) {
        // 当路由变化时重新加载数据
        this.userInfo = getUserInfo() || {}
      },
      immediate: true // 组件创建时立即执行一次
    }
  },

  mounted() {
    this.userInfo = getUserInfo() || {}
  },

  methods: {
    showAgent(){
      this.$emit('openPage', 1);
    },

    showManager(){
      this.$emit('openPage', 0);
    },

    handleCommand(command) {
      if (command === 'logout') {
        this.logout()
      }
    },
    logout() {
      clearAuth()
      this.$router.push({ path: '/login' }).catch(() => {})
    },
  },
}
</script>

<style scoped lang="scss">
@use '@/styles/layout.scss' as *;

.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: $layout-header-height;
  padding: 0 20px;
  background: #fff;

  .top-nav__brand {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .top-nav__logo {
    width: 36px;
    height: 24px;
  }

  .top-nav__title {
    font-size: 18px;
    font-weight: 600;
    color: #1d2129;
    white-space: nowrap;
  }

  .top-nav__actions {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .top-nav__user {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    outline: none;

    &:hover {
      .top-nav__username {
        color: #0073ff;
      }
    }
  }

  .top-nav__username {
    font-size: 14px;
    color: #1d2129;
    max-width: 120px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    transition: color 0.2s;
  }

  .top-nav__arrow {
    font-size: 12px;
    color: #86909c;
  }
}
</style>
