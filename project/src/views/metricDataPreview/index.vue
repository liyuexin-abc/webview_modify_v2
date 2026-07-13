
<template>
  <div style="display: flex; width: 100%; height: 100%" class="my-custom-style">
    <div class="allbg">
      <div class="tablebg" style="display: flex; flex-direction: row">
        <div
          style="
            width: 250px;
            background-color: white;
            border-right-style: solid;
            border-right-width: 1px;
            border-right-color: #ccc;
          "
        >
          <div>
            <div style="text-align: left; padding: 10px 20px 5px 20px">
              <el-input
                placeholder="请输入内容..."
                v-model="queryTreeParams.keyword"
                suffix-icon="el-icon-search"
                @keyup.enter.native="handleEnter"
              >
              </el-input>
            </div>

            <div style="display: flex">
              <div
                class="one-bgdiv"
                style="
                  display: flex;
                  align-items: center;
                  padding: 0px 30px 5px 20px;
                "
              >
                <div class="vertical-line"></div>
                <div class="title16-one-bgdiv">&nbsp;&nbsp;维度选择</div>
              </div>
            </div>

            <div style="height: 23vh; overflow-y: auto" class="no-scrollbar">
              <el-tree
                :data="dimensionsData"
                show-checkbox
                node-key="id"
                :default-expanded-keys="[]"
                :default-checked-keys="[]"
                :props="defaultDimensionsProps"
                @check-change="selectDimension"
                ref="dimensionTree"
              >
              </el-tree>
            </div>

            <div style="display: flex">
              <div
                class="one-bgdiv"
                style="
                  display: flex;
                  align-items: center;
                  padding: 10px 30px 5px 20px;
                "
              >
                <div class="vertical-line"></div>
                <div class="title16-one-bgdiv">&nbsp;&nbsp;指标选择</div>
              </div>
            </div>

            <div style="height: 23vh; overflow-y: auto" class="no-scrollbar">
              <el-tree
                :data="metricsData"
                show-checkbox
                node-key="id"
                :default-expanded-keys="[]"
                :default-checked-keys="[]"
                :props="defaultMetricsProps"
                @check-change="selectMetrics"
                ref="metricsTree"
              >
              </el-tree>
            </div>
          </div>

          <div class="horizontal-line" style="margin: 10px 0 0px 0"></div>

          <div
            style="
              display: flex;
              align-items: center;
              justify-content: space-between;
              padding: 0px 10px 0px 20px;
              font-size: 14px;
              height: 30px;
            "
          >
            <div>{{ showText }}</div>
            <div><el-button type="text" @click="clear()">清空</el-button></div>
          </div>

          <div
            style="
              display: flex;
              flex-wrap: wrap;
              overflow-y: auto;
              min-height: 12vh;
              justify-content: flex-start;
              align-content: flex-start;
              padding: 10px 10px 10px 20px;
            "
            class="no-scrollbar"
          >
            <el-tag
              v-for="tag in tags"
              :key="tag.id"
              closable
              type="info"
              @close="closeTags(tag)"
              style="margin-right: 10px"
            >
              {{ tag.name }}
            </el-tag>
          </div>
        </div>

        <div style="width: 80%; height: 100%">
          <div class="searchBox" style="display: flex; flex-direction: column">
            <div
              style="
                display: flex;
                justify-content: space-between;
                padding: 0 0 10px 0px;
                flex-wrap: wrap;
                gap: 10px;
              "
            >
              <div style="display: flex">
                <div style="display: flex; align-items: center">
                  <div style="width: 50px; text-align: left">日期:</div>

                  <el-date-picker
                    v-model="metricDateRange"
                    type="daterange"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    :value-format="'yyyy-MM-dd'"
                    @change="changeDateRange"
                    style="width: 250px"
                  >
                    <template slot="suffix">
                      <i class="el-input__icon el-icon-date"></i>
                      <!-- 自定义图标位置 -->
                    </template>
                  </el-date-picker>
                </div>

                <div
                  style="display: flex; align-items: center; margin-left: 10px"
                >
                  <div style="width: 80px; text-align: left">时间粒度:</div>

                  <el-select
                    placeholder="选择时间粒度"
                    v-model="queryParams.dateGranularity"
                    style="width: 120px"
                  >
                    <el-option
                      v-for="item in granularityEnum"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </div>
              </div>

              <div style="display: flex">
                <div>
                  <el-button icon="el-icon-search" @click="getMetricsPreview()"
                    >查看</el-button
                  >
                </div>
                <div style="margin-left: 10px">
                  <el-button icon="el-icon-refresh" @click="reset()"
                    >重置</el-button
                  >
                </div>
              </div>
            </div>

            <div style="display: flex; justify-content: space-between">
              <div>
                <el-button @click="openTopNPageClick">TopN</el-button>
              </div>
              <div>
                <el-button
                  style="margin-left: 10px"
                  @click="openFilterPageClick"
                  >过滤</el-button
                >
              </div>
              <div>
                <el-button style="margin-left: 10px" @click="openSortPageClick"
                  >排序</el-button
                >
              </div>

              <div>
                <el-button
                  style="margin-left: 10px"
                  @click="isSqlPage = true"
                  :disabled="metricPreviewData.sql == ''"
                  >SQL</el-button
                >
              </div>

              <div>
                <el-button
                  style="margin-left: 10px"
                  @click="downFile"
                  :disabled="metricPreviewData.sql == ''"
                  >下载</el-button
                >
              </div>

              <div style="width: 100%"></div>

              <div style="display: none">
                <el-select
                  placeholder="展示方式:表格"
                  style="width: 100%; text-align: right"
                  v-model="queryParams.chartType"
                >
                  <el-option
                    v-for="item in chartTypeEnum"
                    :key="item.value"
                    :label="item.name"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </div>
            </div>
          </div>

          <div style="padding: 10px 20px 10px 20px">
            <div class="table-container">
              <div class="drag-table">
                <el-table
                  :key="tableKey"
                  empty-text="请选择条件"
                  :data="metricPreviewData.records"
                  border
                  v-loading="loading"
                  element-loading-text="加载中..."
                  element-loading-background="rgb(248 248 248 / 50%)"
                  ref="tableRef"
                >
                  <el-table-column
                    sortable
                    show-overflow-tooltip
                    :render-header="renderHeader"
                    v-for="column in metricPreviewData.columns"
                    :key="column.key"
                    :prop="column.key"
                    :label="
                      column.unit
                        ? column.name + '(' + column.unit + ')'
                        : column.name
                    "
                    resizable
                    width="auto"
                    :min-width="tableWidth"
                  >
                  </el-table-column>
                </el-table>

                <pagination
                  v-show="queryParams.total > 0"
                  :total="queryParams.total"
                  :page.sync="queryParams.page"
                  :limit.sync="queryParams.pageSize"
                  @pagination="getMetricsPreview"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      append-to-body
      class="my-custom-style"
      :show-close="false"
      :close-on-click-modal="false"
      top="10vh"
      title="topN配置"
      :visible.sync="isTOPNPage"
    >
      <topN-Page
        :topNData="queryParams.top"
        :dimensionsTagItem="dimensionsTag"
        :metricsTagItem="metricsTag"
        @close="closeTopNPage"
        @sureTopN="sureTopNPage"
        v-if="isTOPNPage"
      />
    </el-dialog>

    <el-dialog
      append-to-body
      class="my-custom-style"
      :show-close="false"
      :close-on-click-modal="false"
      top="10vh"
      title="过滤配置"
      :visible.sync="isFiltersPage"
    >
      <filter-Page
        :filterData="queryParams.filters"
        :dimensionsTagItem="dimensionsTag"
        :metricsTagItem="metricsTag"
        @close="closeFilterPage"
        @sureFilter="sureFilterPage"
        v-if="isFiltersPage"
      />
    </el-dialog>

    <el-dialog
      append-to-body
      class="my-custom-style"
      :show-close="false"
      :close-on-click-modal="false"
      top="10vh"
      title="排序配置"
      :visible.sync="isSortPage"
    >
      <sort-Page
        :sortData="queryParams.orderList"
        :dimensionsTagItem="dimensionsTag"
        :metricsTagItem="metricsTag"
        @close="closeSortPage"
        @sureSort="sureSortPage"
        v-if="isSortPage"
      />
    </el-dialog>

    <el-dialog
      append-to-body
      class="my-custom-style"
      :show-close="false"
      :close-on-click-modal="false"
      top="10vh"
      title="SQL"
      :modal="false"
      :visible.sync="isSqlPage"
    >
      <div class="horizontal-line"></div>

      <div
        style="
          color: white;
          text-align: left;
          width: 100%;
          overflow-y: auto;
          overflow-x: hidden;
          max-height: 50vh;
          padding: 0 10px 0 10px;
        "
        class="no-scrollbar"
      >
        <div
          style="padding: 10px; white-space: pre-wrap; background-color: black"
        >
          {{ formatSQL(metricPreviewData.sql) }}
        </div>
      </div>

      <div class="horizontal-line"></div>

      <div style="margin-top: 10px"></div>

      <div style="display: flex">
        <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
          <el-button @click="isSqlPage = false" style="width: 80px"
            >关闭</el-button
          >
        </div>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import {
  getMetricsTreeAPI,
  getMetricsDataPreviewAPI,
  granularityEnum,
  chartTypeEnum,
} from "@/api/metricDataPreview/metricPreviewAPI.js";
import topNPage from "@/views/metricDataPreview/topNPage";
import filterPage from "@/views/metricDataPreview/filterPage";
import sortPage from "@/views/metricDataPreview/sortPage";

