<template>
  <div
    style="
      width: 100%;
      height: 100%;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      justify-content: space-between;
    "
    class="my-custom-style"
  >
    <div v-if="isNewDialog" style="height: 100%">
      <div
        style="
          display: flex;
          flex-direction: column;
          justify-content: center;
          height: 100%;
          align-items: center;
        "
      >
        <div style="font-size: 30px; display: flex; justify-content: center">
          你好，欢迎使用&nbsp;
          <div style="color: blue">{{ selectedAgent.name }}</div>
          &nbsp;智能体
        </div>

        <div style="font-size: 20px; color: silver; text-align: left">
          你好，我是{{ selectedAgent.name }}。
        </div>
      </div>
    </div>

    <div
      v-if="!isNewDialog"
      ref="mainContent"
      style="width: 100%; height: 100%; overflow-y: auto; margin-bottom: 25px"
      class="no-scrollbar"
    >
      <div v-for="(groupChatItemTemp, index) in agentList" :key="index">
        <div
          v-for="(groupChatItem, index1) in groupChatItemTemp"
          :key="index1"
          style="margin-top: 20px"
        >
          <div v-if="groupChatItem.type == 'user'">
            <div
              v-for="(chatItemInfo, index2) in groupChatItem.chatItemInfo"
              :key="index2"
              style="display: flex; margin-top: 20px; justify-content: flex-end"
            >
              <div class="userPanel">
                {{ chatItemInfo.title }}
              </div>
              <div
                style="text-align: right; margin-left: 10px; margin-right: 10px"
              >
                <!--<el-avatar size="medium" icon="el-icon-user-solid">{{userInfo.name}}</el-avatar>-->

                <el-avatar
                  :size="32"
                  :style="{ backgroundColor: '#0073FF', color: 'white' }"
                >
                  {{ avatarText }}
                </el-avatar>
              </div>
            </div>
          </div>

          <div v-if="groupChatItem.type == 'ai'">
            <div
              style="
                text-align: left;
                margin-left: 10px;
                display: flex;
                align-items: center;
                margin-bottom: 10px;
              "
            >
              <div style="display: flex; align-items: center">
                <img
                  class="agent-sidebar__logo"
                  src="@/assets/svgs/logo.svg"
                  alt=""
                />
              </div>

              <div>{{ selectedAgent.name }}</div>
            </div>

            <div class="aiPanel">
              <div
                v-for="(chatItemInfo, index2) in groupChatItem.chatItemInfo"
                :key="index2"
                style="margin: 10px 20px"
              >
                <div v-if="chatItemInfo.stepType == 'think'">
                  <el-collapse class="aiThinkCollapse">
                    <el-collapse-item class="aiThinkCollapse" name="think">
                      <span slot="title" style="width: 100%">
                        <div style="display: flex; align-items: center">
                          <div
                            style="
                              width: 24px;
                              height: 24px;
                              background-color: #9ea0f2;
                              display: flex;
                              align-items: center;

                              justify-content: center;
                              border-radius: 50px;
                            "
                          >
                            <i
                              style="color: white; font-size: 16px"
                              class="el-icon-check"
                            ></i>
                          </div>
                          &nbsp;&nbsp;
                          <div>
                            {{ chatItemInfo.title }}
                          </div>
                        </div>
                      </span>

                      <div style="padding: 10px" class="think">
                        <markdown-it-vue
                          :content="chatItemInfo.think"
                        ></markdown-it-vue>
                      </div>
                    </el-collapse-item>
                  </el-collapse>
                </div>
                <div v-if="chatItemInfo.stepType == 'query'">
                  <el-collapse class="aiCollapse">
                    <el-collapse-item
                      class="aiCollapse"
                      :name="`query${groupChatItem.chatId}`"
                    >
                      <span slot="title" style="width: 100%">
                        <div style="display: flex; align-items: center">
                          <div class="aiTitleNo">
                            {{ chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div class="aiTitleType" style="min-width: 46px">
                            查询
                          </div>
                          &nbsp;&nbsp;
                          <div class="title">{{ chatItemInfo.title }}</div>
                        </div>
                      </span>

                      <div
                        style="
                          padding: 10px;
                          border: 1px solid #e8ecf2;
                          border-radius: 10px;
                        "
                      >
                        <div
                          style="
                            background: #fafbfe;
                            border-bottom: 1px solid #e8ecf2;
                            height: 48px;
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            padding: 0 20px;
                          "
                        >
                          <div>
                            <el-button
                              size="mini"
                              @click="showSQL(chatItemInfo.viewSql)"
                              ><i class="el-icon-tickets"></i
                              >&nbsp;SQL</el-button
                            >

                            <el-button
                              size="mini"
                              @click="downFile(chatItemInfo)"
                              ><i class="el-icon-download"></i>&nbsp;下载
                            </el-button>
                          </div>

                          <div class="chatType-DropDown" style="display: none">
                            <el-dropdown
                              @command="
                                (val) =>
                                  handleCommandChartType(val, chatItemInfo)
                              "
                            >
                              <span style="margin-right: 5px">
                                展示方式:
                                {{ chartTypeEnum[chatItemInfo.chartType].name
                                }}<i
                                  class="el-icon-arrow-down el-icon--right"
                                ></i>
                              </span>
                              <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item
                                  v-for="item in chartTypeEnum"
                                  :key="item.value"
                                  :value="item.value"
                                  :command="item.value"
                                >
                                  {{ item.name }}
                                </el-dropdown-item>
                              </el-dropdown-menu>
                            </el-dropdown>
                          </div>
                        </div>

                        <div
                          style="
                            border-bottom: 1px solid #e7e9ec;
                            min-height: 48px;
                            padding: 5px 20px;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                          "
                        >
                          <div style="display: flex; align-items: center">
                            <div style="width: 60px">维度</div>
                            
                            <div style="display: flex;align-items: center;flex-wrap: wrap;gap: 5px; width:90%;">
                            <div
                              v-for="dim in chatItemInfo.other.dimList"
                              :key="dim.name"
                              class="queryDimPanel"
                            >
                              <div>
                                <!--<el-checkbox
                                  v-model="dim.check"
                                  @change="
                                    (val) => selectDim(val, dim, chatItemInfo)
                                  "
                                >
                                </el-checkbox>-->
                              </div>
                              <el-tooltip :content="dim.name" placement="top">
                              <div style="max-width:80px;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">
                                
                                {{dim.name}} </div>
                              </el-tooltip>

                              <div
                                @click="
                                  (val) => deleteDim(val, dim, chatItemInfo)
                                "
                              >
                                <i class="el-icon-close"></i>
                              </div>
                            </div>

                            
                            </div>

                          </div>
                          <div>
                            <el-dropdown
                              @command="
                                (val) => handleCommandDims(val, chatItemInfo)
                              "
                            >
                              <span>
                                <el-button
                                  size="mini"
                                  icon="el-icon-plus"
                                  style="
                                    border-radius: 50%;
                                    padding: 6px;
                                    height: 26px;
                                  "
                                ></el-button>
                              </span>
                              <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item
                                  :command="null"
                                  v-if="
                                    chatItemInfo.candidate.dimList.length == 0
                                  "
                                >
                                  无可选维度
                                </el-dropdown-item>

                                <el-dropdown-item
                                  v-for="item in chatItemInfo.candidate.dimList"
                                  :key="item.id"
                                  :value="item.id"
                                  :command="item"
                                >
                                  {{ item.name }}
                                </el-dropdown-item>
                              </el-dropdown-menu>
                            </el-dropdown>
                          </div>
                        </div>

                        <div
                          style="
                            border-bottom: 1px solid #e7e9ec;
                            min-height: 48px;
                            padding: 5px 20px;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                          "
                        >
                          <div style="display: flex; align-items: center">
                            <div style="width: 60px">指标</div>
                            
                            
                            <div style="display: flex;align-items: center;flex-wrap: wrap;gap: 5px;width:90%;">
                            <div
                              v-for="mertic in chatItemInfo.other.merticList"
                              :key="mertic.name"
                              class="queryDimPanel"
                            >
                              <div>
                                <!--<el-checkbox
                                  v-model="mertic.check"
                                  @change="
                                    (val) =>
                                      selectMetric(val, mertic, chatItemInfo)
                                  "
                                >
                                </el-checkbox>-->
                              </div>
                              <el-tooltip :content="mertic.name" placement="top">
                              <div style="max-width:80px;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">{{ mertic.name }}</div>
                              </el-tooltip>
                              <div
                                @click="
                                  (val) =>
                                    deleteMetric(val, mertic, chatItemInfo)
                                "
                              >
                                <i class="el-icon-close"></i>
                              </div>
                            </div>
                            </div>
                          </div>
                          <div>
                            <el-dropdown
                              @command="
                                (val) => handleCommandMetrics(val, chatItemInfo)
                              "
                            >
                              <span>
                                <el-button
                                  size="mini"
                                  icon="el-icon-plus"
                                  style="
                                    border-radius: 50%;
                                    padding: 6px;
                                    height: 26px;
                                  "
                                ></el-button>
                              </span>
                              <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item
                                  :command="null"
                                  v-if="
                                    chatItemInfo.candidate.merticList.length ==
                                    0
                                  "
                                >
                                  无可选指标
                                </el-dropdown-item>
                                <el-dropdown-item
                                  v-for="item in chatItemInfo.candidate
                                    .merticList"
                                  :key="item.id"
                                  :value="item.id"
                                  :command="item"
                                >
                                  {{ item.name }}
                                </el-dropdown-item>
                              </el-dropdown-menu>
                            </el-dropdown>
                          </div>
                        </div>

                        <div
                          style="
                            padding: 5px 20px;
                            background: #fafbfe;
                            display: flex;
                            justify-content: space-between;
                            border-bottom: 1px solid rgb(234 234 234);
                          "
                        >
                          <div style="display: flex; width: 100%">
                            <div style="width: 60px">筛选器</div>

                            <div style="width: 90%">
                              <div
                                style="
                                  display: flex;
                                  flex-wrap: wrap;
                                  gap: 10px;
                                "
                              >
                                <div style="display: flex">
                                  <div>
                                    <el-select
                                      placeholder="日期"
                                      v-model="chatItemInfo.dateGranularity"
                                      style="width: 100px; border-radius: 0px"
                                      class="selectStyle"
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
                                    v-model="chatItemInfo.dataRange"
                                    type="daterange"
                                    start-placeholder="开始日期"
                                    end-placeholder="结束日期"
                                    :value-format="'yyyy-MM-dd'"
                                    style="width: 250px; border-radius: 0px"
                                    class="myDate"
                                  >
                                    <template slot="suffix">
                                      <i
                                        class="el-input__icon el-icon-date"
                                      ></i>
                                      <!-- 自定义图标位置 -->
                                    </template>
                                  </el-date-picker>

                                  <!--<div
                                    style="
                                      width: 30px;
                                      height: 30px;
                                      margin-left: 10px;
                                    "
                                  ></div>-->
                                </div>

                                <div
                                  v-for="(
                                    filter, index3
                                  ) in chatItemInfo.filter"
                                  :key="index3"
                                  style="display: flex"
                                >
                                  <div class="queryfilterName">
                                    {{ filter.name }}
                                  </div>
                                  <div>
                                    <el-select
                                      placeholder="操作"
                                      v-model="filter.operator"
                                      style="width: 100px; border-radius: 0px"
                                      class="selectStyle"
                                      @change="operatorChange(filter)"
                                    >
                                      <el-option
                                        v-for="item in operatorEnum"
                                        :key="item.value"
                                        :label="item.name"
                                        :value="item.value"
                                      >
                                      </el-option>
                                    </el-select>
                                  </div>

                                  <!--按照操作符变化输入框和下拉框-->
                                  <div
                                    v-if="filter.operator <= 9"
                                    style="position: static"
                                  >
                                    <el-input
                                      v-model="filter.value"
                                      style="width: 150px; border-radius: 0px"
                                      class="myinput"
                                      placeholder="请输入值"
                                    >
                                      <template slot="suffix">
                                        <span
                                          class="clear-btn"
                                          @click="
                                            deleteFilter(index3, chatItemInfo)
                                          "
                                        >
                                          <span class="triangle">
                                            <span class="x-mark">×</span>
                                          </span>
                                        </span>
                                      </template>
                                    </el-input>
                                  </div>
                                  <!--<div
                                    v-if="
                                      filter.type == filterTypeEnum['dim'].value
                                    "
                                  >-->
                                  <div v-else style="position: static">
                                    <div>
                                      <el-select
                                        placeholder="请选择值"
                                        v-model="filter.value"
                                        style="width: 150px; border-radius: 0px"
                                        class="select-clear-Style"
                                        multiple
                                        collapse-tags
                                      >
                                        <template slot="prefix">
                                          <span
                                            class="clear-btn"
                                            style="background: transparent"
                                          >
                                            <span
                                              class="triangle"
                                              @click.stop="
                                                deleteFilter(
                                                  index3,
                                                  chatItemInfo
                                                )
                                              "
                                            >
                                              <span class="x-mark">×</span>
                                            </span>
                                          </span>
                                        </template>

                                        <el-option
                                          v-for="item in filter.diaplayValue"
                                          :key="item"
                                          :label="item"
                                          :value="item"
                                        >
                                        </el-option>
                                      </el-select>
                                    </div>
                                  </div>

                                  <!--<div style="margin-left: 10px">
                                    <el-button
                                      type="text"
                                      style="
                                        color: red;
                                        width: 30px;
                                        height: 30px;
                                        line-height: 0px;
                                      "
                                      @click="deleteFilter(index3, chatItemInfo)"
                                      >删除</el-button
                                    >
                                  </div>-->
                                </div>
                              </div>

                              <div style="padding: 5px 0px 0px 0px">
                                <el-button
                                  type="primary"
                                  width="100px"
                                  icon="el-icon-search"
                                  style="height: 30px; padding: 0px 20px"
                                  @click="getMetricsPreview(chatItemInfo)"
                                  >搜索</el-button
                                >
                              </div>
                            </div>
                          </div>

                          <div>
                            <el-dropdown
                              :ref="`filterVisible${index}${index1}${index2}`"
                              trigger="manual"
                              popper-append-to-body
                            >
                              <span>
                                <el-button
                                  size="mini"
                                  icon="el-icon-plus"
                                  style="
                                    border-radius: 50%;
                                    padding: 6px;
                                    height: 26px;
                                  "
                                  @click.stop="
                                    openFilter(
                                      `filterVisible${index}${index1}${index2}`,
                                      `${index}${index1}${index2}`
                                    )
                                  "
                                ></el-button>
                              </span>

                              <el-dropdown-menu slot="dropdown">
                                <div style="width: 250px; padding: 8px">
                                  <div
                                    style="padding: 0 0 0 10px; font-size: 12px"
                                  >
                                    添加筛选器
                                  </div>

                                  <div>
                                    <el-tabs
                                      :ref="`activeName${index}${index1}${index2}`"
                                      stretch
                                      style="width: 100%"
                                    >
                                      <el-tab-pane
                                        label="维度"
                                        :name="`first${index}${index1}${index2}`"
                                      >
                                        <div
                                          style="width: 100%; padding: 5px 10px"
                                        >
                                          <el-checkbox-group
                                            v-model="dimFilter"
                                          >
                                            <el-checkbox
                                              class="filterPanel"
                                              v-for="dim in chatItemInfo.other
                                                .dimList"
                                              :key="dim.id"
                                              :label="dim"
                                            >
                                              {{ dim.name }}
                                            </el-checkbox>
                                          </el-checkbox-group>
                                        </div>
                                      </el-tab-pane>

                                      <el-tab-pane
                                        label="指标"
                                        :name="`second${index}${index1}${index2}`"
                                      >
                                        <div
                                          style="width: 100%; padding: 5px 10px"
                                        >
                                          <el-checkbox-group
                                            v-model="metricFilter"
                                          >
                                            <el-checkbox
                                              class="filterPanel"
                                              v-for="mertic in chatItemInfo
                                                .other.merticList"
                                              :key="mertic.id"
                                              :label="mertic"
                                            >
                                              {{ mertic.name }}
                                            </el-checkbox>
                                          </el-checkbox-group>
                                        </div>
                                      </el-tab-pane>
                                    </el-tabs>
                                  </div>

                                  <div class="horizontal-line"></div>

                                  <div style="display: flex">
                                    <div
                                      class="one-bgdiv"
                                      style="
                                        padding: 0 5px 0px 0px;
                                        display: flex;
                                        justify-content: flex-end;
                                      "
                                    >
                                      <el-button
                                        type="primary"
                                        size="mini"
                                        @click.stop="
                                          sureFilter(
                                            `filterVisible${index}${index1}${index2}`,
                                            chatItemInfo
                                          )
                                        "
                                        >确定</el-button
                                      >
                                    </div>
                                  </div>
                                </div>
                              </el-dropdown-menu>
                            </el-dropdown>

                            <!--<el-dropdown>
                              <span>
                                <el-button
                                  size="mini"
                                  icon="el-icon-plus"
                                  style="border-radius: 50%; padding: 6px"
                                   @click.stop="openFilter"
                                ></el-button>
                              </span>

                              <el-dropdown-menu slot="dropdown">
                                <div style="width: 250px">
                                  <div
                                    style="padding: 0 0 0 10px; font-size: 12px"
                                  >
                                    添加筛选器
                                  </div>

                                  <div>
                                    <el-tabs
                                      v-model="activeName"
                                      stretch
                                      style="width: 100%"
                                    >
                                      <el-tab-pane label="维度" name="first">
                                        <div
                                          style="width: 100%; padding: 5px 10px"
                                        >
                                          <el-checkbox-group
                                            v-model="dimFilter"
                                          >
                                            <el-checkbox
                                              class="filterPanel"
                                              v-for="dim in chatItemInfo.other
                                                .dimList"
                                              :key="dim.id"
                                              :label="dim"
                                            >
                                              {{ dim.name }}
                                            </el-checkbox>
                                          </el-checkbox-group>
                                        </div>
                                      </el-tab-pane>

                                      <el-tab-pane label="指标" name="second">
                                        <div
                                          style="width: 100%; padding: 5px 10px"
                                        >
                                          <el-checkbox-group
                                            v-model="metricFilter"
                                          >
                                            <el-checkbox
                                              class="filterPanel"
                                              v-for="mertic in chatItemInfo
                                                .other.merticList"
                                              :key="mertic.id"
                                              :label="mertic"
                                            >
                                              {{ mertic.name }}
                                            </el-checkbox>
                                          </el-checkbox-group>
                                        </div>
                                      </el-tab-pane>
                                    </el-tabs>
                                  </div>

                                  <div style="display: flex">
                                    <div
                                      class="one-bgdiv"
                                      style="
                                        padding: 5px;
                                        display: flex;
                                        justify-content: flex-end;
                                      "
                                    >
                                      <el-button
                                        type="primary"
                                        size="mini"
                                        @click.stop="sureFilter(chatItemInfo)"
                                        >确定</el-button
                                      >
                                    </div>
                                  </div>
                                </div>
                              </el-dropdown-menu>
                            </el-dropdown>-->
                          </div>
                        </div>

                        <div class="drag-table">
                          <el-table
                            :data="chatItemInfo.data.records"
                            style="width: 100%"
                            border
                            stripe
                            class="query-tableBox"
                            v-loading="chatItemInfo.loading"
                            element-loading-text="加载中..."
                            element-loading-background="rgb(248 248 248 / 50%)"
                          >
                            <el-table-column
                              width="auto"
                              v-for="column in chatItemInfo.data.columns"
                              :key="column.key"
                              :prop="column.key"
                              :label="
                                column.unit
                                  ? column.name + '(' + column.unit + ')'
                                  : column.name
                              "
                              resizable
                              sortable
                              show-overflow-tooltip
                              :render-header="renderHeader"
                            ></el-table-column>
                          </el-table>

                          <pagination
                            v-show="chatItemInfo.data.total > 0"
                            :total="chatItemInfo.data.total"
                            :page.sync="chatItemInfo.data.page"
                            :limit.sync="chatItemInfo.data.pageSize"
                            @pagination="getMetricsPreview(chatItemInfo)"
                            style="padding: 10px"
                          />
                        </div>
                      </div>
                    </el-collapse-item>
                  </el-collapse>
                </div>

                <div v-if="chatItemInfo.stepType == 'compute'">
                  <el-collapse class="aiCollapse">
                    <el-collapse-item
                      class="aiCollapse"
                      :name="`compute${groupChatItem.chatId}`"
                    >
                      <span style="width: 100%" slot="title">
                        <div style="display: flex; align-items: center">
                          <div class="aiTitleNo">
                            {{ chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div
                            class="aiTitleType"
                            style="
                              background: rgb(219, 240, 252);
                              color: rgb(0, 126, 172);
                              min-width: 46px;
                            "
                          >
                            计算
                          </div>
                          &nbsp;&nbsp;
                          <div class="title">{{ chatItemInfo.title }}</div>
                        </div>
                      </span>

                      <div style="padding: 10px" class="drag-table">
                        <el-table
                          :data="chatItemInfo.data.records"
                          style="width: 100%"
                          border
                          stripe
                          class="compute-tableBox"
                        >
                          <el-table-column
                            width="auto"
                            v-for="column in chatItemInfo.data.columns"
                            :key="column.name"
                            :prop="column.name"
                            :label="
                              column.unit
                                ? column.name + '(' + column.unit + ')'
                                : column.name
                            "
                            resizable
                            sortable
                            show-overflow-tooltip
                            :render-header="renderHeader"
                          ></el-table-column>
                        </el-table>
                      </div>
                    </el-collapse-item>
                  </el-collapse>
                </div>

                <div v-if="chatItemInfo.stepType == 'analyze'">
                  <el-collapse class="aiCollapse">
                    <el-collapse-item
                      class="aiCollapse"
                      :name="`analyze${groupChatItem.chatId}`"
                    >
                      <span style="width: 100%" slot="title">
                        <div style="display: flex; align-items: center">
                          <div class="aiTitleNo">
                            {{ chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div
                            class="aiTitleType"
                            style="
                              background: rgb(216 235 246)
                              color: rgb(0, 126, 172);
                                  min-width: 46px;
                            "
                          >
                            分析
                          </div>
                          &nbsp;&nbsp;
                          <div class="title">{{ chatItemInfo.title }}</div>
                        </div>
                      </span>

                      <div style="padding: 10px">
                        <el-collapse
                          class="aiAnalysisCollapse"
                          style="margin-top: 10px"
                          v-for="record in chatItemInfo.analyzeData"
                          :key="record.id"
                        >
                          <el-collapse-item
                            class="aiAnalysisCollapse"
                            :name="`analysis${record.title}`"
                          >
                            <span style="width: 100%" slot="title">
                              <div class="title">
                                {{ record.title }}
                              </div>
                            </span>
                            <div style="padding: 10px">
                              <div
                                style="
                                  background: rgb(239 250 252);
                                  padding: 10px;
                                  border-radius: 10px;
                                "
                              >
                                <markdown-it-vue
                                  :content="record.analysisResult"
                                ></markdown-it-vue>
                              </div>
                            </div>
                          </el-collapse-item>
                        </el-collapse>
                        <!--<el-table
                          :data="chatItemInfo.data.records"
                          style="width: 100%"
                          border
                          stripe
                          class="compute-tableBox"
                        >
                          <el-table-column

                            width="auto"
                            v-for="column in chatItemInfo.data.columns"
                            :key="column.name"
                            :prop="column.name"
                            :label="column.name"
                            resizable
                            sortable
                          ></el-table-column>
                        </el-table>-->
                      </div>
                    </el-collapse-item>
                  </el-collapse>
                </div>

                <div v-if="chatItemInfo.stepType == 'summarize'">
                  <el-collapse
                    class="aiCollapse"
                    :value="[`summarize${groupChatItem.chatId}`]"
                  >
                    <el-collapse-item
                      class="aiCollapse"
                      :name="`summarize${groupChatItem.chatId}`"
                    >
                      <span style="width: 100%" slot="title">
                        <div style="display: flex; align-items: center">
                          <div class="aiTitleNo">
                            {{ chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div
                            class="aiTitleType"
                            style="
                              color: rgb(4, 120, 87);
                              background: linear-gradient(
                                135deg,
                                #eff6ff,
                                #f0fdfa
                              );
                              min-width: 46px;
                            "
                          >
                            总结
                          </div>
                          &nbsp;&nbsp;
                          <div class="title">{{ chatItemInfo.title }}</div>
                        </div>
                      </span>

                      <div>
                        <div style="padding: 10px">
                          <div
                            style="
                              padding: 14px 16px;
                              background: linear-gradient(
                                135deg,
                                #eff6ff,
                                #f0fdfa
                              );
                              border: 1px solid #bae6fd;
                              border-radius: 10px;
                              font-size: 14px;
                              line-height: 1.8;
                              color: rgb(71, 85, 105);
                            "
                          >
                            {{ chatItemInfo.answer }}
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

      <div v-if="!resultReady" style="margin-top: 20px">
        <div style="margin-top: 20px">
          <div
            style="display: flex; margin-top: 20px; justify-content: flex-end"
          >
            <div class="userPanel">
              {{ showQueryString }}
            </div>

            <div
              style="text-align: right; margin-left: 10px; margin-right: 10px"
            >
              <!--<el-avatar size="medium" icon="el-icon-user-solid"></el-avatar>-->
              <el-avatar
                :size="32"
                :style="{ backgroundColor: '#0073FF', color: 'white' }"
              >
                {{ avatarText }}
              </el-avatar>
            </div>
          </div>
        </div>

        <div style="margin-top: 20px">
          <div
            style="
              text-align: left;
              margin-left: 10px;
              display: flex;
              align-items: center;
              margin-bottom: 10px;
            "
          >
            <div style="display: flex; align-items: center">
              <img
                class="agent-sidebar__logo"
                src="@/assets/svgs/logo.svg"
                alt=""
              />
            </div>

            <div>{{ selectedAgent.name }}</div>
          </div>

          <div class="aiPanel">
            <div style="padding: 10px">
              <el-collapse class="aiDisableCollapse" :value="['thinking']">
                <el-collapse-item class="aiDisableCollapse" name="thinking">
                  <span slot="title"> 思考中... </span>
                  <div>
                    <div style="padding: 10px" class="think">
                      <markdown-it-vue
                        :content="streamingThinking"
                      ></markdown-it-vue>
                    </div>

                    <div
                      class="custom-loading"
                      style="width: 100px; height: 30px; margin-left: 10px"
                      v-loading="loading"
                      element-loading-text="思考中"
                    ></div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      style="
        background: transparent;
        display: flex;
        width: 100%;
        justify-content: center;
        margin-bottom: 15px;
      "
    >
      <div
        :style="
          isNewDialog
            ? `background: transparent; height: 100%;display: flex;
    justify-content: center;flex-direction: column;width: 80%;min-height: 122px;max-height:122px;`
            : `background: transparent; height: 100%;display: flex;
    justify-content: center;flex-direction: column;width: 95%;margin-bottom: 15px;min-height: 122px;max-height:122px;`
        "
        class="aiInput"
      >
        <div style="width: 100%">
          <el-input
            placeholder="请输入您的问题,如:资产质量情况怎么样?"
            v-model="queryString"
            type="textarea"
            resize="none"
            class="aiInput-textarea"
            :disabled="chatLoading"
            @keyup.enter.native="handleEnter"
          >
          </el-input>
        </div>
        <div
          class="aiInput-bottom"
          style="display: flex; justify-content: flex-end"
        >
          <div style="margin-bottom: 10px">
            <el-button
              :disabled="chatLoading"
              style="font-size: 14px; padding: 10px; border-radius: 10px"
              type="primary"
              icon="el-icon-s-promotion"
              @click="handleEnter"
            ></el-button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isNewDialog" style="height: 40%"></div>

    <el-dialog
      :show-close="false"
      :close-on-click-modal="false"
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
          {{ viewSql }}
        </div>
      </div>

      <div class="horizontal-line"></div>

      <div style="margin-top: 10px"></div>

      <div style="display: flex">
        <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
          <el-button @click="isSqlPage = false">关闭</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import {
  chartTypeEnum,
  granularityEnum,
  getMetricsTreeAPI,
  getMetricsDataPreviewAPI,
  operatorEnum,
  filterTypeEnum,
} from "@/api/metricDataPreview/metricPreviewAPI.js";

import { getUserInfo } from "@/utils/auth";

import { sendChat, getChatInfo } from "@/api/smartQuery/smartQueryAPI.js";
import { connectChatWebSocket } from "@/views/smartQuery/utils/chatWebSocket.js";

export default {
  name: "queryPage",
  props: [],
  components: {},
  data() {
    return {
      dimFilter: [],
      metricFilter: [],

      userInfo: getUserInfo(),
      avatarText: "用户",

      loading: true,

      chartTypeEnum,
      granularityEnum,
      operatorEnum,
      filterTypeEnum,

      isNewDialog: true, //是否是新对话

      selectedAgent: { name: "", code: "" }, //当前agent
      chatSessionId: null, //对话ID

      queryString: "", //查询字符串
      showQueryString: "", //用户得显示字符串
      streamingThinking: "", //思考流

      wsShouldFetchOnClose: null,
      resultReady: true, //结果是否OK
      chatLoading: false, //chat是否正在运行

      isSqlPage: false, //显示sql页
      viewSql: "", //sql页内容

      agentList: [], //主要对话列表

      dimensionsData: [], //维度数据
      metricsData: [], //指标数据

      groupChatItem: {
        chatId: "",
        type: "", //user和ai

        chatItemInfo: [
          {
            stepType: "", //think,query,compute,analyze,summarize   user类型没有这个
            title: "",

            think: "", //思维过程文本，think
            chartType: 1,
            //query
            data: {
              //数据表
              records: [],
              columns: [],
              page: 1,
              pageSize: 10,
              total: 0,
            },
            candidate: {
              dimList: [{ id: "", name: "", check: "" }],
              merticList: [{ id: "", name: "", check: "" }],
            },
            other: {
              //维度，指标候选
              dimList: [{ id: "", name: "", check: "" }],
              merticList: [{ id: "", name: "", check: "" }],
            },
            dataRange: [], //时间筛选
            dateGranularity: "day",
            filter: [
              {
                type: "", //指标还是维度 用于判断显示什么控件
                name: "",
                operator: "",
                value: "",
                diaplayValue: "", //当类型是维度时，需要选择
                key: "",
              },
            ],

            viewSql: "",

            data: {
              //表格 compute
              rows: [],
              columns: [],
            },
            answer: "", //回答 summarize
          },
        ],
      },
    };
  },

  mounted() {
    //await this.getmetricTreeList();
    //this.isNew = false;
    //this.getChatHistoryListDetail();
    this.avatarText = this.userInfo.name.charAt(0).toUpperCase();
  },

  methods: {
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

    operatorChange(filter) {
      //通过filter.value的类型判断，以保留当前值，只有切换类型时，值为空
      if (filter.operator > 9) {
        if (typeof filter.value != "object") {
          filter.value = [];
        }
      } else {
        if (typeof filter.value != "string") {
          filter.value = "";
        }
      }
    },

    openFilter(name, tabName) {
      //this.$refs[`activeName${tabName}`][0].setCurrentName(`first${tabName}`);

      if (
        this.$refs[`activeName${tabName}`] &&
        this.$refs[`activeName${tabName}`][0].setCurrentName
      ) {
        this.$refs[`activeName${tabName}`][0].setCurrentName(`first${tabName}`);
      }

      if (this.$refs[name] && this.$refs[name][0].show) {
        this.$refs[name][0].show();
      }

      this.dimFilter = [];
      this.metricFilter = [];
    },

    sureFilter(name, chatItemInfo) {
      for (let i = 0; i < this.dimFilter.length; i++) {
        let dim = this.dimFilter[i];

        let filter = {};
        filter.type = filterTypeEnum["dim"].value; //维度类型为0
        filter.name = dim.name;
        filter.key = dim.key;
        filter.value = dim.value || null;
        filter.operator = dim.operator || null;

        let diaplayValueList = [];
        for (let l = 0; l < chatItemInfo.data.records.length; l++) {
          if (
            diaplayValueList.findIndex(
              (item) => item == chatItemInfo.data.records[l][filter.key]
            ) < 0
          ) {
            diaplayValueList.push(chatItemInfo.data.records[l][filter.key]);
          }
        }
        filter.diaplayValue = diaplayValueList;

        if (filter.diaplayValue.length > 0)
          filter.value = filter.diaplayValue[0];

        chatItemInfo.filter.push(filter);
      }
      for (let i = 0; i < this.metricFilter.length; i++) {
        let metric = this.metricFilter[i];
        let filter = {};
        filter.type = filterTypeEnum["metric"].value; //指标类型为1
        filter.name = metric.name;
        filter.key = metric.key;
        filter.value = metric.value || null;
        filter.operator = metric.operator || null;

        let diaplayValueList = [];
        for (let l = 0; l < chatItemInfo.data.records.length; l++) {
          if (
            diaplayValueList.findIndex(
              (item) => item == chatItemInfo.data.records[l][filter.key]
            ) < 0
          ) {
            diaplayValueList.push(chatItemInfo.data.records[l][filter.key]);
          }
        }
        filter.diaplayValue = diaplayValueList;

        if (filter.diaplayValue.length > 0) {
          filter.value = filter.diaplayValue[0];
          //filter.multipleValue = [filter.diaplayValue[0]];
        }

        chatItemInfo.filter.push(filter);
      }

      if (this.$refs[name] && this.$refs[name][0].show) {
        this.$refs[name][0].hide();
      }
    },

    deleteFilter(index, chatItemInfo) {
      chatItemInfo.filter.splice(index, 1);
    },

    //日期格式化，用于下载文件的尾部
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
    //下载文件
    downFile(chatItemInfo) {
      let tempQuery = {
        dimList: [],
        indexList: [],
        filters: [],
        timeRange: { start: null, end: null },
      };
      tempQuery.downloadFlag = 1;
      for (let i = 0; i < chatItemInfo.other.dimList.length; i++) {
        let dim = {};
        dim.dimKey = chatItemInfo.other.dimList[i].key;
        dim.dimName = chatItemInfo.other.dimList[i].name;
        dim.id = chatItemInfo.other.dimList[i].id;
        tempQuery.dimList.push(dim);
      }
      for (let i = 0; i < chatItemInfo.other.merticList.length; i++) {
        let mertic = {};
        mertic.indKey = chatItemInfo.other.merticList[i].key;
        mertic.indName = chatItemInfo.other.merticList[i].name;
        mertic.id = chatItemInfo.other.merticList[i].id;
        tempQuery.indexList.push(mertic);
      }

      if (tempQuery.dimList.length == 0 && tempQuery.indexList.length == 0) {
        this.$message({
          message: "请选择指标或维度",
          type: "error",
          duration: this.$messageDuration,
        });
        chatItemInfo.data.total = 0;
        return;
      }

      for (let i = 0; i < chatItemInfo.filter.length; i++) {
        let filterItem = {
          filterField: {
            fieldClazz: chatItemInfo.filter[i].type,
            name: chatItemInfo.filter[i].name,
            key: chatItemInfo.filter[i].key,
          },
          filterValue: chatItemInfo.filter[i].value,
          operator: chatItemInfo.filter[i].operator,
        };
        tempQuery.filters.push(filterItem);
      }

      tempQuery.page = chatItemInfo.data.page;
      tempQuery.pageSize = chatItemInfo.data.pageSize;
      tempQuery.total = chatItemInfo.data.total;

      if (chatItemInfo.hasOwnProperty("dataRange")) {
        if (chatItemInfo.dataRange != null) {
          tempQuery.timeRange.start = chatItemInfo.dataRange[0];
          tempQuery.timeRange.end = chatItemInfo.dataRange[1];
        } else {
          tempQuery.timeRange = null;
        }
      } else {
        tempQuery.timeRange = null;
      }
      tempQuery.dateGranularity = chatItemInfo.dateGranularity;

      this.download(
        "/api/v1/chat-server/getdata",
        tempQuery,
        `数据导出_${this.formatDate(new Date())}.xlsx`
      );
    },

    showSQL(viewSql) {
      //this.viewSql = viewSql
      this.viewSql = this.formatSQL(viewSql);
      this.isSqlPage = true;
    },

    //sql字符串格式化
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

    //显示历史
    setHistory(agent, histoyList) {
      this.rest();
      this.isNewDialog = false;
      this.selectedAgent = agent;
      this.chatSessionId = histoyList.chatSessionId;

      for (let i = 0; i < histoyList.chatInfo.length; i++) {
        this.agentList.push(this.praseAnswer(histoyList.chatInfo[i]));
      }
      this.resultReady = true;

      this.scrollToBottom();
    },

    setSelectedAgent(agent) {
      this.rest();
      this.selectedAgent = agent;
    },

    rest() {
      this.agentList = [];

      this.isNewDialog = true;

      this.selectedAgent = null;
      this.chatSessionId = null;

      this.queryString = "";
      this.showQueryString = "";
      this.streamingThinking = "";

      this.resultReady = true;
      this.chatLoading = false;
      this.closeChatWebSocket();
    },

    selectDim(val, dim, chatItemInfo) {
      //选择维度
      if (val) {
        let filter = {};
        filter.type = filterTypeEnum["dim"].value; //维度类型为0
        filter.name = dim.name;
        filter.key = dim.key;
        filter.value = dim.value || null;
        filter.operator = dim.operator || null;

        let diaplayValueList = [];
        for (let l = 0; l < chatItemInfo.data.records.length; l++) {
          if (
            diaplayValueList.findIndex(
              (item) => item == chatItemInfo.data.records[l][filter.key]
            ) < 0
          ) {
            diaplayValueList.push(chatItemInfo.data.records[l][filter.key]);
          }
        }
        filter.diaplayValue = diaplayValueList;

        if (filter.diaplayValue.length > 0)
          filter.value = filter.diaplayValue[0];

        chatItemInfo.filter.push(filter);
      } else {
        let index = chatItemInfo.filter.findIndex(
          (item) => item.key == dim.key
        );
        if (index > -1) {
          chatItemInfo.filter.splice(index, 1);
        }
      }
    },

    deleteDim(event, dim, chatItemInfo) {
      //删除维度
      this.selectDim(false, dim, chatItemInfo);

      let index = chatItemInfo.other.dimList.findIndex(
        (item) => item.key == dim.key
      );
      if (index > -1) {
        chatItemInfo.other.dimList.splice(index, 1);

        //添加删除，重置为第1页
        chatItemInfo.data.page = 1;
        this.getMetricsPreview(chatItemInfo);
        this.getMetricTreeList(chatItemInfo);
      }
    },

    handleCommandDims(val, chatItemInfo) {
      //添加维度
      if (val == null) return;

      let dim = { id: val.id, key: val.key, name: val.name, check: false };

      let index = chatItemInfo.other.dimList.findIndex(
        (item) => item.key == val.key
      );
      if (index < 0) {
        chatItemInfo.other.dimList.push(dim);

        //添加删除，重置为第1页
        chatItemInfo.data.page = 1;
        this.getMetricsPreview(chatItemInfo);
        this.getMetricTreeList(chatItemInfo);
      }
    },

    selectMetric(val, metric, chatItemInfo) {
      //选择指标
      if (val) {
        let filter = {};
        filter.type = filterTypeEnum["metric"].value; //指标类型为1
        filter.name = metric.name;
        filter.key = metric.key;
        filter.value = metric.value || null;
        filter.operator = metric.operator || null;

        chatItemInfo.filter.push(filter);
      } else {
        let index = chatItemInfo.filter.findIndex(
          (item) => item.key == metric.key
        );
        if (index > -1) {
          chatItemInfo.filter.splice(index, 1);
        }
      }
    },

    deleteMetric(event, metric, chatItemInfo) {
      //删除指标
      this.selectMetric(false, metric, chatItemInfo);

      let index = chatItemInfo.other.merticList.findIndex(
        (item) => item.key == metric.key
      );
      if (index > -1) {
        chatItemInfo.other.merticList.splice(index, 1);

        //添加删除，重置为第1页
        chatItemInfo.data.page = 1;
        this.getMetricsPreview(chatItemInfo);
        this.getMetricTreeList(chatItemInfo);
      }
    },

    handleCommandMetrics(val, chatItemInfo) {
      //添加指标
      if (val == null) return;
      let metric = { id: val.id, key: val.key, name: val.name, check: false };

      let index = chatItemInfo.other.merticList.findIndex(
        (item) => item.key == val.key
      );
      if (index < 0) {
        chatItemInfo.other.merticList.push(metric);

        //添加删除，重置为第1页
        chatItemInfo.data.page = 1;
        this.getMetricsPreview(chatItemInfo);
        this.getMetricTreeList(chatItemInfo);
      }
    },

    //获取数据预览
    getMetricsPreview(chatItemInfo) {
      //要注意下filter.value 不同操作符的值不一样，一个是[],一个是''
      let tempQuery = {
        dimList: [],
        indexList: [],
        filters: [],
        timeRange: { start: null, end: null },
      };
      tempQuery.downloadFlag = 0;
      for (let i = 0; i < chatItemInfo.other.dimList.length; i++) {
        let dim = {};
        dim.dimKey = chatItemInfo.other.dimList[i].key;
        dim.dimName = chatItemInfo.other.dimList[i].name;
        dim.id = chatItemInfo.other.dimList[i].id;
        tempQuery.dimList.push(dim);
      }
      for (let i = 0; i < chatItemInfo.other.merticList.length; i++) {
        let mertic = {};
        mertic.indKey = chatItemInfo.other.merticList[i].key;
        mertic.indName = chatItemInfo.other.merticList[i].name;
        mertic.id = chatItemInfo.other.merticList[i].id;
        tempQuery.indexList.push(mertic);
      }

      if (tempQuery.dimList.length == 0 && tempQuery.indexList.length == 0) {
        this.$message({
          message: "请选择指标或维度",
          type: "error",
          duration: this.$messageDuration,
        });
        chatItemInfo.data.total = 0;
        return;
      }

      for (let i = 0; i < chatItemInfo.filter.length; i++) {
        let filterItem = {
          filterField: {
            fieldClazz: chatItemInfo.filter[i].type,
            name: chatItemInfo.filter[i].name,
            key: chatItemInfo.filter[i].key,
          },
          filterValue: chatItemInfo.filter[i].value,
          operator: chatItemInfo.filter[i].operator,
        };
        tempQuery.filters.push(filterItem);
      }

      tempQuery.page = chatItemInfo.data.page;
      tempQuery.pageSize = chatItemInfo.data.pageSize;
      tempQuery.total = chatItemInfo.data.total;

      if (chatItemInfo.hasOwnProperty("dataRange")) {
        if (chatItemInfo.dataRange != null) {
          tempQuery.timeRange.start = chatItemInfo.dataRange[0];
          tempQuery.timeRange.end = chatItemInfo.dataRange[1];
        } else {
          tempQuery.timeRange = null;
        }
      } else {
        tempQuery.timeRange = null;
      }
      tempQuery.dateGranularity = chatItemInfo.dateGranularity;

      //目前还不支持
      //tempQuery.chartType = chatItemInfo.chartType;
      //const loading = this.loadingScreen();
      chatItemInfo.loading = true;
      getMetricsDataPreviewAPI(tempQuery)
        .then((response) => {
          if (response.code == 200) {
            chatItemInfo.data.columns = [];
            chatItemInfo.data.records = [];
            chatItemInfo.viewSql = "";

            chatItemInfo.data.page = response.data.page;
            chatItemInfo.data.pageSize = response.data.pageSize;
            chatItemInfo.data.total = response.data.total;

            chatItemInfo.data.columns = response.data.columns;
            chatItemInfo.data.records = response.data.records;
            chatItemInfo.viewSql = response.data.sql;
          } else {
            chatItemInfo.data.total = 0;

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
          chatItemInfo.loading = false;
        });
    },

    //展现形式改变
    handleCommandChartType(val, chatItemInfo) {
      chatItemInfo.chartType = val;
    },

    getMetricTreeList(chatItemInfo) {
      let metricIds = [];
      let dimensionIds = [];

      if (
        chatItemInfo != null &&
        chatItemInfo.hasOwnProperty("other") &&
        chatItemInfo.other.hasOwnProperty("merticList") &&
        chatItemInfo.other.hasOwnProperty("dimList")
      ) {
        for (let i = 0; i < chatItemInfo.other.merticList.length; i++) {
          metricIds.push(chatItemInfo.other.merticList[i].id);
        }

        for (let i = 0; i < chatItemInfo.other.dimList.length; i++) {
          dimensionIds.push(chatItemInfo.other.dimList[i].id);
        }
      }

      let dimmensionTreeParams = {
        type: "dim",
        metricIds: metricIds,
        dimensionIds: dimensionIds,
      };

      //let loading = this.loadingScreen();
      getMetricsTreeAPI(dimmensionTreeParams)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              chatItemInfo.candidate.dimList = [];
              //this.dimensionsData = response.data;
              chatItemInfo.candidate.dimList = Object.assign([], response.data);
            }
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

      //loading = this.loadingScreen();
      let metricsTreeParams = {
        type: "metric",
        metricIds: metricIds,
        dimensionIds: dimensionIds,
      };
      getMetricsTreeAPI(metricsTreeParams)
        .then((response) => {
          if (response.code == 200) {
            if (response.data != null) {
              chatItemInfo.candidate.merticList = [];
              //this.metricsData = response.data;
              chatItemInfo.candidate.merticList = Object.assign(
                [],
                response.data
              );
            }
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

    //要将chatInfo重新组织，按类型，填充值
    praseAnswer(chatInfo) {
      let oneDialog = [];

      let groupChatItem = {};
      groupChatItem.chatItemInfo = [];

      let lastType = "";
      let think = null;

      for (let j = 0; j < chatInfo.chatItemInfo.length; j++) {
        groupChatItem.chatId = chatInfo.chatId;

        const chatItemInfo = chatInfo.chatItemInfo[j];
        let obj = {};
        obj.loading = false;
        const type = chatItemInfo.type;
        const stepType = chatItemInfo.stepType;

        if (type == "user") {
          //用户，只拿标题
          obj.title = chatItemInfo.question;
        } else if (type == "ai") {
          think = chatItemInfo.think;
          obj.itemType = chatItemInfo.itemId;
          if (stepType == "query") {
            obj.stepType = stepType;

            obj.title = chatItemInfo.question;
            if (chatItemInfo.chartData.dataVO.code != 200) {
              this.$message({
                message: "数据返回错误",
                type: "error",
                duration: this.$messageDuration,
              });
              continue;
            }

            obj.data = {};
            if (chatItemInfo.chartData.dataVO.hasOwnProperty("data")) {
              const firstRecodes =
                chatItemInfo.chartData.dataVO.data.records.splice(
                  0,
                  Math.min(
                    chatItemInfo.chartData.dataVO.data.records.length,
                    10
                  )
                );
              /*this.$set(
                obj.data,
                "records",
                chatItemInfo.chartData.dataVO.data.records
              );*/

              this.$set(obj.data, "records", firstRecodes);

              this.$set(
                obj.data,
                "columns",
                chatItemInfo.chartData.dataVO.data.columns
              );
              this.$set(obj.data, "page", 1);
              this.$set(obj.data, "pageSize", 10);
              this.$set(
                obj.data,
                "total",
                chatItemInfo.chartData.dataVO.data.total
              );

              /*this.$set(
                obj.data,
                "page",
                chatItemInfo.chartData.dataVO.data.page
              );
                            this.$set(
                obj.data,
                "pageSize",
                chatItemInfo.chartData.dataVO.data.pageSize
              );
               this.$set(
                obj.data,
                "total",
                chatItemInfo.chartData.dataVO.data.total
              );*/
            }
            //所有的，用于展示选择
            obj.candidate = { merticList: [], dimList: [] };
            //obj.candidate.merticList = Object.assign([], this.metricsData);
            //obj.candidate.dimList = Object.assign([], this.dimensionsData);

            //加属性值判断
            if (chatItemInfo.chartData.dataVO.data.hasOwnProperty("sql")) {
              obj.viewSql = chatItemInfo.chartData.dataVO.data.sql;
            }

            obj.chartType = chatItemInfo.chartData.dataRequestDTO.chartType;

            if (
              chatItemInfo.chartData.dataRequestDTO.hasOwnProperty("timeRange")
            ) {
              obj.dataRange = [
                chatItemInfo.chartData.dataRequestDTO.timeRange.start,
                chatItemInfo.chartData.dataRequestDTO.timeRange.end,
              ];
            }
            obj.dateGranularity =
              chatItemInfo.chartData.dataRequestDTO.dateGranularity;

            obj.other = { merticList: [], dimList: [] };
            //添加目前界面上应该显示的指标和维度，有filter的情况下，在filter里直接处理，没在filter中的在这里处理
            for (let k = 0; k < obj.data.columns.length; k++) {
              //在筛选里找，筛选器里有的，已经添加，没有的则单独添加
              let dimIndex = obj.other.dimList.findIndex(
                (item) => item.key == obj.data.columns[k].key
              );
              let merticIndex = obj.other.merticList.findIndex(
                (item) => item.key == obj.data.columns[k].key
              );

              if (dimIndex < 0 && merticIndex < 0) {
                //let index = obj.candidate.merticList.findIndex(
                //  (item) => item.key == obj.data.columns[k].key
                //);

                let index =
                  chatItemInfo.chartData.dataRequestDTO.indexList.findIndex(
                    (item) => item.indKey == obj.data.columns[k].key
                  );

                if (index > -1) {
                  let other = {
                    id: chatItemInfo.chartData.dataRequestDTO.indexList[index]
                      .id,
                    key: obj.data.columns[k].key,
                    name: obj.data.columns[k].name,
                    operator: "",
                    value: "",
                    diaplayValue: "",
                    check: false,
                  };
                  obj.other.merticList.push(other);
                }
                //index = obj.candidate.dimList.findIndex(
                //  (item) => item.key == obj.data.columns[k].key
                //);
                //因为有显示的值，所以取行里找
                index = chatItemInfo.chartData.dataRequestDTO.dimList.findIndex(
                  (item) => item.dimKey == obj.data.columns[k].key
                );
                if (index > -1) {
                  let diaplayValueList = [];
                  for (let l = 0; l < obj.data.records.length; l++) {
                    if (
                      diaplayValueList.findIndex(
                        (item) =>
                          item == obj.data.records[l][obj.data.columns[k].key]
                      ) < 0
                    ) {
                      diaplayValueList.push(
                        obj.data.records[l][obj.data.columns[k].key]
                      );
                    }
                  }

                  let other = {
                    id: chatItemInfo.chartData.dataRequestDTO.dimList[index].id,
                    key: obj.data.columns[k].key,
                    name: obj.data.columns[k].name,
                    operator: "",
                    value: "",
                    diaplayValue: diaplayValueList,
                    check: false,
                  };
                  obj.other.dimList.push(other);
                }
              }
            }

            obj.filter = [];
            if (
              chatItemInfo.chartData.dataRequestDTO.hasOwnProperty("filters")
            ) {
              for (
                let k = 0;
                k < chatItemInfo.chartData.dataRequestDTO.filters.length;
                k++
              ) {
                let filter = {};
                filter.type =
                  chatItemInfo.chartData.dataRequestDTO.filters[
                    k
                  ].filterField.fieldClazz; //0是维度
                filter.name =
                  chatItemInfo.chartData.dataRequestDTO.filters[
                    k
                  ].filterField.name;
                filter.key =
                  chatItemInfo.chartData.dataRequestDTO.filters[
                    k
                  ].filterField.key;
                filter.value =
                  chatItemInfo.chartData.dataRequestDTO.filters[k].filterValue;
                filter.operator =
                  chatItemInfo.chartData.dataRequestDTO.filters[k].operator;

                //if (filter.type == filterTypeEnum["dim"].value) {
                //维度是0，1是指标
                let diaplayValueList = [];
                for (let l = 0; l < obj.data.records.length; l++) {
                  if (
                    diaplayValueList.findIndex(
                      (item) => item == obj.data.records[l][filter.key]
                    ) < 0
                  ) {
                    diaplayValueList.push(obj.data.records[l][filter.key]);
                  }
                }
                filter.diaplayValue = diaplayValueList;

                //}

                obj.filter.push(filter);

                let index = obj.other.dimList.findIndex(
                  (item) => item.key == filter.key
                );
                if (index > -1) {
                  obj.other.dimList[index].check = true;
                }
                index = obj.other.merticList.findIndex(
                  (item) => item.key == filter.key
                );
                if (index > -1) {
                  obj.other.merticList[index].check = true;
                }

                /*let id = null;
                let index = obj.data.columns.findIndex(
                  (item) => item.key == filter.key
                );
                if (index > -1) {
                  id = obj.data.columns[index].id;
                }

                let other = {
                  id: id,
                  key: filter.key,
                  name: filter.name,
                  operator: filter.operator,
                  value: filter.value,
                  diaplayValue: filter.diaplayValue,
                  check: true,
                };


                if (filter.type == filterTypeEnum["metric"].value) {
                  //指标
                  obj.other.merticList.push(other);
                }
                if (filter.type == filterTypeEnum["dim"].value) {
                  //维度
                  obj.other.dimList.push(other);
                }*/
              }
            }
            //添加目前界面上应该显示的指标和维度，有filter的情况下，在filter里直接处理，没在filter中的在这里处理
            /*for (let k = 0; k < obj.data.columns.length; k++) {
              //在筛选里找，筛选器里有的，已经添加，没有的则单独添加
              let dimIndex = obj.other.dimList.findIndex(
                (item) => item.key == obj.data.columns[k].key
              );
              let merticIndex = obj.other.merticList.findIndex(
                (item) => item.key == obj.data.columns[k].key
              );

              if (dimIndex < 0 && merticIndex < 0) {
                //let index = obj.candidate.merticList.findIndex(
                //  (item) => item.key == obj.data.columns[k].key
                //);

                let index =
                  chatItemInfo.chartData.dataRequestDTO.indexList.findIndex(
                    (item) => item.indKey == obj.data.columns[k].key
                  );

                if (index > -1) {
                  let other = {
                    id: chatItemInfo.chartData.dataRequestDTO.indexList[index]
                      .id,
                    key: obj.data.columns[k].key,
                    name: obj.data.columns[k].name,
                    operator: "",
                    value: "",
                    diaplayValue: "",
                    check: false,
                  };
                  obj.other.merticList.push(other);
                }
                //index = obj.candidate.dimList.findIndex(
                //  (item) => item.key == obj.data.columns[k].key
                //);
                //因为有显示的值，所以取行里找
                index = chatItemInfo.chartData.dataRequestDTO.dimList.findIndex(
                  (item) => item.dimKey == obj.data.columns[k].key
                );
                if (index > -1) {
                  let diaplayValueList = [];
                  for (let l = 0; l < obj.data.records.length; l++) {
                    if (
                      diaplayValueList.findIndex(
                        (item) =>
                          item == obj.data.records[l][obj.data.columns[k].key]
                      ) < 0
                    ) {
                      diaplayValueList.push(
                        obj.data.records[l][obj.data.columns[k].key]
                      );
                    }
                  }

                  let other = {
                    id: chatItemInfo.chartData.dataRequestDTO.dimList[index].id,
                    key: obj.data.columns[k].key,
                    name: obj.data.columns[k].name,
                    operator: "",
                    value: "",
                    diaplayValue: diaplayValueList,
                    check: false,
                  };
                  obj.other.dimList.push(other);
                }
              }
            }*/

            //需要按需求重新获取指标维度
            this.getMetricTreeList(obj);
            //为了分页功能，需要调取下
            //this.getMetricsPreview(obj);
          } else if (stepType == "compute") {
            obj.data = {};
            //计算的话，拿四个
            obj.stepType = stepType;
            obj.title = chatItemInfo.question;
            this.$set(obj.data, "records", chatItemInfo.chartData.dataVO.rows);
            this.$set(
              obj.data,
              "columns",
              chatItemInfo.chartData.dataVO.columns
            );

            //obj.data.records = chatItemInfo.chartData.dataVO.rows;
            //obj.data.columns = chatItemInfo.chartData.dataVO.columns;
          } else if (stepType == "analyze") {
            //obj.data = {};
            //计算的话，拿四个
            obj.stepType = stepType;
            obj.title = chatItemInfo.question;
            obj.analyzeData = [];

            let entityList = chatItemInfo.chartData.dataVO.columns.filter(
              (item) => item.name == "entity"
            );
            let resultList = chatItemInfo.chartData.dataVO.columns.filter(
              (item) => item.name == "analysis_result"
            );
            if (entityList.length > 0 && resultList.length > 0) {
              for (
                let i = 0;
                i < chatItemInfo.chartData.dataVO.rows.length;
                i++
              ) {
                let temp = {
                  title: chatItemInfo.chartData.dataVO.rows[i]["entity"],
                  analysisResult:
                    chatItemInfo.chartData.dataVO.rows[i]["analysis_result"],
                };
                obj.analyzeData.push(temp);
              }
            } else {
              this.$message({
                message: "数据返回错误",
                type: "error",
                duration: this.$messageDuration,
              });
            }
          } else if (stepType == "summarize") {
            //总结的话，拿三个东西
            obj.stepType = stepType;
            obj.title = chatItemInfo.question;
            obj.answer = chatItemInfo.chartData.dataVO.rows[0].answer; //固定位置
          }
        }

        if (lastType == "") {
          groupChatItem.chatItemInfo.push(obj);
        } else if (lastType == type) {
          groupChatItem.chatItemInfo.push(obj);
        } else {
          groupChatItem.type = lastType;
          oneDialog.push(groupChatItem);

          groupChatItem = {};
          groupChatItem.chatItemInfo = [];
          groupChatItem.chatItemInfo.push(obj);
        }
        lastType = type;
      }
      groupChatItem.type = lastType;
      oneDialog.push(groupChatItem);

      if (think != null) {
        let index = oneDialog.findIndex((item) => item.type == "ai");
        if (index >= -1) {
          let obj = {
            stepType: "think",
            title: "已推理思考(持续" + think.speed + "s)",
            think: think.message,
          };

          oneDialog[index].chatItemInfo = [
            obj,
            ...oneDialog[index].chatItemInfo,
          ];
        }
      }
      return oneDialog;
    },

    //问题输入
    handleEnter() {
      /*let groupChatItem = {
          chatId: 'aaa',
          type: 'user',
          chatItemInfo: [{title: this.queryString}]
      };
        let oneDialog = [];
        oneDialog.push(groupChatItem);
       
      this.agentList.push(oneDialog)*/
      //this.showQueryString = this.queryString;

      this.handleChatSend(this.queryString);
      this.queryString = "";
    },

    clearDisplayState() {
      this.isNewDialog = false;
      this.agentList = [];
    },

    // ---------- 对话发送与 WebSocket ----------

    handleChatSend(text) {
      if (this.chatLoading) return;

      if (!this.selectedAgent) {
        this.$message({
          message: "请先选择智能体",
          type: "warning",
          duration: this.$messageDuration,
        });

        return;
      }

      const aicode = this.selectedAgent.code;
      if (!aicode) {
        this.$message({
          message: "当前智能体缺少编码",
          type: "warning",
          duration: this.$messageDuration,
        });
        return;
      }

      this.resetChatState(text);

      //const loading = this.loadingScreen();
      sendChat({
        aicode,
        question: text,
        chatSessionId: this.chatSessionId || undefined,
      })
        .then((data) => this.startChatSession(data.data))
        .catch(() => {
          this.chatLoading = false;
        })
        .finally(() => {
          //loading.close();
        });
    },

    resetChatState(text) {
      // 在历史会话中追加提问时，保留已有对话轮次
      if (!this.chatSessionId || !this.agentList.length) {
        this.clearDisplayState();
      }

      this.showQueryString = text;
      this.streamingThinking = "";
      this.resultReady = false;
      this.chatLoading = true;
      this.closeChatWebSocket();
      this.scrollToBottom();
    },

    /** 主内容区滚动到底部 */
    scrollToBottom(smooth = true) {
      this.$nextTick(() => {
        this.$nextTick(() => {
          const el = this.$refs.mainContent;
          if (!el) return;
          el.scrollTo({
            top: el.scrollHeight,
            behavior: smooth ? "smooth" : "auto",
          });
        });
      });
    },

    startChatSession({ chatSessionId, chatId, host }) {
      this.chatSessionId = chatSessionId;
      this.currentChatId = chatId;
      this.openThinkingWebSocket(chatSessionId, chatId, host);
    },

    openThinkingWebSocket(chatSessionId, chatId, host) {
      this.wsShouldFetchOnClose = true;
      this.loading = true;
      this.chatWs = connectChatWebSocket({
        chatSessionId,
        chatId,
        host,
        onMessage: this.handleWsMessage,
        onClose: () => {
          this.chatWs = null;
          if (this.wsShouldFetchOnClose) {
            this.wsShouldFetchOnClose = false;
            this.fetchChatResult(chatSessionId, chatId);
          }
          this.loading = false;
        },
        onError: () => {
          this.$message({
            message: "思考过程连接异常",
            type: "error",
            duration: this.$messageDuration,
          });

          this.chatWs = null;
          this.loading = false;
        },
      });
    },

    handleWsMessage(msg) {
      const text = this.extractThinkingText(msg);
      if (text) {
        this.streamingThinking = this.streamingThinking
          ? `${this.streamingThinking}\n${text}`
          : text;

        this.scrollToBottom(false);
      }
    },

    closeChatWebSocket() {
      this.wsShouldFetchOnClose = false;
      if (this.chatWs) {
        this.chatWs.close();
        this.chatWs = null;
      }
    },

    extractThinkingText(msg) {
      if (!msg || typeof msg !== "object") return null;
      if (msg.metadata && msg.metadata.close) return null;

      const candidates = [
        msg.content,
        msg.text,
        msg.message,
        msg.thinking,
        msg.data && typeof msg.data === "string" ? msg.data : null,
        msg.data && msg.data.content,
        msg.data && msg.data.text,
      ];

      return (
        candidates
          .find((item) => typeof item === "string" && item.trim())
          ?.trim() || null
      );
    },

    // ---------- 查询结果获取与解析 ----------

    async fetchChatResult(chatSessionId, chatId) {
      try {
        const data = await getChatInfo({ chatSessionId, chatId });
        this.applyChatResult(data.data);
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.chatLoading = false;
        //this.fetchChatSessionList();
      }
    },

    applyChatResult(data) {
      this.agentList.push(this.praseAnswer(data));
      //const parsed = this.praseAnswer(data);

      this.streamingThinking = "";
      this.showQueryString = "";
      this.resultReady = true;
      this.scrollToBottom();
      /*const newRound = {
        chatId: data.chatId,
        queryText: parsed.queryText || this.pendingQueryText,
        thinkingMessage: parsed.thinkingMessage,
        resultItems: parsed.resultItems,
      };
      this.pendingQueryText = "";

      const existingIndex = this.agentList.findIndex(
        (round) => round.chatId === data.chatId
      );
      if (existingIndex >= 0) {
        this.$set(this.chatRounds, existingIndex, newRound);
      } else {
        this.chatRounds = [...this.chatRounds, newRound];
      }
      this.resultReady = this.chatRounds.some(
        (round) => round.resultItems.length
      );
      this.scrollToBottom();*/
    },
  },
};
</script>


 <style scoped lang="scss">
.title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 86%;
}

/*.no-scrollbar {
  scrollbar-width: none; 
  -ms-overflow-style: none; 
}

.no-scrollbar::-webkit-scrollbar {
  overflow: hidden auto;
  display: none; 
}*/

.aiInput {
  //border: 1px solid #DCDFE6;
  border-radius: 14px;
  transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  background: transparent;
  box-shadow: 0 0 2px #00000005, 0 0 4px #0000000a, 0 0 8px #00000014;

  //width: 100%;
  //flex: 1;
  outline: none;
  border: none;
  resize: none;
  font-family: -apple-system, Segoe UI, Roboto, sans-serif;
  //padding: 20px 20px 8px;
  font-size: 16px;
}

.aiInput:focus {
  /* 移除默认的聚焦轮廓（outline） */
  outline: none;
  /* 自定义边框颜色 */
  box-shadow: 0 0 2px #204ce90f, 0 0 4px #204c9c1a, 0 0 8 #204ce92e;
  border-color: #204ce9;
}

.aiInput-bottom {
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: nowrap;
  overflow: hidden;
}

.aiInput-textarea ::v-deep .el-textarea__inner {
  border: none;
  //border: 1px solid #DCDFE6;
  border-radius: 14px;
  background: transparent;

  width: 100%;
  flex: 1;
  outline: none;
  border: none;
  resize: none;
  font-family: -apple-system, Segoe UI, Roboto, sans-serif;
  padding: 20px 20px 8px;
  font-size: 16px;
}

.userPanel {
  white-space: normal;
  word-break: break-word;
  text-align: left;
  max-width: 80%;
  padding: 9px 15px;
  border-radius: 10px;
  height: 42px;

  background: #e3e7fc;
  border-radius: 9px 0 8px 9px;
  color: #53555e;
}

.aiPanel {
  text-align: left;
  width: 80%;
  background-color: white;
  margin-left: 50px;
  border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
}

.el-collapse {
  border-top: 0;
  border-bottom: 0;
  border: 1px solid #ebeef5;
  border-radius: 10px;
}

.el-collapse-item__content {
  padding-bottom: 0px;
}

.aiDisableCollapse ::v-deep .el-icon-arrow-right:before {
  content: "";
}

.aiDisableCollapse ::v-deep .el-collapse-item__header {
  background: #f6f6f6;
  padding: 10px 30px;
  height: 42px;
  //border: 1px solid rgb(210 210 210);
  color: rgb(95, 102, 116);
  //border-radius: 10px;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  border-bottom: 1px solid #ebeef5;
  border-radius: 10px;
}
.aiDisableCollapse ::v-deep .el-collapse-item__content {
  padding-bottom: 0px;
}

.aiDisableCollapse ::v-deep .el-collapse-item:last-child {
  margin-bottom: -1px;
  //border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
}
.aiDisableCollapse ::v-deep .el-collapse-item__wrap {
  border-radius: 10px;
}

.aiThinkCollapse ::v-deep .el-collapse-item__header {
  background: #f6f6f6;
  padding: 10px 30px;
  height: 42px;
  //border: 1px solid rgb(210 210 210);
  color: rgb(95, 102, 116);
  //border-radius: 10px;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  border-bottom: 1px solid #ebeef5;
  border-radius: 10px;
}

.aiThinkCollapse ::v-deep .el-collapse-item:last-child {
  margin-bottom: -1px;
  //border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
}
.aiThinkCollapse ::v-deep .el-collapse-item__wrap {
  border-radius: 10px;
}

.aiThinkCollapse ::v-deep .el-collapse-item__content {
  padding-bottom: 0px;
}

.aiCollapse ::v-deep .el-collapse-item__header {
  background: #fafbfe;
  padding: 10px 30px;
  height: 42px;
  //border: 1px solid rgb(232, 234, 237);
  color: rgb(95, 102, 116);
  //border-radius: 10px;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  border-bottom: 1px solid #ebeef5;
  border-radius: 10px;
}

.aiCollapse ::v-deep .el-collapse-item:last-child {
  margin-bottom: -1px;
  //border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
}
.aiCollapse ::v-deep .el-collapse-item__wrap {
  border-radius: 10px;
}

.aiCollapse ::v-deep .el-collapse-item__content {
  padding-bottom: 0px;
}

.aiAnalysisCollapse ::v-deep .el-collapse-item__header {
  background: #f1f5ff;
  padding: 10px 30px;
  height: 42px;
  //border: 1px solid rgb(232, 234, 237);
  color: rgb(95, 102, 116);
  //border-radius: 10px;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  border-bottom: 1px solid #ebeef5;
  border-radius: 10px;
}

.aiAnalysisCollapse ::v-deep .el-collapse-item:last-child {
  margin-bottom: -1px;
  //border: 1px solid rgb(232, 234, 237);
  border-radius: 10px;
}
.aiAnalysisCollapse ::v-deep .el-collapse-item__wrap {
  border-radius: 10px;
}

.aiAnalysisCollapse ::v-deep .el-collapse-item__content {
  padding-bottom: 0px;
}

.aiTitleNo {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgb(59, 130, 246);
  color: rgb(255, 255, 255);
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.aiTitleType {
  background: rgb(219, 234, 254);
  color: rgb(29, 78, 216);
  padding: 2px 3px 2px 3px;
  height: 20px;
  display: flex;
  align-content: center;
  padding: 2px 10px;
  flex-wrap: wrap;
}

.queryDimPanel {
  display: flex;
  align-items: center;
  gap: 5px;
  background: #e0f2fe;
  border-color: #7dd3fc;
  color: #0369a1;
  padding: 0 10px;
  border-radius: 4px;
  height: 30px;
  margin-right: 5px;
}

.queryfilterName {
  width: 100px;
  border: 1px solid #e0e0e6;

  line-height: 24px;
  border-radius: 3px;
  background: #fafafc;
  text-align: center;
  padding: 2px 0px 2px 0px;
  height: 30px;
}

.query-tableBox {
  //border-left: solid 1px #b3c6f2;
  //border-right: solid 1px #b3c6f2;
  //border-bottom: solid 1px #b3c6f2;

  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}



.compute-tableBox {
  //border-left: solid 1px #b3c6f2;
  //border-right: solid 1px #b3c6f2;
  //border-bottom: solid 1px #b3c6f2;

  border-radius: 10px;
}

.chatType-DropDown {
  width: 140px;
  height: 32px;
  background: #e1eafc;
  border-radius: 4px;
  border: 1px solid #e7e9ec;
  cursor: pointer;
  padding: 0 3px 0 6px;
  line-height: 32px;
  font-size: 14px;
  color: #0b0b0b;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.el-dropdown {
  display: inline-block;
  position: relative;
  color: #606266;
  font-size: 14px;
}

::v-deep .el-table th.el-table__cell {
  background-color: rgb(248, 249, 251);
  color: rgb(71, 85, 105);
}

.agent-sidebar__logo {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-right: 8px;
  object-fit: contain;
}

/* 使用深度选择器穿透 scoped 样式限制 */
.selectStyle ::v-deep .el-input__inner {
  height: 30px; /* 修改输入框高度 */
  background: #f7f8fa !important;
  text-align: center;
  border-radius: 0px;
}

/* 修复右侧图标位置，防止偏移 */
.selectStyle ::v-deep .el-input__suffix {
  top: 0; /* 或根据实际情况调整 */
  display: flex;
  align-items: center;
  /* 或者使用 height: 100%; */
}

/* 修复下拉箭头图标垂直居中 */
.selectStyle ::v-deep .el-input__icon {
  line-height: 30px; /* 与输入框高度保持一致 */
}

.select-clear-Style ::v-deep .el-input__inner {
  height: 30px; /* 修改输入框高度 */
  background: #f7f8fa !important;
  text-align: center;
  border-radius: 0px;
}

.select-clear-Style ::v-deep .el-input__prefix {
  top: 0; /* 或根据实际情况调整 */
  display: flex;
  align-items: center;

  left: 145px;
  top: 4px;
}

.select-clear-Style ::v-deep .el-input__icon {
  line-height: 30px; /* 与输入框高度保持一致 */
}

.myDate {
  height: 30px;
}
.myDate ::v-deep .el-range__icon {
  line-height: 24px;
}

.myDate ::v-deep .el-range__close-icon {
  line-height: 24px;
}

.myDate ::v-deep .el-range-separator {
  line-height: 18px;
}

.myinput ::v-deep .el-input__inner {
  line-height: 24px;
  height: 30px;
  border-radius: 0px;
}

.mybutton ::v-deep .el-button--primary {
  height: 30px;
  padding: 0px 20px;
}

.think {
  ::v-deep .markdown-body p {
    margin-left: 25px;
    margin-top: 0;
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
    background: #409eff;
    color: #fff;
    border-radius: 50%;
    font-size: 12px;
    font-weight: bold;
  }

  /* 4. 生成步骤之间的连接竖线 */
  ::v-deep .markdown-body h3::after {
    content: "";
    position: absolute;
    left: 11px; /* 圆点中心位置 (24/2 - 1) */
    top: 28px; /* 圆点底部 */
    width: 2px;
    height: calc(100% + 8px); /* 延伸到下一个步骤 */
    background: #dcdfe6;
  }

  /* 5. 最后一个步骤不需要竖线 */
  ::v-deep .markdown-body h3:last-child::after {
    display: none;
  }
}

.analysis {
}

.one-bgdiv {
  width: 100%;
  text-align: left;
  padding: 0px 5px 0 0;
}

::v-deep .el-tabs__item {
  line-height: 24px;
  height: 24px;
  font-size: 12px;
}

::v-deep .el-tabs__header {
  margin: 0 0 5px;
}

.filterPanel ::v-deep .el-checkbox__label {
  font-size: 12px;
}

.el-popper {
  padding: 0px;
}

.horizontal-line {
  border-top: 1px solid #ccc;
  margin: 5px 0;
}

.clearable-select {
  position: relative;
  display: inline-block;
}
.clear-btn {
  position: absolute;
  top: 0;
  right: 0;
  cursor: pointer;
  padding: 0 10px; /* 根据实际需要调整 */
  line-height: 32px; /* 与 el-select 的高度一致 */
  background-color: #fff; /* 或者其他背景色 */
}

/* 让 suffix 容器可以绝对定位子元素 */
.el-input ::v-deep .el-input__suffix {
  position: relative;
}

/* 清除按钮容器（负责裁剪） */
.clear-btn {
  display: inline-flex;
  position: relative;
  right: -126.5px;
  top: -29px;

  width: 28px;
  height: 28px;
  overflow: hidden;
  cursor: pointer;
  z-index: 1;
}

/* 带圆角的“正方形”旋转后形成三角形 */
.clear-btn .triangle {
  position: absolute;
  top: -2px;
  right: 20px;
  width: 40px;
  height: 40px;
  transform: rotate(220deg);
  transform-origin: top right;
  background: #d7d4d4;
  border-radius: 0 0 0 50%;
  border-radius: 50px;
}

/* × 字符，绝对定位在可视区域内 */
.clear-btn .x-mark {
  position: absolute;
  top: 1px;
  right: 12px;
  font-size: 10px;
  font-weight: bold;
  color: #8b8585;
  z-index: 2;
  pointer-events: none;
  line-height: 1;
  transform: rotate(142deg);
}

.custom-loading ::v-deep .el-loading-spinner .circular {
  height: 24px;
  width: 24px;
}

.custom-loading ::v-deep .el-loading-spinner {
  display: flex;
  gap: 5px;
}
.custom-loading ::v-deep .el-loading-spinner .el-loading-text {
  font-size: 10px;
}

.tableBoxDiv ::v-deep .el-table .el-table__cell {
  padding: 4px 0;
}

.tableBoxDiv ::v-deep .el-table td {
  padding: 0 0;
}
.tableBoxDiv ::v-deep .el-table .cell {
  line-height: 36px;
  padding: 0 10px;
  /*height: 36px;*/
}

.tableBoxDiv ::v-deep .el-table__fixed td {
  padding: 0 0;
}
.tableBoxDiv ::v-deep .el-table__fixed .cell {
  line-height: 36px;
  /*height: 36px;*/
}

.tableBoxDiv ::v-deep .el-table td.el-table__cell div {
  align-content: center;
}

.tableBoxDiv ::v-deep .el-table thead th {
  padding: 0 0;
  height: 36px;
}

.tableBoxDiv ::v-deep .el-table thead .cell {
  line-height: 36px;
  padding: 0 10px;

  align-content: center;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.tableBoxDiv ::v-deep .el-table td.el-table__cell div {
  align-content: center;
}

.tableBoxDiv ::v-deep .el-table--border,
.el-table--group {
  border: none;
}

.tableBoxDiv ::v-deep .el-table--border::after,
.el-table--group::after,
.el-table::before {
  background-color: #ffffff;
}

.tableBoxDiv ::v-deep .el-table__header {
  border-left: 1px solid #ebeef5;
}

.tableBoxDiv ::v-deep .el-table__body {
  border-left: 1px solid #ebeef5;
}

.tableBoxDiv ::v-deep .el-table__body,
.el-table__footer {
  /*padding-bottom: 1px;*/
  border-bottom: 1px solid #ebeef5;
}

.tableBoxDiv ::v-deep .el-table--border::after,
.el-table--group::after {
  width: 0px;
}
</style>
