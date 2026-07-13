<template>
  <div
    style="
      display: flex;
      justify-content: space-between;
      flex-direction: column;
      width: 100%;
      height: 100%;
    "
  >
    <div>
      <div class="horizontal-line"></div>

      <div
        style="max-height: 82vh; overflow-y: auto; overflow-x: hidden"
        class="no-scrollbar"
      >
        <div style="display: flex">
          <div class="two-front-bgdiv">
            维度英文名<span style="color: red">*</span>
          </div>

          <div class="two-back-bgdiv">
            维度中文名<span style="color: red">*</span>
          </div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            <el-input
              v-model="dimensionData.englishName"
              placeholder="请输入维度编码"
              :disabled="dimensionItem != null"
              @input="handleDimensionsKeyInput(dimensionData.englishName)"
            ></el-input>
            <div style="color: red">{{ englishNameText }}</div>
          </div>

          <div class="two-back-bgdiv">
            <el-input
              v-model="dimensionData.chineseName"
              placeholder="如:科室"
              @input="handleDimensionsNameInput(dimensionData.chineseName)"
            ></el-input>

            <div style="color: red">{{ chineseNameText }}</div>
          </div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            维度类型<span style="color: red">*</span>
          </div>

          <div class="two-back-bgdiv">维度别名</div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            <el-select
              placeholder="请选择维度类型"
              v-model="dimensionData.extension.dimensionType"
              style="width: 100%"
            >
              <el-option
                v-for="item in dimensionTypeEnum"
                :key="item.value"
                :label="item.name"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </div>

          <div class="two-back-bgdiv">
            <el-input
              v-model="dimensionData.alias"
              placeholder="多个别名用|分隔,如:部门|组织"
            ></el-input>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">描述</div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <el-input
              v-model="dimensionData.extension.caliberDescription"
              placeholder="维度说明"
              type="textarea"
              :autosize="{ minRows: 3, maxRows: 6 }"
              resize="none"
            ></el-input>
          </div>
        </div>

        <div
          style="display: flex"
          v-if="dimensionData.extension.dimensionType != ''"
        >
          <div class="title16-one-padding-bgdiv">
            <div class="horizontal-line"></div>

            <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
              "
            >
              <div>
                映射表
                <!--<i
                  v-if="!expandItem"
                  class="el-icon-caret-right"
                  @click="expandClick()"
                ></i>
                <i
                  v-if="expandItem"
                  class="el-icon-caret-bottom"
                  @click="expandClick()"
                ></i>-->
              </div>
              <div
                v-if="
                  dimensionData.extension.collectStatus !=
                  collectStatusEnum[0].value
                "
              >
                <el-button @click="openDimensPreview()"
                  ><i class="el-icon-view"></i>&nbsp;维度值预览</el-button
                >
              </div>
            </div>
          </div>
        </div>

        <!--<div v-if="expandItem">-->

        <div
          v-if="
            dimensionData.extension.dimensionType ==
            dimensionTypeEnum['1'].value
          "
        >
          <div style="display: flex">
            <div class="one-bgdiv">
              <div class="warntext-bg">
                选择取值来源后，后端自动执行 SELECT DISTINCT ... LIMIT 100
                采集维值。<br />
                采集结果 &lt;100 条 = 全量采集，≥100 条 = 部分采集。
              </div>
            </div>
          </div>

          <div style="display: flex">
            <div class="one-bgdiv">
              <div class="drag-table">
                <el-table
                  :data="mappingListItem"
                  border
                  :row-style="setRowStyle"
                >
                  <el-table-column
                    label="来源表"
                    prop="soucreTableName"
                    width="auto"
                    min-width="60%"
                    resizable
                    sortable
                    show-overflow-tooltip
                    :render-header="renderHeader"
                  />
                  <el-table-column
                    label="来源字段"
                    prop="sourceField"
                    width="auto"
                    min-width="30%"
                    resizable
                    sortable
                    show-overflow-tooltip
                    :render-header="renderHeader"
                  />

                  <el-table-column
                    label="采集维度值"
                    prop="soucreTableId"
                    width="auto"
                    min-width="20%"
                    align="center"
                    resizable
                    :render-header="renderHeader"
                  >
                    <template slot-scope="scope">
                      <el-radio
                        :label="scope.row.soucreTableId"
                        v-model="dimensionData.extension.databaseTableId"
                      />
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </div>

          <div class="one-bgdiv">取数筛选条件</div>

          <div class="one-bgdiv">
            <el-input
              v-model="dimensionData.extension.valueFilter"
              placeholder="如:status = 1 AND is_deleted = 0"
              :disabled="!dimensionData.extension.databaseTableId"
            ></el-input>
          </div>

          <div class="one-bgdiv" style="font-size: 10px">
            填写 WHERE 之后的 SQL 条件片段，用于过滤采集范围
          </div>

          <!--<div style="display: flex">
              <div class="two-front-bgdiv">取数来源</div>

              <div class="two-back-bgdiv">取数筛选条件</div>
            </div>

            <div style="display: flex">
              <div class="two-front-bgdiv">
                <el-select
                  placeholder="请选择取数来源"
                  v-model="dimensionData.extension.databaseTableId"
                  style="width: 100%"
                >
                  <el-option label="请选择取数来源" value=""></el-option>

                  <el-option
                    v-for="item in dimensionData.mappingList"
                    :key="item.soucreTableId"
                    :label="item.soucreTableName"
                    :value="item.soucreTableId"
                  >
                  </el-option>
                </el-select>
              </div>

              <div class="two-back-bgdiv">
                <el-input
                  v-model="dimensionData.extension.valueFilter"
                  placeholder="如:status = 1 AND is_deleted = 0"
                ></el-input>
              </div>
            </div>-->
        </div>

        <div
          v-if="
            dimensionData.extension.dimensionType ==
            dimensionTypeEnum['2'].value
          "
        >
          <div style="display: flex">
            <div class="one-bgdiv">
              <div class="warntext-bg">
                手工填入维度值映射。填入后即为全量采集，未填即为未采集。<br />
                表内值 = 库中实际存储值，展示值 = 页面显示文案
              </div>
            </div>
          </div>

          <div style="display: flex">
            <div class="one-bgdiv">
              <div class="drag-table">
                <el-table :data="dimensionData.mappingList" border>
                  <el-table-column
                    label="来源表"
                    prop="soucreTableName"
                    width="auto"
                    min-width="70%"
                    resizable
                    sortable
                    show-overflow-tooltip
                    :render-header="renderHeader"
                  />
                  <el-table-column
                    label="来源字段"
                    prop="sourceField"
                    width="auto"
                    min-width="30%"
                    resizable
                    sortable
                    show-overflow-tooltip
                    :render-header="renderHeader"
                  />
                </el-table>
              </div>
            </div>
          </div>

          <div style="display: flex">
            <div class="one-bgdiv">
              <div class="drag-table">
                <el-table
                  :data="dimensionData.extension.valueEntries"
                  border
                  ref="tableRef"
                  @header-dragend="onDragEnd"
                >
                  <el-table-column
                    label="表内值"
                    prop="rawValue"
                    width="auto"
                    min-width="40%"
                    resizable
                    :render-header="renderHeader"
                  >
                    <template slot-scope="scope">
                      <el-input
                        placeholder="表内值"
                        v-model="scope.row.rawValue"
                      ></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="展示值"
                    prop="displayValue"
                    width="auto"
                    min-width="40%"
                    resizable
                    :render-header="renderHeader"
                  >
                    <template slot-scope="scope">
                      <el-input
                        placeholder="展示值"
                        v-model="scope.row.displayValue"
                      ></el-input>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="操作"
                    align="center"
                    width="auto"
                    min-width="10%"
                  >
                    <template slot-scope="scope">
                      <el-button
                        style="color: red"
                        type="text"
                        @click="deleteEntries(scope.row)"
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
              <el-button @click="newEntries()"
                ><i class="el-icon-plus"></i>&nbsp;添加映射</el-button
              >
            </div>
          </div>
        </div>
        <!--</div>-->

        <!--<div style="display: flex">
          <div class="title16-one-padding-bgdiv">映射字段</div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <div class="drag-table">
              <el-table :data="dimensionData.mappingList" border>
                <el-table-column
                  label="来源表"
                  prop="soucreTableName"
                  width="auto"
                  min-width="50%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="来源字段"
                  prop="sourceField"
                  width="auto"
                  min-width="50%"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
              </el-table>
            </div>
          </div>
        </div> -->
      </div>
    </div>
    <div>
      <div class="horizontal-line"></div>

      <div style="display: flex">
        <div class="one-bgdiv" style="text-align: end">
          <el-button @click="close()">取消</el-button>
          <el-button type="primary" @click="newDimensionData()">提交</el-button>
        </div>
      </div>
    </div>

    <el-dialog
      title="行业名称-维度值预览"
      :modal="false"
      :visible.sync="dimensPreview"
      :show-close="false"
      width="70%"
      append-to-body
      class="my-custom-style"
    >
      <div>
        <div class="horizontal-line"></div>

        <div
          style="max-height: 65vh; overflow-y: auto; overflow-x: hidden"
          class="no-scrollbar"
        >
          <div style="display: flex">
            <div class="one-bgdiv">
              <div class="table-container">
                <div class="normal-table">
                  <el-table :data="dimensionValuesList" border>
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
                      prop="value"
                      label="维度值"
                      width="auto"
                      min-width="100%"
                      resizable
                      sortable
                      show-overflow-tooltip
                      :render-header="renderHeader"
                    >
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="horizontal-line"></div>

        <div style="display: flex; padding-bottom: 5px">
          <div
            class="one-bgdiv"
            style="display: flex; justify-content: flex-end"
          >
            <div
              style="
                display: flex;
                flex-direction: row;
                justify-content: space-between;
              "
            >
              <el-button @click="closeDimensPreview()">关闭</el-button>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getDimensionDetailAPI,
  highLevelFlagEnum,
  dimensionTypeEnum,
  saveDimensionDataAPI,
  dimensionValuesAPI,
  collectStatusEnum,
} from "@/api/dimensionManager/dimensionAPI.js";

