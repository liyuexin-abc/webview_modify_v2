<template>
  <div style="width: 100%; height: 100%">
    <div style="background-color: #e6e6e6; width: 100%; height: 91%">
      <div v-if="isNew" style="height: 100%;">
        <div
          style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
          "
        >
          <div style="font-size: 30px; display: flex; justify-content: center">
            你好，欢迎使用
            <div style="color: blue">{{ agentItem.name }}</div>
            智能体
          </div>

          <div style="font-size: 20px; color: silver">
            你好，我是{{ agentItem.name }}智能助手，可以帮你查询电力相关数据。
          </div>
        </div>
      </div>

      <div v-if="!isNew"
        style="
          height: 100%;
          max-width: 100%;
          overflow-y: auto;
          overflow-x: hidden;
        "
      >

        <div v-for="(chatInfo,index) in items.chatInfo" :key="index">
          

        <div v-for="(chatItemInfoTemp,index1) in chatInfo.chatItemInfo" :key="index1">
      
          <div v-if="chatItemInfoTemp.type=='user'">
            
      <div style="display: flex;margin-top: 20px;
    justify-content: flex-end;">

<div
                style="
                  white-space: normal;
                  word-break: break-word;
                  text-align: left;
                  max-width: 80%;
                  padding: 15px;
                  background-color: aliceblue;
                  border-radius: 10px;
                  border: solid 1px #ee9f66;
                "
              >

        <div v-for="(chatItemInfo,index2) in chatItemInfoTemp.item" :key="index2">

            
                {{ chatItemInfo.question }}
              
          </div>
</div>
               <div
                style="text-align: right; margin-left: 10px; margin-right: 10px"
              >
                <el-avatar size="medium" icon="el-icon-user-solid"></el-avatar>
          
              </div>

</div>

          </div>



          
           <div v-if="chatItemInfoTemp.type=='ai'">

          <div style="text-align: left; margin-left: 10px; margin-top: 20px;display: flex; align-items: center;">
            <el-avatar size="medium" icon="el-icon-user-solid"></el-avatar>

            <div>&nbsp;&nbsp;{{items.name}}</div>
          </div>


<div
              style="
                text-align: left;
                width: 80%;
                background-color: white;
                margin-left: 50px;
                border: 1px solid rgb(90, 157, 216);
                border-radius: 5px;
              "
            >


        

          <div v-for="(chatItemInfo,index2) in chatItemInfoTemp.item" :key="index2">
          
 

            <div style="width: 95%; padding: 10px 20px 10px 20px;">



             <div v-if="index2 == 0" style="margin-bottom: 20px;"> 
               
                <el-collapse class="select-one">

                  <el-collapse-item class="select-one" name="1">
                        <span class="collapse-title" slot="title">
                          <div style="display:flex;align-items: center;">
                            <i class="el-icon-check"></i>&nbsp;&nbsp;

                          <div style="display: flex;align-items: center;">
                              已推理思考(持续
                              {{
                                chatItemInfoTemp.item[ Object.keys(chatItemInfoTemp.item).length -1].think.speed
                              }}秒)
                          </div>
                          </div>
                        </span>
                      <div>


  <div style="padding:10px;">

<div>

<div style="text-align: left;height:30%;"> 
  <markdown-it-vue :content="chatItemInfoTemp.item[ Object.keys(chatItemInfoTemp.item).length -1].think.message"></markdown-it-vue>
 </div>
</div>
</div>
  
                        </div>


                  </el-collapse-item>
                </el-collapse>

                 </div>




        <el-collapse class="select-one">
                <el-collapse-item class="select-one" name="1">
                        <span class="collapse-title" slot="title">
           
           <div style="display: flex;align-items: center;">
           <div style="width: 20px;
    height: 20px;
    border-radius: 50%;
    background: rgb(59, 130, 246);
    color: rgb(255, 255, 255);
    font-size: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;"> {{chatItemInfo.itemId}} </div>
          &nbsp;&nbsp;



          <div v-if="chatItemInfo.stepType === 'query'"
          style="background: rgb(219, 234, 254);
    color: rgb(29, 78, 216);
                                padding: 2px 3px 2px 3px;
                                height: 20px;
                                display: flex;
                                align-content: center;
                                flex-wrap: wrap;"> 查询  </div>
          <div v-if="chatItemInfo.stepType === 'compute'"
          style="background: rgb(219, 240, 252);
                  color: rgb(0, 126, 172);
                                padding: 2px 3px 2px 3px;
                                height: 20px;
                                display: flex;
                                align-content: center;
                                flex-wrap: wrap;"> 计算  </div>
          <div v-if="chatItemInfo.stepType === 'summarize'"
          style="background: rgb(236, 253, 245);
    color: rgb(4, 120, 87);
                                padding: 2px 3px 2px 3px;
                                height: 20px;
                                display: flex;
                                align-content: center;
                                flex-wrap: wrap;">总结 </div>

            <div>&nbsp; &nbsp;{{chatItemInfo.question}}</div>

            </div>
          </span>






