<template>
  <div style="display: flex; width: 100%; height: 100%; max-height: 86vh; overflow-y: auto; overflow-x: hidden">
    <div class="allbg">
      <div class="tablebg" style="display: flex; flex-direction: row">
        <div style="width: 300px; background-color: white; border-right-style: solid; border-right-width: 1px; border-right-color: #ccc; height: 100%">
          <div style="margin-top: 10px; text-align: left; padding: 0 10px 0 20px">我的智能体</div>

          <div style="height: 48%; max-height: 48%; overflow-y: auto; overflow-x: hidden">
            <div v-for="(item, index) in agentList" :key="item.id">
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 20px 0 20px">
                <div style="display: flex; align-items: center">
                  <div class="green-dot"></div>
                  &nbsp;&nbsp;
                  <el-button type="text" size="medium" @click="selectAgent(item)">{{ item.name }}</el-button>
                </div>

                <div style="display: flex; align-items: center">
                  <el-button size="mini" icon="el-icon-plus" style="border-radius: 50%; padding: 4px"></el-button>
                  <el-button size="mini">编辑</el-button>
                </div>
              </div>
            </div>
          </div>

          <div class="horizontal-line"></div>

          <div style="height: 44%; width: 300px">
            <div style="text-align: left; padding: 10px 10px 10px 20px; font-size: 13px">历史记录</div>

            <div style="margin-left: 5px; height: 100%; max-height: 100%; overflow-y: auto; overflow-x: hidden">
              <el-collapse v-model="activeNames">
                <el-collapse-item name="1" v-if="chatHistoryListItem.today.length > 0">
                  <span class="collapse-title" slot="title">今天</span>
                  <div
                    v-for="item in chatHistoryListItem.today"
                    :key="item.id"
                    style="text-align: left; padding: 0 10px 0 20px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
                  >
                    <el-button style="padding: 5px; color: black" type="text" @click="changeChat(item)">{{ item.chatName }}</el-button>
                  </div>
                </el-collapse-item>

                <el-collapse-item name="2" v-if="chatHistoryListItem.yesterday.length > 0">
                  <span class="collapse-title" slot="title">昨天</span>
                  <div
                    v-for="item in chatHistoryListItem.yesterday"
                    :key="item.id"
                    style="text-align: left; padding: 0 10px 0 20px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
                  >
                    <el-button style="padding: 5px; color: black" type="text" @click="changeChat(item)">{{ item.chatName }}</el-button>
                  </div>
                </el-collapse-item>

                <el-collapse-item name="3" v-if="chatHistoryListItem.lastWeek.length > 0">
                  <span class="collapse-title" slot="title">近一周</span>

                  <div
                    v-for="item in chatHistoryListItem.lastWeek"
                    :key="item.id"
                    style="text-align: left; padding: 0 10px 0 20px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
                  >
                    <el-button style="padding: 5px; color: black" type="text" @click="changeChat(item)">{{ item.chatName }}</el-button>
                  </div>
                </el-collapse-item>
                <el-collapse-item name="4" v-if="chatHistoryListItem.lastMonth.length > 0">
                  <span class="collapse-title" slot="title">近一月</span>
                  <div
                    v-for="item in chatHistoryListItem.lastMonth"
                    :key="item.id"
                    style="text-align: left; padding: 0 10px 0 20px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
                  >
                    <el-button style="padding: 5px; color: black" type="text" @click="changeChat(item)">{{ item.chatName }}</el-button>
                  </div>
                </el-collapse-item>
                <el-collapse-item name="5" v-if="chatHistoryListItem.lastSixMonth.length > 0">
                  <span class="collapse-title" slot="title">近六月</span>
                  <div
                    v-for="item in chatHistoryListItem.lastSixMonth"
                    :key="item.id"
                    style="text-align: left; padding: 0 10px 0 20px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
                  >
                    <el-button style="padding: 5px; color: black" type="text" @click="changeChat(item)">{{ item.chatName }}</el-button>
                  </div>
                </el-collapse-item>

                <el-collapse-item name="6" v-if="chatHistoryListItem.moreThanSixMonth.length > 0">
                  <span class="collapse-title" slot="title">六个月前</span>

                  <div
                    v-for="item in chatHistoryListItem.moreThanSixMonth"
                    :key="item.id"
                    style="text-align: left; padding: 0 10px 0 20px; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis"
                  >
                    <el-button style="padding: 5px; color: black" type="text" @click="changeChat(item)">{{ item.chatName }}</el-button>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </div>

        <div style="width: 100%; height: 100%">
          <div style="height: 100%">
            <!--<div style="width: 100%; height: 100%">
          <div style="height:100%;">
            <div
              style="
                display: flex;
                justify-content: space-between;

                height:100%;
              "
            >-->

            <query-Page ref="childRef" :agentItem="agentItem" />

            <!--</div>-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import queryPage from '@/views/smartQuery/queryPage';

