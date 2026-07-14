<template>
  <div class="my-custom-style agent-config">
    <el-form label-position="top" size="small" class="agent-config__form">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="智能体名称" required>
            <el-input
              v-model="agentDetail.name"
              placeholder="如:销售分析智能体"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="描述">
            <el-input
              v-model="agentDetail.description"
              placeholder="简要描述该智能体的用途"
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-tabs v-model="activeName" class="agent-config__tabs">
      <el-tab-pane name="first">
        <span slot="label" class="agent-config__tab-label">
          <base-icon name="table" :size="14" /> 数据表
        </span>

        <div class="agent-config__panes">
          <!-- 左:候选表 -->
          <div class="agent-config__pane">
            <div class="agent-config__pane-title">选择数据表</div>
            <div class="agent-config__toolbar">
              <el-select
                placeholder="选择数据源"
                v-model="queryParams.sourceId"
                @change="getAiBodyCandidateTables"
                size="small"
                style="width: 46%"
              >
                <el-option
                  v-for="item in dataSourceList"
                  :key="item.id"
                  :label="`${item.name}(${item.dbType})`"
                  :value="item.id"
                >
                </el-option>
              </el-select>
              <el-input
                v-model="queryParams.keyword"
                placeholder="搜索表名..."
                size="small"
                style="flex: 1"
                @keyup.enter.native="getAiBodyCandidateTables"
              >
                <base-icon slot="suffix" name="search" :size="14" style="margin: 8px 6px 0 0; color: #94a3b8" />
              </el-input>
            </div>

            <div class="agent-config__table-wrap no-scrollbar">
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

          <!-- 右:已选关系 -->
          <div class="agent-config__pane">
            <div class="agent-config__pane-title">已选数据表(按数据源分组)</div>
            <div class="agent-config__table-wrap agent-config__table-wrap--tall no-scrollbar">
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
                              class="op-icon-btn is-danger"
                              @click="deleteMetric(scope.row)"
                              ><base-icon name="trash" :size="14"
                            /></el-button>
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

      <el-tab-pane name="second">
        <span slot="label" class="agent-config__tab-label">
          <base-icon name="book" :size="14" /> 行业知识
        </span>

        <div class="agent-config__knowledge no-scrollbar">
          <div
            class="agent-config__knowledge-row"
            v-for="(knowledge, index) in agentDetail.knowledgeList"
            :key="index"
          >
            <span class="agent-config__knowledge-no">{{ index + 1 }}</span>
            <el-input
              v-model="knowledge.knowledgeElement"
              placeholder="知识内容(标准术语)"
              size="small"
            ></el-input>
            <el-button
              type="text"
              class="op-icon-btn is-danger"
              @click="deleteKnowledge(index)"
              ><base-icon name="trash" :size="14"
            /></el-button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <div class="horizontal-line"></div>

    <div class="agent-config__footer">
      <div v-show="activeName == 'second'">
        <el-button size="small" @click="newKnowledge()">
          <base-icon name="plus" :size="13" />&nbsp;添加</el-button
        >
      </div>
      <div style="flex: 1"></div>
      <el-button @click="close()"> 取消 </el-button>
      <el-button type="primary" @click="newAIBody()"> 确定 </el-button>
    </div>
  </div>
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

    //从已选关系中删除某张表(原代码引用但未实现,补齐避免运行时报错)
    deleteMetric(row) {
      for (let i = 0; i < this.tableRelations.length; i++) {
        const relations = this.tableRelations[i].relations;
        const idx = relations.findIndex(
          (item) =>
            item.relationId == row.relationId && item.sourceId == row.sourceId
        );
        if (idx > -1) {
          relations.splice(idx, 1);
          if (relations.length == 0) {
            this.tableRelations.splice(i, 1);
          }
          break;
        }
      }
      //同步左侧勾选状态
      if (row.sourceId == this.queryParams.sourceId && this.$refs.multipleTable) {
        const cIdx = this.candidateTables.findIndex(
          (item) => item.relationId == row.relationId
        );
        if (cIdx > -1) {
          this.$refs.multipleTable.toggleRowSelection(
            this.candidateTables[cIdx],
            false
          );
        }
      }
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
.agent-config {
  width: 100%;
  padding: 4px 28px 20px;
  box-sizing: border-box;
}

.agent-config__form {
  ::v-deep .el-form-item__label {
    padding-bottom: 6px;
    font-weight: 600;
    color: #334155;
  }
  ::v-deep .el-form-item {
    margin-bottom: 20px;
  }
}

.agent-config__tabs {
  ::v-deep .el-tabs__header {
    margin-bottom: 18px;
  }
}

.agent-config__tab-label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.agent-config__panes {
  display: flex;
  gap: 20px;
}

.agent-config__pane {
  flex: 1;
  min-width: 0;
  border: 1px solid var(--border-color, #e5eaf1);
  border-radius: 12px;
  padding: 18px;
  background: linear-gradient(160deg, #fcfdff, #f9fbfe);
}

.agent-config__pane-title {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 14px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;

  &::before {
    content: "";
    width: 3px;
    height: 12px;
    border-radius: 2px;
    background: var(--accent-gradient, linear-gradient(180deg, #3b82f6, #06b6d4));
  }
}

.agent-config__toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}

.agent-config__table-wrap {
  max-height: 38vh;
  overflow-y: auto;
  overflow-x: hidden;

  &--tall {
    max-height: 45vh;
  }
}

.expand-table ::v-deep .el-table__expanded-cell {
  padding: 0px;
}

.agent-config__knowledge {
  max-height: 42vh;
  overflow-y: auto;
  padding: 2px 4px;
}

.agent-config__knowledge-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.agent-config__knowledge-no {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.agent-config__footer {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 0 4px;
  margin-top: 6px;
  border-top: 1px solid var(--border-color, #e5eaf1);
}
</style>