<div v-if="chatItemInfo.stepType === 'query'"><!--查询-->


<div style="padding:20px;">

            <div class="searchBox" v-if="chatItemInfo.chartData.dataVO.data != null">
            <div
              style="
                display: flex;
                flex-direction: column;
                padding: 0 0 10px 0px;
              "
            >

            <div style="display: flex; padding:10px;">



              <div>
                <el-button style="margin-left: 10px" @click="isSqlPage = true"
                  >SQL</el-button
                >
              </div>

              <div>
                <el-button style="margin-left: 10px" @click="downFile">下载</el-button>
              </div>

             
              
              <div style="margin-left: 10px">
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

            <div style="display: flex;padding:10px;">
              <div style="width:100%;height: 30px;background-color: white;">


                <div style="width:60px;height:100%;"> 维度 </div>
                <div> 
                  
                  <div v-for="dim in chatItemInfo.chartData.dataRequestDTO.dimList" :key="dim.id">
              
                    <div>
                      <el-checkbox v-model="checked">
                      
                      {{dim.dimName}}
                      </el-checkbox>
                      <i class="el-icon-close"></i>
                      
                      </div>
       

                  </div>

              </div>


              </div>

            </div>

            <div style="display: flex;padding:10px;">
              <div style="width:100%;height: 30px;background-color: white;">


                <div style="width:60px;height:100%;"> 指标 </div>
                <div > <el-tag
              v-for="tag in metricTags"
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

            </div>

              <div style="display: flex;padding:10px;">
                <div style="width:60px;    margin-top: 7px;
    font-weight: bold;">筛选器
                </div>

                <div>
                  <div style="display: flex;">
                <div style="display: flex; align-items: center">
                  <div style=" text-align: left">

                  <el-select
                    placeholder="类型"
                    v-model="queryParams.dateGranularity"
                    style="width:100px;"
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

                  <el-date-picker
                    v-model="metricDateRange"
                    type="daterange"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    :value-format="'yyyy-MM-dd'"
                    @change="changeDateRange"
                  >
                    <template slot="suffix">
                      <i class="el-input__icon el-icon-date"></i>
                      <!-- 自定义图标位置 -->
                    </template>
                  </el-date-picker>
                </div>

  
</div>


                                <div style="padding-top:10px;">
                  <el-button type="primary" icon="el-icon-search" @click="getMetricsPreview()">搜索</el-button>
                </div>

              </div>
              </div>


            </div>


          </div>


                         <el-table
                  :data="chatItemInfo.chartData.dataVO.data.records"
                  style="width: 100%"
                  border
                  class="tableBox"
                >
                  <el-table-column

                    width="auto"
                    v-for="column in chatItemInfo.chartData.dataVO.data.columns"
                    :key="column.key"
                    :prop="column.key"
                    :label="column.name"
                  ></el-table-column>
                </el-table>
                

          </div>


</div>

<div v-if="chatItemInfo.stepType === 'compute'"><!--计算-->

<div style="padding:20px;">
              <el-table
                  :data="chatItemInfo.chartData.dataVO.data.rows"
                  style="width: 100%"
                  border
                  class="tableBox2"
                >
                  <el-table-column
         
                    width="auto"
                    v-for="column in chatItemInfo.chartData.dataVO.data.columns"
                    :key="column.key"
                    :prop="column.key"
                    :label="column.name"
                  ></el-table-column>
                </el-table>
</div>

</div>


<div v-if="chatItemInfo.stepType === 'summarize'"><!--总结-->

<div style="padding:20px;">
<div style="padding: 14px 16px;
    background: linear-gradient(135deg, rgb(239, 246, 255), rgb(240, 253, 250));
    border: 1px solid rgb(186, 230, 253);
    border-radius: 10px;
    font-size: 14px;
    line-height: 1.8;
    color: rgb(71, 85, 105);">
{{chatItemInfo.chartData.dataVO.rows[0].answer}}
</div>
</div>

</div>




</el-collapse-item>
</el-collapse>

            </div>

</div>


