<template>
  <div
    style="
      display: flex;
      width: 100%;
      height: 100%;
      overflow-y: hidden;
      overflow-x: hidden;
      background-image: radial-gradient(
          ellipse at 15% 30%,
          rgba(248, 234, 252, 0.8) 0%,
          transparent 45%
        ),
        radial-gradient(
          ellipse at 85% 70%,
          rgba(226, 238, 255, 0.8) 0%,
          transparent 45%
        ),
        radial-gradient(
          ellipse at 50% 10%,
          rgba(255, 255, 255, 0.9) 0%,
          transparent 50%
        );
      border-top: 1px solid rgb(217 223 236);
    "
  >
    <div style="display: flex; width: 100%; height: 100%">
      <div
        style="
          width: 20%;
          max-width: 230px;
          min-width: 230px;
          height: 100%;
          border-right: 1px solid rgb(217 223 236);
        "
      >
        <div style="height: 50%; padding: 10px">
          <aiBody-Page ref="aiBodyRef" @changeAgent="changeAgent" />
        </div>
        <div style="height: 50%; padding: 10px">
          <ai-HistoryPage ref="aiHistoryRef" @changeHistory="changeHistory" />
        </div>
      </div>

      <div style="width: 80%; min-width: 790px; height: 100%">
        <query-Page ref="childRef" />
      </div>
    </div>
  </div>
</template>

<script>
import queryPage from "@/views/newBI/queryPage";
import aiHistoryPage from "@/views/newBI/aiHistoryPage";
import aiBodyPage from "@/views/newBI/aiBodyPage";

export default {
  name: "smartQuery",
  components: {
    queryPage,
    aiHistoryPage,
    aiBodyPage,
  },
  data() {
    return {
      selectedAgent: null,
    };
  },

  mounted() {},

  methods: {
    changeHistory(history) {
      let agent = this.$refs.aiBodyRef.getAgent(history.aiBodyCode);

      if (agent != null) {
        //拿到历史,设置给queryPage
        this.$refs.childRef.setHistory(agent, history);
      } else {
        this.$message({
          message: "该智能体已被删除，历史记录不能使用",
          type: "error",
          duration: this.$messageDuration,
        });
      }
    },

    changeAgent(agent) {
      if (agent == null) {
        this.$message({
          message: "该智能体不存在",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      this.$refs.childRef.setSelectedAgent(agent);
      this.$refs.aiHistoryRef.getChatHistoryList(agent.code);
    },
  },
};
</script>

<style scoped lang="scss">
/*.no-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.no-scrollbar::-webkit-scrollbar {
  overflow: hidden auto;
  display: none;
}

::v-deep .el-dialog__body {
  padding: 0;
}

::v-deep .el-dialog__header {
  text-align: left;
  font-weight: bold;
  font-size: 20px;
  padding: 10px 20px 0px 20px;
}

::v-deep .el-dialog {
  border-radius: 10px;
}

::v-deep .el-table,
::v-deep .el-table__body-wrapper {
  font-size: 14px;
}

::v-deep .el-table th {
  background-color: #f1f1f3;
  color: #4e5969;
}*/
</style>
