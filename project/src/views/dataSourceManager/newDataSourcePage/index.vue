<template>
  <div>
    <div style="display: flex; flex-direction: column;">
      <div class="horizontal-line"></div>

      <div style="display: flex">
        <div class="title16-one-padding-bgdiv">
          基本信息 - 连接配置
          <div class="horizontal-line"></div>
        </div>
      </div>

      <div style="display: flex;">
        <div class="two-front-bgdiv">数据源名称<span style="color: red">*</span></div>

        <div class="two-back-bgdiv">数据库类型<span style="color: red">*</span></div>
      </div>

      <div style="display: flex;">
        <div class="two-front-bgdiv">
          <el-input
            v-model="dataSource.name"
            placeholder="给数据源起个业务可辨识得名字"
          ></el-input>
        </div>

        <div class="two-back-bgdiv">
          <el-select
            v-model="dataSource.dbType"
            placeholder="数据库类型"
            @change="selectDatabaseType"
            style="width: 100%;"
          >
            <el-option
              v-for="item in databaseTypeList"
              :key="item.name"
              :label="item.name"
              :value="item.name"
            >
            </el-option>
          </el-select>
        </div>
      </div>

      <div style="display: flex">
        <div class="two-front-bgdiv">主机地址/IP<span style="color: red">*</span></div>

        <div class="two-back-bgdiv">端口<span style="color: red">*</span></div>
      </div>

      <div style="display: flex">
        <div class="two-front-bgdiv">
          <el-input
            v-model="dataSource.host"
            placeholder="如10.0.1.100"
          ></el-input>
        </div>

        <div class="two-back-bgdiv">
          <el-input v-model="dataSource.port" placeholder="3306"></el-input>
        </div>
      </div>

      <div style="display: flex;">
        <div class="two-front-bgdiv">
          数据库/Database
          <span style="color: red">*</span>
        </div>

        <div class="two-back-bgdiv">Schema(选填)</div>
      </div>

      <div style="display: flex;">
        <div class="two-front-bgdiv">
          <el-input
            v-model="dataSource.defaultDb"
            placeholder="MySql 的 database, 如 clinic_ops"
          ></el-input>
        </div>

        <div class="two-back-bgdiv">
          <el-input
            v-model="dataSource.schemaName"
            placeholder="PG/GaussDB选填"
          ></el-input>
        </div>
      </div>

      <div style="display: flex;">
        <div class="two-front-bgdiv">用户名<span style="color: red">*</span></div>

        <div class="two-back-bgdiv" style="display: flex;">
          密码<span style="color: red">*</span>
          <div style="color: silver" v-if="dataSourceItem != null">
            &nbsp;&nbsp;(不修改时不输入)
          </div>
        </div>
      </div>

      <div style="display: flex;">
        <div class="two-front-bgdiv">
          <el-input
            v-model="dataSource.username"
            placeholder="输入用户名"
          ></el-input>
        </div>

        <div class="two-back-bgdiv">
          <el-input
            v-model="dataSource.password"
            placeholder="输入密码"
            show-password
            autocomplete="new-password"
          ></el-input>
        </div>
      </div>

      <div style="display: flex;">
        <div class="one-bgdiv">JDBC URL （自动生成，仅供确认）</div>
      </div>

      <div style="display: flex;">
        <div class="one-bgdiv">
          <!--<el-input
          v-model="JDBCSplice"
          readonly
          disabled
          placeholder=""
        ></el-input>-->
          <div
            style="
              background-color: #f6f6f3;
              border-radius: 5px;
              padding: 6px 12px;
              border: solid 1px silver;
            "
          >
            {{ JDBCSplice }} &nbsp;
          </div>
        </div>
      </div>

      <div style="display: flex;" v-if="JDBCTestText != ''">
        <div class="one-bgdiv">
          <div
            style="
              background-color: rgb(222 252 230);
              border-radius: 5px;
                  padding: 6px 12px;
              border: solid 1px silver;
            "
          >
            {{ JDBCTestText }}
          </div>
        </div>
      </div>
    </div>

    

    <div class="horizontal-line"></div>

    <div style="display: flex;padding-bottom: 5px;">
      <div
        class="one-bgdiv"
        style="display: flex; justify-content: space-between;"
      >
        <div>
          <el-button @click="testDataSource()">测试连接</el-button>
        </div>
        <div>
          <el-button @click="close()">取消</el-button>
          <el-button type="primary" @click="newDataSource()">
            <div v-if="dataSourceItem == null">创建</div>
            <div v-else>更新</div>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {
  getDataSourceDetailAPI,
  newDataSourceAPI,
  testDataSourceAPI,
  editDataSourceAPI,
  //getJDBCPrefixAPI,
  getDBTypeAPI,
  getJDBCURLAPI,
} from "@/api/dataSourceManager/dataSourceAPI.js";

