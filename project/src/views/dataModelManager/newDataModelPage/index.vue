<template>
  <div>
    <div style="display: flex; flex-direction: column">
      <div class="horizontal-line"></div>

      <div
        style="max-height: 60vh; overflow-y: auto; overflow-x: hidden"
        class="no-scrollbar"
      >
        <div style="display: flex">
          <div class="title16-one-padding-bgdiv">
            基本配置

            <div class="horizontal-line"></div>
          </div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            模型名称<span style="color: red">*</span>
          </div>

          <div class="two-back-bgdiv">
            数据源<span style="color: red">*</span>
          </div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            <el-input
              v-model="dataModel.name"
              placeholder="如:门诊运营模型"
            ></el-input>
          </div>

          <div class="two-back-bgdiv">
            <el-select
              v-model="dataModel.sourceId"
              placeholder="请选择数据源"
              @change="getDataModelCandidateFactTable()"
              style="width: 100%"
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
          <div class="title16-one-padding-bgdiv">
            主表与关联表
            <div class="horizontal-line"></div>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">主表<span style="color: red">*</span></div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv" style="width: 50%">
            <el-select
              v-model="dataModel.factTableId"
              placeholder="请选择主表"
              @change="getDataModelCandidateDimTable"
            >
              <el-option
                v-for="item in candidateFactTableList"
                :key="item.tableId"
                :label="item.tableName"
                :value="item.tableId"
              >
              </el-option>
            </el-select>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">关联表(join到主表)</div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <div class="drag-table">
              <el-table
                :data="dataModel.joins"
                ref="tableRef"
                border
                @header-dragend="onDragEnd"
              >
                <el-table-column
                  prop="dimTables"
                  label="关联表"
                  width="auto"
                  min-width="30%"
                  resizable
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <el-select
                      v-model="scope.row.dimTableId"
                      placeholder="请选择关联表"
                    >
                      <el-option
                        v-for="item in candidateDimTableList.dimTables"
                        :key="item.tableId"
                        :label="item.tableName"
                        :value="item.tableId"
                      >
                      </el-option>
                    </el-select>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="joinType"
                  label="关联关系"
                  width="auto"
                  min-width="20%"
                  resizable
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <el-select
                      v-model="scope.row.joinType"
                      placeholder="请选择关联关系"
                    >
                      <!--<el-option label="LEFT JOIN" value="LEFT JOIN"></el-option>
                <el-option label="INNER JOIN" value="INNER JOIN"></el-option>
                <el-option label="RIGHT JOIN" value="RIGHT JOIN"></el-option>-->

                      <el-option
                        v-for="item in joinTypeEnum"
                        :key="item.value"
                        :label="item.value"
                        :value="item.value"
                      ></el-option>
                    </el-select>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="factColumns"
                  label="主表字段"
                  width="auto"
                  min-width="20%"
                  resizable
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <el-select
                      v-model="scope.row.factFkColumn"
                      placeholder="请选择主表字段"
                    >
                      <el-option
                        v-for="item in candidateDimTableList.factColumns"
                        :key="item.columnName"
                        :label="item.columnName"
                        :value="item.columnName"
                      >
                      </el-option>
                    </el-select>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="dimColumns"
                  label="关联表字段"
                  width="auto"
                  min-width="20%"
                  resizable
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <el-select
                      v-model="scope.row.dimPkColumn"
                      placeholder="请选择关联表字段"
                      class="my-select"
                    >
                      <el-option
                        v-for="item in candidateDimTableList.dimColumns[
                          scope.row.dimTableId
                        ]"
                        :key="item.columnName"
                        :label="item.columnName"
                        :value="item.columnName"
                      >
                      </el-option>
                    </el-select>
                  </template>
                </el-table-column>

                <el-table-column
                  label="操作"
                  align="center"
                  width="auto"
                  min-width="10%"
                  resizable
                >
                  <template slot-scope="scope">
                    <el-button
                      type="text"
                      style="color: red"
                      @click="delCandidateTable(scope.$index)"
                      >删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <el-button @click="addCandidateTable"
              ><i class="el-icon-plus"></i>添加关联表</el-button
            >
          </div>
        </div>
      </div>

      <div class="horizontal-line"></div>

      <div style="display: flex; padding-bottom: 5px">
        <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
          <el-button @click="close()">取消</el-button>
          <el-button type="primary" @click="newDataModel()">
            <div v-if="dataModelItem == null">创建</div>
            <div v-else>更新</div>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {
  getDataModelCandidateFactTableAPI,
  getDataModelCandidateDimTableAPI,
  getDataModelDetailAPI,
  newDataModelAPI,
  editDataModelAPI,
  joinTypeEnum,
} from "@/api/dataModelManager/dataModelAPI.js";

