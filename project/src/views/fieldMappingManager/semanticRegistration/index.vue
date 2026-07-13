<template>
  <div
    style="
      display: flex;
      flex-direction: column;
      justify-content: space-between;
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
          <div class="two-front-bgdiv">表英文名</div>

          <div class="two-back-bgdiv">表中文名</div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            <el-input
              v-model="semanticData.tbName"
              placeholder="请输入英文名"
            ></el-input>
          </div>

          <div class="two-back-bgdiv">
            <el-input
              v-model="semanticData.cnName"
              placeholder="请输入中文名"
            ></el-input>
          </div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">表类型</div>
        </div>

        <div style="display: flex">
          <div class="two-front-bgdiv">
            <el-radio-group v-model="semanticData.typeKey" @input="changeType">
              <el-radio label="fact">事实表</el-radio>
              <el-radio label="dim">维度表</el-radio>
            </el-radio-group>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">描述</div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <el-input
              type="textarea"
              resize="none"
              :autosize="{ minRows: 3, maxRows: 5 }"
              placeholder="统计范围、统计规则、特殊说明"
              v-model="semanticData.note"
            >
            </el-input>
          </div>
        </div>

        <!--<div
        style="display: flex"
        v-if="semanticData.tbTypeKey == tbTypeKeyEnum[1].value"
      >
        <div class="onebgdiv">SQL</div>
      </div>

      <div
        style="display: flex"
        v-if="semanticData.tbTypeKey == tbTypeKeyEnum[1].value"
      >
        <div class="onebgdiv">
          <el-input
            type="textarea"
            resize="none"
            :autosize="{ minRows: 3, maxRows: 5 }"
            placeholder="SELECT ... FROM ... JOIN ... WHERE ..."
            v-model="semanticData.viewSql"
          >
          </el-input>
        </div>
      </div>

      <div
        style="display: flex"
        v-if="semanticData.tbTypeKey == tbTypeKeyEnum[1].value"
      >
        <div class="onebgdiv">
          <div style="display: flex; align-items: center">
            <el-button type="primary" @click="parseTableSql"
              >执行并解析</el-button
            >

            <div style="margin-left: 20px; color: green">{{ parseText }}</div>
          </div>
        </div>
      </div>-->

        <div style="display: flex">
          <div class="one-bgdiv">
            <div style="display: flex; justify-content: space-between">
              <div style="display: flex; align-items: center">
                <div class="vertical-line"></div>
                <div class="title16-one-bgdiv">&nbsp;&nbsp;字段列表</div>
              </div>

              <div style="text-align: end">
                <el-button
                  @click="openViewPage"
                  v-if="semanticData.tbTypeKey == '1'"
                  >编辑视图</el-button
                >
                <el-button @click="openDim">注册维度</el-button>
                <el-button
                  @click="openMetric"
                  v-if="semanticData.typeKey == 'fact'"
                  >注册指标</el-button
                >
              </div>
            </div>

            <div class="horizontal-line"></div>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <div v-if="showText != ''" class="warntext-bg">
              <i style="color: red" class="el-icon-warning-outline"></i>
              &nbsp;{{ showText }}
            </div>
          </div>
        </div>

        <div style="display: flex">
          <div class="one-bgdiv">
            <div class="drag-table">
              <el-table :data="semanticData.fields" border @header-dragend="onDragEnd" ref="tableRef">
                <el-table-column
                  label="原表字段"
                  width="auto"
                  min-width="25%"
                  prop="fieldKey"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <div style="text-align: left">
                      <div style="height: 24px; line-height: 24px">
                        {{ scope.row.fieldKey }}
                      </div>
                      <div
                        style="
                          color: silver;
                          height: 24px;
                          line-height: 24px;
                          margin-top: -4px;
                        "
                      >
                        {{ scope.row.fieldName }}
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  label="字段类型"
                  width="auto"
                  min-width="20%"
                  prop="fieldType"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="注册类型"
                  width="auto"
                  min-width="15%"
                  prop="basicTypeKey"
                  resizable
                  sortable

                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <el-select
                      placeholder="请选择"
                      v-model="scope.row.basicTypeKey"
                      @change="(val) => changeTypeKey(val, scope.row)"
                    >
                      <el-option label="维度" value="dim"></el-option>
                      <el-option label="指标" value="index"></el-option>
                      <el-option label="忽略" value=""></el-option>
                    </el-select>
                  </template>
                </el-table-column>

                <el-table-column
                  label="注册状态"
                  width="auto"
                  min-width="15%"
                  prop="compareStatus"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                />
                <el-table-column
                  label="注册名称"
                  width="auto"
                  min-width="25%"
                  prop="basicName"
                  resizable
                  sortable
                  show-overflow-tooltip
                  :render-header="renderHeader"
                >
                  <template slot-scope="scope">
                    <div>
                      {{ scope.row.basicName }}
                    </div>
                    <div style="color: red">
                      {{ scope.row.isMetricNew ? "新建" : "" }}
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div class="horizontal-line"></div>

      <div style="display: flex">
        <div class="one-bgdiv" style="text-align: end">
          <el-button @click="close">取消</el-button>
          <el-button type="primary" @click="sureSemantic">保存</el-button>
        </div>
      </div>
    </div>

    <el-dialog
      title="注册维度"
      :close-on-click-modal="false"
      width="80%"
      :visible.sync="isRegisteredDim"
      :modal="false"
      :show-close="false"
      top="10vh"
      append-to-body
      class="my-custom-style"
    >
      <div class="horizontal-line"></div>
      <div style="display: flex; align-items: center; padding: 5px 10px">
        <div style="width: 160px">
          <el-select placeholder="请选择时间列" v-model="ptdateValue">
            <el-option
              v-for="item in ptdate"
              :key="item.id"
              :label="item.englishName"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </div>
        <div>&nbsp;&nbsp;设置时间列</div>
      </div>
      <div
        style="max-height: 50vh; overflow-y: auto; overflow-x: hidden"
        class="no-scrollbar"
      >

        <div style="padding: 5px 10px;">
          <div class="table-container">
          <div class="drag-table">
            <el-table :data="dimensionItem" border @header-dragend="onDragDimEnd" ref="tableDimRef">
              <el-table-column
                label="字段英文名"
                prop="fieldKey"
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
                min-width="20%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />
              <el-table-column
                label="字段类型"
                prop="fieldType"
                width="auto"
                min-width="15%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />

              <el-table-column
                label="维度名称(中文/英文)"
                prop="basicKey"
                width="auto"
                min-width="35%"
                resizable
                sortable
                
                :render-header="renderHeader"
              >
                <template slot-scope="scope">
                  <div
                    style="
                      display: flex;
                      align-items: center;
                      justify-content: flex-start;
                    "
                  >
                    <div>{{ scope.row.basicKey }}</div>
                    <div v-if="scope.row.basicId != null">&nbsp;/&nbsp;</div>
                    <div>{{ scope.row.basicName }}</div>
                    &nbsp;&nbsp;

                    <el-select
                      placeholder="请选择"
                      v-model="scope.row.basicId"
                      style="width: 160px"
                      @change="selectDim(scope.row)"
                      clearable
                      @clear="clearDim(scope.row)"
                    >
                      <el-option
                        v-for="item in allDimensionItem"
                        :key="item.id"
                        :label="item.chineseName + '/' + item.englishName"
                        :value="item.id"
                      >
                      </el-option>
                    </el-select>
                  </div>
                </template>
              </el-table-column>

              <el-table-column
                label="状态"
                width="auto"
                min-width="10%"
                resizable
                show-overflow-tooltip
                :render-header="renderHeader"
              >
                复用
              </el-table-column>

              <!--<el-table-column label="维度类型" align="center" fixed="left">
              <template slot-scope="scope">
                <el-select
                  placeholder="请选择"
                  v-model="scope.row.dimensionType"
                >
                  <el-option
                    v-for="item in dimensionTypeEnum"
                    :key="item.value"
                    :label="item.name"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </template>
            </el-table-column>-->
            </el-table>
          </div>
          </div>
        </div>
      </div>

      <div class="horizontal-line"></div>

      <div style="display: flex; padding-bottom: 5px">
        <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
          <el-button @click="isRegisteredDim = false">关闭</el-button>

          <el-button
            v-show="ptdateValue != ''"
            @click="sureDim()"
            type="primary"
            >确定</el-button
          >
        </div>
      </div>
    </el-dialog>

    <el-dialog
      title="注册指标"
      :close-on-click-modal="false"
      width="80%"
      :visible.sync="isRegisteredMetric"
      :modal="false"
      :show-close="false"
      top="10vh"
      append-to-body
      class="my-custom-style"
    >
      <div class="horizontal-line"></div>

      <div
        style="max-height: 50vh; overflow-y: auto; overflow-x: hidden"
        class="no-scrollbar"
      >
        <div style="padding: 5px 10px">
          <div class="table-container">
          <div class="drag-table">
            <el-table :data="metricDataItem" border @header-dragend="onDragMetricEnd" ref="tableMetricRef" >
              <el-table-column
                label="字段英文名"
                prop="fieldKey"
                width="auto"
                min-width="15%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />
              <el-table-column
                label="字段中文名"
                prop="fieldName"
                width="auto"
                min-width="15%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />
              <el-table-column
                label="字段类型"
                prop="fieldType"
                width="auto"
                min-width="15%"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              />

              <el-table-column
                label="指标名称(英文/中文)"
                prop="basicKey"
                width="auto"
                min-width="40%"
                resizable
                sortable
                :render-header="renderHeader"
              >
                <template slot-scope="scope">
                  <div style="display: flex; flex-direction: column">
                    <div
                      style="display: flex; align-items: center"
                      v-if="scope.row.basicId != null"
                    >
                      <div style="height: 40px">
                        <el-input
                          v-model="scope.row.basicKey"
                          :readonly="!!scope.row.basicId"
                          :class="
                            scope.row.englishNameText ? 'my-red-input' : ''
                          "
                          @input="handleMetricsKeyInput(scope.row)"
                        ></el-input>
                      </div>
                      /
                      <div style="height: 40px">
                        <el-input
                          v-model="scope.row.basicName"
                          :readonly="!!scope.row.basicId"
                          @input="handleMetricsNameInput(scope.row)"
                          :class="
                            scope.row.chineseNameText ? 'my-red-input' : ''
                          "
                        ></el-input>
                      </div>
                    </div>

                    <div style="height: 40px">
                      <el-select
                        placeholder="请选择"
                        v-model="scope.row.basicId"
                        style="width: 100%"
                        @change="selectMetric(scope.row)"
                        clearable
                        @clear="clearMetric(scope.row)"
                      >
                        <el-option label="+新建指标" :value="0"></el-option>
                        <el-option
                          v-for="item in allMetricDataItem"
                          :key="item.id"
                          :label="item.chineseName + '/' + item.englishName"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </div>
                  </div>
                </template>
              </el-table-column>

              <el-table-column
                label="汇总方式*"
                prop="summaryKey"
                width="auto"
                min-width="12%"
                resizable
                sortable
                :render-header="renderHeader"
              >
                <template slot="header" slot-scope="{}">
                  汇总方式<span style="color: red">*</span>
                </template>

                <template slot-scope="scope">
                  <el-select
                    placeholder="请选择"
                    v-model="scope.row.summaryKey"
                  >
                    <el-option
                      v-for="item in summaryKeyEnum"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </template>
              </el-table-column>

              <el-table-column
                label="指标单位"
                prop="unit"
                width="auto"
                min-width="10%"
                resizable
                sortable
                :render-header="renderHeader"
              >
                <template slot-scope="scope">
                  <el-input v-model="scope.row.unit"> </el-input>
                </template>
              </el-table-column>

              <el-table-column
                label="状态"
                width="auto"
                min-width="8%"
                prop="basicId"
                resizable
                sortable
                show-overflow-tooltip
                :render-header="renderHeader"
              >
                <template slot-scope="scope">
                  <div v-if="scope.row.basicId == null"></div>

                  <div v-else-if="scope.row.basicId == 0">新建</div>

                  <div v-else>复用</div>
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
          <el-button @click="isRegisteredMetric = false">关闭</el-button>
          <el-button @click="sureMetric()" type="primary">确定</el-button>
        </div>
      </div>
    </el-dialog>

    <el-dialog
      :close-on-click-modal="false"
      top="10vh"
      title="编辑视图"
      :visible.sync="isViewPage"
      :modal="false"
      :show-close="false"
      append-to-body
      class="my-custom-style"
    >
      <viewRegistered-Page
        :viewID="viewID"
        @close="closeViewPage"
        v-if="isViewPage"
        @sure="sureViewPage"
      />
    </el-dialog>
  </div>
