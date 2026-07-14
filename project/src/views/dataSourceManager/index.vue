
<template>
  <div style="display: flex; width: 100%; height: 100%" class="my-custom-style">
    <div class="allbg">
      <div class="tablebg">
        <div class="searchBox">
          <div style="display: flex">
            <div style="width: 240px">
              <el-input
                v-model="queryParams.keyword"
                placeholder="搜索数据源名称..."
                @keyup.enter.native="handleEnter"
                suffix-icon="el-icon-search"
              />
            </div>
            <div style="margin-left: 10px; width: 120px">
              <el-select
                placeholder="请选择状态"
                v-model="queryParams.status"
                @change="handleEnter"
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
            <div style="margin-left: 10px">
              <el-button @click="getDataSourceList"
                ><base-icon name="refresh" :size="14"
              /></el-button>
            </div>
          </div>
          <div style="width: 100%"></div>

          <div style="text-align: right">
            <div>
              <el-button type="primary" @click="newDataSourceClick()"
                ><base-icon name="plus" :size="14" />&nbsp;新建数据源</el-button
              >
            </div>
          </div>
        </div>

        <div style="padding: 5px 20px 5px 20px">
          <div class="table-container">
            <div class="normal-table">
              <el-table
                :data="dataSourceList"
                border
                v-loading="loading"
                element-loading-text="加载中..."
                element-loading-background="rgb(248 248 248 / 50%)"
              >
                <el-table-column
                  type="index"
                  label="序号"
                  align="center"
                  width="65"
                  min-width="65"
                  fixed="left"
                  :resizable="false"
                />

                <el-table-column
                  prop="name"
                  label="数据源名称"
                  width="auto"
                  min-width="150%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                </el-table-column>
                <el-table-column
                  prop="dbType"
                  label="数据库类型"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                ></el-table-column>
                <el-table-column
                  prop="host"
                  label="主机地址"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                ></el-table-column>
                <el-table-column
                  prop="port"
                  label="端口"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                ></el-table-column>
                <el-table-column
                  prop="displayDbSchema"
                  label="数据库/Schema"
                  width="auto"
                  min-width="150%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                ></el-table-column>
                <el-table-column
                  label="操作"
                  align="center"
                  min-width="140px"
                  :resizable="false"
                >
                  <template slot-scope="scope">
                    <el-tooltip content="编辑" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="editDataSourceClick(scope.row)"><base-icon name="edit" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="采集" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="collectClick(scope.row)"><base-icon name="database" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="元数据" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="metaDataClick(scope.row)"><base-icon name="layers" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="采集历史" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="collectHistoryClick(scope.row)"><base-icon name="history" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="删除" placement="top">
                      <el-button type="text" class="op-icon-btn is-danger" @click="deleteDataSource(scope.row)"><base-icon name="trash" :size="15" /></el-button>
                    </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>

              <pagination
                v-show="queryParams.total > 0"
                :total="queryParams.total"
                :page.sync="queryParams.page"
                :limit.sync="queryParams.pageSize"
                @pagination="getDataSourceList"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      title="数据源"
      :close-on-click-modal="false"
      :visible.sync="isNewDataSource"
      :show-close="false"
      width="60%"
      top="10vh"
      append-to-body
      class="my-custom-style"
    >
      <newDataSource-Page
        v-if="isNewDataSource"
        :dataSourceItem="dataSourceItem"
        @close="closeNewDataSource"
        @sure="sureNewDataSource"
      />
    </el-dialog>

    <el-dialog
      :close-on-click-modal="false"
      :title="`元数据采集 - ${dataSourceItem ? dataSourceItem.name : ''}`"
      :visible.sync="isCollect"
      @close="closeCollect"
      :show-close="false"
      width="60%"
      top="10vh"
      append-to-body
      class="my-custom-style"
    >
      <collect-Page
        v-if="isCollect"
        :dataSourceItem="dataSourceItem"
        @close="isCollect = false"
      />
    </el-dialog>

    <el-dialog
      :close-on-click-modal="false"
      :title="`元数据信息 - ${dataSourceItem ? dataSourceItem.name : ''}`"
      :visible.sync="isMetaData"
      @close="closeMetaData"
      :show-close="false"
      width="60%"
      top="10vh"
      append-to-body
      class="my-custom-style"
    >
      <metaData-Page
        v-if="isMetaData"
        :dataSourceItem="dataSourceItem"
        @close="isMetaData = false"
      />
    </el-dialog>

    <el-dialog
      :close-on-click-modal="false"
      :title="`采集历史 - ${dataSourceItem ? dataSourceItem.name : ''}`"
      width="80%"
      top="10vh"
      :visible.sync="isCollectHistory"
      @close="closeCollectHistory"
      :show-close="false"
      append-to-body
      class="my-custom-style"
    >
      <collectHistory-Page
        v-if="isCollectHistory"
        :dataSourceItem="dataSourceItem"
        @close="isCollectHistory = false"
      />
    </el-dialog>
  </div>
