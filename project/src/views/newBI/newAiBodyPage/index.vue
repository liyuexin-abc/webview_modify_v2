<template>
  <div style="width: 100%" class="my-custom-style">
    <div style="width: 100%">
      <el-tabs stretch v-model="activeName">
        <el-tab-pane label="数据表" name="first">
          <div style="display: flex; justify-content: space-between">
            <div style="width: 50%">
              <div style="display: flex">
                <div class="two-front-bgdiv">
                  智能体名称<span style="color: red">*</span>
                </div>
                <div class="two-back-bgdiv">描述</div>
              </div>

              <div style="display: flex">
                <div class="two-front-bgdiv">
                  <el-input
                    v-model="agentDetail.name"
                    placeholder=""
                  ></el-input>
                </div>
                <div class="two-back-bgdiv">
                  <el-input
                    v-model="agentDetail.description"
                    placeholder=""
                  ></el-input>
                </div>
              </div>

              <div>
                <div class="one-bgdiv">数据源</div>
              </div>

              <div style="width: 100%; display: flex">
                <div class="two-front-bgdiv">
                  <el-select
                    placeholder="选择数据源"
                    v-model="queryParams.sourceId"
                    @change="getAiBodyCandidateTables"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="item in dataSourceList"
                      :key="item.id"
                      :label="`${item.name}(${item.dbType})`"
                      :value="item.id"
                    >
                    </el-option
                  ></el-select>
                </div>
                <div class="two-back-bgdiv">
                  <el-input
                    v-model="queryParams.keyword"
                    placeholder="搜索表名..."
                    @keyup.enter.native="getAiBodyCandidateTables"
                  ></el-input>
                </div>
              </div>

              <div
                style="
                  width: 100%;
                  max-height: 40vh;
                  overflow-y: auto;
                  overflow-x: hidden;
                "
                class="no-scrollbar"
              >
                <div class="one-bgdiv">
    
                    <div class="drag-table">
                    <el-table
                      ref="multipleTable"
                      :data="candidateTables"
                      style="width: 100%"
                      border
                      @selection-change="handleSelectionChange"
                      stripe
                    >
                      <el-table-column label="序号" type="selection" width="55">
                      </el-table-column>

                      <el-table-column
                        label="表名"
                        prop="tableName"
                        width="auto"
                        min-width="13%"
                        resizable
                        sortable
                        show-overflow-tooltip
                        :render-header="renderHeader"
                      />

                      <el-table-column
                        label="注释"
                        prop="tableComment"
                        width="auto"
                        min-width="13%"
                        resizable
                        sortable
                        show-overflow-tooltip
                        :render-header="renderHeader"
                      />
                    </el-table>
                    </div>
           
                </div>
              </div>
            </div>

            <div
              style="
                width: 50%;
                max-height: 55vh;
                overflow-y: auto;
                overflow-x: hidden;
              "
              class="no-scrollbar"
            >
              <div class="one-bgdiv">

                  <div class="drag-table">
                  <el-table
                    :data="tableRelations"
                    style="width: 100%"
                    border
                    stripe
                    class="expand-table"
                  >
                    <el-table-column type="expand" width="20px">
                      <template slot-scope="props">
                        <el-table
                          :data="props.row.relations"
                          style="width: 100%"
                          :row-style="{ backgroundColor: '#F5F7FA' }"
                          border
                        >
                          <el-table-column
                            label="表名"
                            prop="tableName"
                            width="auto"
                            min-width="40%"
                            resizable
                            sortable
                            show-overflow-tooltip
                            :render-header="renderHeader"
                          />

                          <el-table-column
                            label="注释"
                            prop="tableComment"
                            width="auto"
                            min-width="40%"
                            resizable
                            sortable
                            show-overflow-tooltip
                            :render-header="renderHeader"
                          />
                          <el-table-column
                            label="操作"
                            align="center"
                            width="auto"
                            min-width="20%"
                          >
                            <template slot-scope="scope">
                              <el-button
                                type="text"
                                style="color: red"
                                @click="deleteMetric(scope.row)"
                                >删除</el-button
                              >
                            </template>
                          </el-table-column>
                        </el-table>
                      </template>
                    </el-table-column>

                    <el-table-column
                      label="表名"
                      prop="name"
                      width="auto"
                      min-width="40%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    />

                    <el-table-column
                      label="数量"
                      prop=""
                      width="auto"
                      min-width="30%"
                      resizable
                      show-overflow-tooltip
                      sortable
                      :sort-method="
                        (a, b) => a.relations.length - b.relations.length
                      "
                      :render-header="renderHeader"
                    >
                      <template slot-scope="scope">
                        {{ scope.row.relations.length }}
                      </template>
                    </el-table-column>
                  </el-table>
                  </div>
              
              </div>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="行业知识" name="second">
          <div style="padding: 0 20px 0 20px; height: 100%">
            <div style="overflow-y: auto; height: 38vh" class="no-scrollbar">
              <div
                style="display: flex"
                v-for="(knowledge, index) in agentDetail.knowledgeList"
                :key="index"
              >
                <div
                  class="one-bgdiv"
                  style="
                    display: flex;
                    align-items: center;
                    padding: 0px 0px 10px 0px;
                  "
                >
                  <div
                    style="
                      width: 5%;
                      text-align: center;
                      padding: 0px 0px 10px 0px;
                    "
                  >
                    <div
                      style="
                        width: 20px;
                        height: 20px;
                        border-radius: 50%;
                        background: rgb(59, 130, 246);
                        color: rgb(255, 255, 255);
                        font-size: 12px;
                        font-weight: 500;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        flex-shrink: 0;
                      "
                    >
                      {{ index + 1 }}
                    </div>
                  </div>

                  <div
                    style="
                      width: 85%;
                      text-align: left;
                      padding: 0px 0px 10px 0px;
                    "
                  >
                    <el-input
                      v-model="knowledge.knowledgeElement"
                      placeholder="知识内容(标准术语)"
                    ></el-input>
                  </div>

                  <div
                    style="
                      width: 10%;
                      text-align: left;
                      padding: 0px 20px 10px 20px;
                    "
                  >
                    <el-button
                      type="text"
                      style="color: red"
                      @click="deleteKnowledge(index)"
                      >删除</el-button
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <div class="horizontal-line"></div>

    <div style="display: flex; justify-content: space-between;padding-bottom:5px;">
      <div class="one-bgdiv" v-show="activeName == 'second'">
        <el-button @click="newKnowledge()">
          <i class="el-icon-plus"></i>&nbsp;添加</el-button
        >
      </div>
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
        <el-button @click="close()"> 取消 </el-button>

        <el-button type="primary" @click="newAIBody()"> 确定 </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getAiBodyDetailAPI,
  getAiBodyCandidateTablesAPI,
  saveAiBodyAPI,
} from "@/api/smartQuery/smartQueryAPI";
import { getDataSourcesListAPI } from "@/api/fieldMappingManager/fieldMappingAPI.js";

