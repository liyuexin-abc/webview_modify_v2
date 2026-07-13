<template>
  <div>
    <div class="horizontal-line"></div>

    <div
      style="max-height: 70vh; overflow-y: auto; overflow-x: hidden"
      class="no-scrollbar"
    >
      <div style="display: flex">
        <div class="one-bgdiv">数据源<span style="color: red">*</span></div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          <el-select
            placeholder="请选择数据源"
            v-model="viewData.sourceId"
            style="width: 70%"
          >
            <el-option
              v-for="item in dataSourceList"
              :key="item.id"
              :label="`${item.name}(${item.dbType})`"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </div>
      </div>

      <div style="display: flex">
        <div class="two-front-bgdiv" style="display: flex">
          <div>视图英文名<span style="color: red">*</span></div>
          <div style="color:silver;">（固定 view_ 前缀）</div>
        </div>

        <div class="two-back-bgdiv">
          视图中文名<span style="color: red">*</span>
        </div>
      </div>

      <div style="display: flex">
        <div class="two-front-bgdiv">
          <el-input
            v-model="viewData.viewEnName"
            placeholder="view_"
          ></el-input>
        </div>

        <div class="two-back-bgdiv">
          <el-input
            v-model="viewData.viewCnName"
            placeholder="如:患者汇总视图"
          ></el-input>
        </div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">视图SQL<span style="color: red">*</span></div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          <el-input
            v-model="viewData.sql"
            :autosize="{ minRows: 3, maxRows: 20 }"
            type="textarea"
            resize="none"
            placeholder="SELECT ... FROM ... JOIN ... WHERE ..."
          ></el-input>
        </div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          <div style="display: flex; align-items: center">
            <el-button type="primary" @click="sureParseTableSql"
              >执行并解析</el-button
            >

            <div style="margin-left: 20px; color: green">{{ parseText }}</div>
          </div>
        </div>
      </div>

      <div style="display: flex" v-if="parseData.length > 0">
        <div class="title16-one-padding-bgdiv">
          解析字段列表

          <div class="horizontal-line"></div>
        </div>
      </div>

      <div style="display: flex" v-if="parseData.length > 0">
        <div class="one-bgdiv">
          <div class="drag-table">
            <el-table
              empty-text='请先编写SQL并点击"执行并解析"'
              :data="parseData"
              border
              v-loading="loading"
              element-loading-text="加载中..."
              element-loading-background="rgb(248 248 248 / 50%)"
              @header-dragend="onDragEnd"
              ref="tableRef"
            >
              <el-table-column
                label="字段名"
                prop="fieldKey"
                width="auto"
                min-width="40%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              >
                <template slot-scope="scope">
                  <div style="display: flex; gap: 5px">
                    <div
                      v-if="
                        scope.row.compareStatus == compareStatusEnum['0'].value
                      "
                      style="
                        text-align: center;
                        background-color: #c8eac8;
                        width: 35px;
                        padding: 0 2px 0 2px;
                        color: rgb(0 124 0);
                      "
                    >
                      {{ compareStatusEnum["0"].name }}
                    </div>

                    <div
                      v-if="
                        scope.row.compareStatus == compareStatusEnum['1'].value
                      "
                      style="
                        text-align: center;
                        background-color: rgb(190 203 240);
                        width: 35px;
                        padding: 0 2px 0 2px;
                        color: rgb(52 98 228);
                      "
                    >
                      {{ compareStatusEnum["1"].name }}
                    </div>

                    <div
                      v-if="
                        scope.row.compareStatus == compareStatusEnum['2'].value
                      "
                      style="
                        text-align: center;
                        background-color: rgb(254 178 178);
                        width: 35px;
                        padding: 0 2px 0 2px;
                        color: rgb(255 8 8);
                      "
                    >
                      {{ compareStatusEnum["2"].name }}
                    </div>

                    <div>{{ scope.row.fieldKey }}</div>
                  </div>
                </template>
              </el-table-column>

              <el-table-column
                label="字段类型"
                prop="fieldType"
                width="auto"
                min-width="20%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />
              <el-table-column
                label="字段中文名"
                prop="fieldName"
                width="auto"
                min-width="40%"
                sortable
                resizable
          
                :render-header="renderHeader"
              >
                <template slot-scope="scope">
                  <el-input
                    v-model="scope.row.fieldName"
                    :disabled="
                      scope.row.compareStatus == compareStatusEnum['2'].value
                    "
                  />
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </div>
    <div class="horizontal-line"></div>

    <div style="display: flex; padding-bottom: 5px">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
        <el-button @click="close">取消</el-button>
        <el-button type="primary" @click="sureView">保存并注册</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import {
  newRegisterViewAPI,
  parseTableSqlAPI,
  getDataSourcesListAPI,
  getViewDetalAPI,
  compareStatusEnum,
} from "@/api/fieldMappingManager/fieldMappingAPI.js";