export default {
  name: "metricDataPreview",
  components: {
    topNPage,
    filterPage,
    sortPage,
  },
  data() {
    return {
      granularityEnum,
      chartTypeEnum,

      tableKey: 0,
      tableWidth: "",

      loading: false,

      metricDateRange: [new Date(), new Date()],

      isTOPNPage: false,
      isFiltersPage: false,
      isSortPage: false,
      isSqlPage: false,

      queryTreeParams: {
        keyword: "",
        metricIds: [],
        dimensionIds: [],
      },

      //维度数据列表
      dimensionsData: [],

      //指标数据列表
      metricsData: [],

      queryParams: {
        dimList: [],
        indexList: [],

        timeRange: {
          start: this.formatInitializationDate(new Date()),
          end: this.formatInitializationDate(new Date()),
        }, //日期
        dateGranularity: "day",
        filters: [],
        orderList: [],
        top: {
          groupDims: [{ id: null }],
          orders: [{ id: null, key: "", name: "", order: "desc" }],
          //groupDims: [{id: 90}],
          //orders: [{id: 145, key: "deposit_balance", name: "存款余额", order: "desc"}],
          topNum: 10,
        },

        downloadFlag: 0,
        chartType: 1,

        page: 1,
        pageSize: 10,
        total: 0,
      },
      //列表数据
      metricPreviewData: {
        sql: "",
        records: [],
        columns: [],
      },

      //Tree的变量
      tags: [],

      defaultDimensionsProps: {
        children: "children",
        label: "name",
      },
      dimensionsTag: [],
      dimensionCheckedNodes: [],

      defaultMetricsProps: {
        children: "items",
        label: "name",
      },
      metricsTag: [],
      metricsCheckedNodes: [],
    };
  },

  computed: {
    showText: function () {
      //let count = this.dimensionsData.length + this.metricsData.length;

      return `已选项(${
        //this.dimensionCheckedNodes.length + this.metricsCheckedNodes.length
        this.tags.length
      })`;
    },
  },

  mounted() {
    this.getMetricTreeList();
    window.addEventListener("resize", this.caluWidth);
  },

  methods: {
    computeTableWidth() {
      this.$nextTick(() => {
        const tableEl = this.$refs.tableRef.$el; // 或 this.$refs.tableRef
        const width =
          (tableEl.clientWidth - 10) / this.metricPreviewData.columns.length; // 内容宽度（不含边框）

        this.tableWidth = width + "px";
      });
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

    formatInitializationDate(date) {
      const year = date.getFullYear();
      const month = ("0" + (date.getMonth() + 1)).slice(-2); // 月份是从0开始的，所以加1，并用'0'补齐为两位数
      const day = ("0" + date.getDate()).slice(-2); // 用'0'补齐为两位数
      return `${year}-${month}-${day}`; // YYYY-MM-DD 格式的日期字符串
    },

    changeDateRange(value) {
      if (value && value.length === 2) {
        if (this.queryParams.timeRange == null) {
          this.queryParams.timeRange = { start: "", end: "" };
        }
        this.queryParams.timeRange.start = value[0];
        this.queryParams.timeRange.end = value[1];
      } else {
        this.queryParams.timeRange = null;
      }
    },

    openTopNPageClick() {
      this.isTOPNPage = true;
    },

    sureTopNPage(data) {
      this.queryParams.top = data;
      this.isTOPNPage = false;
    },

    //关闭数据源
    closeTopNPage() {
      // 执行关闭逻辑，例如隐藏对话框等
      this.isTOPNPage = false;
    },

    openFilterPageClick() {
      this.isFiltersPage = true;
    },

    sureFilterPage(data) {
      this.queryParams.filters = data;
      this.isFiltersPage = false;
    },

    closeFilterPage() {
      this.isFiltersPage = false;
    },

    openSortPageClick() {
      this.isSortPage = true;
    },

    sureSortPage(data) {
      this.queryParams.orderList = data;
      this.isSortPage = false;
    },

    closeSortPage() {
      this.isSortPage = false;
    },

    formatSQL(sql) {
      sql = sql.replace(/\n/g, "");
      // 使用正则表达式匹配关键词
      const regex = /\b(SELECT|FROM|WHERE|ORDER BY|GROUP BY|HAVING|LIMIT)\b/gi;
      return sql.replace(regex, (match, keyword) => {
        switch (keyword.toUpperCase()) {
          case "SELECT":
            return `${keyword}\n`;
          case "FROM":
            return `\n${keyword}\n`;
          case "WHERE":
            return `\n${keyword} `; // 注意这里的空格，根据实际需要调整
          case "ORDER BY":
            return `\n${keyword}\n`;
          case "GROUP BY":
            return `\n${keyword}\n`;
          case "HAVING":
            return `\n${keyword}\n`;
          case "LIMIT":
            return `\n${keyword}\n`;
          default:
            return keyword; // 默认返回原关键词，以防新增未处理的关键词
        }
      });
    },

    //左侧指标、维度树
    getMetricTreeList() {
      let dimmensionTreeParams = this.queryTreeParams;
      dimmensionTreeParams.type = "dim";
      //let loading = this.loadingScreen();
      getMetricsTreeAPI(dimmensionTreeParams)
        .then((response) => {
          if (response.code == 200) {
            this.dimensionsData = response.data;
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

      let metricsTreeParams = this.queryTreeParams;
      metricsTreeParams.type = "metric";
      //loading = this.loadingScreen();
      getMetricsTreeAPI(metricsTreeParams)
        .then((response) => {
          if (response.code == 200) {
            this.metricsData = response.data;
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

    handleEnter() {
      this.getMetricTreeList();
    },

    //获取预览
    getMetricsPreview() {
      this.queryParams.downloadFlag = 0;
      this.queryParams.dimList = [];
      for (let i = 0; i < this.dimensionsTag.length; i++) {
        let data = {
          id: this.dimensionsTag[i].id,
          dimKey: this.dimensionsTag[i].key,
          dimName: this.dimensionsTag[i].name,
        };
        this.queryParams.dimList.push(data);
      }
      this.queryParams.indexList = [];
      for (let i = 0; i < this.metricsTag.length; i++) {
        let data = {
          id: this.metricsTag[i].id,
          indKey: this.metricsTag[i].key,
          indName: this.metricsTag[i].name,
        };

        this.queryParams.indexList.push(data);
      }

      if (
        this.queryParams.dimList.length == 0 &&
        this.queryParams.indexList.length == 0
      ) {
        this.$message({
          message: "请选择指标或维度",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }
      //top没有不能传
      let tempQuery = Object.assign({}, this.queryParams);

      tempQuery.top = {};
      if (
        this.queryParams.top.orders[0].id != null &&
        this.queryParams.top.orders[0].id != ""
      ) {
        this.$set(tempQuery.top, "orders", [
          {
            id: this.queryParams.top.orders[0].id,
            key: this.queryParams.top.orders[0].key,
            name: this.queryParams.top.orders[0].name,
            order: this.queryParams.top.orders[0].order,
          },
        ]);
        this.$set(tempQuery.top, "topNum", this.queryParams.top.topNum);
      }
      if (
        this.queryParams.top.groupDims[0].id != null &&
        this.queryParams.top.groupDims[0].id != ""
      ) {
        this.$set(tempQuery.top, "groupDims", [
          { id: this.queryParams.top.groupDims[0].id },
        ]);
      }

      console.log(this.queryParams);

      //const loading = this.loadingScreen();
      this.loading = true;
      getMetricsDataPreviewAPI(tempQuery)
        .then((response) => {
          if (response.code == 200) {
            this.metricPreviewData.sql = "";
            this.metricPreviewData.records = [];
            this.metricPreviewData.columns = [];

            this.queryParams.total = response.data.total;
            this.queryParams.page = response.data.page;
            this.queryParams.pageSize = response.data.pageSize;
            this.metricPreviewData = response.data;

            this.tableKey++;
            this.computeTableWidth();
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

    //下载文件
    downFile() {
      this.queryParams.downloadFlag = 1;
      this.queryParams.dimList = [];
      for (let i = 0; i < this.dimensionsTag.length; i++) {
        let data = {
          id: this.dimensionsTag[i].id,
          dimKey: this.dimensionsTag[i].key,
          dimName: this.dimensionsTag[i].name,
        };
        this.queryParams.dimList.push(data);
      }
      this.queryParams.indexList = [];
      for (let i = 0; i < this.metricsTag.length; i++) {
        let data = {
          id: this.metricsTag[i].id,
          indKey: this.metricsTag[i].key,
          indName: this.metricsTag[i].name,
        };

        this.queryParams.indexList.push(data);
      }

      if (
        this.queryParams.dimList.length == 0 &&
        this.queryParams.indexList.length == 0
      ) {
        this.$message({
          message: "请选择指标或维度",
          type: "error",
          duration: this.$messageDuration,
        });

        return;
      }
      //top没有不能传
      let tempQuery = Object.assign({}, this.queryParams);

      tempQuery.top = {};
      if (
        this.queryParams.top.orders[0].id != null &&
        this.queryParams.top.orders[0].id != ""
      ) {
        this.$set(tempQuery.top, "orders", [
          {
            id: this.queryParams.top.orders[0].id,
            key: this.queryParams.top.orders[0].key,
            name: this.queryParams.top.orders[0].name,
            order: this.queryParams.top.orders[0].order,
          },
        ]);
        this.$set(tempQuery.top, "topNum", this.queryParams.top.topNum);
      }
      if (
        this.queryParams.top.groupDims[0].id != null &&
        this.queryParams.top.groupDims[0].id != ""
      ) {
        this.$set(tempQuery.top, "groupDims", [
          { id: this.queryParams.top.groupDims[0].id },
        ]);
      }

      this.download(
        "/api/v1/chat-server/getdata",
        tempQuery,
        `数据导出_${this.formatDate(new Date())}.xlsx`
      );
    },

    formatDate(date) {
      return (
        date.getFullYear() +
        "" +
        (date.getMonth() + 1).toString().padStart(2, "0") +
        "" +
        date.getDate().toString().padStart(2, "0") +
        "" +
        date.getHours().toString().padStart(2, "0") +
        "" +
        date.getMinutes().toString().padStart(2, "0") +
        "" +
        date.getSeconds().toString().padStart(2, "0")
      );
    },

    //选择维度
    selectDimension(data, checked, node) {
      const checkedTreeNode = this.getDimensionCheckedTreeNodes();
      this.dimensionCheckedNodes = checkedTreeNode;

      console.log(this.queryTreeParams.dimensionIds);
      //新对象，要不然会冲突
      //this.dimensionsTag = [];
      //this.queryTreeParams.dimensionIds = []
      for (let i = 0; i < checkedTreeNode.length; i++) {
        this.dimensionsTag.push(checkedTreeNode[i]);
        this.queryTreeParams.dimensionIds.push(checkedTreeNode[i].id); //每次点击都需要刷新树，把选的加进去
      }

      this.getMetricsPreview();

      this.tags = [];
      for (let i = 0; i < this.metricsTag.length; i++) {
        this.tags.push(this.metricsTag[i]);
      }
      for (let i = 0; i < this.dimensionsTag.length; i++) {
        this.tags.push(this.dimensionsTag[i]);
      }

      this.getMetricTreeList(); //每次点击都需要刷新树，把选的加进去
    },
    //获取选择的维度树
    getDimensionCheckedTreeNodes() {
      let checkedTreeNode = [];
      const allCheckedNodes = this.$refs.dimensionTree.getCheckedNodes(); // 获取所有选中的节点（包括半选节点）

      for (let i = 0; i < allCheckedNodes.length; i++) {
        if (allCheckedNodes[i].id != null) {
          checkedTreeNode.push(allCheckedNodes[i]);
        }
      }
      return checkedTreeNode;
    },
    //选择指标
    selectMetrics(data, checked, node) {
      const checkedTreeNode = this.getMetricsCheckedTreeNodes();
      this.metricsCheckedNodes = checkedTreeNode;

      //新对象，要不然会冲突
      //this.metricsTag = [];
      //this.queryTreeParams.metricIds = []
      for (let i = 0; i < checkedTreeNode.length; i++) {
        this.metricsTag.push(checkedTreeNode[i]);
        this.queryTreeParams.metricIds.push(checkedTreeNode[i].id); //每次点击都需要刷新树，把选的加进去
      }

      this.getMetricsPreview();

      this.tags = [];
      for (let i = 0; i < this.metricsTag.length; i++) {
        this.tags.push(this.metricsTag[i]);
      }
      for (let i = 0; i < this.dimensionsTag.length; i++) {
        this.tags.push(this.dimensionsTag[i]);
      }
      this.getMetricTreeList(); //每次点击都需要刷新树，把选的加进去
    },
    //获取选择的指标树
    getMetricsCheckedTreeNodes() {
      let checkedTreeNode = [];
      const allCheckedNodes = this.$refs.metricsTree.getCheckedNodes(); // 获取所有选中的节点（包括半选节点）

      for (let i = 0; i < allCheckedNodes.length; i++) {
        if (allCheckedNodes[i].id != null) {
          checkedTreeNode.push(allCheckedNodes[i]);
        }
      }
      return checkedTreeNode;
    },

    reset() {
      this.metricDateRange = [new Date(), new Date()];

      if (this.queryParams.timeRange == null) {
        this.queryParams.timeRange = {
          start: this.formatInitializationDate(new Date()),
          end: this.formatInitializationDate(new Date()),
        };
      } else {
        this.queryParams.timeRange.start = this.formatInitializationDate(
          new Date()
        );
        this.queryParams.timeRange.end = this.formatInitializationDate(
          new Date()
        );
      }

      console.log(this.queryParams);
      this.queryParams.dateGranularity = "day";
      this.queryParams.filters = [];
      this.queryParams.orderList = [];
      this.queryParams.top.groupDims = [{ id: null }];
      this.queryParams.top.orders = [
        { id: null, key: "", name: "", order: "desc" },
      ];
      this.queryParams.top.topNum = 10;

      this.queryParams.chartType = 1;

      this.dimList = [];
      this.indexList = [];

      this.dimensionsTag = [];
      this.metricsTag = [];
      this.tags = [];

      this.clear();
    },

    //清空 需要同步树，以及表格清空
    clear() {
      this.dimensionCheckedNodes = [];
      this.metricsCheckedNodes = [];
      this.$refs.dimensionTree.setCheckedKeys([]);
      this.$refs.metricsTree.setCheckedKeys([]);

      this.tags = [];

      this.dimensionsTag = [];
      this.metricsTag = [];

      this.queryTreeParams.dimensionIds = [];
      this.queryTreeParams.metricIds = [];
      this.getMetricTreeList();

      this.metricPreviewData.sql = "";
      this.metricPreviewData.records = [];
      this.metricPreviewData.columns = [];
      this.queryParams.page = 1;
      this.queryParams.total = 0;
      this.queryParams.pageSize = 10;
    },

    //关闭标签
    closeTags(tag) {
      this.tags.splice(this.tags.indexOf(tag), 1);

      let index = this.metricsTag.indexOf(tag);
      if (index > -1) {
        this.metricsTag.splice(index, 1);
      }
      index = this.dimensionsTag.indexOf(tag);
      if (index > -1) {
        this.dimensionsTag.splice(index, 1);
      }

      index = this.dimensionCheckedNodes.indexOf(tag);
      if (index != -1) {
        this.dimensionCheckedNodes.splice(index, 1);
        let checkID = [];
        for (let i = 0; i < this.dimensionCheckedNodes.length; i++) {
          checkID.push(this.dimensionCheckedNodes[i].id);
        }

        this.$refs.dimensionTree.setCheckedKeys(checkID);
      }

      index = this.metricsCheckedNodes.indexOf(tag);
      if (index != -1) {
        this.metricsCheckedNodes.splice(index, 1);
        let checkID = [];
        for (let i = 0; i < this.metricsCheckedNodes.length; i++) {
          checkID.push(this.metricsCheckedNodes[i].id);
        }

        this.$refs.metricsTree.setCheckedKeys(checkID);
      }

      index = this.queryTreeParams.metricIds.indexOf(tag.id);
      if (index > -1) {
        this.queryTreeParams.metricIds.splice(index, 1);
      }
      index = this.queryTreeParams.dimensionIds.indexOf(tag.id);
      if (index > -1) {
        this.queryTreeParams.dimensionIds.splice(index, 1);
      }

      this.getMetricTreeList();

      this.getMetricsPreview();
    },
  },
};
</script>


 <style scoped lang="scss">
::v-deep .el-tag.el-tag--info {
  margin-bottom: 10px;
}
</style>