<template>
  <div style="display: flex; flex-direction: column; width: 100%">

<div class="horizontal-line"></div>
          <div style="display: flex">
      <div style="  width: 33%;
  text-align: left;
  padding: 0px 10px 10px 30px;">排序字段</div>

      <div style="  width: 33%;
  text-align: left;
  padding: 0px 10px 10px 10px;">N值</div>
      <div style="width: 33%;
  text-align: left;
  padding: 0px 30px 10px 10px;">排序方式</div>

    </div>

             <div style="display: flex">
      <div style="  width: 33%;
  text-align: left;
  padding: 0px 10px 10px 30px;">

                <el-select
          v-model="topNData.orders[0].name"
          placeholder="类型"
          
        >
          <el-option
            v-for="item in metricsTagItem"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>

      </div>

      <div style="  width: 33%;
  text-align: left;
  padding: 0px 10px 10px 10px;">
        <el-input v-model="topNData.topNum" placeholder="请输入内容"></el-input>

      </div>
      <div style="width: 33%;
  text-align: left;
  padding: 0px 30px 10px 10px;">
                <el-select
          v-model="topNData.orders[0].order"
          placeholder="排序方式"
        
        >
                      <el-option
              v-for="item in orderEnum"
              :key="item.value"
              :label="item.name"
              :value="item.value"
            >
 </el-option>


        </el-select>

      </div>

    </div>

        <div style="display: flex">
      <div class="one-bgdiv">
        分组字段
      </div>
    </div>

            <div style="display: flex">
      <div class="one-bgdiv">
              <el-select
        v-model="topNData.groupDims[0]"
        placeholder="类型"
      
      >
        <el-option label="不分组" value=""></el-option>
        <el-option
          v-for="item in dimensionsTagItem"
          :key="item.id"
          :label="item.name"
          :value="item.id"
        >
        </el-option>
      </el-select>
      </div>
    </div>

<div class="horizontal-line"></div>
        <div style="display: flex">
      <div class="one-bgdiv" style="    display: flex;
    justify-content: flex-end;">
              <el-button @click="close()" style="width: 80px">取消</el-button>
      <el-button type="primary" @click="sureTopN()" style="width: 80px"
        >确定</el-button
      >
      </div>
    </div>


  </div>
</template>


<script>
import {
  orderEnum,
} from "@/api/metricDataPreview/metricPreviewAPI.js";

export default {
  name: "topNPage",
  props: ["dimensionsTagItem", "metricsTagItem", "topNData"],
  components: {},
  data() {
    return {
      orderEnum,
      /*topNData: {
        groupDims: [{id: 90}],
        orders: [{id: 145, key: "deposit_balance", name: "存款余额", order: "desc"}],
        topNum: 10


      },*/
    };
  },

  mounted() {

  },
  methods: {
    sureTopN() {

      this.$emit("sureTopN", this.topNData);
      //this.$emit("close");
    },

    //关闭窗口
    close() {
      this.$emit("close");
    },
  },
};
</script>


 <style scoped lang="scss">
 .threebgdiv {
  width: 33%;
  text-align: left;
  padding: 0px 30px 10px 30px;
}

.twobgdiv {
  width: 50%;
  text-align: left;
  padding: 0px 30px 10px 30px;
}

.onebgdiv {
  width: 100%;
  text-align: left;
  padding: 0px 30px 10px 30px;
}



.el-select {
  width: 100%;
}

.select-one ::v-deep .el-tag {
  background: #e6f1ff;
  border-radius: 4px 4px 4px 4px;
}

.select-two ::v-deep .el-tag {
  background: #e6f8ea;
  border-radius: 4px 4px 4px 4px;
}

::v-deep .el-select .el-tag__close.el-icon-close {
  background-color: transparent;
}


.horizontal-line {
  border-top: 1px solid #ccc; /* 1px 厚的横线，颜色为浅灰色 */
  margin: 10px 0; /* 根据需要调整间距 */
}

</style>