export default {
  name: "viewRegisteredPage",
  //props: ["viewRegisteredItem"],
  props: ["viewID"],
  components: {},
  data() {
    return {
      compareStatusEnum,

      loading: false,

      parseText: "",
      viewData: {
        id: null,
        sourceId: "",
        viewEnName: "",
        viewCnName: "",
        sql: "",
      },
      parseData: {},
      dataSourceList: [],
    };
  },

  mounted() {
    this.getDataSourceList();
    this.getViewDetal();
  },

  methods: {
    onDragEnd(newWidth, oldWidth, column) {
      if (column.property == 'fieldName') {
        const minWidth = 120;
        if (newWidth < minWidth) {
          // 修正列宽
          column.width = minWidth;
          this.$nextTick(() => {
            this.$refs.tableRef.doLayout();
          });
        }
      }
    },

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

    //添加
    sureView() {
      this.viewData.columns = [];
      for (let i = 0; i < this.parseData.length; i++) {
        let data = {
          fieldKey: this.parseData[i].fieldKey,
          fieldName: this.parseData[i].fieldName,
          fieldType: this.parseData[i].fieldType,
        };
        if (this.parseData[i].hasOwnProperty("compareStatus")) {
          data.compareStatus = this.parseData[i].compareStatus;
        }

        this.viewData.columns.push(data);
      }

      if (this.viewData.sourceId == null || this.viewData.sourceId == "") {
        this.$message({
          message: "数据源不能为空",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }
      if (this.viewData.viewEnName == null || this.viewData.viewEnName == "") {
        this.$message({
          message: "视图英文名不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (!this.viewData.viewEnName.toLowerCase().startsWith("view_")) {
        this.$message({
          message: "视图英文名要以view_开头",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (this.viewData.viewCnName == null || this.viewData.viewCnName == "") {
        this.$message({
          message: "视图中文名不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (this.viewData.sql == null || this.viewData.sql == "") {
        this.$message({
          message: "sql语句不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      if (this.viewData.columns.length == 0) {
        this.$message({
          message: "数据表不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      //const loading = this.loadingScreen();
      newRegisterViewAPI(this.viewData)
        .then((response) => {
          if (response.code == 200) {
            this.$message({
              message: "添加成功",
              type: "success",
              duration: this.$messageDuration,
            });

            //this.$emit("sureView", null);
            this.$emit("sure");
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

    //关闭窗口
    close() {
      this.$emit("close");
    },

    sureParseTableSql() {
      if (this.viewData.id != null && this.viewData.id != "") {
        this.$confirm(
          `<div style="padding:10px;">本次重新解析会自动匹配新旧输出字段：<br/>
        · <span style="color:rgb(0 124 0);">【保留】</span>：该字段标识（fieldKey）与修改前一致，系统保留已填写的指标 / 维度映射关系；<br/>
        · <span style="color:rgb(52 98 228);">【新增】</span>：本次 SQL 解析新增输出字段，后续需要手动补充中文名和映射配置；<br/>
        · <span style="color:rgb(255 8 8);">【废弃】</span>：本次SQL 解析后已不输出的字段，页面标记为废弃，保存后该字段会从该视图移除，其指标维度映射关系也会同步移除。<br/><br/>
        确认要执行解析吗？</div>`,

          "字段结构变更确认",
          {
            customClass: "custom-confirm",
            dangerouslyUseHTMLString: true,
            confirmButtonText: "确认解析",
            cancelButtonText: "取消",
          }
        )
          .then(() => {
            this.parseTableSql();
          })
          .catch(() => {});
      } else {
        this.parseTableSql();
      }
    },

    //执行解析SQL
    parseTableSql() {
      this.parseText = "";

      let data = { sourceId: this.viewData.sourceId, sql: this.viewData.sql };
      if (this.viewData.id != null && this.viewData.id != "") {
        data.tableId = this.viewData.id;
      }

      if (data.sourceId == null || data.sourceId == "") {
        this.$message({
          message: "数据源不能为空",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }
      if (data.sql == null || data.sql == "") {
        this.$message({
          message: "sql语句不能为空",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }

      //const loading = this.loadingScreen();
      this.loading = true;
      parseTableSqlAPI(data)
        .then((response) => {
          if (response.code == 200) {
            this.parseData = response.data;
            //this.parseText = "解析成功," + this.parseData.fieldComment;
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

    //获取数据源列表
    getDataSourceList() {
      //const loading = this.loadingScreen();
      getDataSourcesListAPI()
        .then((response) => {
          if (response.code == 200) {
            this.dataSourceList = [];

            this.dataSourceList = response.data;

            /*if (response.data != null) {
            for (let i = 0; i < response.data.length; i++) {
              this.dataSourceList.push(response.data[i]);
            }
          }*/
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
        });
    },

    getViewDetal() {
      if (this.viewID != null) {
        let query = { id: this.viewID };
        //const loading = this.loadingScreen();
        getViewDetalAPI(query)
          .then((response) => {
            if (response.code == 200) {
              this.viewData = response.data;
              this.parseData = [];
              for (let i = 0; i < response.data.columns.length; i++) {
                this.parseData.push({
                  fieldKey: response.data.columns[i].fieldKey,
                  fieldName: response.data.columns[i].fieldName,
                  fieldType: response.data.columns[i].fieldType,
                });
              }
              this.viewData.id = this.viewID;
              //this.$set(this.viewData,'id',this.viewID)
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
          });
      }
    },
  },
};
</script>


 <style scoped lang="scss">

</style>
