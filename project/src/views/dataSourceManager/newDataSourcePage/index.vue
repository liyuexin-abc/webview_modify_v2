<template>
  <div class="ds-form-wrap">
    <div class="ds-form__section-title">基本信息 · 连接配置</div>

    <el-form label-position="top" size="small" class="ds-form">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="数据源名称" required>
            <el-input
              v-model="dataSource.name"
              placeholder="给数据源起个业务可辨识的名字"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="数据库类型" required>
            <el-select
              v-model="dataSource.dbType"
              placeholder="数据库类型"
              @change="selectDatabaseType"
              style="width: 100%"
            >
              <el-option
                v-for="item in databaseTypeList"
                :key="item.name"
                :label="item.name"
                :value="item.name"
              >
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="主机地址/IP" required>
            <el-input
              v-model="dataSource.host"
              placeholder="如10.0.1.100"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="端口" required>
            <el-input v-model="dataSource.port" placeholder="3306"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="数据库/Database" required>
            <el-input
              v-model="dataSource.defaultDb"
              placeholder="MySql 的 database, 如 clinic_ops"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="Schema(选填)">
            <el-input
              v-model="dataSource.schemaName"
              placeholder="PG/GaussDB选填"
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="用户名" required>
            <el-input
              v-model="dataSource.username"
              placeholder="输入用户名"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item required>
            <template slot="label"
              >密码
              <span class="ds-form__hint" v-if="dataSourceItem != null"
                >(不修改时不输入)</span
              ></template
            >
            <el-input
              v-model="dataSource.password"
              placeholder="输入密码"
              show-password
              autocomplete="new-password"
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="JDBC URL(自动生成,仅供确认)">
        <div class="ds-form__jdbc">{{ JDBCSplice }}&nbsp;</div>
      </el-form-item>

      <el-form-item v-if="JDBCTestText != ''">
        <div class="ds-form__test-ok">
          <base-icon name="check-circle" :size="14" /> {{ JDBCTestText }}
        </div>
      </el-form-item>
    </el-form>

    <div class="horizontal-line"></div>

    <div class="ds-form__footer">
      <el-button @click="testDataSource()"
        ><base-icon name="zap" :size="14" />&nbsp;测试连接</el-button
      >
      <div style="flex: 1"></div>
      <el-button @click="close()">取消</el-button>
      <el-button type="primary" @click="newDataSource()">
        <div v-if="dataSourceItem == null">创建</div>
        <div v-else>更新</div>
      </el-button>
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
      var host = this.dataSource.host || "";
      var port = this.dataSource.port || "";
      var defaultDb = this.dataSource.defaultDb || "";
      if (host !== "" || port !== "" || defaultDb !== "") {
        return this.JDBCPrefix + host + ":" + port + "/" + defaultDb;
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
.ds-form-wrap {
  padding: 2px 4px 0;
}

.ds-form__section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;

  &::before {
    content: "";
    width: 4px;
    height: 14px;
    border-radius: 2px;
    background: var(--accent-gradient, linear-gradient(180deg, #3b82f6, #06b6d4));
  }
}

.ds-form {
  ::v-deep .el-form-item__label {
    padding-bottom: 4px;
    font-weight: 600;
    color: #334155;
  }
  ::v-deep .el-form-item {
    margin-bottom: 14px;
  }
}

.ds-form__hint {
  font-weight: 400;
  color: #94a3b8;
  font-size: 12px;
}

.ds-form__jdbc {
  padding: 7px 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color, #e5eaf1);
  background: #f8fafc;
  font-family: var(--font-mono, Consolas, Menlo, monospace);
  font-size: 12.5px;
  color: #475569;
  word-break: break-all;
  line-height: 1.6;
}

.ds-form__test-ok {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 8px;
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
  font-size: 12.5px;
}

.ds-form__footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 4px 4px;
}
</style>