export default {
  name: "newDataSourcePage",
  props: ["dataSourceItem"], //传递过来的行
  components: {},
  data() {
    return {
      JDBCPrefix: "",
      JDBCURL: "",
      JDBCTestText: "",

      //数据库类型列表
      databaseTypeList: [],
      //数据源，用于显示和保存
      dataSource: {
        name: "",
        dbType: "",
        host: "",
        port: "",
        defaultDb: "",
        schemaName: "",
        username: "",
        password: "",
      },
    };
  },

  computed: {
    JDBCSplice: function () {
      if (
        this.dataSource.hasOwnProperty("host") &&
        this.dataSource.hasOwnProperty("port") &&
        this.dataSource.hasOwnProperty("defaultDb") &&
        (this.dataSource.host !='' || this.dataSource.port!='' || this.dataSource.defaultDb != '')
      ) {
        return (
          this.JDBCPrefix +
          this.dataSource.host +
          ":" +
          this.dataSource.port +
          "/" +
          this.dataSource.defaultDb
        );
      } else {
        return this.JDBCPrefix;
      }
      //else
      //  return this.dataSource.jdbcUrl
    },
  },

  mounted() {
    this.getDBType();
    this.getDataSourceDetail();
  },

  methods: {
      /*loadingScreen() {
        const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });

        return loading
      },*/

    //获取数据源详情
    getDataSourceDetail() {
      if (this.dataSourceItem != null) {
        //const loading = this.loadingScreen()
        getDataSourceDetailAPI(this.dataSourceItem.id).then((response) => {
          if (response.code == 200) {
            this.dataSource = response.data;
            //this.dataSource.password = '******'
          } else {
            //访问失败
            this.$message({
            message: response.message,
            type: 'error',
            duration: this.$messageDuration  
          });
          }
        })
        .catch(() => {})
        .finally(() => {
          //loading.close()
        })
      }
    },

    //关闭窗口
    close() {
      this.$emit("close");
    },

    detectError() {
      if (this.dataSource.name == null || this.dataSource.name == "") {
          this.$message({
            message: '请选择数据源名称',
            type: 'error',
            duration: this.$messageDuration  
          });

        return false;
      }

      if (this.dataSource.dbType == null || this.dataSource.dbType == "") {
                  this.$message({
            message: '请选择数据库类型',
            type: 'error',
            duration: this.$messageDuration 
          });

 
        return false;
      }

      if (this.dataSource.host == null || this.dataSource.host == "") {
                       this.$message({
            message: '请输入主机地址',
            type: 'error',
            duration: this.$messageDuration 
          });
        return false;
      }

      if (this.dataSource.port == null || this.dataSource.port == "") {
                               this.$message({
            message: '请输入端口',
            type: 'error',
            duration: this.$messageDuration 
          });

        return false;
      }

      if (
        this.dataSource.defaultDb == null ||
        this.dataSource.defaultDb == ""
      ) {
                           this.$message({
            message: '请输入数据库',
            type: 'error',
            duration: this.$messageDuration 
          });
   
        return false;
      }

      if (this.dataSource.username == null || this.dataSource.username == "") {
                      this.$message({
            message: '请输入用户名',
            type: 'error',
            duration: this.$messageDuration 
          });

        return false;
      }
      return true;
    },

    //测试连接
    testDataSource() {
      //this.getJDBCURL()
      if (!this.detectError()) return;

      let data = {
        id: this.dataSource.id,
        dbType: this.dataSource.dbType,
        host: this.dataSource.host,
        port: this.dataSource.port,
        defaultDb: this.dataSource.defaultDb,
        schemaName: this.dataSource.schemaName,
        username: this.dataSource.username,
        password: this.dataSource.password,
        jdbcUrl: this.dataSource.jdbcUrl,
      };
      //const loading = this.loadingScreen()
      testDataSourceAPI(data).then((response) => {
        if (response.code == 200) {
          if (response.data.success) {
            //成功
            //this.$message({
            //  message: response.data.message,
            //  type: "success",
            //});
            this.JDBCTestText = response.data.message;
          } else {
            //this.$message.error(response.data.message);
            this.JDBCTestText = response.data.message;
          }
        } else {
  
          this.$message({
            message: response.message,
            type: 'error',
            duration: this.$messageDuration 
          });

        }
      })
        .catch(() => {})
        .finally(() => {
          //loading.close()
        })
    },

    //新建和更新数据源
    newDataSource() {
      if (!this.detectError()) return;

      if (this.dataSourceItem == null) {
        //const loading = this.loadingScreen()
        newDataSourceAPI(this.dataSource).then((response) => {
          if (response.code == 200) {
            //成功
            this.$message({
              message: "添加成功",
              type: "success",
              duration: this.$messageDuration 
            });
            this.$emit("sure");
          } else {
                                 this.$message({
            message: response.message,
            type: 'error',
            duration: this.$messageDuration 
          });

          }
        })
        .catch(() => {})
        .finally(() => {
          //loading.close()
        })
      } else {
        //const loading = this.loadingScreen()
        editDataSourceAPI(this.dataSourceItem.id, this.dataSource).then(
          (response) => {
            if (response.code == 200) {
              this.$message({
                message: "修改成功",
                type: "success",
                duration: this.$messageDuration 
              });
              this.$emit("sure");
            } else {
                                               this.$message({
            message: response.message,
            type: 'error',
            duration: this.$messageDuration 
          });
            }
          })
        .catch(() => {})
        .finally(() => {
          //loading.close()
        })
      }
    },

    /*getJDBCURL() {
      let data = {
        dbType: "MySQL",
        host: "10.0.1.100",
        port: 3306,
        defaultDb: "clinic_ops",
        schemaName: "",
      };
      getJDBCURLAPI(data).then((response) => {
        if (response.code == 200) {
          this.JDBCURL = response.data;
        } else {
          this.$message.error(response.message);
        }
      });
    },*/

    getDBType() {
      getDBTypeAPI().then((response) => {
        if (response.code == 200) {
          this.databaseTypeList = response.data;

          this.$nextTick(() => {
            if (this.databaseTypeList.length > 0) {
              this.dataSource.dbType = this.databaseTypeList[0].name;
              let selected = this.databaseTypeList[0].name; // 设置默认值并触发change事件
              this.selectDatabaseType(selected); // 直接调用handleChange方法也可以触发change事件监听器中的逻辑
            }
          });
        } else {
                                                 this.$message({
            message: response.message,
            type: 'error',
            duration: this.$messageDuration 
          });
        }
      });
    },

    selectDatabaseType(item) {
      let selectItem = this.databaseTypeList.filter(
        (itemtemp) => itemtemp.name == item
      );

      if (selectItem.length > 0) {
        this.JDBCPrefix = selectItem[0].jdbcPrefix;
        this.JDBCURL = selectItem[0].jdbcPrefix;
        this.dataSource.port = selectItem[0].defaultPort;
      }
    },
  },
};
</script>

 <style scoped lang="scss">

</style>