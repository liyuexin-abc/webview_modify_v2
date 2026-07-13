<template>
  <div style="height: 100%" class="my-custom-style">
    <div
      style="
        text-align: left;
        font-size: 13px;
        display: flex;
        align-items: center;
      "
    >
      <RecordHistory class="agent-sidebar__history-icon" />
      <span style="font-weight: bold">&nbsp;&nbsp;历史记录</span>
    </div>

    <div
      style="
        max-height: 95%;
        height: 95%;
        overflow-y: auto;
        overflow-x: hidden;
        margin-top: 5px;
      "
      class="no-scrollbar"
    >
      <div
        v-for="item in chatHistoryListItem"
        :key="item.key"
        style="margin-bottom: 5px"
      >
        <el-collapse class="aiCollapse">
          <el-collapse-item :name="item.key" v-if="item.records.length > 0">
            <span slot="title">{{ item.name }}</span>
            <div
              v-for="record in item.records"
              :key="record.id"
              style="text-align: left; padding: 0 10px 0 10px; font-size: 14px"
            >
              <el-button
                style="
                  padding: 5px;
                  color: black;
                  width: 100%;
                  text-align: left;
                  overflow: hidden;
                  text-overflow: ellipsis;
                  white-space: nowrap;
                "
                type="text"
                class="my-btn"
                @click="getChatHistoryListDetail(record)"
                >{{ record.chatName }}</el-button
              >
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getChatHistoryListAPI,
  getChatHistoryListDetailAPI,
} from "@/api/smartQuery/smartQueryAPI";
import RecordHistory from "@/components/svgs/RecordHistory.vue";

export default {
  name: "aiHistoryPage",
  components: {
    RecordHistory,
  },
  data() {
    return {
      chatHistoryListItem: [],
    };
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
/*.collapse-title {
  flex: 1 0 90%; 
  order: 1; 
  text-align: left;
}*/

/* 将箭头图标的 flex 顺序提前 */
.aiCollapse ::v-deep .el-collapse-item__header {
  flex: 1 0 auto;
  order: -1; /* order 值越小越靠前，将箭头移至最左侧 */
  height: 30px;
  border-bottom: 0;
  background: transparent;
}

.aiCollapse ::v-deep .el-collapse-item__arrow {
  margin: 0 2px 0 auto;
}

.aiCollapse {
  border-top: 0px;
  border-bottom: 0px;
}

.aiCollapse ::v-deep .el-collapse-item__content {
  padding-bottom: 0;
}

.aiCollapse ::v-deep .el-collapse-item__wrap {
  background: transparent;
  border-bottom: 0;
}

.aiCollapse ::v-deep .el-collapse-item__header {
  height: 24px;
  line-height: 24px;
}

.aiCollapse ::v-deep .my-btn:hover {
  color: #95c5fd !important;
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
</style>
