<!-- 左侧智能体侧边栏：展示智能体列表与按时间分组的历史会话记录 -->
<template>
  <div :class="['agent-sidebar-wrap', { 'is-collapsed': collapsed }]">
    <aside v-show="!collapsed" class="agent-sidebar">
    <div class="agent-sidebar__agents">
      <div class="agent-sidebar__header">
        <div class="agent-sidebar__header-left">
          <IntelligentAgent class="agent-sidebar__title-icon" />
          <span class="agent-sidebar__title">我的智能体</span>
        </div>
        <el-button type="text" icon="el-icon-plus" class="agent-sidebar__add-btn" @click="$emit('add-agent')" />
      </div>

      <ul v-loading="loading" class="agent-sidebar__list" @scroll="handleScroll">
        <li v-for="agent in agents" :key="agent.id" :class="['agent-sidebar__item', {'is-active': agent.id === currentAgentId}]" @click="handleSelect(agent)">
          <img class="agent-sidebar__logo" src="@/assets/svgs/logo.svg" alt="" />
          <span class="agent-sidebar__name">{{ agent.name }}</span>
          <div class="agent-sidebar__actions">
            <el-button type="text" size="mini" title="新会话" class="agent-sidebar__new-chat-btn" @click.stop="handleNewSession(agent)">
              <NewChat class="agent-sidebar__new-chat-icon" />
            </el-button>
            <el-button type="text" size="mini" @click.stop="$emit('edit-agent', agent)" style="margin-left: 0px">编辑</el-button>
          </div>
        </li>

        <li v-if="!loading && !agents.length" class="agent-sidebar__empty">暂无智能体</li>
      </ul>
    </div>

    <div class="agent-sidebar__history">
      <div class="agent-sidebar__history-title">
        <RecordHistory class="agent-sidebar__history-icon" />
        <span>历史记录</span>
      </div>
      <div v-loading="sessionLoading" class="agent-sidebar__history-body">
        <template v-if="visibleSessionGroups.length">
          <div v-for="group in visibleSessionGroups" :key="group.key" class="agent-sidebar__history-group">
            <div
              :class="['agent-sidebar__history-group-title', {'is-expanded': isGroupExpanded(group.key)}]"
              @click="toggleGroup(group.key)"
            >
              <i :class="isGroupExpanded(group.key) ? 'el-icon-arrow-down' : 'el-icon-arrow-right'" />
              <span>{{ group.label }}</span>
            </div>
            <div v-show="isGroupExpanded(group.key)" class="agent-sidebar__history-group-body">
              <ul class="agent-sidebar__history-list">
                <li
                  v-for="session in group.sessions"
                  :key="session.id"
                  :class="['agent-sidebar__history-item', {'is-active': session.id === activeSessionId}]"
                  @click="handleSelectSession(session)"
                >
                  <span class="agent-sidebar__history-name" :title="session.chatName">
                    {{ session.chatName }}
                  </span>
                  <i class="el-icon-delete agent-sidebar__history-delete" title="删除会话" @click.stop="handleDeleteSession(session)" />
                </li>
              </ul>
            </div>
          </div>
        </template>
        <div v-else-if="!sessionLoading" class="agent-sidebar__history-empty">暂无历史会话</div>
      </div>
    </div>

    <div class="agent-sidebar__footer">
      <button type="button" class="agent-sidebar__collapse-btn" @click="handleCollapse">
        <span class="agent-sidebar__collapse-icon" aria-hidden="true">«</span>
        <span>收起侧边栏</span>
      </button>
    </div>
  </aside>

    <button
      v-if="collapsed"
      type="button"
      class="agent-sidebar__expand-btn"
      title="展开侧边栏"
      @click="handleExpand"
    >
      <i class="el-icon-arrow-right" />
    </button>
  </div>
</template>

<script>
import {getAibodyList} from '@/api/smartQuery/aibody';
import IntelligentAgent from '@/components/svgs/IntelligentAgent.vue';
import RecordHistory from '@/components/svgs/RecordHistory.vue';
import NewChat from '@/components/svgs/NewChat.vue';

