<template>
  <div :class="['left-menu', { 'is-collapse': isCollapse }]">
    <div class="left-menu__content">
      <el-menu
        default-active="1-1"
        active-text-color="#0073FF"
        :collapse="isCollapse"
        :default-openeds="['1', '2', '3', '4']"
        :collapse-transition="false"
      >
        <el-submenu index="1">
          <template slot="title">
            <DataAccess class="left-menu__icon" />
            <span>数据接入</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="1-1" @click="handleClick(RouterEnum.DATASOURCEMANAGER)">数据源管理</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <ModelAndMapping class="left-menu__icon" />
            <span>模型与映射</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="2-1" @click="handleClick(RouterEnum.DATAMODELMANAGER)">数据模型管理</el-menu-item>
            <el-menu-item index="2-2" @click="handleClick(RouterEnum.FIELDMAPPINGMANAGER)">数据表管理</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title">
            <MetricsAndDimensions class="left-menu__icon" />
            <span>指标与维度</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="3-1" @click="handleClick(RouterEnum.METRICDATAMANAGER)">指标管理</el-menu-item>
            <el-menu-item index="3-2" @click="handleClick(RouterEnum.DIMENSIONMANAGER)">维度管理</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="4">
          <template slot="title">
            <ConsumptionLayer class="left-menu__icon" />
            <span>消费层</span>
          </template>
          <el-menu-item-group>
            <el-menu-item index="4-1" @click="handleClick(RouterEnum.PORTFOLIOMANAGER)">指标组合管理</el-menu-item>
            <el-menu-item index="4-2" @click="handleClick(RouterEnum.METRICDATAPREVIEW)">指标数据预览</el-menu-item>
            <!--<el-menu-item index="4-3" @click="handleClick(RouterEnum.NEWBI)">智能问数</el-menu-item>-->
          </el-menu-item-group>
        </el-submenu>
      </el-menu>
    </div>

    <div class="left-menu__footer">
      <el-button
        size="small"
        :icon="!isCollapse ? 'el-icon-s-fold' : 'el-icon-s-unfold'"
        @click="toggleCollapse"
      />
    </div>
  </div>
</template>

<script>
import {RouterEnum} from '@/utils/common.js';
import DataAccess from '@/components/svgs/DataAccess.vue';
import ModelAndMapping from '@/components/svgs/ModelAndMapping.vue';
import MetricsAndDimensions from '@/components/svgs/MetricsAndDimensions.vue';
import ConsumptionLayer from '@/components/svgs/ConsumptionLayer.vue';

export default {
  name: 'LeftMenu',
  components: {
    DataAccess,
    ModelAndMapping,
    MetricsAndDimensions,
    ConsumptionLayer,
  },
  data() {
    return {
      RouterEnum,
      isCollapse: false,
    };
  },
  methods: {
    handleClick(val) {
      this.$emit('openlink', val);
    },
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
      this.$emit('collapse-change', this.isCollapse);
    },
  },
};
</script>

<style scoped lang="scss">
@use '@/styles/layout.scss' as *;

.left-menu {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: $layout-sidebar-width;
  height: 100%;
  background: #fff;
  transition: width 0.2s;

  &.is-collapse {
    width: $layout-sidebar-collapse-width;
  }

  .left-menu__content {
    flex: 1;
    min-height: 0;
    overflow-x: hidden;
    overflow-y: auto;
  }

  .left-menu__footer {
    flex-shrink: 0;
    display: flex;
    justify-content: flex-end;
    padding: 10px;

    .el-button {
      font-size: 16px;
    }
  }

  ::v-deep .el-menu {
    border-right: none;
  }

  ::v-deep .el-menu-item-group__title {
    padding: 0;
  }

  .left-menu__icon {
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 5px;
    vertical-align: middle;
    color: #909399;

    svg {
      width: 100%;
      height: 100%;
      display: block;
    }

    path {
      fill: currentColor;
    }
  }

  ::v-deep .el-submenu.is-active > .el-submenu__title .left-menu__icon,
  ::v-deep .el-submenu__title:hover .left-menu__icon {
    color: #0073ff;
  }
}
</style>