</template>


<script>
import {
  dimensionTypeEnum,
  getShowDimensionListAPI,
} from "@/api/dimensionManager/dimensionAPI.js";

import {
  summaryKeyEnum,
  tbTypeKeyEnum,
  getFieldMappingDetailAPI,
  saveMappingsAPI,
  parseTableSqlAPI,
  getFieldMappingsPtdateAPI,
  checkMetricsEnameAPI,
  checkMetricsCnameAPI,
} from "@/api/fieldMappingManager/fieldMappingAPI.js";

import { getShowMetricDataListAPI } from "@/api/metricDataManager/metricDataAPI.js";
import viewRegisteredPage from "@/views/fieldMappingManager/viewRegisteredPage";

export default {
  name: "semanticRegistrationPage",
  props: ["semanticItem"],
  components: { viewRegisteredPage },
  data() {
    return {
      //获取所有指标、维度，获取详情，在指标里显示详情的，选择列表显示所有指标的，点击进行关联

      dimensionTypeEnum,
      summaryKeyEnum,
      tbTypeKeyEnum,

      //englishNameText: '',
      //chineseNameText: '',

      isViewPage: false,
      viewID: null,

      //提示文本
      showText: "",
      //解析后显示的文本
      parseText: "",

      isRegisteredDim: false,
      isRegisteredMetric: false,

      //获取所有的维度对象--通过调用获取
      allDimensionItem: [],

      //显示的维度列表--从明细字段里筛选出来
      dimensionItem: [],

      //获取所有的指标对象--通过调用获取
      allMetricDataItem: [],

      //显示的指标列表--从明细字段里筛选出来
      metricDataItem: [],

      //明细-有没有编辑视图，取决于他是不是视图类型，tbTypeKey，0-物理表 1-视图，有没有维度注册取决于是不是维度表，typeKey，fac和dim
      semanticData: {
        id: 0,
        metaTableId: 0,
        tbName: "",
        cnName: "",
        sourceId: 0,
        sourceName: "-主库",
        tbTypeKey: "",
        tbTypeName: "",
        typeKey: "",
        viewSql: "",
        note: "",
        fields: [],
      },

      //详细中的原始，用于对比提交
      originalFields: [],

      factFields: [],
      viewFields: [],

      ptdateValue: "",
      ptdate: [
        {
          id: 1,
          chineseName: "分区日期",
          englishName: "ptdate",
          alias: null,
          category: 1,
          dimensionType: 1,
          collectStatus: 1,
          status: 2,
        },
      ],
    };
  },

  async mounted() {
    await this.getShowMetricDataList();
    await this.getShowDimensionList();

    this.getFieldMappingDetail();
    this.getFieldMappingsPtdate();
  },
  methods: {
    onDragEnd(newWidth, oldWidth, column) {
      if (column.property == 'basicTypeKey') {
        const minWidth = 80;
        if (newWidth < minWidth) {
          // 修正列宽
          column.width = minWidth;
          this.$nextTick(() => {
            this.$refs.tableRef.doLayout();
          });
        }
      }
    },

    onDragDimEnd(newWidth, oldWidth, column) {
      if (column.property == 'basicKey') {
        const minWidth = 300;
        if (newWidth < minWidth) {
          // 修正列宽
          column.width = minWidth;
          this.$nextTick(() => {
            this.$refs.tableDimRef.doLayout();
          });
        }
      }
    },

    onDragMetricEnd(newWidth, oldWidth, column) {
      if (column.property == 'basicKey') {
        const minWidth = 260;
        if (newWidth < minWidth) {
          // 修正列宽
          column.width = minWidth;
          this.$nextTick(() => {
            this.$refs.tableMetricRef.doLayout();
          });
        }
      }
      if (column.property == 'summaryKey') {
        const minWidth = 80;
        if (newWidth < minWidth) {
          // 修正列宽
          column.width = minWidth;
          this.$nextTick(() => {
            this.$refs.tableMetricRef.doLayout();
          });
        }
      }
      if (column.property == 'unit') {
        const minWidth = 80;
        if (newWidth < minWidth) {
          // 修正列宽
          column.width = minWidth;
          this.$nextTick(() => {
            this.$refs.tableMetricRef.doLayout();
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

    //打开注册指标-筛选指标
    openMetric() {
      this.isRegisteredMetric = true;
      let tempItem = this.semanticData.fields.filter(
        (item) => item.basicTypeKey === "index"
      );

      this.metricDataItem = [];
      for (let i = 0; i < tempItem.length; i++) {
        if (!tempItem[i].hasOwnProperty("basicKey")) {
          this.$set(tempItem[i], "basicKey", "");
        }
        if (!tempItem[i].hasOwnProperty("basicName")) {
          this.$set(tempItem[i], "basicName", "");
        }

        this.metricDataItem.push(Object.assign({}, tempItem[i]));
      }

      for (let i = 0; i < this.metricDataItem.length; i++) {
        if (!this.metricDataItem[i].hasOwnProperty("fieldKey")) {
          this.$set(this.metricDataItem[i], "fieldKey", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("fieldName")) {
          this.$set(this.metricDataItem[i], "fieldName", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("fieldType")) {
          this.$set(this.metricDataItem[i], "fieldType", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("basicId")) {
          this.$set(this.metricDataItem[i], "basicId", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("basicKey")) {
          this.$set(this.metricDataItem[i], "basicKey", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("basicName")) {
          this.$set(this.metricDataItem[i], "basicName", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("basicType")) {
          this.$set(this.metricDataItem[i], "basicType", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("basicTypeKey")) {
          this.$set(this.metricDataItem[i], "basicTypeKey", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("compareStatus")) {
          this.$set(this.metricDataItem[i], "compareStatus", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("dimensionType")) {
          this.$set(this.metricDataItem[i], "dimensionType", null);
        }

        if (!this.metricDataItem[i].hasOwnProperty("summaryKey")) {
          this.$set(this.metricDataItem[i], "summaryKey", null);
        }
        if (!this.metricDataItem[i].hasOwnProperty("unit")) {
          this.$set(this.metricDataItem[i], "unit", null);
        }

        this.checkMetricsEname(this.metricDataItem[i]);
        this.checkMetricsCname(this.metricDataItem[i]);
      }
    },
    //确认指标
    sureMetric() {
      let nullIndex = this.metricDataItem.findIndex(
        (item) => item.basicId == null
      );
      if (nullIndex > -1) {
        this.$message({
          message: "有没有填充的项",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      nullIndex = this.metricDataItem.findIndex(
        (item) => item.englishNameText != "" || item.chineseNameText != ""
      );
      if (nullIndex > -1) {
        this.$message({
          message: "不能提交重复的名称",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      for (let i = 0; i < this.metricDataItem.length; i++) {
        if (
          this.metricDataItem[i].basicId != null &&
          this.metricDataItem[i].basicId != 0
        ) {
          let title =
            this.metricDataItem[i].fieldName || this.metricDataItem[i].fieldKey;

          if (
            this.metricDataItem[i].summaryKey == null ||
            this.metricDataItem[i].summaryKey == ""
          ) {
            this.$message({
              message: "请填写" + title + "的汇总方式",
              type: "error",
              duration: this.$messageDuration,
            });

            return;
          }
          /*if(this.metricDataItem[i].unit == null || this.metricDataItem[i].unit == ''){
            this.$message.error('请填写'+ title + '的指标单位')
            return 
          }*/
        }
      }

      //注册指标确定后，从名字的字段映射中找到对应项，并重新赋值
      for (let i = 0; i < this.semanticData.fields.length; i++) {
        let index = this.metricDataItem.findIndex(
          (item) => item.fieldKey == this.semanticData.fields[i].fieldKey
        );
        if (index > -1) {
          let data = {};
          data.id = this.metricDataItem[index].id;
          data.fieldKey = this.metricDataItem[index].fieldKey;
          data.fieldName = this.metricDataItem[index].fieldName;
          data.fieldType = this.metricDataItem[index].fieldType;
          data.basicId = this.metricDataItem[index].basicId;
          data.basicKey = this.metricDataItem[index].basicKey;
          data.basicName = this.metricDataItem[index].basicName;
          data.basicType = this.metricDataItem[index].basicType;
          data.basicTypeKey = this.metricDataItem[index].basicTypeKey;
          data.compareStatus = this.metricDataItem[index].compareStatus;

          if (this.metricDataItem[index].summaryKey != null) {
            data.summary =
              summaryKeyEnum[this.metricDataItem[index].summaryKey].name;
          }

          data.summaryKey = this.metricDataItem[index].summaryKey;
          data.unit = this.metricDataItem[index].unit;
          data.isMetricNew = this.metricDataItem[index].isMetricNew;

          this.$set(this.semanticData.fields, i, data);
        }
      }

      this.isRegisteredMetric = false;
    },

    //打开注册维度--筛选维度
    openDim() {
      this.isRegisteredDim = true;

      //将字段映射进行拆分赋值
      let tempItem = this.semanticData.fields.filter(
        (item) => item.basicTypeKey === "dim"
      );

      this.dimensionItem = [];
      for (let i = 0; i < tempItem.length; i++) {
        this.dimensionItem.push(Object.assign({}, tempItem[i]));
      }

      for (let i = 0; i < this.dimensionItem.length; i++) {
        if (!this.dimensionItem[i].hasOwnProperty("fieldKey")) {
          this.$set(this.dimensionItem[i], "fieldKey", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("fieldName")) {
          this.$set(this.dimensionItem[i], "fieldName", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("fieldType")) {
          this.$set(this.dimensionItem[i], "fieldType", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("basicId")) {
          this.$set(this.dimensionItem[i], "basicId", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("basicKey")) {
          this.$set(this.dimensionItem[i], "basicKey", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("basicName")) {
          this.$set(this.dimensionItem[i], "basicName", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("basicType")) {
          this.$set(this.dimensionItem[i], "basicType", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("basicTypeKey")) {
          this.$set(this.dimensionItem[i], "basicTypeKey", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("compareStatus")) {
          this.$set(this.dimensionItem[i], "compareStatus", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("dimensionType")) {
          this.$set(this.dimensionItem[i], "dimensionType", null);
        }

        if (!this.dimensionItem[i].hasOwnProperty("summaryKey")) {
          this.$set(this.dimensionItem[i], "summaryKey", null);
        }
        if (!this.dimensionItem[i].hasOwnProperty("unit")) {
          this.$set(this.dimensionItem[i], "unit", null);
        }
      }
    },
    //确认维度
    sureDim() {
      console.log(this.dimensionItem);
      let nullIndex = this.dimensionItem.findIndex(
        (item) => item.basicId == null
      );
      if (nullIndex > -1) {
        this.$message({
          message: "有没有填充的项",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }

      //注册指标确定后，从名字的字段映射中找到对应项，并重新赋值
      for (let i = 0; i < this.semanticData.fields.length; i++) {
        let index = this.dimensionItem.findIndex(
          (item) => item.fieldKey == this.semanticData.fields[i].fieldKey
        );
        if (index > -1) {
          let data = {};
          data.id = this.dimensionItem[index].id;
          data.fieldKey = this.dimensionItem[index].fieldKey;
          data.fieldName = this.dimensionItem[index].fieldName;
          data.fieldType = this.dimensionItem[index].fieldType;
          data.basicId = this.dimensionItem[index].basicId;
          data.basicKey = this.dimensionItem[index].basicKey;
          data.basicName = this.dimensionItem[index].basicName;
          data.basicType = this.dimensionItem[index].basicType;
          data.basicTypeKey = this.dimensionItem[index].basicTypeKey;
          data.compareStatus = this.dimensionItem[index].compareStatus;

          data.dimensionType = this.dimensionItem[index].dimensionType;

          if (this.dimensionItem[index].summaryKey != null) {
            data.summary =
              summaryKeyEnum[this.dimensionItem[index].summaryKey].name;
          }

          data.summaryKey = this.dimensionItem[index].summaryKey;
          data.unit = this.dimensionItem[index].unit;
          data.isMetricNew = this.dimensionItem[index].isMetricNew;

          this.$set(this.semanticData.fields, i, data);
        }
      }

      this.isRegisteredDim = false;
    },

    openViewPage() {
      this.viewID = this.semanticData.id;
      this.isViewPage = true;
    },

    closeViewPage() {
      this.isViewPage = false;
    },

    sureViewPage() {
      this.isViewPage = false;
      this.getFieldMappingDetail();
    },

    //选择注册类型
    changeTypeKey(value, row) {
      row.basicId = null;
      row.basicKey = null;
      row.basicName = null;
      row.basicType = null;
      //row.basicTypeKey = null
      row.isMetricNew = null;
      row.dimensionType = null;
      row.summaryKey = null;
      row.unit = null;
    },

    //选择类型
    changeType(val) {
      /*if (this.semanticData.tbTypeKey == "0") {
        this.semanticData.fields = this.factFields;
      }
      if (this.semanticData.tbTypeKey == "1") {
        this.semanticData.fields = this.viewFields;
      }*/
      //this.otherInformation();
    },
    //保存
    sureSemantic() {
      this.saveMappings();
    },

    getFieldMappingsPtdate() {
      //const loading = this.loadingScreen();
      getFieldMappingsPtdateAPI()
        .then((response) => {
          if (response.code == 200) {
            if (response.data.hasOwnProperty("id") && response.data.id != "") {
              this.ptdate = [];

              this.ptdate.push(response.data);
              if (this.ptdate.length > 0) {
                this.ptdateValue = this.ptdate[0].id;
              }
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

    //关闭窗口
    close() {
      this.$emit("close");
    },
    //获取详情
    getFieldMappingDetail() {
      if (this.semanticItem != null) {
        //const loading = this.loadingScreen();
        getFieldMappingDetailAPI(this.semanticItem.id)
          .then((response) => {
            if (response.code == 200) {
              if (response.data != null) {
                this.semanticData = response.data;
                //this.originalFields = [...this.semanticData.fields]

                for (let i = 0; i < this.semanticData.fields.length; i++) {
                  this.originalFields.push(
                    Object.assign({}, this.semanticData.fields[i])
                  );
                }

                //将明细中的映射，先按事实、视图维度分别保存，用于后续切换
                //if (this.semanticData.tbTypeKey == "0") {
                //  this.factFields = this.semanticData.fields;
                //}
                //if (this.semanticData.tbTypeKey == "1") {
                //  this.viewFields = this.semanticData.fields;
                //}

                this.otherInformation();
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
      }
    },

    //拆分指标、维度
    otherInformation() {
      let temp = this.semanticData.fields.filter(
        (item) => item.compareStatus == "已注册"
      );

      this.showText =
        "提示:该列表共" +
        this.semanticData.fields.length +
        "个字段，已注册 " +
        temp.length +
        " 个，未注册 " +
        (this.semanticData.fields.length - temp.length) +
        " 个";
    },

    //保存
    saveMappings() {
      if (this.semanticData.tbName == null || this.semanticData.tbName == "") {
        this.$message({
          message: "表英文名不能为空",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }
      let data = {
        tableId: this.semanticData.id,
        typeKey: this.semanticData.typeKey,
        tbName: this.semanticData.tbName,
        cnName: this.semanticData.cnName,
        note: this.semanticData.note,
        viewSql: this.semanticData.viewSql,
        //fields: this.semanticData.fields,
      };

      let tempData = [];
      for (let i = 0; i < this.semanticData.fields.length; i++) {
        let canSumbit = false;

        let index = this.originalFields.findIndex(
          (item) => item.fieldKey === this.semanticData.fields[i].fieldKey
        );

        if (index > -1) {
          if (
            this.originalFields[index].basicId !=
            this.semanticData.fields[i].basicId
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].basicKey !=
            this.semanticData.fields[i].basicKey
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].basicName !=
            this.semanticData.fields[i].basicName
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].basicType !=
            this.semanticData.fields[i].basicType
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].basicTypeKey !=
            this.semanticData.fields[i].basicTypeKey
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].summary !=
            this.semanticData.fields[i].summary
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].summaryKey !=
            this.semanticData.fields[i].summaryKey
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].unit != this.semanticData.fields[i].unit
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].isMetricNew !=
            this.semanticData.fields[i].isMetricNew
          ) {
            canSumbit = true;
          } else if (
            this.originalFields[index].dimensionType !=
            this.semanticData.fields[i].dimensionType
          ) {
            canSumbit = true;
          }
        }
        if (canSumbit) {
          tempData.push(this.semanticData.fields[i]);
        }
      }

      if (tempData.length == 0) {
        this.$message({
          message: "没有注册字段不能提交",
          type: "error",
          duration: this.$messageDuration,
        });
        return false;
      }
      data.fields = tempData;
      //const loading = this.loadingScreen();
      saveMappingsAPI(data)
        .then((response) => {
          if (response.code == 200) {
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
    },

    //清除维度
    clearDim(row) {
      row.basicId = null;
      row.basicKey = null;
      row.basicName = null;
      row.basicType = null;
      row.dimensionType = null;
    },
    //选择维度
    async selectDim(row) {
      //选择空
      if (row.basicId == null) {
        //row.basicId = null
        row.basicKey = null;
        row.basicName = null;
        row.basicType = null;
        row.dimensionType = null;
        //row.basicTypeKey = null
        return;
      }
      console.log(row);

      let item = this.allDimensionItem.filter((item) => item.id == row.basicId);
      if (item.length > 0) {
        row.basicKey = item[0].englishName;
        row.basicName = item[0].chineseName;
        row.basicType = "维度";
        row.basicTypeKey = "dim";
        row.dimensionType = item[0].dimensionType;
      }
    },

    //清除指标
    clearMetric(row) {
      row.basicId = null;
      row.basicKey = null;
      row.basicName = null;
      row.basicType = null;
      row.isMetricNew = null;
    },
    //选择指标
    selectMetric(row) {
      //选择空
      if (row.basicId == null) {
        //row.basicId = null
        row.basicKey = null;
        row.basicName = null;
        row.basicType = null;
        //row.basicTypeKey = null
        row.isMetricNew = null;
        return;
      }

      //选择新建
      if (row.basicId == 0) {
        row.isMetricNew = true;
        row.basicName = row.fieldName;
        row.basicKey = row.fieldKey;
      } else {
        row.isMetricNew = false;
      }

      let item = this.allMetricDataItem.filter(
        (item) => item.id == row.basicId
      );

      if (item.length > 0) {
        row.basicKey = item[0].englishName;
        row.basicName = item[0].chineseName;
        row.basicType = "指标";
        row.basicTypeKey = "index";
      }

      this.checkMetricsEname(row);
      this.checkMetricsCname(row);
    },

    async handleMetricsKeyInput(row) {
      await this.checkMetricsEname(row);
    },
    async handleMetricsNameInput(row) {
      await this.checkMetricsCname(row);
    },

    async checkMetricsEname(row) {
      let data = { name: row.basicKey, id: row.basicId };
      return checkMetricsEnameAPI(data)
        .then((response) => {
          if (response.code == 200) {
            if (response.data.exist) {
              this.$set(row, "englishNameText", response.data.errMsg);
            } else {
              this.englishNameText = "";
              this.$set(row, "englishNameText", "");
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

    async checkMetricsCname(row) {
      let data = { name: row.basicName, id: row.basicId };
      return checkMetricsCnameAPI(data)
        .then((response) => {
          if (response.code == 200) {
            if (response.data.exist) {
              this.$set(row, "chineseNameText", response.data.errMsg);
            } else {
              this.$set(row, "chineseNameText", "");
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

    //获取所有维度
    async getShowDimensionList() {
      let queryParams = { keyword: "" };
      //const loading = this.loadingScreen();
      return getShowDimensionListAPI(queryParams)
        .then((response) => {
          if (response.code == 200) {
            this.allDimensionItem = response.data;
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
    //获取所有指标
    async getShowMetricDataList() {
      let queryParams = { keyword: "" };
      //const loading = this.loadingScreen();
      return getShowMetricDataListAPI(queryParams)
        .then((response) => {
          if (response.code == 200) {
            this.allMetricDataItem = response.data;
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

    //解析SQL语句，重填映射字段------取消了
    parseTableSql() {
      let data = {
        sourceId: this.semanticItem.sourceId,
        sql: this.semanticData.viewSql,
      };
      parseTableSqlAPI(data).then((response) => {
        if (response.code == 200) {
          let parseData = response.data;
          this.parseText = "解析成功," + parseData.fieldComment;
          //通过SQL解析的就是放到视图字段中，并给明细重新赋值
          this.viewFields.fields = parseData.columns;
          this.semanticData.fields = parseData.columns;

          this.otherInformation();
        } else {
          this.$message({
            message: response.message,
            type: "error",
            duration: this.$messageDuration,
          });
        }
      });
    },
  },
};
</script>



 <style scoped lang="scss">


</style>