</div>
                


          </div>

        </div>

        </div>
      </div>
    </div>

    <div style="background-color: white; height: 9%">
      <div style="padding: 20px">
        <el-input
          placeholder="请输入您的问题"
          style="font-size: 20px"
          v-model="queryString"
          @keyup.enter.native="handleEnter"
        >
          <el-button slot="append" circle icon="el-icon-position"></el-button>
        </el-input>
      </div>
    </div>


    <el-dialog  :close-on-click-modal="false" top="20vh" title="topN配置" :visible.sync="isTOPNPage">
      <topN-Page
        :topNData="queryParams.top"
        :dimensionsTagItem="dimensionsTag"
        :metricsTagItem="metricsTag"
        @close="closeTopNPage"
        @sureTopN="sureTopNPage"
        v-if="isTOPNPage"
      />
    </el-dialog>

  </div>
</template>


<script>
import topNPage from "@/views/metricDataPreview/topNPage";

export default {
  name: "queryPage",
  props: [],
components: {
    topNPage,

  },
  data() {
    return {
      queryString: "",
      //agentName: '深圳问数',
      agentItem: "",
      isNew: true,

      lastType: '',
      totalAI: 0,

      /*items: [
        {
          id: 1,
          type: "self",
          context: {
            text: "你好",
          },
        },
        {
          id: 2,
          type: "robot",
          context: {
            chatId: "b223c297-82e8-4d2f-bbbb-1e87aedfada9",
            chatItemInfo: [
              {
                type: "user",
                question:
                  "广东省2026年2月份风能的发电量是多少？环比1月份新增多少",
                itemId: 0,
                chartData: null,
                updateUser: "yanshi",
                updateTime: "2026-06-22 18:03:35",
                statu: 1,
                think: {
                  status: null,
                  message: "",
                  speed: null,
                },
                interactionMode: 3,
                feedback: null,
                reason: null,
                enableContext: true,
                host: "172.17.0.8",
                questionRewriter: null,
                questionConfirm: 0,
                enableDeepThinking: null,
                dimInfos: null,
                stepType: "",
              },
              {
                type: "ai",
                question:
                  "查询广东省2026年1月1日至2026年2月28日的风能发电量，按月份聚合",
                itemId: 1,
                chartData: null,
                updateUser: null,
                updateTime: "2026-06-22 18:04:26",
                status: 5,
                think: {
                  status: null,
                  message: "",
                  speed: 0,
                },
                interactionMode: 0,
                feedback: null,
                reason: null,
                enableContext: null,
                host: "172.17.0.8",
                questionRewriter: null,
                questionConfirm: 0,
                enableDeepThinking: null,
                dimInfos: null,
                stepType: "query",
              },
              {
                type: "ai",
                question:
                  "查询广东省2026年1月1日至2026年2月28日的风能发电量，按月份聚合",
                itemId: 2,
                chartData: null,
                updateUser: null,
                updateTime: "2026-06-22 18:04:26",
                status: 5,
                think: {
                  status: null,
                  message: "",
                  speed: 0,
                },
                interactionMode: 0,
                feedback: null,
                reason: null,
                enableContext: null,
                host: "172.17.0.8",
                questionRewriter: null,
                questionConfirm: 0,
                enableDeepThinking: null,
                dimInfos: null,
                stepType: "compute",
              },
            ],
          },
        },
      ],*/

      items:[],

      metricDateRange: [new Date(), new Date()],
      queryParams: {
        dimList: [],
        indexList: [],

        timeRange: {
          start: "2026-01-01",
          end: "2026-01-01",
        }, //日期
        dateGranularity: "day",
        filters: [
 
        ],
        orderList: [

        ],
        top: {
          groupDims: [],
          orders: [{ id: null, key: "", name: "", order: "desc" }],
          //groupDims: [{id: 90}],
          //orders: [{id: 145, key: "deposit_balance", name: "存款余额", order: "desc"}],
          topNum: 10,
        },

        downloadFlag: 0,
        chartType: 1,

        page: 1,
        pageSize: 10,
        total: 1,
      },

      
      data: {
        code: 1,
        message: "操作成功",
      },



    };
  },

  

  mounted() {},

  methods: {

    addOne(){

    },

    show(type){
      if(type == this.lastType){
        return false
      }
      this.lastType = type
      return true

    },
    tt(){
      //筛选那一堆

    },
    setItems(item){
      this.isNew = false

      this.items = this.newItems(item)

      //this.totalAI = 2

      //this.items = item
    },


    //重组对象，将chatItemInfo中相同type的合并到一个对象中，要不然头像没法显示
    newItems(item){
      let cloneItem = Object.assign({}, item);

    
      for(let i = 0; i < cloneItem.chatInfo.length;i++){
        let cloneChatInfo = cloneItem.chatInfo[i]
        let cloneChatItemInfo = []

        let lastType = ''
        let newObjList = []

         for(let j = 0;j < cloneChatInfo.chatItemInfo.length;j++){
           if(cloneChatInfo.chatItemInfo[j].type === lastType){
             newObjList.push(cloneChatInfo.chatItemInfo[j])
  
           }else{
            if(lastType != ''){
              if(newObjList.length != 0){
                cloneChatItemInfo.push({type: lastType,item: Object.assign([], newObjList)})
        
              }
              newObjList = []   
    
            }
            newObjList.push(cloneChatInfo.chatItemInfo[j])
           }
           lastType = cloneChatInfo.chatItemInfo[j].type
          console.log(lastType)
           
         }
         if(newObjList.length != 0){
            cloneChatItemInfo.push({type: lastType,item: Object.assign([], newObjList)})
          }

        
         cloneChatInfo.chatItemInfo = cloneChatItemInfo
     
      }

      console.log(cloneItem)
      return cloneItem
    },


    handleEnter() {
      this.isNew = false

      this.items.push({
        id: 1,
        type: "self",
        context: {
          text: this.queryString,
        },
      });

      this.queryString = "";
    },

    newPage(item) {
      this.agentItem = item;
    },
  },
};
</script>


 <style scoped lang="scss">
