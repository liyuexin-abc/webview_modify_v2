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
      <div class="welcome-hero">
        <div class="welcome-hero__badge">
          <base-icon name="sparkles" :size="26" :stroke-width="1.8" />
        </div>
        <div class="welcome-hero__title">
          你好，欢迎使用
          <span class="welcome-hero__agent">{{
            selectedAgent ? selectedAgent.name : ""
          }}</span>
        </div>

        <div class="welcome-hero__subtitle">
          用自然语言提问，我会为你完成取数、计算、分析与总结
        </div>

        <div class="welcome-hero__tips">
          <span class="welcome-hero__tip">
            <base-icon name="bar-chart" :size="13" :stroke-width="2" />
            指标查询
          </span>
          <span class="welcome-hero__tip">
            <base-icon name="trending-up" :size="13" :stroke-width="2" />
            趋势分析
          </span>
          <span class="welcome-hero__tip">
            <base-icon name="lightbulb" :size="13" :stroke-width="2" />
            归因总结
          </span>
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
                          <div class="think-badge">
                            <base-icon
                              name="brain"
                              :size="14"
                              :stroke-width="2"
                            />
                          </div>
                          &nbsp;&nbsp;
                          <div>
                            {{ chatItemInfo.title }}
                          </div>
                        </div>
                      </span>

                      <div class="think think-content">
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
                            {{ chatItemInfo.stepNo || chatItemInfo.itemType }}
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
                              class="toolbar-btn"
                              @click="showSQL(chatItemInfo.viewSql)"
                              ><base-icon
                                name="file-code"
                                :size="13"
                                :stroke-width="2"
                              />&nbsp;SQL</el-button
                            >

                            <el-button
                              size="mini"
                              class="toolbar-btn"
                              @click="downFile(chatItemInfo)"
                              ><base-icon
                                name="download"
                                :size="13"
                                :stroke-width="2"
                              />&nbsp;下载
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
                          <div class="query-row__main">
                            <div class="query-row__label">维度</div>

                            <div class="query-row__tags">
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
                              <truncate-tip
                                class="queryDimPanel__text"
                                :text="dim.name"
                              />

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
                          <div class="query-row__main">
                            <div class="query-row__label">指标</div>

                            <div class="query-row__tags">
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
                              <truncate-tip
                                class="queryDimPanel__text"
                                :text="mertic.name"
                              />
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

                        <div class="query-row query-row--filter">
                          <div class="query-row__main">
                            <div class="query-row__label">筛选器</div>

                            <div class="filter-area">
                              <div class="filter-conds">
                                <!-- 日期条件（固定第一个） -->
                                <div class="filter-cond">
                                  <el-select
                                    placeholder="日期"
                                    v-model="chatItemInfo.dateGranularity"
                                    class="filter-cond__field selectStyle"
                                  >
                                    <el-option
                                      v-for="item in granularityEnum"
                                      :key="item.value"
                                      :label="item.name"
                                      :value="item.value"
                                    >
                                    </el-option>
                                  </el-select>

                                  <el-date-picker
                                    v-model="chatItemInfo.dataRange"
                                    type="daterange"
                                    range-separator="至"
                                    start-placeholder="开始日期"
                                    end-placeholder="结束日期"
                                    :value-format="'yyyy-MM-dd'"
                                    class="filter-cond__date myDate"
                                  >
                                    <template slot="suffix">
                                      <i
                                        class="el-input__icon el-icon-date"
                                      ></i>
                                    </template>
                                  </el-date-picker>
                                </div>

                                <!-- 动态筛选条件 -->
                                <div
                                  v-for="(
                                    filter, index3
                                  ) in chatItemInfo.filter"
                                  :key="index3"
                                  class="filter-cond"
                                >
                                  <truncate-tip
                                    class="filter-cond__name"
                                    :text="filter.name"
                                  />

                                  <el-select
                                    placeholder="操作"
                                    v-model="filter.operator"
                                    class="filter-cond__op selectStyle"
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

                                  <!--按照操作符变化输入框和下拉框-->
                                  <el-input
                                    v-if="filter.operator <= 9"
                                    v-model="filter.value"
                                    class="filter-cond__value myinput"
                                    placeholder="请输入值"
                                  >
                                  </el-input>
                                  <el-select
                                    v-else
                                    placeholder="请选择值"
                                    v-model="filter.value"
                                    class="filter-cond__value filter-cond__value--select"
                                    multiple
                                    collapse-tags
                                  >
                                    <el-option
                                      v-for="item in filter.diaplayValue"
                                      :key="item"
                                      :label="item"
                                      :value="item"
                                    >
                                    </el-option>
                                  </el-select>

                                  <button
                                    type="button"
                                    class="filter-cond__remove"
                                    title="删除此条件"
                                    @click.stop="
                                      deleteFilter(index3, chatItemInfo)
                                    "
                                  >
                                    <i class="el-icon-close"></i>
                                  </button>
                                </div>
                              </div>

                              <div class="filter-area__actions">
                                <el-button
                                  type="primary"
                                  icon="el-icon-search"
                                  class="filter-area__search"
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

                              <el-dropdown-menu
                                slot="dropdown"
                                class="filter-pop-menu"
                              >
                                <div class="filter-pop">
                                  <div class="filter-pop__header">
                                    <span class="filter-pop__icon">
                                      <base-icon
                                        name="filter"
                                        :size="13"
                                        :stroke-width="2"
                                      />
                                    </span>
                                    添加筛选器
                                  </div>

                                  <div class="filter-pop__body">
                                    <el-tabs
                                      :ref="`activeName${index}${index1}${index2}`"
                                      stretch
                                      style="width: 100%"
                                    >
                                      <el-tab-pane
                                        label="维度"
                                        :name="`first${index}${index1}${index2}`"
                                      >
                                        <div class="filter-pop__list">
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
                                        <div class="filter-pop__list">
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

                                  <div class="filter-pop__footer">
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
                            {{ chatItemInfo.stepNo || chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div
                            class="aiTitleType aiTitleType--compute"
                            style="min-width: 46px"
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
                            {{ chatItemInfo.stepNo || chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div
                            class="aiTitleType aiTitleType--analyze"
                            style="min-width: 46px"
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
                              <div class="ai-result-card ai-result-card--analyze">
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
                            {{ chatItemInfo.stepNo || chatItemInfo.itemType }}
                          </div>
                          &nbsp;&nbsp;
                          <div
                            class="aiTitleType aiTitleType--summary"
                            style="min-width: 46px"
                          >
                            总结
                          </div>
                          &nbsp;&nbsp;
                          <div class="title">{{ chatItemInfo.title }}</div>
                        </div>
                      </span>

                      <div>
                        <div style="padding: 10px">
                          <div class="ai-result-card ai-result-card--summary">
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
              class="send-btn"
              type="primary"
              @click="handleEnter"
            >
              <base-icon name="send" :size="16" :stroke-width="2" />
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isNewDialog" style="height: 40%"></div>

    <el-dialog
      :show-close="false"
      :close-on-click-modal="false"
      title="查询 SQL"
      :modal="false"
      width="640px"
      :visible.sync="isSqlPage"
    >
      <div style="padding: 0 20px">
        <sql-panel :sql="viewSql" title="本次查询语句" />
      </div>

      <div style="display: flex; padding: 14px 20px 16px">
        <div class="one-bgdiv" style="display: flex; justify-content: flex-end">
          <el-button @click="isSqlPage = false">关 闭</el-button>
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
import SqlPanel from "@/components/SqlPanel";
import TruncateTip from "@/components/TruncateTip";

import { sendChat, getChatInfo } from "@/api/smartQuery/smartQueryAPI.js";
import { connectChatWebSocket } from "@/views/smartQuery/utils/chatWebSocket.js";

export default {
  name: "queryPage",
  props: [],
  components: { SqlPanel, TruncateTip },
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
      // SqlPanel 内置 formatSQL 自动格式化(括号深度感知/子查询缩进),直接传原始 SQL
      this.viewSql = viewSql || "";
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
      let stepNo = 0; // 步骤序号(查数/计算/分析/总结依次编号)

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
          obj.stepNo = ++stepNo;
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

/* ---------- 欢迎页 ---------- */
.welcome-hero {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  gap: 14px;
  padding: 0 24px;
}

.welcome-hero__badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 18px;
  color: #fff;
  background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
  box-shadow: 0 8px 24px rgba(43, 92, 255, 0.28);
  margin-bottom: 4px;
}

.welcome-hero__title {
  font-size: clamp(22px, 2vw, 30px);
  font-weight: 600;
  color: var(--text-primary, #1e293b);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.welcome-hero__agent {
  background: linear-gradient(135deg, #2b5cff, #06b6d4);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.welcome-hero__subtitle {
  font-size: clamp(13px, 1.1vw, 16px);
  color: var(--text-muted, #94a3b8);
}

.welcome-hero__tips {
  display: flex;
  gap: 10px;
  margin-top: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.welcome-hero__tip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 14px;
  font-size: 12px;
  color: var(--text-secondary, #475569);
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--border-light, #e5eaf1);
  border-radius: 999px;
  box-shadow: 0 1px 3px rgba(30, 41, 59, 0.05);
}

/* ---------- 思考徽标 / 步骤徽标 / 工具按钮 ---------- */
.think-badge {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #fff;
  background: linear-gradient(135deg, #4f8cff, #2b5cff);
  box-shadow: 0 2px 6px rgba(43, 92, 255, 0.28);
  flex-shrink: 0;
}

.toolbar-btn {
  display: inline-flex;
  align-items: center;
  border-radius: 8px;

  .base-icon {
    vertical-align: middle;
  }
}

.send-btn {
  width: 40px;
  height: 36px !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 !important;
  border-radius: 12px;
  background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
  border: none;
  box-shadow: 0 4px 12px rgba(43, 92, 255, 0.3);
  transition: all 0.15s;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(43, 92, 255, 0.4);
  }
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
  border-radius: 16px;
  transition: box-shadow 0.2s cubic-bezier(0.645, 0.045, 0.355, 1),
    border-color 0.2s;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid var(--border-light, #e5eaf1);
  box-shadow: 0 4px 20px rgba(30, 41, 59, 0.07);
  backdrop-filter: blur(8px);

  outline: none;
  resize: none;
  font-family: -apple-system, Segoe UI, Roboto, sans-serif;
  font-size: 15px;

  &:focus-within {
    border-color: rgba(43, 92, 255, 0.4);
    box-shadow: 0 4px 20px rgba(43, 92, 255, 0.12),
      0 0 0 3px rgba(43, 92, 255, 0.08);
  }
}

.aiInput-bottom {
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: nowrap;
  overflow: hidden;
}

.aiInput-textarea ::v-deep .el-textarea__inner,
.aiInput-textarea.is-disabled ::v-deep .el-textarea__inner,
.aiInput-textarea ::v-deep .el-textarea__inner:disabled {
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  color: var(--text-primary, #1e293b);
  -webkit-text-fill-color: var(--text-primary, #1e293b);
  cursor: text;
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

/* 分析/总结结果文字卡片: 多段渐变底 + 内高光, 体现质感 */
.ai-result-card {
  padding: 14px 18px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.8;
  color: #3f4a63;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9),
    0 1px 4px rgba(30, 41, 59, 0.04);
}

.ai-result-card--analyze {
  background: linear-gradient(
    130deg,
    #f0f7ff 0%,
    #eef4ff 30%,
    #f0f0ff 65%,
    #f6f1ff 100%
  );
  border: 1px solid rgba(99, 102, 241, 0.16);
}

.ai-result-card--summary {
  background: linear-gradient(
    130deg,
    #eff8ff 0%,
    #ecfbf9 40%,
    #f0fdf6 75%,
    #f3fcff 100%
  );
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.think-content {
  margin: 8px 10px 10px;
  padding: 12px 16px;
  border-radius: 10px;
  background: linear-gradient(130deg, #f8fbff 0%, #f5f9ff 55%, #f3fbfe 100%);
  border: 1px solid rgba(43, 92, 255, 0.08);
}

.userPanel {
  white-space: normal;
  word-break: break-word;
  text-align: left;
  max-width: 80%;
  padding: 10px 16px;
  min-height: 42px;
  font-size: 14px;
  line-height: 1.6;

  background: linear-gradient(
    135deg,
    #e8efff 0%,
    #e3f0ff 40%,
    #ddf3ff 75%,
    #e6f0ff 100%
  );
  border: 1px solid rgba(43, 92, 255, 0.16);
  border-radius: 16px 4px 16px 16px;
  color: var(--text-primary, #1e293b);
  box-shadow: 0 2px 8px rgba(43, 92, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.85);
}

.aiPanel {
  text-align: left;
  width: 80%;
  background-color: rgba(255, 255, 255, 0.92);
  margin-left: 50px;
  border: 1px solid var(--border-light, #e5eaf1);
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(30, 41, 59, 0.05);
  backdrop-filter: blur(6px);
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
  position: relative;
  overflow: hidden;
  padding: 10px 24px;
  height: 44px;
  color: #5b5e7a;
  font-weight: 500;
  border: 1px solid rgba(43, 92, 255, 0.14);
  border-radius: 12px;
  /* 水波纹式光晕: 同色系蓝调渐变自左向右缓慢流动 */
  background: linear-gradient(
    100deg,
    #f0f6ff 0%,
    #e9f2ff 30%,
    #e7f6fd 50%,
    #e9f2ff 70%,
    #f0f6ff 100%
  );
  background-size: 220% 100%;
  animation: think-wave 5.5s ease-in-out infinite;
}

/* 高光扫过(水波光晕) */
.aiDisableCollapse ::v-deep .el-collapse-item__header::after {
  content: "";
  position: absolute;
  top: 0;
  left: -70%;
  width: 55%;
  height: 100%;
  background: linear-gradient(
    105deg,
    transparent 0%,
    rgba(255, 255, 255, 0.5) 50%,
    transparent 100%
  );
  animation: think-shine 4.8s ease-in-out infinite;
  pointer-events: none;
}

@keyframes think-wave {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes think-shine {
  0% {
    left: -70%;
  }
  45% {
    left: 120%;
  }
  100% {
    left: 120%;
  }
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
  background: linear-gradient(120deg, #f4f8ff 0%, #eef5ff 50%, #f0faff 100%);
  padding: 10px 24px;
  height: 44px;
  color: #4c5670;
  border: 1px solid rgba(43, 92, 255, 0.12);
  border-radius: 12px;
  transition: box-shadow 0.2s ease, border-color 0.2s ease,
    transform 0.2s ease;
}

.aiThinkCollapse ::v-deep .el-collapse-item__header:hover {
  border-color: rgba(43, 92, 255, 0.28);
  box-shadow: 0 4px 14px rgba(43, 92, 255, 0.12);
  transform: translateY(-1px);
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
  background: linear-gradient(120deg, #f7faff 0%, #f4f8ff 55%, #f2fbfd 100%);
  padding: 10px 24px;
  height: 44px;
  color: #47506b;
  border: 1px solid rgba(59, 130, 246, 0.13);
  border-radius: 12px;
  transition: box-shadow 0.22s ease, border-color 0.22s ease,
    transform 0.22s ease, background 0.22s ease;
}

.aiCollapse ::v-deep .el-collapse-item__header:hover {
  background: linear-gradient(120deg, #f0f6ff 0%, #edf4ff 55%, #e9f9fc 100%);
  border-color: rgba(59, 130, 246, 0.35);
  box-shadow: 0 6px 18px rgba(43, 92, 255, 0.13);
  transform: translateY(-2px);
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
  background: linear-gradient(120deg, #f2f6ff 0%, #f1f0fe 60%, #f5f0ff 100%);
  padding: 10px 24px;
  height: 42px;
  color: #4c5470;
  border: 1px solid rgba(99, 102, 241, 0.13);
  border-radius: 12px;
  transition: box-shadow 0.2s ease, border-color 0.2s ease,
    transform 0.2s ease;
}

.aiAnalysisCollapse ::v-deep .el-collapse-item__header:hover {
  border-color: rgba(99, 102, 241, 0.32);
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.13);
  transform: translateY(-1px);
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
  border-radius: 8px;
  background: var(--accent-gradient, linear-gradient(135deg, #3b82f6, #06b6d4));
  color: rgb(255, 255, 255);
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(43, 92, 255, 0.25);
}

.aiTitleType {
  background: rgba(59, 130, 246, 0.12);
  color: #1d4ed8;
  height: 20px;
  display: flex;
  align-content: center;
  padding: 2px 10px;
  flex-wrap: wrap;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
  justify-content: center;

  &--compute {
    background: rgba(6, 182, 212, 0.12);
    color: #0e7490;
  }

  &--analyze {
    background: rgba(139, 92, 246, 0.12);
    color: #6d28d9;
  }

  &--summary {
    background: rgba(16, 185, 129, 0.12);
    color: #047857;
  }
}

.queryDimPanel {
  display: flex;
  align-items: center;
  gap: 5px;
  background: linear-gradient(135deg, #e3f1fe, #dbf3fd);
  border: 1px solid rgba(59, 130, 246, 0.16);
  color: #0369a1;
  padding: 0 14px;
  border-radius: 999px;
  height: 30px;
  margin-right: 5px;
  transition: box-shadow 0.18s ease, transform 0.18s ease,
    border-color 0.18s ease;
}

.queryDimPanel:hover {
  border-color: rgba(59, 130, 246, 0.38);
  box-shadow: 0 3px 10px rgba(59, 130, 246, 0.16);
  transform: translateY(-1px);
}

/* 标签文本：超长单行省略；仅当确实被截断时才显示 Tooltip（TruncateTip 组件控制） */
.queryDimPanel__text {
  max-width: 7em; /* 约 7 个汉字，超出即省略 */
  cursor: default;
}

/* ---------- 行级布局（维度/指标/筛选器公用，尺寸自适应） ---------- */
.query-row--filter {
  padding: 10px 20px;
  background: #fafbfe;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #eaeaea;
}

.query-row__main {
  display: flex;
  align-items: flex-start;
  flex: 1 1 auto;
  min-width: 0; /* 允许内部收缩，防止撑破 */
}

.query-row__label {
  flex: 0 0 60px;
  width: 60px;
  line-height: 30px;
  color: #303a4e;
  font-weight: 500;
  white-space: nowrap;
}

.query-row__tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  flex: 1 1 auto;
  min-width: 0;
  padding: 2px 0;
}

/* ---------- 筛选条件区：响应式胶囊卡片 ---------- */
.filter-area {
  flex: 1 1 auto;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-conds {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px 12px;
}

/* 单个条件：圆角胶囊，内部元素无缝拼接 */
.filter-cond {
  display: inline-flex;
  align-items: stretch;
  border: 1px solid #dde3ee;
  border-radius: 8px;
  background: #fff;
  overflow: hidden;
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.filter-cond:hover {
  border-color: rgba(43, 92, 255, 0.4);
  box-shadow: 0 2px 8px rgba(43, 92, 255, 0.08);
}

.filter-cond:focus-within {
  border-color: #2b5cff;
  box-shadow: 0 0 0 2px rgba(43, 92, 255, 0.12);
}

/* 条件名（字段名）：固定宽度，超长省略，保证每个筛选器长度一致 */
.filter-cond__name {
  display: block;
  box-sizing: border-box;
  width: 108px;
  padding: 0 10px;
  height: 30px;
  line-height: 30px;
  background: #f2f5fb;
  color: #303a4e;
  font-weight: 500;
  border-right: 1px solid #e6eaf3;
  flex: 0 0 auto;
}

.filter-cond__field {
  width: 88px;
  flex: 0 0 auto;
}

.filter-cond__op {
  width: 84px;
  flex: 0 0 auto;
}

.filter-cond__date {
  width: 230px;
  flex: 0 0 auto;
}

/* 值区域：固定宽度，所有条件胶囊总长一致（108+84+110+26） */
.filter-cond__value {
  width: 110px;
  flex: 0 0 auto;
}

/* 胶囊内部控件去边框，由外层胶囊统一描边 */
.filter-cond ::v-deep .el-input__inner,
.filter-cond ::v-deep .el-range-editor.el-input__inner {
  border: none !important;
  border-radius: 0 !important;
  height: 30px;
  line-height: 30px;
  background: #fff !important;
}

.filter-cond ::v-deep .selectStyle .el-input__inner {
  background: #f7f9fd !important;
  border-right: 1px solid #e6eaf3 !important;
  text-align: center;
}

.filter-cond ::v-deep .el-date-editor .el-range-input {
  background: transparent;
}

.filter-cond ::v-deep .el-select__tags {
  max-width: calc(100% - 26px) !important;
}

/* 日期区间：分隔符"至"垂直水平居中、两侧输入均分宽度 */
.filter-cond__date ::v-deep .el-range-separator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 30px;
  height: 30px;
  padding: 0;
  width: 10%;
  font-size: 12px;
  color: #98a2b8;
}

.filter-cond__date ::v-deep .el-range-input {
  width: 42%;
  font-size: 13px;
}

.filter-cond__date ::v-deep .el-range__icon {
  line-height: 30px;
  margin-left: 2px;
}

.filter-cond__date ::v-deep .el-range__close-icon {
  line-height: 30px;
  width: 16px;
}

/* 删除按钮：悬停变红，替代原三角形 × hack */
.filter-cond__remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  border: none;
  border-left: 1px solid #e6eaf3;
  background: #f7f9fd;
  color: #98a2b8;
  cursor: pointer;
  padding: 0;
  transition: background 0.15s ease, color 0.15s ease;
}

.filter-cond__remove:hover {
  background: #fef0f0;
  color: #f56c6c;
}

.filter-area__actions {
  display: flex;
}

.filter-area__search {
  height: 30px;
  padding: 0 20px;
}

/* 窄屏：条件胶囊内部允许换行 */
@media (max-width: 768px) {
  .filter-cond {
    flex-wrap: wrap;
  }
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

/* ===== 添加筛选器卡片 ===== */
.filter-pop-menu {
  padding: 0 !important;
  border-radius: 14px !important;
  border: 1px solid rgba(43, 92, 255, 0.1) !important;
  box-shadow: 0 12px 32px rgba(30, 60, 120, 0.14) !important;
  overflow: hidden;
}

.filter-pop {
  width: 264px;
}

.filter-pop__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px 10px;
  font-size: 13px;
  font-weight: 600;
  color: #2c3550;
  background: linear-gradient(120deg, #f4f8ff 0%, #f0f7ff 60%, #f2fbfe 100%);
  border-bottom: 1px solid rgba(43, 92, 255, 0.08);
}

.filter-pop__icon {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  color: #fff;
  background: linear-gradient(135deg, #4f8cff, #2b5cff);
  box-shadow: 0 2px 5px rgba(43, 92, 255, 0.25);
  flex-shrink: 0;
}

.filter-pop__body {
  padding: 4px 8px 0;
}

.filter-pop__body ::v-deep .el-tabs__header {
  margin-bottom: 6px;
}

.filter-pop__body ::v-deep .el-tabs__item {
  font-size: 12.5px;
  height: 36px;
  line-height: 36px;
  color: #66758a;
  transition: color 0.2s ease;
}

.filter-pop__body ::v-deep .el-tabs__item.is-active {
  color: var(--brand, #2b5cff);
  font-weight: 600;
}

.filter-pop__body ::v-deep .el-tabs__active-bar {
  background: linear-gradient(90deg, #3b82f6, #2b5cff);
  height: 3px;
  border-radius: 3px;
}

.filter-pop__body ::v-deep .el-tabs__nav-wrap::after {
  height: 1px;
  background-color: rgba(43, 92, 255, 0.08);
}

.filter-pop__list {
  width: 100%;
  max-height: 180px;
  overflow-y: auto;
  padding: 2px 8px 6px;
}

.filter-pop__list .filterPanel {
  display: flex;
  align-items: center;
  width: 100%;
  margin: 0 0 2px;
  padding: 7px 10px;
  border-radius: 8px;
  transition: background 0.15s ease;
}

.filter-pop__list .filterPanel:hover {
  background: rgba(43, 92, 255, 0.05);
}

.filter-pop__list .filterPanel ::v-deep .el-checkbox__label {
  font-size: 12.5px;
  color: #3c465e;
}

.filter-pop__footer {
  display: flex;
  justify-content: flex-end;
  padding: 10px 14px 12px;
  border-top: 1px solid rgba(43, 92, 255, 0.08);
  background: #fbfcff;
}

.filter-pop__footer .el-button--mini {
  padding: 6px 18px;
  border-radius: 8px;
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
