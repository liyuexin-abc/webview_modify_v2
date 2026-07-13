<template>
  <div
    class="app-layout"
    :class="{ 'app-layout--sidebar-collapse': sidebarCollapsed }"
  >
    <el-container class="app-layout__container">
      <el-header class="app-layout__header">
        <top-nav @openPage="openPage" />
      </el-header>

      <el-container class="app-layout__body" v-show="page == 0">
        <el-aside class="app-layout__aside">
          <left-menu
            @openlink="openlink"
            @collapse-change="sidebarCollapsed = $event"
          />
        </el-aside>

        <el-main class="app-layout__main">
          <div class="app-layout__tabs-spacer" />
          <el-tabs
            v-model="editableTabsValue"
            type="card"
            closable
            class="app-layout__tabs"
            @edit="handleTabsEdit"
          >
            <el-tab-pane
              v-for="item in editableTabs"
              :key="item.name"
              :label="item.title"
              :name="item.name"
              :class="{
                'app-layout__tab-pane--active':
                  editableTabsValue === item.name,
              }"
            >
              <keep-alive>
                <component :is="item.component" />
              </keep-alive>
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>

      <el-container class="app-layout__body" v-show="page == 1">
        <new-BI />
      </el-container>
    </el-container>
  </div>

</template>

<script>
import LeftMenu from "@/components/LeftMenu";
import TopNav from "@/components/TopNav";
import { RouterEnum } from "@/utils/common.js";

import newBI from "@/views/newBI";

export default {
  name: "index",
  components: {
    LeftMenu,
    TopNav,
    RouterEnum,
    newBI,

    dataSourceManager: () => import("@/views/dataSourceManager"),
    metricDataManager: () => import("@/views/metricDataManager"),
    fieldMappingManager: () => import("@/views/fieldMappingManager"),
    portfolioManager: () => import("@/views/portfolioManager"),
    metricDataPreview: () => import("@/views/metricDataPreview"),
    dataModelManager: () => import("@/views/dataModelManager"),
    dimensionManager: () => import("@/views/dimensionManager"),
    //smartQuery: () => import('@/views/smartQuery'),
    //newBI: () => import('@/views/newBI'),
  },
  data() {
    return {
      page: 1,

      editableTabsValue: "",
      editableTabs: [],
      sidebarCollapsed: false,
    };
  },

  mounted() {
    this.openlink(RouterEnum.DATASOURCEMANAGER);
  },

  watch: {
    editableTabsValue() {
      this.scheduleActiveTabTablesLayout();
    },
    sidebarCollapsed() {
      this.scheduleActiveTabTablesLayout();
    },
  },

  methods: {
    scheduleActiveTabTablesLayout() {
      this.$nextTick(() => {
        requestAnimationFrame(() => {
          this.fixActiveTabTablesLayout();
        });
      });
    },

    fixActiveTabTablesLayout() {
      const activePane = this.$el?.querySelector(
        ".app-layout__tabs .el-tab-pane.app-layout__tab-pane--active"
      );
      if (!activePane) return;

      activePane.querySelectorAll(".el-table").forEach((tableEl) => {
        let vm = tableEl.__vue__;
        while (vm && typeof vm.doLayout !== "function") {
          vm = vm.$parent;
        }
        if (vm) vm.doLayout();
      });
    },
    openlink(data) {
      if (
        this.editableTabs.filter((item) => item.name == data.name).length != 0
      ) {
        this.editableTabsValue = data.name;
        return;
      }

      this.editableTabs.push({
        title: data.name,
        name: data.name,
        component: data.component,
      });

      this.editableTabsValue = data.name;
    },

    openPage(page) {
      this.page = page;
    },

    handleTabsEdit(targetName, action) {
      if (action === "add") {
        let newTabName = ++this.tabIndex + "";
        this.editableTabs.push({
          title: "New Tab",
          name: newTabName,
          content: "New Tab content",
        });
        this.editableTabsValue = newTabName;
      }
      if (action === "remove") {
        let tabs = this.editableTabs;
        let activeName = this.editableTabsValue;
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabs[index + 1] || tabs[index - 1];
              if (nextTab) {
                activeName = nextTab.name;
              }
            }
          });
        }

        this.editableTabsValue = activeName;
        this.editableTabs = tabs.filter((tab) => tab.name !== targetName);
      }
    },
  },
};
</script>

<style scoped lang="scss">
@use "@/styles/layout.scss" as *;


</style>
