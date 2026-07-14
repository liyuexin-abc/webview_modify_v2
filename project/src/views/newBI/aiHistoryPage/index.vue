<template>
  <div class="history-sidebar my-custom-style">
    <div class="history-sidebar__header">
      <span class="history-sidebar__header-badge">
        <base-icon name="history" :size="14" :stroke-width="2" />
      </span>
      <span>历史记录</span>
    </div>

    <div class="history-sidebar__list no-scrollbar">
      <template v-for="item in chatHistoryListItem">
        <div v-if="item.records.length > 0" :key="item.key" class="history-sidebar__group">
          <div class="history-sidebar__group-label">{{ item.name }}</div>

          <div
            v-for="record in item.records"
            :key="record.chatSessionId"
            class="history-sidebar__item"
            :title="record.chatName"
            @click="getChatHistoryListDetail(record)"
          >
            <base-icon
              name="message-plus"
              :size="13"
              :stroke-width="1.8"
              class="history-sidebar__item-icon"
            />
            <span class="history-sidebar__item-name">{{ record.chatName }}</span>
          </div>
        </div>
      </template>

      <div v-if="isAllEmpty" class="history-sidebar__empty">
        <base-icon name="clock" :size="22" :stroke-width="1.6" />
        <span>暂无历史对话</span>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getChatHistoryListAPI,
  getChatHistoryListDetailAPI,
} from "@/api/smartQuery/smartQueryAPI";

export default {
  name: "aiHistoryPage",
  data() {
    return {
      chatHistoryListItem: [],
    };
  },

  computed: {
    isAllEmpty() {
      return (
        this.chatHistoryListItem.length === 0 ||
        this.chatHistoryListItem.every((item) => item.records.length === 0)
      );
    },
  },

  mounted() {
    //this.getChatHistoryList();
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

    getChatHistoryList(aiBodyCode) {
      //const loading = this.loadingScreen();
      getChatHistoryListAPI()
        .then((response) => {
          if (response.code == 200) {
            this.chatHistoryListItem = [];

            let today = {
              key: "today",
              name: "今天",
              records: response.data.today.filter(
                (item) => item.aiBodyCode == aiBodyCode
              ),
            };
            this.chatHistoryListItem.push(today);

            let yesterday = {
              key: "yesterday",
              name: "昨天",
              records: response.data.yesterday.filter(
                (item) => item.aiBodyCode == aiBodyCode
              ),
            };
            this.chatHistoryListItem.push(yesterday);
            let lastWeek = {
              key: "lastWeek",
              name: "上周",
              records: response.data.lastWeek.filter(
                (item) => item.aiBodyCode == aiBodyCode
              ),
            };
            this.chatHistoryListItem.push(lastWeek);
            let lastMonth = {
              key: "lastMonth",
              name: "上个月",
              records: response.data.lastMonth.filter(
                (item) => item.aiBodyCode == aiBodyCode
              ),
            };
            this.chatHistoryListItem.push(lastMonth);
            let lastSixMonth = {
              key: "lastSixMonth",
              name: "六个月",
              records: response.data.lastSixMonth.filter(
                (item) => item.aiBodyCode == aiBodyCode
              ),
            };
            this.chatHistoryListItem.push(lastSixMonth);
            let moreThanSixMonth = {
              key: "moreThanSixMonth",
              name: "六个月前",
              records: response.data.moreThanSixMonth.filter(
                (item) => item.aiBodyCode == aiBodyCode
              ),
            };
            this.chatHistoryListItem.push(moreThanSixMonth);
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
    },

    getChatHistoryListDetail(row) {
      let query = { chatSessionId: row.chatSessionId };
      //const loading = this.loadingScreen();
      getChatHistoryListDetailAPI(query)
        .then((response) => {
          if (response.code == 200) {
            let chatHistoryDetail = response.data;
            this.$emit("changeHistory", chatHistoryDetail);
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
    },
  },
};
</script>

<style scoped lang="scss">
.history-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.history-sidebar__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 2px 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
  flex-shrink: 0;
}

.history-sidebar__header-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 7px;
  color: #fff;
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.25);
}

.history-sidebar__list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.history-sidebar__group {
  margin-bottom: 10px;
}

.history-sidebar__group-label {
  padding: 4px 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--text-muted, #94a3b8);
  text-align: left;
}

.history-sidebar__item {
  display: flex;
  align-items: center;
  gap: 7px;
  height: 32px;
  padding: 0 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover {
    background: rgba(43, 92, 255, 0.06);

    .history-sidebar__item-name {
      color: var(--brand, #2b5cff);
    }

    .history-sidebar__item-icon {
      color: var(--brand, #2b5cff);
    }
  }
}

.history-sidebar__item-icon {
  flex-shrink: 0;
  color: var(--text-muted, #94a3b8);
  transition: color 0.15s;
}

.history-sidebar__item-name {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  color: var(--text-secondary, #475569);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
  transition: color 0.15s;
}

.history-sidebar__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px 8px;
  font-size: 12px;
  color: var(--text-muted, #94a3b8);
}
</style>
