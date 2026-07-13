<template>
  <div>
    <div class="horizontal-line"></div>

    <div
      style="max-height: 65vh; overflow-y: auto; overflow-x: hidden"
      class="no-scrollbar"
    >
      <div style="display: flex">
        <div class="title16-one-padding-bgdiv">
          目标数据源

          <div class="horizontal-line"></div>
        </div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          {{ dataSourceItem.name }} ({{ dataSourceItem.dbType }} |
          {{ dataSourceItem.host }}:{{ dataSourceItem.port }} |
          {{ dataSourceItem.defaultDb }})
        </div>
      </div>

      <div style="display: flex">
        <div class="title16-one-padding-bgdiv">
          采集方式

          <div class="horizontal-line"></div>
        </div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          <el-radio-group
            v-model="collectTypeRadio"
            @change="handleRadioChange"
          >
            <el-radio :label="collectTypeEnum.FULL.value">{{
              collectTypeEnum.FULL.name
            }}</el-radio>
            <el-radio :label="collectTypeEnum.SELECT.value">{{
              collectTypeEnum.SELECT.name
            }}</el-radio>
          </el-radio-group>
        </div>
      </div>

      <div style="display: flex">
        <div
          v-if="collectTypeRadio == collectTypeEnum.FULL.value"
          class="one-bgdiv"
        >
          <div class="warntext-bg">
            将对目标库中所有表执行全量元数据采集，包括表名、字段、类型、注释等信息。
          </div>
        </div>
        <div
          v-if="collectTypeRadio == collectTypeEnum.SELECT.value"
          class="one-bgdiv"
        >
          <div
            style="display: flex; padding: 0px 0px 5px; align-items: center"
          >
            <el-input
              v-model="queryParams.tableName"
              placeholder="搜索表名"
              style="width: 200px"
              @keyup.enter.native="handleEnter"
            ></el-input>

            <div style="margin-left: 10px">
              <el-button type="text" @click="toggleAllSelection"
                >全选</el-button
              >
            </div>
            <div style="margin-left: 10px">
              <el-button type="text" @click="clearAllSelection"
                >取消全选</el-button
              >
            </div>

            <div style="margin-left: 10px">
              已选
              {{
                allMultipleCollectRemoteTables.length +
                multipleCollectRemoteTables.length
              }}
              张表
            </div>
          </div>

          <div class="drag-table">
            <el-table
              :reserve-selection="true"
              ref="multipleTable"
              @selection-change="handleSelectionChange"
              :data="collectRemoteTables"
              border
            >
              <el-table-column label="序号" type="selection" width="55">
              </el-table-column>

              <el-table-column
                prop="tableName"
                label="表名"
                width="auto"
                min-width="100%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              ></el-table-column>
              <el-table-column
                prop="tableComment"
                label="注释"
                width="auto"
                min-width="100%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              ></el-table-column>
              <el-table-column
                prop="rowCountDisplay"
                label="预估行数"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
                width="auto"
                min-width="100%"
              ></el-table-column>
            </el-table>

            <pagination
              v-show="queryParams.total > 0"
              :total="queryParams.total"
              :page.sync="queryParams.page"
              :limit.sync="queryParams.pageSize"
              @pagination="pageSave"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="horizontal-line"></div>

    <div style="display: flex; padding-bottom: 5px">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
        <div
          style="
            display: flex;
            flex-direction: row;
            justify-content: space-between;
          "
        >
          <el-button @click="close()">取消</el-button>
          <el-button
            type="primary"
            @click="getBeginCollect()"
            style="width: 100px"
            >开始采集</el-button
          >
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {
  getCollectRemoteTablesListAPI,
  getBeginCollectAPI,
  getSelectTableListAPI,
  collectTypeEnum,
} from "@/api/dataSourceManager/dataSourceAPI.js";

