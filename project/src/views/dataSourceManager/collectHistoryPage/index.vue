<template>
  <div>
    <div class="horizontal-line"></div>

    <div
      style="max-height: 65vh; overflow-y: auto; overflow-x: hidden"
      class="no-scrollbar"
    >
      <div style="display: flex">
        <div class="one-bgdiv">
        <div class="drag-table">
          <el-table :data="collectHistory" style="width: 100%" border>
            <el-table-column
              prop="startedAt"
              label="开始时间"
              width="auto"
              min-width="20%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            />
            <el-table-column
              prop="finishedAt"
              label="结束时间"
              width="auto"
              min-width="20%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            ></el-table-column>
            <el-table-column
              prop="collectTypeLabel"
              label="采集方式"
              width="auto"
              min-width="14%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            ></el-table-column>
            <el-table-column
              prop="tableCount"
              label="采集表数"
              width="auto"
              min-width="14%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            ></el-table-column>
            <el-table-column
              prop="diffSummary"
              label="新增/变更/删除"
              width="auto"
              min-width="18%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            ></el-table-column>
            <el-table-column
              prop="status"
              label="状态"
              width="auto"
              min-width="10%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            >
              <template slot-scope="scope">
                <!--<div :style="{ borderStyle:'solid', borderWidth: '1px',  borderColor: collectStatusEnum[scope.row.status].color, backgroundColor: collectStatusEnum[scope.row.status].bgColor, color: collectStatusEnum[scope.row.status].color }"> 
            -->
                {{ scope.row.status }}
                <!--</div>-->
              </template>
            </el-table-column>

            <el-table-column
              prop="durationSeconds"
              label="耗时"
              width="auto"
              min-width="10%"
              resizable
              sortable
              show-overflow-tooltip
              :render-header="renderHeader"
            ></el-table-column>

            <el-table-column
              label="操作"
              align="center"
              width="auto"
              min-width="10%"
            >
              <template slot-scope="scope">
                <el-button
                  type="text"
                  @click="showCollectHistoryDetail(scope.row)"
                  >详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>

                      <pagination
              v-show="queryParams.total > 0"
              :total="queryParams.total"
              :page.sync="queryParams.page"
              :limit.sync="queryParams.pageSize"
              @pagination="getCollectHistoryList"
            />
          </div>

        </div>
      </div>
    </div>

    <div class="horizontal-line"></div>

    <div style="display: flex">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
        <el-button @click="close">关闭</el-button>
      </div>
    </div>

    <el-dialog
      title="采集日志详情"
      :modal="false"
      :visible.sync="isCollectHistoryDetail"
      :show-close="false"
      width="70%"
      append-to-body
      class="my-custom-style"
    >
      <div class="horizontal-line"></div>

      <div style="width: 100%; display: flex; justify-content: center">
        <div
          style="
            height: 40vh;
            overflow-y: auto;
            background-color: #f6f6f3;
            width: 94%;
          "
        >
          <div style="text-align: left; margin-bottom: 5px; color: blue">
            # 采集日志
          </div>

          <div
            v-for="item in collectHistoryDetailList"
            :key="item.time"
            style="
              display: flex;
              align-items: flex-start;
              text-align: left;
              margin-bottom: 5px;
              margin-left: 15px;
            "
          >
            <div style="min-width: 70px">[{{ item.time }}]</div>
            &nbsp;
            <div style="min-width: 80px">[{{ item.level }}]</div>
            &nbsp;
            <div>{{ item.msg }}</div>
            <div>&nbsp;&nbsp;</div>
          </div>
        </div>
      </div>

      <div class="horizontal-line"></div>

      <div style="display: flex; padding-bottom: 5px">
        <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
          <el-button @click="isCollectHistoryDetail = false">关闭</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import {
  getCollectHistoryListAPI,
  getCollectHistoryDetailListAPI,
  collectStatusEnum,
} from "@/api/dataSourceManager/dataSourceAPI.js";

export default {
  name: "collectHistoryPage",
  props: ["dataSourceItem"],
  components: {},
  data() {
    return {
      collectStatusEnum,

      queryParams: {
        sourceId: null,
        status: null,
        page: 1,
        pageSize: 10,
        total: 0,
      },

      collectHistory: [],

      isCollectHistoryDetail: false,
      collectHistoryDetailList: [],
    };
  },

  mounted() {
    this.getCollectHistoryList();
  },

  methods: {
    renderHeader(h, { column }) {
      return h(
        "el-tooltip",
        {
          props: {
            content: column.label,
            placement: "top",
            effect: "dark",
          },
        },
        [
          h(
            "span",
            {
              class: "ellipsis-text",
              style: { maxWidth: "100%" },
            },
            column.label
          ),
        ]
      );
    },
    /*loadingScreen() {
        const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });

        return loading
      },*/

    close() {
      this.$emit("close");
    },

    findNthOccurrence(str, char, n) {
      const arr = str.split(char); // 分割字符串，不包括目标字符的片段将作为数组元素
      if (arr.length - 1 < n) return -1; // 如果分割后的数组长度小于n，说明没有足够的出现次数
      let position = 0;
      for (let i = 0; i < n; i++) {
        position += arr[i].length + char.length; // 累计每个片段的长度加上目标字符的长度得到位置
      }
      return position - char.length; // 返回第n次出现的位置（减去最后一个字符的长度，因为我们加了两次）
    },

    //采集历史列表
    getCollectHistoryList() {
      if (this.dataSourceItem != null) {
        this.queryParams.sourceId = this.dataSourceItem.id;
        //const loading = this.loadingScreen()
        getCollectHistoryListAPI(this.queryParams)
          .then((response) => {
            if (response.code == 200) {
              if (response.data != null) {
                this.collectHistory = [];

                this.queryParams.total = response.data.total;
                this.queryParams.page = response.data.page;
                this.queryParams.pageSize = response.data.pageSize;
                for (let i = 0; i < response.data.records.length; i++) {
                  let index = this.findNthOccurrence(
                    response.data.records[i].diffSummary,
                    "/",
                    3
                  );
                  if (index > -1) {
                    response.data.records[i].diffSummary =
                      response.data.records[i].diffSummary.substring(0, index);
                  }

                  this.collectHistory.push(response.data.records[i]);
                }
              }
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
            //loading.close()
          });
      }
    },

    showCollectHistoryDetail(row) {
      this.getCollectHistoryDetailList(row);
      this.isCollectHistoryDetail = true;
    },

    getCollectHistoryDetailList(row) {
      //const loading = this.loadingScreen()

      getCollectHistoryDetailListAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              this.collectHistoryDetailList = [];
              for (let i = 0; i < response.data.logLines.length; i++) {
                this.collectHistoryDetailList.push(response.data.logLines[i]);
              }
            }
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
          //loading.close()
        });
    },
  },
};
</script>


 <style scoped lang="scss">

</style>