import {
  checkDimensionsEnameAPI,
  checkDimensionsCnameAPI,
} from "@/api/fieldMappingManager/fieldMappingAPI.js";

export default {
  name: "newDimensionPage",
  props: ["dimensionItem"],
  components: {},
  data() {
    return {
      highLevelFlagEnum,
      dimensionTypeEnum,
      collectStatusEnum,

      chineseNameText: "",
      englishNameText: "",

      mappingListItem: [],

      expandItem: false,
      dimensPreview: false,
      dimensionValuesList: [],

      dimensionData: {
        englishName: "",
        chineseName: "",
        alias: "",

        extension: {
          dimensionType: "",
          caliberDescription: "",
          collectStatus: 0,

          valueEntries: [],

          //标准维
          valueFilter: "",
          databaseTableId: "",
          valueSourceTable: 0,
          valueSourceField: "",
        },

        mappingList: [],
      },
    };
  },

  watch: {
    /*dimensionItem(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.getDimensionDetail();
      }
    },*/
  },

  mounted() {
    this.getDimensionDetail();
    this.newEntries();
  },
  methods: {
    setRowStyle({ row }) {
      if (row.soucreTableId === "") {
        return { backgroundColor: "#f4f4f48a" };
      } else {
        return {};
      }
    },

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

    dimensionValues() {
      if (this.dimensionItem != null) {
        //const loading = this.loadingScreen();
        dimensionValuesAPI(this.dimensionItem.id).then((response) => {
          if (response.code == 200) {
            this.dimensionValuesList = [];
            this.dimensionValuesList = response.data.map((item) => ({
              value: item,
            }));
          }
        });
      }
    },

    openDimensPreview() {
      this.dimensionValues();
      this.dimensPreview = true;
    },

    closeDimensPreview() {
      this.dimensPreview = false;
    },

    async handleDimensionsKeyInput(name) {
      let id = null;
      if (this.dimensionItem != null) {
        id = this.dimensionItem.id;
      }
      await this.checkDimensionsEname(name, id);
    },
    async handleDimensionsNameInput(name) {
      let id = null;
      if (this.dimensionItem != null) {
        id = this.dimensionItem.id;
      }
      this.checkDimensionsCname(name, id);
    },

    async checkDimensionsEname(name, id) {
      let data = { name: name, id: id };
      return checkDimensionsEnameAPI(data)
        .then((response) => {
          if (response.code == 200) {
            if (response.data.exist) {
              this.englishNameText = response.data.errMsg;
            } else {
              this.englishNameText = "";
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
        });
    },

    async checkDimensionsCname(name, id) {
      let data = { name: name, id: id };
      return checkDimensionsCnameAPI(data)
        .then((response) => {
          if (response.code == 200) {
            if (response.data.exist) {
              this.chineseNameText = response.data.errMsg;
            } else {
              this.chineseNameText = "";
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
        });
    },

    newEntries() {
      if (!this.dimensionData.hasOwnProperty("extension")) {
        this.$set(this.dimensionData, "extension", { valueEntries: [] });
      }
      if (!this.dimensionData.extension.hasOwnProperty("valueEntries")) {
        this.$set(this.dimensionData.extension, "valueEntries", []);
      }

      for (
        let i = 0;
        i < this.dimensionData.extension.valueEntries.length;
        i++
      ) {
        if (
          this.dimensionData.extension.valueEntries[i].rawValue == "" ||
          this.dimensionData.extension.valueEntries[i].displayValue == ""
        ) {
          return;
        }
      }

      this.dimensionData.extension.valueEntries.push({
        rawValue: "",
        displayValue: "",
      });
    },

    deleteEntries(row) {
      let index = this.dimensionData.extension.valueEntries.findIndex(
        (item) => item == row
      );
      if (index > -1) {
        this.dimensionData.extension.valueEntries.splice(index, 1);
      }
    },

    expandClick() {
      this.expandItem = !this.expandItem;
    },

    //关闭窗口
    close() {
      this.$emit("close");
    },

    getDimensionDetail() {
      if (this.dimensionItem != null) {
        //const loading = this.loadingScreen();
        getDimensionDetailAPI(this.dimensionItem.id)
          .then((response) => {
            if (response.code == 200) {
              this.dimensionData = response.data;

              if (!this.dimensionData.hasOwnProperty("englishName")) {
                this.$set(this.dimensionData, "englishName", "");
              }

              if (!this.dimensionData.hasOwnProperty("chineseName")) {
                this.$set(this.dimensionData, "chineseName", "");
              }
              if (!this.dimensionData.hasOwnProperty("alias")) {
                this.$set(this.dimensionData, "alias", "");
              }
              if (!this.dimensionData.hasOwnProperty("mappingList")) {
                this.$set(this.dimensionData, "mappingList", []);
              }

              if (!this.dimensionData.hasOwnProperty("extension")) {
                this.$set(this.dimensionData, "extension", {});
              }

              if (
                !this.dimensionData.extension.hasOwnProperty(
                  "caliberDescription"
                )
              ) {
                this.$set(
                  this.dimensionData.extension,
                  "caliberDescription",
                  ""
                );
              }

              if (
                !this.dimensionData.extension.hasOwnProperty("dimensionType")
              ) {
                this.$set(this.dimensionData.extension, "dimensionType", "1");
              }

              if (
                !this.dimensionData.extension.hasOwnProperty("databaseTableId")
              ) {
                this.$set(this.dimensionData.extension, "databaseTableId", "");
              }
              if (
                !this.dimensionData.extension.hasOwnProperty("valueSourceField")
              ) {
                this.$set(this.dimensionData.extension, "valueSourceField", "");
              }
              if (
                !this.dimensionData.extension.hasOwnProperty("valueSourceTable")
              ) {
                this.$set(this.dimensionData.extension, "valueSourceTable", "");
              } else {
                if (
                  this.dimensionData.extension.valueSourceTable != null &&
                  this.dimensionData.extension.valueSourceTable != ""
                ) {
                  this.dimensionData.extension.valueSourceTable = parseInt(
                    this.dimensionData.extension.valueSourceTable,
                    10
                  );
                }
              }
              if (!this.dimensionData.extension.hasOwnProperty("valueFilter")) {
                this.$set(this.dimensionData.extension, "valueFilter", "");
              }

              if (
                !this.dimensionData.extension.hasOwnProperty("valueEntries")
              ) {
                this.$set(this.dimensionData.extension, "valueEntries", []);
              }

              this.mappingListItem = Object.assign(
                [],
                this.dimensionData.mappingList
              );

              this.mappingListItem.push({
                soucreTableName: "不采集维度值",
                sourceField: "-",
                soucreTableId: "",
              });
              this.newEntries();
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

    newDimensionData() {
      if (this.englishNameText != "" || this.chineseNameText != "") {
        this.$message({
          message: "不能提交重复的名称",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (
        this.dimensionData.englishName == null ||
        this.dimensionData.englishName == ""
      ) {
        this.$message({
          message: "维度编码不能为空",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }

      if (
        this.dimensionData.chineseName == null ||
        this.dimensionData.chineseName == ""
      ) {
        this.$message({
          message: "维度名称不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      if (
        this.dimensionData.extension.dimensionType == null ||
        this.dimensionData.extension.dimensionType == ""
      ) {
        this.$message({
          message: "维度类型不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      /*if(this.dimensionData.extension.dimensionType == dimensionTypeEnum['1'].value){
        if(this.dimensionData.extension.valueSourceTable != '' && this.dimensionData.extension.valueFilter == ''){
          this.$message({
            message: "请填写取数筛选条件",
            type: "error",
            duration: this.$messageDuration,
          });
          return;
        }
        if(this.dimensionData.extension.valueSourceTable == '' && this.dimensionData.extension.valueFilter != ''){
          this.$message({
            message: "请填写取数来源",
            type: "error",
            duration: this.$messageDuration,
          });
          return;
        }
      }*/

      if (
        this.dimensionData.hasOwnProperty("extension") &&
        this.dimensionData.extension.hasOwnProperty("valueEntries")
      ) {
        for (
          let i = 0;
          i < this.dimensionData.extension.valueEntries.length;
          i++
        ) {
          if (
            this.dimensionData.extension.valueEntries[i].rawValue == "" &&
            this.dimensionData.extension.valueEntries[i].displayValue == ""
          ) {
            this.dimensionData.extension.valueEntries.splice(i, 1);
            i--;
          }
        }
      }

      let tempDimensionData = Object.assign({}, this.dimensionData);

      if (
        tempDimensionData.extension.dimensionType ==
        dimensionTypeEnum["1"].value
      ) {
        //标准维
        //清除杂项维的东西，然后在整理标准维的数据
        tempDimensionData.extension.valueEntries = [];

        if (
          tempDimensionData.extension.valueSourceTable == null ||
          tempDimensionData.extension.valueSourceTable == ""
        ) {
          tempDimensionData.extension.valueFilter = "";
        }

        let tempList = tempDimensionData.mappingList.filter(
          (item) =>
            item.soucreTableId == tempDimensionData.extension.databaseTableId
        );
        if (tempList.length > 0) {
          tempDimensionData.extension.valueSourceTable =
            tempDimensionData.mappingList[0].soucreTableName;
          tempDimensionData.extension.valueSourceField =
            tempDimensionData.mappingList[0].sourceField;
        }
      } else if (
        tempDimensionData.extension.dimensionType ==
        dimensionTypeEnum["2"].value
      ) {
        //杂项维，清除标准维的数据
        tempDimensionData.extension.databaseTableId = "";
        tempDimensionData.extension.valueSourceTable = "";
        tempDimensionData.extension.valueSourceField = 0;
        tempDimensionData.extension.valueFilter = "";
      }

      //const loading = this.loadingScreen();
      saveDimensionDataAPI(tempDimensionData)
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

      /*if (this.dimensionItem == null) {
        newDimensionDataAPI(this.dimensionData).then((response) => {
          if (response.code == 200) {
            //成功
            this.$message({
              message: "添加成功",
              type: "success",
            });

            this.close();
          } else {
            this.$message.error(response.message);
          }
        });
      } else {
        editDimensionDataAPI(this.dimensionItem.id, this.dimensionData).then(
          (response) => {
            if (response.code == 200) {
              this.$message({
                message: "修改成功",
                type: "success",
              });

              this.close();
            } else {
              this.$message.error(response.message);
            }
          }
        );
      }*/
    },
  },
};
</script>

 <style scoped lang="scss">
::v-deep .el-radio__label {
  display: none;
}
</style>