export default {
  name: 'AgentSidebar',
  components: {
    IntelligentAgent,
    RecordHistory,
    NewChat,
  },
  props: {
    sessionGroups: {
      type: Array,
      default: () => [],
    },
    activeSessionId: {
      type: [Number, String],
      default: null,
    },
    activeAgentId: {
      type: [Number, String],
      default: null,
    },
    sessionLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      agents: [],
      activeId: null,
      loading: false,
      page: 1,
      pageSize: 20,
      total: 0,
      keyword: '',
      expandedGroups: {},
      collapsed: false,
    };
  },
  computed: {
    hasMore() {
      return this.agents.length < this.total;
    },
    currentAgentId() {
      return this.activeAgentId ?? this.activeId;
    },
    visibleSessionGroups() {
      return this.sessionGroups.filter(group => group.sessions.length);
    },
  },
  watch: {
    visibleSessionGroups: {
      immediate: true,
      handler(groups) {
        groups.forEach(group => {
          if (this.expandedGroups[group.key] === undefined) {
            const hasActive = group.sessions.some(session => session.id === this.activeSessionId);
            this.$set(this.expandedGroups, group.key, hasActive);
          }
        });
      },
    },
    activeSessionId(id) {
      if (!id) return;
      const group = this.visibleSessionGroups.find(item =>
        item.sessions.some(session => session.id === id),
      );
      if (group) {
        this.$set(this.expandedGroups, group.key, true);
      }
    },
  },
  mounted() {
    this.fetchAgentList();
  },
  methods: {
    /** 加载智能体列表，append 为 true 时追加下一页 */
    async fetchAgentList(append = false) {
      if (this.loading) return;
      if (append && !this.hasMore) return;

      this.loading = true;
      try {
        const page = append ? this.page + 1 : 1;
        const data = await getAibodyList({
          page,
          pageSize: this.pageSize,
          keyword: this.keyword || undefined,
        });
        const list = data.data.list || [];
        this.agents = append ? [...this.agents, ...list] : list;
        this.page = data.data.page;
        this.total = data.data.total;

        if (!append && list.length && !this.currentAgentId) {
          this.setActiveAgent(list[0]);
        }
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.loading = false;
      }
    },
    handleScroll(e) {
      const {scrollTop, scrollHeight, clientHeight} = e.target;
      if (scrollHeight - scrollTop - clientHeight < 20) {
        this.fetchAgentList(true);
      }
    },
    setActiveAgent(agent) {
      this.activeId = agent.id;
      this.$emit('select-agent', agent);
    },
    handleSelect(agent) {
      this.setActiveAgent(agent);
    },
    handleNewSession(agent) {
      this.setActiveAgent(agent);
      this.$emit('new-session', agent);
    },
    handleSelectSession(session) {
      this.$emit('select-session', session);
    },
    handleDeleteSession(session) {
      this.$emit('delete-session', session);
    },
    isGroupExpanded(key) {
      return !!this.expandedGroups[key];
    },
    toggleGroup(key) {
      this.$set(this.expandedGroups, key, !this.expandedGroups[key]);
    },
    refresh(keyword = '') {
      this.keyword = keyword;
      this.activeId = null;
      this.fetchAgentList();
    },
    /** 根据智能体编码查找已加载的智能体 */
    findAgentByCode(code) {
      if (!code) return null;
      return (
        this.agents.find(agent => {
          const agentCode = agent.aicode || agent.code;
          return agentCode === code;
        }) || null
      );
    },
    handleCollapse() {
      this.collapsed = true;
      this.$emit('collapse-change', true);
    },
    handleExpand() {
      this.collapsed = false;
      this.$emit('collapse-change', false);
    },
  },
};
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.agent-sidebar-wrap {
  flex-shrink: 0;
  height: 100%;
  position: relative;
  transition: width 0.25s ease;

  &:not(.is-collapsed) {
    width: $sidebar-width;
  }

  &.is-collapsed {
    width: 0;
    overflow: visible;
  }
}

