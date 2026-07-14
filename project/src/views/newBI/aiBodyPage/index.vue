<template>
  <div class="agent-sidebar my-custom-style">
    <div class="agent-sidebar__header">
      <div class="agent-sidebar__header-title">
        <span class="agent-sidebar__header-badge">
          <base-icon name="bot" :size="14" :stroke-width="2" />
        </span>
        <span>我的智能体</span>
      </div>

      <button
        class="agent-sidebar__add-btn"
        title="新建智能体"
        @click="showNewAiBodyPage()"
      >
        <base-icon name="plus" :size="14" :stroke-width="2.2" />
      </button>
    </div>

    <div class="agent-sidebar__list no-scrollbar">
      <div
        v-for="agent in agentList"
        :key="agent.code"
        class="agent-sidebar__item"
        :class="{
          'is-active': currentAgent && currentAgent.code === agent.code,
        }"
        @click="selectAgent(agent)"
      >
        <span class="agent-sidebar__avatar">
          <base-icon name="sparkles" :size="14" :stroke-width="2" />
        </span>

        <span class="agent-sidebar__name" :title="agent.name">
          {{ agent.name }}
        </span>

        <span class="agent-sidebar__actions" @click.stop>
          <button
            class="agent-sidebar__action-btn"
            title="编辑"
            @click="showNewAiBodyPage(agent)"
          >
            <base-icon name="edit" :size="13" :stroke-width="2" />
          </button>
          <button
            class="agent-sidebar__action-btn agent-sidebar__action-btn--danger"
            title="删除"
            @click="deleteAgent(agent)"
          >
            <base-icon name="trash" :size="13" :stroke-width="2" />
          </button>
        </span>
      </div>

      <div v-if="agentList.length === 0" class="agent-sidebar__empty">
        <base-icon name="bot" :size="22" :stroke-width="1.6" />
        <span>暂无智能体，点击右上角 + 新建</span>
      </div>
    </div>

    <el-dialog
      width="880px"
      top="8vh"
      title="智能体配置"
      :visible.sync="isShowNewAiBodyPage"
      :show-close="false"
      :close-on-click-modal="false"
      append-to-body
      class="my-custom-style"
    >
      <new-AiBodyPage
        :agentItem="agentItem"
        v-if="isShowNewAiBodyPage"
        @close="close"
        @sure="sure"
      />
    </el-dialog>
  </div>
</template>

<script>
import {
  getAiBodyListAPI,
  deleteAiBodyAPI,
} from "@/api/smartQuery/smartQueryAPI";

import newAiBodyPage from "@/views/newBI/newAiBodyPage";
export default {
  name: "aiBodyPage",
  components: {
    newAiBodyPage,
  },
  data() {
    return {
      isShowNewAiBodyPage: false,
      agentList: [],
      agentItem: null, //编辑用的
      currentAgent: null, //当前选择得

      aiQueryParams: {
        keyword: "",
        page: 1,
        pageSize: 20,
        total: 1,
      },
    };
  },

  mounted() {
    this.getAiBodyList();
  },

  methods: {
    /*loadingScreen() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });

      return loading;
    },*/

    close() {
      this.isShowNewAiBodyPage = false;
    },

    sure() {
      this.isShowNewAiBodyPage = false;
      this.getAiBodyList();
    },

    getAgent(aiBodyCode) {
      let list = this.agentList.filter((item) => item.code == aiBodyCode);

      if (list.length > 0) return list[0];
      return null;
    },

    showNewAiBodyPage(item) {
      this.agentItem = item;
      this.isShowNewAiBodyPage = true;
    },

    selectAgent(agent) {
      this.currentAgent = agent;
      this.$emit("changeAgent", agent);
    },

    deleteAgent(agent) {
      this.$confirm("确定要删除 " + agent.name + " ?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          //const loading = this.loadingScreen();
          deleteAiBodyAPI(agent.code)
            .then((response) => {
              if (response.code == 200) {
                this.$message({
                  message: "删除成功",
                  type: "success",
                  duration: this.$messageDuration,
                });

                this.getAiBodyList();
              } else {
                this.$message({
                  message: response.message,
                  type: "error",
                  duration: this.$messageDuration,
                });
              }
            })
            .catch(() => {})
            .finally(() => {
              //loading.close();
            });
        })
        .catch(() => {});
    },

    getAiBodyList() {
      //const loading = this.loadingScreen();
      getAiBodyListAPI(this.aiQueryParams)
        .then((response) => {
          if (response.code == 200) {
            this.aiQueryParams.page = response.data.page;
            this.aiQueryParams.pageSize = response.data.pageSize;
            this.aiQueryParams.total = response.data.total;

            this.agentList = response.data.list;

            if (this.agentList.length > 0 && this.currentAgent == null) {
              this.$emit("changeAgent", this.agentList[0]);
              this.currentAgent = this.agentList[0];
            }
            /*if(this.agentList.length > 0){
         this.$refs.childRef.newPage(this.agentList[0]);
        }*/
          }
        })
        .catch(() => {})
        .finally(() => {
          //loading.close();
        });
    },
  },
};
</script>

<style scoped lang="scss">
.agent-sidebar {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.agent-sidebar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 2px 10px;
  flex-shrink: 0;
}

.agent-sidebar__header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
}

.agent-sidebar__header-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 7px;
  color: #fff;
  background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
  box-shadow: 0 2px 6px rgba(43, 92, 255, 0.25);
}

.agent-sidebar__add-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: 1px dashed rgba(43, 92, 255, 0.45);
  border-radius: 7px;
  background: rgba(43, 92, 255, 0.06);
  color: var(--brand, #2b5cff);
  cursor: pointer;
  transition: all 0.15s;

  &:hover {
    background: var(--brand, #2b5cff);
    border-style: solid;
    color: #fff;
    box-shadow: 0 2px 8px rgba(43, 92, 255, 0.3);
  }
}

.agent-sidebar__list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.agent-sidebar__item {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 34px;
  padding: 0 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover:not(.is-active) {
    background: rgba(43, 92, 255, 0.06);
  }

  &.is-active {
    background: rgba(43, 92, 255, 0.1);

    .agent-sidebar__name {
      color: var(--brand, #2b5cff);
      font-weight: 600;
    }

    .agent-sidebar__avatar {
      color: #fff;
      background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
      border-color: transparent;
    }
  }
}

.agent-sidebar__avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  border-radius: 7px;
  border: 1px solid var(--border-light, #e5eaf1);
  background: #fff;
  color: var(--brand, #2b5cff);
  transition: all 0.15s;
}

.agent-sidebar__name {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  color: var(--text-secondary, #475569);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
}

.agent-sidebar__actions {
  display: flex;
  align-items: center;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.15s;
}

.agent-sidebar__item:hover .agent-sidebar__actions,
.agent-sidebar__item.is-active .agent-sidebar__actions {
  opacity: 1;
}

.agent-sidebar__action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  padding: 0;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted, #94a3b8);
  cursor: pointer;
  transition: all 0.15s;

  &:hover {
    background: rgba(43, 92, 255, 0.12);
    color: var(--brand, #2b5cff);
  }

  &--danger:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }
}

.agent-sidebar__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px 8px;
  font-size: 12px;
  color: var(--text-muted, #94a3b8);
}
</style>
