<template>
  <div>
    <div class="horizontal-line"></div>

    <div
      style="max-height: 65vh; overflow-y: auto; overflow-x: hidden"
      class="no-scrollbar"
    >
      <div style="display: flex">
        <div class="one-bgdiv">
          <div class="warntext-bg">
            确认后将自动导入该表全部字段到字段映射表，业务类型（fact/dim）后续在字段设置中指定。
          </div>
        </div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">数据源<span style="color: red">*</span></div>
      </div>

      <div style="display: flex">
        <div class="one-bgdiv">
          <el-select
            placeholder="请选择数据源"
            v-model="queryParams.sourceId"
            @change="getFieldMappingunRegisterTable"
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

      <div style="display: flex" v-if="isTable">
        <div class="one-bgdiv">
          <div style="display: flex; align-items: center; padding: 0 0 5px 0;">
            <el-input
              placeholder="搜索表名..."
              v-model="queryParams.keyword"
              @keyup.enter.native="handleEnter"
              style="width: 240px"
              suffix-icon="el-icon-search"
            >
            </el-input>

            <div style="margin-left: 10px">
              <el-button type="text" @click="toggleAllSelection"
                >全选</el-button
              >
            </div>
            <div style="margin-left: 10px">
              <el-button type="text" @click="clearAllSelection"
                >取消全选</el-button
              >
            </div>
            <div style="margin-left: 10px; line-height: 1">
              已选 {{ multipleCollectRemoteTables.length }} 张表
            </div>
          </div>

          <div class="table-container">
          <div class="drag-table">
          <el-table
            :reserve-selection="true"
            ref="multipleTable"
            :data="collectRemoteTables"
            @selection-change="handleSelectionChange"
            border
          >
            <el-table-column
              label="序号"
              type="selection"
              width="55"
              :selectable="selectableMethod"
            >
            </el-table-column>

            <el-table-column
              prop="tableName"
              label="表名"
              width="auto"
              min-width="35%"
              resizable
              sortable
                     show-overflow-tooltip
                 :render-header="renderHeader"
            ></el-table-column>
            <el-table-column
              prop="tableComment"
              label="注释"
              width="auto"
              min-width="40%"
              resizable
              sortable
                             show-overflow-tooltip
                 :render-header="renderHeader"
            ></el-table-column>
            <el-table-column
              prop="ifRegister"
              label="是否已注册"
              width="auto"
              min-width="25%"
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

    <div style="display: flex;padding-bottom: 5px;">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
        <el-button @click="close">取消</el-button>
        <el-button type="primary" @click="surePhysical">确认注册</el-button>
      </div>
    </div>
  </div>
</template>


<script>
import {
  getFieldMappingunTableBySourceIDAPI,
  newRegisterPhysicalAPI,
  getDataSourcesListAPI,
} from "@/api/fieldMappingManager/fieldMappingAPI.js";

export default {
  name: "physicalRegisteredPage",
  //props: ["physicalRegisteredItem"],
  components: {},
  data() {
    return {
      isTable: false,

      queryParams: {
        sourceId: "",
        keyword: "",
      },

      dataSourceList: [],
      collectRemoteTables: [],
      multipleCollectRemoteTables: [],
    };
  },

  mounted() {
    this.getDataSourceList();
  },
  methods: {
            renderHeader(h, { column }) {
    return h('el-tooltip', {
      props: {
        content: column.label,
        placement: 'top',
        effect: 'dark'
      }
    }, [
      h('span', {
        class: 'ellipsis-text',
        style: { maxWidth: '100%' }
      }, column.label)
    ]);
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

    handleEnter() {
      this.getFieldMappingunRegisterTable();
    },

    selectableMethod(row) {
      // 例如，禁用第二行（索引为1的行）的选择框
      if (row.ifRegister === "已注册") return false;

      return true;
      //return !row.registered; // 或者根据其他逻辑来决定是否可选
    },

    handleSelectionChange(val) {
      this.multipleCollectRemoteTables = [];
      for (let i = 0; i < val.length; i++) {
        this.multipleCollectRemoteTables.push(val[i]);
      }
    },

    // 切换全选状态
    toggleAllSelection() {
      // 通过 $refs 获取表格实例，并调用 toggleAllSelection 方法
      this.$refs.multipleTable.toggleAllSelection();
    },
    // 清空所有选中
    clearAllSelection() {
      this.$refs.multipleTable.clearSelection();
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

    //获取数据源列表
    getFieldMappingunRegisterTable() {
      this.collectRemoteTables = [];

      this.isTable = false;
      if (this.queryParams.sourceId != "") {
        this.isTable = true;
        //const loading = this.loadingScreen();
        getFieldMappingunTableBySourceIDAPI(this.queryParams)
          .then((response) => {
            if (response.code == 200) {
              this.collectRemoteTables = response.data;

              /*if (response.data != null) {
              for (let i = 0; i < response.data.length; i++) {
                this.collectRemoteTables.push(response.data[i]);
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
           // loading.close();
          });
      }
    },

    surePhysical() {
      let data = { sourceId: this.queryParams.sourceId, tableIds: [] };
      for (let i = 0; i < this.multipleCollectRemoteTables.length; i++) {
        data.tableIds.push(this.multipleCollectRemoteTables[i].tableId);
      }

      if (data.sourceId == null || data.sourceId == "") {
        this.$message({
          message: "数据源不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      if (data.tableIds.length == 0) {
        this.$message({
          message: "数据表不能为空",
          type: "error",
          duration: this.$messageDuration,
        });
        return;
      }
      //const loading = this.loadingScreen();
      newRegisterPhysicalAPI(data)
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

    //关闭窗口
    close() {
      this.$emit("close");
    },
  },
};
</script>


 <style scoped lang="scss">

</style>