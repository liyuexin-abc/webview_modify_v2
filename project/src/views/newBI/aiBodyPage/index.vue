<template>
  <div style="width: 100%; height: 100%" class="my-custom-style">
    <div
      style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 10px 0;
        cursor: pointer;
      "
      @click="showNewAiBodyPage()"
    >
      <div style="font-size: 13px; display: flex; align-items: center">
        <IntelligentAgent class="agent-sidebar__title-icon" />

        <span style="font-weight: bold">&nbsp;&nbsp;我的智能体</span>
      </div>

      <div style="margin: 0 10px">
        <!--<el-button
          type="primary"
          size="mini"
          icon="el-icon-plus"
          style="border-radius: 50%; padding: 6px"
          @click="showNewAiBodyPage()"
        ></el-button>-->

        <i class="el-icon-plus"></i>
      </div>
    </div>

    <div
      style="max-height: 95%; height: 95%; overflow-y: auto; overflow-x: hidden"
      class="no-scrollbar"
    >
      <div
        v-for="agent in agentList"
        :key="agent.code"
        style="
          display: flex;
          justify-content: space-between;
          align-items: center;
          height: 30px;
        "
        class="agent-sidebar__item"
      >
        <div style="display: flex; align-items: center">
          <div style="display: flex">
            <img
              class="agent-sidebar__logo"
              src="@/assets/svgs/logo.svg"
              alt=""
            />
          </div>
          <div>
            <el-button type="text" @click="selectAgent(agent)">
              {{ agent.name }}</el-button
            >
          </div>
        </div>

        <div class="agent-sidebar__actions" style="display: flex">
          <div>
            <!--<el-button
            type="text" size="mini"


            @click="selectAgent(agent)"
            class="agent-sidebar__new-chat-btn"
          >
          <NewChat class="agent-sidebar__new-chat-icon" />
          </el-button>-->
            <el-button
              style="
                border-radius: 50px;
                background: transparent;
                width: 16px;
                height: 16px;
                padding: 0px;
                color: #c8c8c8;
              "
              type="text"
              size="mini"
              icon="el-icon-remove"
              @click="deleteAgent(agent)"
            >
            </el-button>
          </div>

          <div style="margin-left: 4px">
            <el-button size="mini" @click="showNewAiBodyPage(agent)" type="text"
              >编辑</el-button
            >
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      width="70%"
      top="10vh"
      title="智能体配置"
      :visible.sync="isShowNewAiBodyPage"
      :show-close="false"
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
import IntelligentAgent from "@/components/svgs/IntelligentAgent.vue";
//import NewChat from "@/components/svgs/NewChat.vue";
export default {
  name: "aiBodyPage",
  components: {
    newAiBodyPage,
    IntelligentAgent,
    //NewChat,
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
.agent-sidebar__actions {
  display: flex;
  align-items: center;
  opacity: 0;
  transition: opacity 0.2s;

  .el-button {
    padding: 0 4px;
    font-size: 14px;
    color: #909399;
  }
}

.agent-sidebar__item {
  display: flex;
  align-items: center;
  padding: 0px 0px 0px 0px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;

  &:hover:not(.is-active) {
    background: rgba(#204ce9, 0.06);
  }

  &.is-active {
    .agent-sidebar__name {
      color: #204ce9;
    }

    .agent-sidebar__actions {
      opacity: 1;

      .el-button {
        color: #204ce9;
      }
    }
  }
}

.agent-sidebar__item:hover .agent-sidebar__actions {
  opacity: 1;
}

.agent-sidebar__logo {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-right: 8px;
  object-fit: contain;
}
</style>