import { getDataSourcesListAPI } from "@/api/fieldMappingManager/fieldMappingAPI.js";

export default {
  name: "newDataModelPage",
  props: ["dataModelItem"],
  components: {},
  data() {
    return {
      joinTypeEnum,

      //数据源
      dataSourceList: [],

      dataModel: {
        name: "",
        sourceId: "",
        joins: [],
        factTableId: "",
      },

      //可选主表列表
      candidateFactTableList: [],
      //可选关联表及字段
      candidateDimTableList: {
        dimTables: [],
        factColumns: [],
        dimColumns: {},
      },
    };
  },
  mounted() {
    //获取数据源
    this.getDataSourceList();

    //获取数据模型
    this.getDataModelDetail();
    //this.getDataModelCandidateFactTable();
  },
  methods: {
    onDragEnd(newWidth, oldWidth, column) {
      if (column.property) {
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

    //获取数据模型详情
    getDataModelDetail() {
      if (this.dataModelItem != null) {
        //const loading = this.loadingScreen();
        getDataModelDetailAPI(this.dataModelItem.id)
          .then((response) => {
            if (response.code == 200) {
              this.dataModel = response.data;
              this.getDataModelCandidateFactTable();
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

    //可选主表列表
    getDataModelCandidateFactTable() {
      this.dataModel.factTableId = "";

      let data = { sourceId: this.dataModel.sourceId };
      //const loading = this.loadingScreen();
      getDataModelCandidateFactTableAPI(data)
        .then((response) => {
          if (response.code == 200) {
            this.dataModel.joins = [];
            this.candidateFactTableList = [];

            this.candidateFactTableList = response.data;
            /*if (response.data != null) {
              for (let i = 0; i < response.data.length; i++) {
                this.candidateFactTableList.push(response.data[i]);
              }
            }*/
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

    //可选关联表及字段
    getDataModelCandidateDimTable() {
      let data = {
        sourceId: this.dataModel.sourceId,
        factTableId: this.dataModel.factTableId,
      };
      //const loading = this.loadingScreen();
      getDataModelCandidateDimTableAPI(data)
        .then((response) => {
          if (response.code == 200) {
            this.dataModel.joins = [];
            //if (response.data != null) {
            this.candidateDimTableList = response.data;

            //去除，并添加一条
            if (!(this.dataModel.joins?.length > 0)) this.addCandidateTable();
            //}
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

    close() {
      this.$emit("close");
    },

    addCandidateTable() {
      if (!this.dataModel.hasOwnProperty("joins")) {
        this.$set(this.dataModel, "joins", []);
      }

      for (let i = 0; i < this.dataModel.joins.length; i++) {
        if (
          this.dataModel.joins[i].dimTableId == null ||
          this.dataModel.joins[i].factFkColumn == null ||
          this.dataModel.joins[i].dimPkColumn == null
        ) {
          return;
        }
      }

      this.dataModel.joins.push({
        dimTableId: null,
        joinType: "LEFT JOIN",
        factFkColumn: null,
        dimPkColumn: null,
      });
    },

    delCandidateTable(index) {
      this.dataModel.joins.splice(index, 1);
    },

    newDataModel() {
      let isHaveEmpty = false;
      for (let i = 0; i < this.dataModel.joins.length; i++) {
        if (
          this.dataModel.joins[i].dimTableId == null ||
          this.dataModel.joins[i].factFkColumn == null ||
          this.dataModel.joins[i].dimPkColumn == null
        ) {
          isHaveEmpty = true;
        }
      }
      if (isHaveEmpty) {
        this.$message({
          message: "值不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (this.dataModel.name == null || this.dataModel.name == "") {
        this.$message({
          message: "模型名称不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      if (this.dataModel.sourceId == null || this.dataModel.sourceId == "") {
        this.$message({
          message: "数据源不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      if (
        this.dataModel.factTableId == null ||
        this.dataModel.factTableId == ""
      ) {
        this.$message({
          message: "主表不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      if (this.dataModel.joins == null || this.dataModel.joins.length == 0) {
        this.$message({
          message: "值不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (this.dataModelItem == null) {
        //const loading = this.loadingScreen();
        newDataModelAPI(this.dataModel)
          .then((response) => {
            if (response.code == 200) {
              //成功
              this.$message({
                message: "添加成功",
                type: "success",
                duration: this.$messageDuration,
              });
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
      } else {
        //const loading = this.loadingScreen();
        editDataModelAPI(this.dataModelItem.id, this.dataModel)
          .then((response) => {
            if (response.code == 200) {
              this.$message({
                message: "修改成功",
                type: "success",
                duration: this.$messageDuration,
              });
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
      }
    },

    //获取数据源列表
    getDataSourceList() {
      //查询数据源的参数

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
  },
};
</script>


<style scoped lang="scss">

</style>