import {getChatHistoryListAPI, getChatHistoryListDetailAPI} from '@/api/smartQuery/smartQueryAPI';

export default {
  name: 'smartQuery',
  components: {
    queryPage,
  },
  data() {
    return {
      activeNames: [],

      agentList: [
        {id: '1', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '电网问数'},
        {id: '2', name: '新疆问数'},
      ],

      agentItem: {id: '1', name: '电网问数'},

      chatHistoryListItem: {
        lastMonth: [],
        lastSixMonth: [],
        lastWeek: [],
        moreThanSixMonth: [],
        today: [],
        yesterday: [],
      },

      chatHistoryDetail: {},
    };
  },

  mounted() {
    this.getChatHistoryList();
  },

  methods: {
    changeChat(row) {
      this.getChatHistoryListDetail(row);
    },

    selectAgent(item) {
      //this.agentItem = item

      this.$refs.childRef.newPage(item);
    },

    getChatHistoryListDetail(row) {
      //let query = {chatSessionId: row.chatSessionId}
      let query = {chatSessionId: 'a4baa727-5ab5-4177-a85c-4f88cfc71597', chatId: '9993229e-49d3-4e72-bc7a-04f6b1097fc7'};

      getChatHistoryListDetailAPI(query).then(response => {
        if (response.code == 200) {
          this.chatHistoryDetail = response.data;

          this.$refs.childRef.setItems(this.chatHistoryDetail);
        }
      });
    },

    getChatHistoryList() {
      getChatHistoryListAPI().then(response => {
        if (response.code == 200) {
          this.chatHistoryListItem = response.data;
        }
      });
    },
  },
};
</script>

<style scoped lang="scss">
.allbg {
  background-color: #f2f3f7;
  width: 100%;

  min-width: 1220px;
  min-height: 812px;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
}

.tablebg {
  background-color: white;

  width: 96%;

  height: 95%;
}

.table-container {
  width: 100%;
}

.searchBox {
  //display: flex;
  //flex-direction: row;
  padding: 20px 20px 10px 20px;
}

::v-deep .el-table::before {
  height: 0px;
}

::v-deep .el-select .el-input .el-select__caret {
  color: #000000;
}

::v-deep .el-header {
  padding: 0;
}

::v-deep .el-main {
  padding: 0;
}

.vertical-line {
  width: 5px; /* 竖线的宽度 */
  height: 15px; /* 竖线的高度 */
  background-color: #037aff; /* 竖线的颜色 */
}

.horizontal-line {
  border-top: 1px solid #ccc; /* 1px 厚的横线，颜色为浅灰色 */
  margin: 0; /* 根据需要调整间距 */
}

::v-deep .el-tag.el-tag--info {
  margin-bottom: 10px;
}

.onebgdiv {
  width: 100%;
  text-align: left;
  padding: 0px 20px 10px 20px;
}

.green-dot {
  width: 10px; /* 或者任何大小 */
  height: 10px; /* 或者任何大小 */
  background-color: green; /* 设置颜色为绿色 */
  border-radius: 50%; /* 使圆角达到圆形效果 */
}

.collapse-title {
  flex: 1 0 90%; /* 让标题占据大部分空间 */
  order: 1; /* order 值越大越靠后，确保标题在箭头右侧 */
  text-align: left;
}

/* 将箭头图标的 flex 顺序提前 */
::v-deep .el-collapse-item__header {
  flex: 1 0 auto;
  order: -1; /* order 值越小越靠前，将箭头移至最左侧 */
  height: 30px;
  border-bottom: 0;
}

::v-deep .el-collapse-item__arrow {
  margin: 0 2px 0 auto;
}

::v-deep .el-collapse {
  border-top: 0;
  border-bottom: 0;
}

::v-deep .el-collapse-item__content {
  padding-bottom: 0;
}

::v-deep .el-collapse-item__wrap {
  border-bottom: 0;
}
</style>