.select-one ::v-deep .el-collapse-item__header {
  background: rgb(241, 244, 249);
  padding: 15px;
border: 1px solid rgb(232, 234, 237);
color: rgb(95, 102, 116);


}

.select-one ::v-deep .el-collapse-item:last-child {
  margin-bottom: -1px;
  border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
  
}
.select-one ::v-deep .el-collapse-item__wrap {
  border-radius: 10px;
}

.disabled-item ::v-deep .el-collapse-item__header {
  cursor: not-allowed; /* 可选，改变鼠标样式提示用户 */
  pointer-events: none; /* 关键：让标题区域的所有鼠标点击失效 */
  padding: 15px;
  background: rgb(241, 244, 249);
  border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
  color: rgb(95, 102, 116);
}
.disabled-item ::v-deep .el-icon-arrow-right:before {
  content: "";
}

.tableBox{
    border-left: solid 1px #b3c6f2;
    border-right: solid 1px #b3c6f2;
    border-bottom: solid 1px #b3c6f2;

    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}

.tableBox2{
    border: solid 1px #b3c6f2;

    border-radius: 10px;
}

.searchBox {
  //display: flex;
  //flex-direction: row;
    background-color: #F2F3F7;;
    padding: 20px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
   
    border-left: solid 1px #b3c6f2;
    border-right: solid 1px #b3c6f2;
    border-top: solid 1px #b3c6f2;
    border-bottom: solid 1px #dddde0;
}


.topBox{
  border-top: 1px solid rgb(90, 157, 216);
    border-left: 1px solid rgb(90, 157, 216);
    border-right: 1px solid rgb(90, 157, 216);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

.centerBox{
    border-left: 1px solid rgb(90, 157, 216);
    border-right: 1px solid rgb(90, 157, 216);
}

.bottomBox{
    border-left: 1px solid rgb(90, 157, 216);
    border-right: 1px solid rgb(90, 157, 216);

    border-bottom: 1px solid rgb(90, 157, 216);
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
}


::v-deep .markdown-body p {
  margin-left: 25px;
  //text-indent: 2em;         /* 首行缩进（可选） */
}


/* 1. 在 .markdown-body 容器上重置计数器 */
::v-deep .markdown-body {
  counter-reset: step-counter;
}


/* 2. 为 h3 添加步骤条样式 */
::v-deep .markdown-body h3 {
  /* 触发计数器递增 */
  counter-increment: step-counter;
  
  /* 布局：为序号和竖线留出空间 */
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 24px;
  
  /* 标题文字样式 */
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 3. 生成步骤序号（圆形数字） */
::v-deep .markdown-body h3::before {
  content: counter(step-counter);
  position: absolute;
  left: 0;
  top: 2px;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background: #409EFF;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
}

/* 4. 生成步骤之间的连接竖线 */
::v-deep .markdown-body h3::after {
  content: '';
  position: absolute;
  left: 11px;  /* 圆点中心位置 (24/2 - 1) */
  top: 28px;   /* 圆点底部 */
  width: 2px;
  height: calc(100% + 8px); /* 延伸到下一个步骤 */
  background: #dcdfe6;
}

/* 5. 最后一个步骤不需要竖线 */
::v-deep .markdown-body h3:last-child::after {
  display: none;
}
</style>

