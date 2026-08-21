
<template>
  <div style="display: flex; width: 100%; height: 100%" class="my-custom-style">
    <div class="allbg">
      <div class="tablebg">
        <div class="searchBox">
          <div style="display: flex">
            <div style="width: 240px">
              <el-input
                placeholder="搜索组合..."
                suffix-icon="el-icon-search"
                v-model="queryParams.keyword"
                @keyup.enter.native="handleEnter"
              >
              </el-input>
            </div>

            <div style="margin-left: 10px; width: 120px">
              <el-select
                placeholder="请选择状态"
                @change="handleEnter"
                v-model="queryParams.status"
              >
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
                @click="getPortfolioDataList"
              ><base-icon name="refresh" :size="14" /></el-button>
            </div>
          </div>

          <div style="width: 100%"></div>
          <div>
            <el-button type="primary" @click="nenPortfolioDataClick"
              ><base-icon name="plus" :size="14" />&nbsp;新建指标组合</el-button
            >
          </div>
        </div>

        <div style="padding: 10px 20px 10px 20px">
          <div class="table-container">
            <div class="normal-table">
              <el-table
                :data="portfolioDataList"
                border
                v-loading="loading"
                element-loading-text="加载中..."
                element-loading-background="rgb(248 248 248 / 50%)"
              >
                <el-table-column
                  label="序号"
                  align="center"
                  type="index"
                  width="65px"
                  min-width="65"
                  fixed="left"
                  :resizable="false"
                />
                <el-table-column
                  label="组合名称"
                  prop="groupName"
                  width="auto"
                  min-width="190%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="编码"
                  prop="groupCode"
                  width="auto"
                  min-width="190%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="字段数"
                  prop="fieldCount"
                  width="auto"
                  min-width="50%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="主题域"
                  prop="subjectDomain"
                  width="auto"
                  min-width="100%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="状态"
                  prop="statusName"
                  width="auto"
                  min-width="55%"
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
                      <el-button type="text" class="op-icon-btn" @click="editPortfolioDataClick(scope.row)"><base-icon name="edit" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="下线" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="offlineCandidates(scope.row)" v-if="scope.row.status == 2"><base-icon name="sort-desc" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="上线" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="onlineCandidates(scope.row)" v-if="scope.row.status == 3"><base-icon name="sort-asc" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="删除" placement="top">
                      <el-button type="text" class="op-icon-btn is-danger" @click="deletePortfolioData(scope.row)"><base-icon name="trash" :size="15" /></el-button>
                    </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>

              <pagination
                v-show="queryParams.total > 0"
                :total="queryParams.total"
                :page.sync="queryParams.page"
                :limit.sync="queryParams.pageSize"
                @pagination="getPortfolioDataList"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-drawer
      title="指标组合"
      :visible.sync="isNewPortfolio"
      direction="rtl"
      size="50%"
      :wrapperClosable="false"
      :show-close="false"
      append-to-body
      class="my-custom-style"
    >
      <span>
        <newPortfolio-Page
          v-if="isNewPortfolio"
          :portfolioDataItem="portfolioDataItem"
          @close="closePortfolioData"
          @sure="surePortfolioData"
        />
      </span>
    </el-drawer>
  </div>
</template>


<script>
import {
  getPortfolioDataListAPI,
  deletePortfolioDataAPI,
  offlineCandidatesAPI,
  onlineCandidatesAPI,
  statusEnum,
} from "@/api/portfolioManager/portfolioAPI.js";
import newPortfolioPage from "@/views/portfolioManager/newPortfolioPage";
export default {
  name: "portfolioManager",
  components: {
    newPortfolioPage,
  },
  data() {
    return {
      statusEnum,

      loading: false,

      isNewPortfolio: false,

      portfolioDataItem: null,
      portfolioDataList: [],

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
    this.getPortfolioDataList();
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
    nenPortfolioDataClick() {
      this.portfolioDataItem = null;
      this.isNewPortfolio = true;
    },

    //编辑数据源
    editPortfolioDataClick(row) {
      this.portfolioDataItem = row;
      this.isNewPortfolio = true;
    },

    //关闭数据源
    closePortfolioData() {
      // 执行关闭逻辑，例如隐藏对话框等
      this.isNewPortfolio = false;
      //this.getPortfolioDataList();
    },

    surePortfolioData() {
      // 执行关闭逻辑，例如隐藏对话框等
      this.isNewPortfolio = false;
      this.getPortfolioDataList();
    },

    handleEnter() {
      this.getPortfolioDataList();
    },

    getPortfolioDataList() {
      //const loading = this.loadingScreen();
      this.loading = true;
      getPortfolioDataListAPI(this.queryParams)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              this.portfolioDataList = [];

              this.queryParams.total = response.data.total;
              this.queryParams.page = response.data.page;
              this.queryParams.pageSize = response.data.pageSize;
              this.portfolioDataList = response.data.list;
              /*for (let i = 0; i < response.data.list.length; i++) {
              this.portfolioDataList.push(response.data.list[i]);
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

    offlineCandidates(row) {
      //const loading = this.loadingScreen();
      offlineCandidatesAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "下线成功",
              type: "success",
              duration: this.$messageDuration,
            });
            this.getPortfolioDataList();
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

    onlineCandidates(row) {
      //const loading = this.loadingScreen();
      onlineCandidatesAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "下线成功",
              type: "success",
              duration: this.$messageDuration,
            });
            this.getPortfolioDataList();
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
    deletePortfolioData(row) {
      this.$confirm("确定要删除 " + row.groupName + " ?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          //const loading = this.loadingScreen();
          deletePortfolioDataAPI(row.id)
            .then((response) => {
              if (response.code == 200) {
                this.$message({
                  message: "删除成功",
                  type: "success",
                  duration: this.$messageDuration,
                });
                this.getPortfolioDataList();
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