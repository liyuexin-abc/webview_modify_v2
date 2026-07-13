<template>
  <div>
    <div class="horizontal-line"></div>

    <div
      style="max-height: 65vh; overflow-y: auto; overflow-x: hidden"
      class="no-scrollbar"
    >
      <div style="display: flex">
        <div class="one-bgdiv">
          <el-input
            v-model="queryParams.tableName"
            placeholder="搜索表名..."
            style="width: 240px"
            @keyup.enter.native="handleEnter"
          />
        </div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          <div class="drag-table">
            <el-table
              :data="metaDataList"
              style="width: 100%"
              @expand-change="expandMetaData"
              class="expand-table"
              border
            >
              <el-table-column type="expand" width="20px">
                <template slot-scope="props">
                  <el-table
                    :data="props.row.metaDataColumnList"
                    style="width: 100%"
                    :row-style="{ backgroundColor: '#F5F7FA' }"
                    border
                  >
                    <el-table-column
                      type="index"
                      label="序号"
                      align="center"
                      width="65"
                      min-width="65"
                    />

                    <el-table-column
                      prop="columnName"
                      label="列名"
                      width="auto"
                      min-width="20%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    />

                    <el-table-column
                      prop="dataType"
                      label="数据类型"
                      width="auto"
                      min-width="20%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    />

                    <el-table-column
                      prop="isNullable"
                      label="可空"
                      width="auto"
                      min-width="15%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    >
                      <template slot-scope="scope">
                        <div v-if="scope.row.isNullable == 0">否</div>
                        <div v-if="scope.row.isNullable == 1">是</div>
                      </template>
                    </el-table-column>

                    <el-table-column
                      prop="isPk"
                      label="主键"
                      width="auto"
                      min-width="15%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    >
                      <template slot-scope="scope">
                        <span v-if="scope.row.isPk == 1" style="font-size: 16px"
                          >✓</span
                        >
                      </template>
                    </el-table-column>

                    <el-table-column
                      prop="columnComment"
                      label="注释"
                      width="auto"
                      min-width="20%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    />
                  </el-table>
                </template>
              </el-table-column>

              <el-table-column
                prop="tableName"
                label="表名"
                width="auto"
                min-width="20%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />
              <el-table-column
                prop="tableComment"
                label="注释"
                width="auto"
                min-width="30%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              ></el-table-column>
              <el-table-column
                prop="columnCount"
                label="字段数"
                width="auto"
                min-width="13%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              ></el-table-column>
              <el-table-column
                prop="rowCountDisplay"
                label="预估行数"
                width="auto"
                min-width="15%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              ></el-table-column>
              <el-table-column
                prop="lastCollectedAt"
                label="最近采集时间"
                width="auto"
                min-width="22%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              ></el-table-column>
            </el-table>

            <pagination
              v-show="queryParams.total > 0"
              :total="queryParams.total"
              :page.sync="queryParams.page"
              :limit.sync="queryParams.pageSize"
              @pagination="getMetadataList"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="horizontal-line"></div>

    <div style="display: flex; padding-bottom: 5px">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
        <el-button @click="close">关闭</el-button>
      </div>
    </div>
  </div>
</template>


<script>
import {
  getMetaDataListAPI,
  getMetaDataColumnsListAPI,
} from "@/api/dataSourceManager/dataSourceAPI.js";

export default {
  name: "metaDataPage",
  props: ["dataSourceItem"],
  components: {},
  data() {
    return {
      queryParams: {
        sourceId: "",
        tableName: "",
        page: 1,
        pageSize: 10,
        total: 0,
      },

      metaDataList: [],
    };
  },

  mounted() {
    if (this.dataSourceItem != null)
      this.queryParams.sourceId = this.dataSourceItem.id;

    this.getMetadataList();
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

    //搜索条件变化
    handleEnter() {
      this.getMetadataList();
    },

    getMetadataList() {
      if (this.dataSourceItem != null) {
        //const loading = this.loadingScreen()
        getMetaDataListAPI(this.queryParams)
          .then((response) => {
            if (response.code == 200) {
              if (response.data != null) {
                this.metaDataList = [];

                this.queryParams.total = response.data.total;
                this.queryParams.page = response.data.page;
                this.queryParams.pageSize = response.data.pageSize;
                for (let i = 0; i < response.data.records.length; i++) {
                  let temp = {
                    id: response.data.records[i].id,
                    tableName: response.data.records[i].tableName,
                    tableComment: response.data.records[i].tableComment,
                    columnCount: response.data.records[i].columnCount,
                    rowCountEstimate: response.data.records[i].rowCountEstimate,
                    rowCountDisplay: response.data.records[i].rowCountDisplay,
                    lastCollectedAt: response.data.records[i].lastCollectedAt,
                    metaDataColumnList: [],
                  };

                  this.metaDataList.push(temp);
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

    expandMetaData(row, expandedRows) {
      //展开的操作
      if (expandedRows.length > 0) {
        let queryParams = { tableId: expandedRows[0].id };
        //const loading = this.loadingScreen()
        getMetaDataColumnsListAPI(queryParams)
          .then((response) => {
            if (response.code == 200) {
              for (let i = 0; i < response.data.length; i++) {
                row.metaDataColumnList.push(response.data[i]);
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