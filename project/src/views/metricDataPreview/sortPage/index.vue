<template>
  <div style="display: flex; flex-direction: column; width: 100%;">
    <div class="horizontal-line"></div>

    <div style="max-height: 60vh; overflow-y: auto; overflow-x: hidden;" class="no-scrollbar">
    <div style="display: flex;">
      <div class="two-front-bgdiv">
        排序字段
      </div>

      <div class="two-back-bgdiv">
        排序方式
      </div>

      <div
        style="width: 10%; text-align: left; padding: 0px 30px 5px 5px;"
      ></div>
    </div>

    <div
      style="display: flex;"
      v-for="(sortItem, index) in sortDataItem"
      :key="sortItem.id"
    >
      <div class="two-front-bgdiv">
        <el-select v-model="sortItem.id" placeholder="请选择排序字段">
          <el-option
            v-for="item in allTagItem"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </div>

      <div class="two-back-bgdiv">
        <el-select v-model="sortItem.order" placeholder="请选择排序方式">
          <el-option
            v-for="item in orderEnum"
            :key="item.value"
            :label="item.name"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </div>

      <div style="width: 10%; text-align: left; padding: 0px 30px 5px 5px;">
        <el-button type="text" style="color: red" @click="deleteSort(index)"
          >删除</el-button
        >
      </div>
    </div>

    <div style="display: flex;padding-top: 5px;">
      <div class="one-bgdiv">
        <el-button @click="newSort()"
          ><i class="el-icon-plus"></i>&nbsp;添加</el-button
        >
      </div>
    </div>
</div>
    <div class="horizontal-line"></div>

    <div style="display: flex;padding-bottom: 5px;">
      <div class="one-bgdiv" style="display: flex; justify-content: flex-end;">
        <el-button @click="close()">取消</el-button>
        <el-button type="primary" @click="sureSort()" 
          >确定</el-button
        >
      </div>
    </div>
  </div>
</template>


<script>
import { orderEnum } from "@/api/metricDataPreview/metricPreviewAPI.js";
export default {
  name: "SortPage",
  props: ["dimensionsTagItem", "metricsTagItem", "sortData"],
  components: {},
  data() {
    return {
      orderEnum,
      allTagItem: [],

      sortDataItem: null,
    };
  },

  mounted() {
    this.allTagItem = [...this.metricsTagItem, ...this.dimensionsTagItem];//将两个合并
    this.sortDataItem = Object.assign([], this.sortData)

    if(!(this.sortDataItem?.length > 0)) this.newSort()
  },

  methods: {
    sureSort() {
      for(let i =0;i< this.sortDataItem.length;i++){
        if(this.sortDataItem[i].id == null || this.sortDataItem[i].id == ''){

                      this.$message({
                message: '有空值,请填好值在提交',
                type: 'error',
                duration: this.$messageDuration 
              });
          return 
        }
      }

      for(let i =0;i< this.sortDataItem.length;i++){
        let index = this.allTagItem.findIndex(item => item.id == this.sortDataItem[i].id)
        if(index > -1){
        this.sortDataItem[i].key = this.allTagItem[index].key
        this.sortDataItem[i].name = this.allTagItem[index].name
        }
      }
      
      this.$emit("sureSort", this.sortDataItem);
      //this.$emit("close");
    },

    //关闭窗口
    close() {
      this.$emit("close");
    },

    newSort() {
      if(this.sortDataItem == null) this.sortDataItem = []
      for(let i =0;i< this.sortDataItem.length;i++){
        if(this.sortDataItem[i].id == null || this.sortDataItem[i].id == ''){
          return 
        }
      }

      this.$set(this.sortDataItem,this.sortDataItem.length, {
        id: "",
        key: "",
        name: '',
        order: "desc",
      })
      
      /*this.sortData.push({
        id: "",
        key: "",
        name: '',
        order: "desc",
      });*/
    },

    deleteSort(index) {
      this.sortDataItem.splice(index, 1);
    },
  },
};
</script>


 <style scoped lang="scss">

.two-front-bgdiv{
  width: 45%; 
  text-align: left; 
  padding: 0px 5px 5px 30px;
}

.two-back-bgdiv{
  width: 45%; 
  text-align: left; 
  padding: 0px 5px 5px 5px;
}


</style>