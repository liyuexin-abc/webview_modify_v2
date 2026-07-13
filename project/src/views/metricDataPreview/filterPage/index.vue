<template>
  <div style="display: flex; flex-direction: column; width: 100%;">
    <div class="horizontal-line"></div>

    <div style="max-height: 60vh; overflow-y: auto; overflow-x: hidden;" class="no-scrollbar">
    <div style="display: flex;">
      <div class="three-front-bgdiv">
        字段
      </div>

      <div class="three-middle-bgdiv">
        条件
      </div>
      <div class="three-middle-bgdiv">
        值
      </div>

      <div style="width: 10%; text-align: left; padding: 0px 30px 5px 5px;">
      </div>
    </div>

    <div
      style="display: flex;"
      v-for="(filterItem, index) in filterDataItem"
      :key="filterItem.filterField.id"
    >
      <div class="three-front-bgdiv">
        <el-select v-model="filterItem.filterField.id" placeholder="请选择字段">
          <el-option
            v-for="item in allTagItem"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </div>

      <div class="three-middle-bgdiv">
        <el-select v-model="filterItem.operator" placeholder="请选择条件">
          <el-option
            v-for="item in operatorEnum"
            :key="item.value"
            :label="item.name"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </div>
      <div class="three-middle-bgdiv">
        <el-input
          v-model="filterItem.filterValue"
          placeholder="如:10000"
        ></el-input>
      </div>

      <div style="width: 10%; text-align: left; padding: 0px 30px 5px 5px">
        <el-button type="text" style="color: red" @click="deleteFilter(index)"
          >删除</el-button
        >
      </div>
    </div>

    <div style="display: flex;padding-top: 5px;">
      <div class="one-bgdiv">
        <el-button @click="newFilter()"
          ><i class="el-icon-plus"></i>&nbsp;添加</el-button
        >
      </div>
    </div>
    </div>
    <div class="horizontal-line"></div>

    <div style="display: flex;padding-bottom: 5px;">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end;">
        <el-button @click="close()" >取消</el-button>
        <el-button type="primary" @click="sureFilter()" 
          >确定</el-button
        >
      </div>
    </div>
  </div>
</template>


<script>
import { operatorEnum,filterTypeEnum} from "@/api/metricDataPreview/metricPreviewAPI.js";

export default {
  name: "filterPage",
  props: ["dimensionsTagItem", "metricsTagItem", "filterData"],
  components: {},
  data() {
    return {
      operatorEnum,
      filterTypeEnum,
      
      allTagItem: [],
      filterDataItem: null,
    };
  },

  mounted() {
    this.allTagItem = [...this.metricsTagItem, ...this.dimensionsTagItem];//将两个合并
    this.filterDataItem = Object.assign([], this.filterData)

    if(!(this.filterDataItem?.length > 0)) this.newFilter()
  },
  methods: {
    sureFilter() {
      for(let i = 0;i < this.filterDataItem.length;i++){
        if(this.filterDataItem[i].filterField.id == '' || this.filterDataItem[i].filterField.id == null
        || this.filterDataItem[i].filterValue == '' ){
  
              this.$message({
                message: '有空值,请填好值在提交',
                type: 'error',
                duration: this.$messageDuration 
              });
          return;
        }
      }

      for(let i =0;i< this.filterDataItem.length;i++){
        let index = this.metricsTagItem.findIndex(item => item.id == this.filterDataItem[i].filterField.id)
        if(index > -1){
          this.filterDataItem[i].filterField.key = this.metricsTagItem[index].key
          this.filterDataItem[i].filterField.name = this.metricsTagItem[index].name
          this.filterDataItem[i].filterField.fieldClazz = filterTypeEnum['metric'].value
        }
      }
      
      for(let i =0;i< this.filterDataItem.length;i++){
        let index = this.dimensionsTagItem.findIndex(item => item.id == this.filterDataItem[i].filterField.id)
        if(index > -1){
          this.filterDataItem[i].filterField.key = this.dimensionsTagItem[index].key
          this.filterDataItem[i].filterField.name = this.dimensionsTagItem[index].name
          this.filterDataItem[i].filterField.fieldClazz = filterTypeEnum['dim'].value
        }
      }

      this.$emit("sureFilter", this.filterDataItem);
      //this.$emit("close");
    },

    //关闭窗口
    close() {
      this.$emit("close");
    },

    newFilter() {
      if(this.filterDataItem == null) this.filterDataItem = []
      for(let i = 0;i < this.filterDataItem.length;i++){
        if(this.filterDataItem[i].filterField.id == '' || this.filterDataItem[i].filterField.id == null
        || this.filterDataItem[i].filterValue == '' ){
          return;
        }
      }

      this.filterDataItem.push({
        filterField: { fieldClazz: null, id: null, key: "", name: "" },
        operator: 2,
        filterValue: "",
      });
    },

    deleteFilter(index) {
      this.filterDataItem.splice(index, 1);
    },
  },
};
</script>


 <style scoped lang="scss">

 .three-front-bgdiv {
    width: 33%; 
    text-align: left; 
    padding: 0px 5px 5px 30px
  }

.three-middle-bgdiv {
    width: 33%; 
    text-align: left; 
    padding: 0px 5px 5px 5px;
  }

</style>