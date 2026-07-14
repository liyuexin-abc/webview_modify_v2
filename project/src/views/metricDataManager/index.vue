
<template>
  <div style="display: flex; width: 100%; height: 100%" class="my-custom-style">
    <div class="allbg">
      <div class="tablebg">
        <div class="searchBox">
          <div style="display: flex">
            <div style="width: 240px">
              <el-input
                v-model="queryParams.keyword"
                @keyup.enter.native="handleEnter"
                placeholder="搜索指标..."
                suffix-icon="el-icon-search"
              >
              </el-input>
            </div>
            <div style="margin-left: 10px; width: 120px">
              <el-select
                placeholder="请选择类型"
                @change="handleEnter"
                v-model="queryParams.type"
              >
                <el-option label="全部类型" value=""></el-option>

                <el-option
                  v-for="item in typeEnum"
                  :key="item.value"
                  :label="item.name"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </div>

            <div style="margin-left: 10px; width: 120px">
              <el-select
                placeholder="请选择状态"
                @change="handleEnter"
                v-model="queryParams.status"
              >
                <el-option label="全部状态" value=""></el-option>

                <el-option
                  v-for="item in statusEnum"
                  :key="item.value"
                  :label="item.name"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </div>

            <div style="margin-left: 10px; text-align: right">
              <el-button
                @click="getMetricDataList"
              ><base-icon name="refresh" :size="14" /></el-button>
            </div>
          </div>

          <div style="width: 100%"></div>

          <div>
            <el-button type="primary" @click="nenMetricDataClick()"
              ><base-icon name="plus" :size="14" />&nbsp;新建指标</el-button
            >
          </div>
        </div>

        <div style="padding: 10px 20px 10px 20px">
          <div class="table-container">
            <div class="normal-table">
              <el-table
                :data="metricDataList"
                border
                v-loading="loading"
                element-loading-text="加载中..."
                element-loading-background="rgb(248 248 248 / 50%)"
              >
                <el-table-column
                  label="序号"
                  align="center"
                  type="index"
                  width="65"
                  min-width="65"
                  fixed="left"
                  :resizable="false"
                />
                <el-table-column
                  label="指标英文名"
                  prop="englishName"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="指标名称"
                  prop="chineseName"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="口径"
                  prop="caliber"
                  width="auto"
                  min-width="70%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="默认单位"
                  prop="unit"
                  width="auto"
                  min-width="40%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="指标类型"
                  prop="type"
                  width="auto"
                  min-width="50%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <div
                      style="
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                      "
                    >
                    
                      {{ !scope.row.type ? '' : typeEnum[scope.row.type.toLowerCase()].name}}
                    </div>
                  </template>
                </el-table-column>

                <el-table-column
                  label="状态"
                  prop="status"
                  width="auto"
                  min-width="50%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <div
                      style="
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                      "
                    >
                      {{ statusEnum[scope.row.status].name }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="负责人"
                  prop="principalName"
                  width="auto"
                  min-width="70%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="更新时间"
                  prop="updatedAt"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="操作"
                  align="center"
                  min-width="100px"
                  :resizable="false"
                >
                  <template slot-scope="scope">
                    <el-tooltip content="编辑" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="editMetricDataClick(scope.row)"><base-icon name="edit" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="下线" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="offlineMetricData(scope.row)" v-if="scope.row.status == 2"><base-icon name="sort-desc" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="上线" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="onlineMetricData(scope.row)" v-if="scope.row.status == 3"><base-icon name="sort-asc" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="删除" placement="top">
                      <el-button type="text" class="op-icon-btn is-danger" @click="deleteMetricData(scope.row)"><base-icon name="trash" :size="15" /></el-button>
                    </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>

              <pagination
                v-show="queryParams.total > 0"
                :total="queryParams.total"
                :page.sync="queryParams.page"
                :limit.sync="queryParams.pageSize"
                @pagination="getMetricDataList"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-drawer
      title="指标"
      :visible.sync="isNewMetricData"
      direction="rtl"
      size="50%"
      :wrapperClosable="false"
      :show-close="false"
      append-to-body
      class="my-custom-style"
    >
      <span>
        <newMetricData-Page
          v-if="isNewMetricData"
          :metricDataItem="metricDataItem"
          @close="closeMetricData"
          @sure="sureMetricData"
        />
      </span>
    </el-drawer>
  </div>
</template>


<script>
import {
  getMetricDataListAPI,
  deleteMetricDataAPI,
  offlineMetricDataAPI,
  onlineMetricDataAPI,
  typeEnum,
  statusEnum,
} from "@/api/metricDataManager/metricDataAPI.js";

import newMetricDataPage from "@/views/metricDataManager/newMetricDataPage";

export default {
  name: "metricDataManager",
  components: {
    newMetricDataPage,
  },
  data() {
    return {
      typeEnum,
      statusEnum,

      loading: false,

      isNewMetricData: false,

      metricDataItem: null,
      //指标列表
      metricDataList: [],

      queryParams: {
        keyword: "",
        type: "",
        status: "",
        page: 1,
        pageSize: 10,
        total: 0,
      },
    };
  },

  mounted() {
    this.getMetricDataList();
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
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });

      return loading;
    },*/

    //新建指标
    nenMetricDataClick() {
      this.metricDataItem = null;
      this.isNewMetricData = true;
    },

    //编辑指标
    editMetricDataClick(row) {
      this.metricDataItem = row;
      this.isNewMetricData = true;
    },

    //关闭指标
    closeMetricData() {
      // 执行关闭逻辑，例如隐藏对话框等
      this.isNewMetricData = false;
      //this.getMetricDataList();
    },

    //关闭指标
    sureMetricData() {
      // 执行关闭逻辑，例如隐藏对话框等
      this.isNewMetricData = false;
      this.getMetricDataList();
    },

    handleEnter() {
      this.getMetricDataList();
    },

    getMetricDataList() {
      //const loading = this.loadingScreen();
      this.loading = true;
      getMetricDataListAPI(this.queryParams)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              this.metricDataList = [];

              this.queryParams.total = response.data.total;
              this.queryParams.page = response.data.page;
              this.queryParams.pageSize = response.data.pageSize;
              this.metricDataList = response.data.records;
              /*for (let i = 0; i < response.data.records.length; i++) {
              this.metricDataList.push(response.data.records[i]);
            }*/
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
          //loading.close();
          this.loading = false;
        });
    },

    //下线
    offlineMetricData(row) {
      // const loading = this.loadingScreen();
      offlineMetricDataAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "下线成功",
              type: "success",
              duration: this.$messageDuration,
            });
            this.getMetricDataList();
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
    //上线
    onlineMetricData(row) {
      //const loading = this.loadingScreen();
      onlineMetricDataAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "上线成功",
              type: "success",
              duration: this.$messageDuration,
            });
            this.getMetricDataList();
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

    //删除
    deleteMetricData(row) {
      this.$confirm("确定要删除 " + row.chineseName + " ?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          //const loading = this.loadingScreen();
          deleteMetricDataAPI(row.id)
            .then((response) => {
              if (response.code == 200) {
                this.$message({
                  message: "删除成功",
                  type: "success",
                  duration: this.$messageDuration,
                });
                this.getMetricDataList();
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
  },
};
</script>


 <style scoped lang="scss">

</style>