</template>


<script>
import {
  getDataSourceListAPI,
  deleteDataSourceAPI,
  statusEnum,
} from "@/api/dataSourceManager/dataSourceAPI.js";

import newDataSourcePage from "@/views/dataSourceManager/newDataSourcePage";
import collectHistoryPage from "@/views/dataSourceManager/collectHistoryPage";
import metaDataPage from "@/views/dataSourceManager/metaDataPage";
import collectPage from "@/views/dataSourceManager/collectPage";

export default {
  name: "dataSourceManager",
  components: {
    newDataSourcePage,
    metaDataPage,
    collectHistoryPage,
    collectPage,
    statusEnum,
  },
  data() {
    return {
      statusEnum,

      loading: false,

      isNewDataSource: false, //显示新建，编辑
      isCollectHistory: false, //显示采集历史
      isMetaData: false, //显示元数据
      isCollect: false,

      dataSourceItem: null, //当前行

      dataSourceList: [],

      queryParams: {
        keyword: "",
        status: "",
        page: 1,
        pageSize: 10,
        total: 0,
      },
    };
  },

  mounted() {
    this.getDataSourceList();
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

    //新建数据源
    newDataSourceClick() {
      this.dataSourceItem = null;
      this.isNewDataSource = true;
    },

    //编辑数据源
    editDataSourceClick(row) {
      this.dataSourceItem = row;
      this.isNewDataSource = true;
    },

    sureNewDataSource() {
      this.isNewDataSource = false;
      this.getDataSourceList();
    },

    //关闭数据源
    closeNewDataSource() {
      // 执行关闭逻辑，例如隐藏对话框等
      this.isNewDataSource = false;
      //this.getDataSourceList();
    },

    //打开元数据
    metaDataClick(row) {
      this.dataSourceItem = row;
      this.isMetaData = true;
    },

    //关闭元数据
    closeMetaData() {
      this.isMetaData = false;

      //this.getDataSourceList();
    },

    //打开采集历史
    collectHistoryClick(row) {
      this.dataSourceItem = row;
      this.isCollectHistory = true;
    },

    //关闭采集历史
    closeCollectHistory() {
      this.isCollectHistory = false;
      //this.getDataSourceList();
    },

    //打开采集历史
    collectClick(row) {
      this.dataSourceItem = row;
      this.isCollect = true;
    },

    //关闭采集历史
    closeCollect() {
      this.isCollect = false;
      //this.getDataSourceList();
    },

    //搜索条件变化
    handleEnter() {
      this.getDataSourceList();
    },

    //获取数据源列表
    getDataSourceList() {
      //const loading = this.loadingScreen();
      this.loading = true;
      getDataSourceListAPI(this.queryParams)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              this.dataSourceList = [];

              this.queryParams.total = response.data.total;
              this.queryParams.page = response.data.page;
              this.queryParams.pageSize = response.data.pageSize;
              this.dataSourceList = response.data.list;

              /*for (let i = 0; i < response.data.list.length; i++) {
              this.dataSourceList.push(response.data.list[i]);
            }*/
            }
          } else {
            //访问失败
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

    //删除
    deleteDataSource(row) {
      this.$confirm("确定要删除 " + row.name + " ?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          //const loading = this.loadingScreen();
          deleteDataSourceAPI(row.id)
            .then((response) => {
              if (response.code == 200) {
                this.$message({
                  message: "删除成功",
                  type: "success",
                  duration: this.$messageDuration,
                });
                this.getDataSourceList();
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