.agent-sidebar {
  width: $sidebar-width;
  height: 100%;
  border-right: 1px solid $border-color;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  .agent-sidebar__agents {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .agent-sidebar__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 12px 12px;
  }

  .agent-sidebar__header-left {
    display: flex;
    align-items: center;
    gap: 6px;
    min-width: 0;
  }

  .agent-sidebar__title-icon {
    flex-shrink: 0;
    color: #000;
    width: 13px;
  }

  .agent-sidebar__title {
    font-size: 15px;
    color: $text-primary;
    margin-left: 6px;
  }

  .agent-sidebar__add-btn {
    font-size: 16px;
    font-weight: 700;
    color: #000;
    padding: 0;
  }

  .agent-sidebar__list,
  .agent-sidebar__history-body {
    scrollbar-width: thin;
    scrollbar-color: #e2e5ec transparent;

    &::-webkit-scrollbar {
      width: 5px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }

    &::-webkit-scrollbar-thumb {
      background: #e2e5ec;
      border-radius: 10px;
    }

    &::-webkit-scrollbar-thumb:hover {
      background: #d4d8e0;
    }
  }

  .agent-sidebar__list {
    list-style: none;
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 0 8px;
    margin-top: 0px;
  }

  .agent-sidebar__item {
    display: flex;
    align-items: center;
    padding: 10px 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;

    &:hover:not(.is-active) {
      background: rgba($primary-color, 0.06);
    }

    &.is-active {
      .agent-sidebar__name {
        color: $primary-color;
      }

      .agent-sidebar__actions {
        opacity: 1;

        .el-button {
          color: $primary-color;
        }
      }
    }
  }

  .agent-sidebar__logo {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    margin-right: 8px;
    object-fit: contain;
  }

  .agent-sidebar__name {
    flex: 1;
    font-size: 13px;
    color: #000;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .agent-sidebar__actions {
    display: flex;
    align-items: center;
    opacity: 0;
    transition: opacity 0.2s;

    .el-button {
      padding: 0 4px;
      font-size: 14px;
      color: $text-secondary;
    }
  }

  .agent-sidebar__new-chat-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .agent-sidebar__new-chat-icon {
    display: block;
    width: 14px;
    height: 14px;
    color: inherit;

    svg {
      display: block;
      width: 100%;
      height: 100%;
    }
  }

  .agent-sidebar__item:hover .agent-sidebar__actions {
    opacity: 1;
  }

  .agent-sidebar__empty {
    padding: 24px 8px;
    text-align: center;
    font-size: 13px;
    color: $text-secondary;
  }

  .agent-sidebar__history {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 12px 12px 16px;
    border-top: 1px solid $border-color;
  }

  .agent-sidebar__history-title {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 8px;
  }

  .agent-sidebar__history-icon {
    flex-shrink: 0;
    width: 16px;
    height: 16px;

    svg {
      display: block;
      width: 100%;
      height: 100%;
    }
  }

  .agent-sidebar__history-body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
  }

  .agent-sidebar__history-group {
    margin-bottom: 4px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .agent-sidebar__history-group-title {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 4px;
    font-size: 13px;
    color: #000;
    cursor: pointer;
    user-select: none;

    i {
      flex-shrink: 0;
      font-size: 12px;
      color: #000;
    }
  }

  .agent-sidebar__history-group-body {
    margin-left: 5px;
    padding-left: 12px;
    border-left: 1px solid #dcdfe6;
  }

  .agent-sidebar__history-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .agent-sidebar__history-item {
    display: flex;
    align-items: center;
    padding: 8px 0;
    font-size: 13px;
    color: #000;
    cursor: pointer;
    transition: color 0.2s;

    &:hover {
      .agent-sidebar__history-delete {
        opacity: 1;
      }
    }

    &.is-active {
      color: $primary-color;
    }
  }

  .agent-sidebar__history-name {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .agent-sidebar__history-delete {
    flex-shrink: 0;
    margin-left: 6px;
    font-size: 16px;
    color: $text-secondary;
    opacity: 0;
    transition: opacity 0.2s, color 0.2s;

    &:hover {
      color: #f56c6c;
    }
  }

  .agent-sidebar__history-item.is-active .agent-sidebar__history-delete,
  .agent-sidebar__history-item:hover .agent-sidebar__history-delete {
    opacity: 1;
  }

  .agent-sidebar__history-empty {
    padding: 12px 4px;
    font-size: 12px;
    color: $text-secondary;
    text-align: center;
  }

  .agent-sidebar__footer {
    flex-shrink: 0;
    padding: 6px 12px;
    border-top: 1px solid $border-color;
  }

  .agent-sidebar__collapse-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    width: 100%;
    padding: 6px 0;
    border: none;
    background: transparent;
    cursor: pointer;
    font-size: 13px;
    color: #909399;
    transition: color 0.2s;

    &:hover {
      color: #606266;
    }
  }

  .agent-sidebar__collapse-icon {
    font-size: 16px;
    line-height: 1;
    letter-spacing: -3px;
  }
}

.agent-sidebar__expand-btn {
  position: absolute;
  left: 0px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  margin: 0;
  padding: 0;
  border: none;
  border-radius: 0 8px 8px 0;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  color: #0b0b0b;
  font-size: 14px;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
  }
}
</style>