export default {
  name: "collectPage",
  props: ["dataSourceItem"],
  components: {},
  data() {
    return {
      collectTypeEnum,
      collectTypeRadio: collectTypeEnum.FULL.value,

      //选择的数据表
      multipleCollectRemoteTables: [],
      allMultipleCollectRemoteTables: [],

      queryParams: {
        sourceId: "",
        tableName: "",
        page: 1,
        pageSize: 10,
        total: 0,
      },

      //远程数据表
      collectRemoteTables: [],
    };
  },

  mounted() {
    if (this.dataSourceItem != null)
      this.queryParams.sourceId = this.dataSourceItem.id;
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

    // 切换全选状态
    toggleAllSelection() {
      // 通过 $refs 获取表格实例，并调用 toggleAllSelection 方法
      this.$refs.multipleTable.toggleAllSelection();
    },
    // 清空所有选中
    clearAllSelection() {
      this.$refs.multipleTable.clearSelection();
    },

    handleRadioChange(val) {
      if (val == collectTypeEnum.SELECT.value) {
        this.getCollectRemoteTablesList();
      }
    },

    handleEnter() {
      this.getCollectRemoteTablesList();
    },

    handleSelectionChange(val) {
      this.multipleCollectRemoteTables = val; // 更新选中项数组
    },

    close() {
      this.$emit("close");
    },

    //获取数据表
    getCollectRemoteTablesList() {
      if (this.dataSourceItem != null) {
        this.queryParams.sourceId = this.dataSourceItem.id;
        //const loading = this.loadingScreen()
        getCollectRemoteTablesListAPI(this.queryParams)
          .then((response) => {
            if (response.code == 200) {
              if (response.data != null) {
                this.collectRemoteTables = [];

                this.queryParams.total = response.data.total;
                this.queryParams.page = response.data.page;
                this.queryParams.pageSize = response.data.pageSize;
                for (let i = 0; i < response.data.records.length; i++) {
                  this.collectRemoteTables.push(response.data.records[i]);

                  const index = this.allMultipleCollectRemoteTables.findIndex(
                    (item) =>
                      item.tableName == response.data.records[i].tableName
                  );

                  if (index > -1) {
                    const rowToSelect = this.collectRemoteTables[i];
                    this.$refs.multipleTable.toggleRowSelection(
                      rowToSelect,
                      true
                    ); // 设置选中状态为 true
                    this.allMultipleCollectRemoteTables.splice(index, 1);
                  }
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

    pageSave() {
      for (let i = 0; i < this.multipleCollectRemoteTables.length; i++) {
        this.allMultipleCollectRemoteTables.push(
          this.multipleCollectRemoteTables[i]
        );
      }
      this.multipleCollectRemoteTables = [];
      this.getCollectRemoteTablesList();
    },

    //开始采集
    getBeginCollect() {
      if (this.dataSourceItem != null) {
        let data = null;
        if (this.collectTypeRadio == collectTypeEnum.FULL.value) {
          data = { collectType: collectTypeEnum.FULL.value };
        } else {
          data = {
            collectType: collectTypeEnum.SELECT.value,
            tableNames: [],
          };

          for (let i = 0; i < this.multipleCollectRemoteTables.length; i++) {
            data.tableNames.push(this.multipleCollectRemoteTables[i].tableName);
          }

          for (let i = 0; i < this.allMultipleCollectRemoteTables.length; i++) {
            data.tableNames.push(
              this.allMultipleCollectRemoteTables[i].tableName
            );
          }

          if (data.tableNames.length == 0) {
            this.$message({
              message: "请选择数据表",
              type: "error",
              duration: this.$messageDuration,
            });
            return;
          }
        }

        //const loading = this.loadingScreen()
        getBeginCollectAPI(this.dataSourceItem.id, data)
          .then((response) => {
            if (response.code == 200) {
              if (response.data != null) {
                this.$message({
                  message: response.data.message,
                  type: "success",
                  duration: this.$messageDuration,
                });

                this.close();
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
  },
};
</script>



 <style scoped lang="scss">

</style>