export default {
  name: "newAiBodyPage",
  props: ["agentItem"],
  components: {},
  data() {
    return {
      activeName: "first",
      dataSourceList: [],
      candidateTables: [],

      queryParams: {
        sourceId: "",
        keyword: "",
      },

      agentDetail: {
        name: "",
        description: "",
        knowledgeList: [],
        tableRelations: [],
      },

      tableRelations: [],
    };
  },

  async mounted() {
    await this.getDataSourceList();
    this.getAiBodyDetail();

    this.newKnowledge();
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

    handleSelectionChange(row) {
      let index = this.tableRelations.findIndex(
        (item) => item.sourceId == this.queryParams.sourceId
      );

      if (index > -1) {
        this.tableRelations[index].relations = row;
      } else {
        let index = this.dataSourceList.findIndex(
          (item) => item.id == this.queryParams.sourceId
        );

        let tables = {
          sourceId: this.queryParams.sourceId,
          name: this.dataSourceList[index].name,
          relations: row,
        };
        this.tableRelations.push(tables);
      }

      for (let i = 0; i < this.tableRelations.length; i++) {
        if (this.tableRelations[i].relations.length == 0) {
          this.tableRelations.splice(i, 1);
          i--;
        }
      }

      /*for (let i = 0; i < this.agentDetail.tableRelations.length; i++) {
        let index = this.candidateTables.findIndex(
          (item) =>
            item.relationId == this.agentDetail.tableRelations[i].relationId
        );
        if (index > -1) {
          this.agentDetail.tableRelations.splice(i, 1);
          i--;
        }
      }

      for (let i = 0; i < row.length; i++) {
        this.agentDetail.tableRelations.push(row[i]);
      }*/
    },

    newKnowledge() {
      if (!this.agentDetail.hasOwnProperty("knowledgeList")) {
        this.$set(this.agentDetail, "knowledgeList", []);
      }

      for (let i = 0; i < this.agentDetail.knowledgeList.length; i++) {
        if (this.agentDetail.knowledgeList[i].knowledgeElement == "") {
          return;
        }
      }

      this.agentDetail.knowledgeList.push({
        knowledgeElement: "",
        //knowledgeAlias: "",
      });
    },

    deleteKnowledge(index) {
      this.agentDetail.knowledgeList.splice(index, 1);
    },

    async getDataSourceList() {
      //查询数据源的参数
      //const loading = this.loadingScreen();
      return getDataSourcesListAPI()
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              this.dataSourceList = [];

              this.dataSourceList = response.data;
              //for (let i = 0; i < response.data.length; i++) {
              //this.dataSourceList.push(response.data[i]);
              //}
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
        });

        
    },

    getAiBodyDetail() {
      //获取详情，把表格按sourceID进行归组
      if (this.agentItem != null) {
        //const loading = this.loadingScreen();
        getAiBodyDetailAPI(this.agentItem.code)
          .then((response) => {
            if (response.code == 200) {
              this.agentDetail = response.data;
              for (let i = 0; i < this.agentDetail.tableRelations.length; i++) {
                let index = this.tableRelations.findIndex(
                  (item) =>
                    item.sourceId == this.agentDetail.tableRelations[i].sourceId
                );

                if (index > -1) {
                  this.tableRelations[index].relations.push(
                    this.agentDetail.tableRelations[i]
                  );
                } else {
                  
                  let index1 = this.dataSourceList.findIndex(
                    (item) =>
                      item.id == this.agentDetail.tableRelations[i].sourceId
                  );
                  let tables = {
                    sourceId: this.agentDetail.tableRelations[i].sourceId,
                    name: this.dataSourceList[index1].name,
                    relations: [this.agentDetail.tableRelations[i]],
                  };

                  this.tableRelations.push(tables);
                }
              }

              //添加一行
              if (!(this.agentDetail.knowledgeList?.length > 0)) this.newKnowledge();
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

    getAiBodyCandidateTables() {
      //将已选得数据选择上
      if (this.queryParams.sourceId == "") {
        this.$message({
          message: "请选择数据源",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      //const loading = this.loadingScreen();
      getAiBodyCandidateTablesAPI(this.queryParams)
        .then((response) => {
          if (response.code == 200) {
            /*for (let i = 0; i < response.data.length; i++) {
            let table = {};
            table.relationId = response.data[i].relationId;
            table.relationName = response.data[i].relationName;
            table.type = response.data[i].type;
            table.sourceId = this.queryParams.sourceId;
            this.candidateTables.push(table);
          }*/
            this.candidateTables = response.data;

            for (let i = 0; i < this.tableRelations.length; i++) {
              for (
                let j = 0;
                j < this.tableRelations[i].relations.length;
                j++
              ) {
                let index = this.candidateTables.findIndex(
                  (item) =>
                    item.relationId ==
                      this.tableRelations[i].relations[j].relationId &&
                    item.sourceId ==
                      this.tableRelations[i].relations[j].sourceId
                );
                if (index > -1) {
                  this.$nextTick(() => {
                    this.$refs.multipleTable.toggleRowSelection(
                      this.candidateTables[index],
                      true
                    );
                  });
                }
              }
            }

            /*for (let i = 0; i < this.agentDetail.tableRelations.length; i++) {
            let index = this.candidateTables.findIndex(
              (item) =>
                item.relationId == this.agentDetail.tableRelations[i].relationId
            );
            if (index > -1) {
              this.$nextTick(() => {
                this.$refs.multipleTable.toggleRowSelection(
                  this.candidateTables[index],
                  true
                );
              });
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

    newAIBody() {
      /*let tablelist = [];
      for (let i = 0; i < this.agentDetail.candidateTables.length; i++) {
        let table = {};
        table.relationId = this.agentDetail.candidateTables[i].relationId;
        table.tableName = this.agentDetail.candidateTables[i].relationName;
        table.tableComment =
          this.agentDetail.candidateTables[i].relationComment;
        table.type = this.agentDetail.candidateTables[i].type;
        table.sourceId = this.agentDetail.candidateTables[i].sourceId;
        tablelist.push(table);
      }

      this.agentDetail.candidateTables = table;*/
      if (this.agentDetail.name == null || this.agentDetail.name == "") {
        this.$message({
          message: "智能体名称不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      this.agentDetail.tableRelations = [];
      for (let i = 0; i < this.tableRelations.length; i++) {
        for (let j = 0; j < this.tableRelations[i].relations.length; j++) {
          this.agentDetail.tableRelations.push(
            this.tableRelations[i].relations[j]
          );
        }
      }

      this.agentDetail.knowledgeList = this.agentDetail.knowledgeList.filter(
        (item) => item.knowledgeElement != ""
      );

      //const loading = this.loadingScreen();
      saveAiBodyAPI(this.agentDetail)
        .then((response) => {
          if (response.code == 200) {
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

    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped lang="scss">
/*.two-front-bgdiv {
  width: 50%;
  text-align: left;
  padding: 0px 10px 10px 30px;
}

.two-back-bgdiv {
  width: 50%;
  text-align: left;
  padding: 0px 30px 10px 10px;
}

.expand-table ::v-deep .el-table__expanded-cell {
  padding: 0px;
}

.one-bgdiv {
  width: 100%;
  text-align: left;
  padding: 0px 30px 10px 30px;
}

.horizontal-line {
  border-top: 1px solid #ccc; 
  margin: 10px 0; 
}


.tableBoxDiv ::v-deep .el-table td {
  padding: 0 0;
}
.tableBoxDiv ::v-deep .el-table .cell {
  line-height: 36px;
  padding: 0 10px;
}

.tableBoxDiv ::v-deep .el-table__fixed td {
  padding: 0 0;
}
.tableBoxDiv ::v-deep .el-table__fixed .cell {
  line-height: 36px;
}

.tableBoxDiv ::v-deep .el-table td.el-table__cell div {
  align-content: center;
}

.tableBoxDiv ::v-deep .el-table thead th {
  padding: 0 0;
  height: 36px;
}

.tableBoxDiv ::v-deep .el-table thead .cell {
  line-height: 36px;
  padding: 0 10px;

  align-content: center;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.tableBoxDiv ::v-deep .el-table td.el-table__cell div {
  align-content: center;
}

.tableBoxDiv ::v-deep .el-table--border,
.el-table--group {
  border: none;
}

.tableBoxDiv ::v-deep .el-table--border::after,
.el-table--group::after,
.el-table::before {
  background-color: #ffffff;
}

.tableBoxDiv ::v-deep .el-table__header {
  border-left: 1px solid #ebeef5;
}

.tableBoxDiv ::v-deep .el-table__body {
  border-left: 1px solid #ebeef5;
}

.tableBoxDiv ::v-deep .el-table__body,
.el-table__footer {
  border-bottom: 1px solid #ebeef5;
}

.tableBoxDiv ::v-deep .el-table--border::after,
.el-table--group::after {
  width: 0px;
}*/
</style>
