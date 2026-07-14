
<template>
  <div style="display: flex; width: 100%; height: 100%" class="my-custom-style">
    <div class="allbg">
      <div class="tablebg">
        <div class="searchBox">
          <div style="display: flex">
            <div style="width: 240px">
              <el-input
                placeholder="搜索维度..."
                suffix-icon="el-icon-search"
                v-model="queryParams.keyword"
                @keyup.enter.native="handleEnter"
              >
              </el-input>
            </div>

            <div style="margin-left: 10px; width: 120px">
              <el-select
                placeholder="请选择类型"
                @change="handleEnter"
                v-model="queryParams.dimensionType"
              >
                <el-option label="全部类型" value=""></el-option>

                <el-option
                  v-for="item in dimensionTypeEnum"
                  :key="item.value"
                  :label="item.name"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </div>

            <div style="margin-left: 10px">
              <el-button
                @click="getDimensionList"
              ><base-icon name="refresh" :size="14" /></el-button>
            </div>
          </div>

          <div style="width: 100%"></div>

          <div style="text-align: right">
            <el-button type="primary" @click="newDimensionClick"
              ><base-icon name="plus" :size="14" />&nbsp;新建维度</el-button
            >
          </div>
        </div>

        <div style="padding: 10px 20px 10px 20px">
          <div class="table-container">
            <div class="normal-table">
              <el-table
                :data="dimensionList"
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
                  label="维度英文名"
                  prop="englishName"
                  width="auto"
                  min-width="150%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="维度中文名"
                  prop="chineseName"
                  width="auto"
                  min-width="150%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="维度类型"
                  width="auto"
                  min-width="50%"
                  resizable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    {{ dimensionTypeEnum[scope.row.dimensionType].name }}
                  </template>
                </el-table-column>

                <el-table-column
                  label="维值采集状态"
                  width="auto"
                  min-width="100%"
                  resizable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <!-- <div :style="{ borderStyle:'solid', borderWidth: '1px',  borderColor: collectStatusEnum[scope.row.collectStatus].color, backgroundColor: collectStatusEnum[scope.row.collectStatus].bgColor, color: collectStatusEnum[scope.row.collectStatus].color }"> 
        -->
                    {{ collectStatusEnum[scope.row.collectStatus].name }}

                    <!-- </div>-->
                  </template>
                </el-table-column>

                <el-table-column
                  label="更新时间"
                  prop="updatedAt"
                  width="auto"
                  min-width="135%"
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
                      <el-button type="text" class="op-icon-btn" @click="editDimensionClick(scope.row)"><base-icon name="edit" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="下线" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="offlineDimensionData(scope.row)" v-if="scope.row.status == 2"><base-icon name="sort-desc" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="上线" placement="top">
                      <el-button type="text" class="op-icon-btn" @click="onlineDimensionData(scope.row)" v-if="scope.row.status == 3"><base-icon name="sort-asc" :size="15" /></el-button>
                    </el-tooltip>

                    <el-tooltip content="删除" placement="top">
                      <el-button type="text" class="op-icon-btn is-danger" @click="deleteDimensionData(scope.row)"><base-icon name="trash" :size="15" /></el-button>
                    </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>

              <pagination
                v-show="queryParams.total > 0"
                :total="queryParams.total"
                :page.sync="queryParams.page"
                :limit.sync="queryParams.pageSize"
                @pagination="getDimensionList"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-drawer
      title="维度"
      :visible.sync="isNewDimension"
      direction="rtl"
      size="50%"
      :wrapperClosable="false"
      :show-close="false"
      append-to-body
      class="my-custom-style"
    >
      <span>
        <newDimension-Page
          v-if="isNewDimension"
          :dimensionItem="dimensionItem"
          @close="closeDimension"
          @sure="sureDimension"
        />
      </span>
    </el-drawer>
  </div>
</template>


<script>
import {
  getDimensionListAPI,
  deleteDimensionDataAPI,
  offlineDimensionDataAPI,
  onlineDimensionDataAPI,
  dimensionTypeEnum,
  collectStatusEnum,
} from "@/api/dimensionManager/dimensionAPI.js";
import newDimensionPage from "@/views/dimensionManager/newDimensionPage";

export default {
  name: "dimensionManager",
  components: {
    newDimensionPage,
  },
  data() {
    return {
      dimensionTypeEnum,
      collectStatusEnum,

      loading: false,

      isNewDimension: false,

      dimensionItem: null,
      //维度列表
      dimensionList: [],

      queryParams: {
        keyword: "",
        dimensionType: "",
        page: 1,
        pageSize: 10,
        total: 0,
      },
    };
  },

  mounted() {
    this.getDimensionList();
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

    //新建维度
    newDimensionClick() {
      this.dimensionItem = null;
      this.isNewDimension = true;
    },

    //编辑维度
    editDimensionClick(row) {
      this.dimensionItem = row;
      this.isNewDimension = true;
    },
    //关闭维度
    closeDimension() {
      this.isNewDimension = false;
      //this.getDimensionList();
    },
    //确认维度
    sureDimension() {
      this.isNewDimension = false;
      this.getDimensionList();
    },

    handleEnter() {
      this.getDimensionList();
    },

    getDimensionList() {
      //const loading = this.loadingScreen();
      this.loading = true;
      getDimensionListAPI(this.queryParams)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              this.dimensionList = [];

              this.queryParams.total = response.data.total;
              this.queryParams.page = response.data.page;
              this.queryParams.pageSize = response.data.pageSize;
              this.dimensionList = response.data.records;
              /*for (let i = 0; i < response.data.records.length; i++) {
              this.dimensionList.push(response.data.records[i]);
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

    offlineDimensionData(row) {
      //const loading = this.loadingScreen();
      offlineDimensionDataAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "下线成功",
              type: "success",
              duration: this.$messageDuration,
            });
            this.getDimensionList();
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

    onlineDimensionData(row) {
      //const loading = this.loadingScreen();
      onlineDimensionDataAPI(row.id)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "上线成功",
              type: "success",
              duration: this.$messageDuration,
            });
            this.getDimensionList();
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
    deleteDimensionData(row) {
      this.$confirm("确定要删除 " + row.englishName + " ?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          //const loading = this.loadingScreen();
          deleteDimensionDataAPI(row.id)
            .then((response) => {
              if (response.code == 200) {
                this.$message({
                  message: "删除成功",
                  type: "success",
                  duration: this.$messageDuration,
                });
                this.getDimensionList();
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