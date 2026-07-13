<!-- 查询结果面板：整合用户问题、思考过程及多条分类结果卡片 -->
<template>
  <div v-if="panelVisible" class="query-panel">
    <div
      v-for="(round, roundIndex) in chatRounds"
      :key="round.chatId || roundIndex"
      class="query-panel__round"
    >
      <QueryBanner v-if="round.queryText" :text="round.queryText" />

      <div class="answer">
        <div class="answer-ai">
          <img :src="agentAvatar" alt="" class="ai-avatar" />
          <span class="ai-name">{{ agentName }}</span>
        </div>

        <div class="answer-box">
          <ThinkingProcess
            v-if="round.thinkingMessage"
            :content="round.thinkingMessage"
          />

          <div
            v-for="(item, index) in round.resultItems"
            :key="`${round.chatId}-${item.itemId}`"
            :class="item.stepType === 'summarize' ? 'qa-box' : 'results-box'"
          >
            <!-- 总结类：QA 卡片 -->
            <template v-if="item.stepType === 'summarize'">
              <div class="qa-header">
                <div class="qa-header-left">
                  <template v-if="getStepMeta(round, index)">
                    <span class="qa-number">{{ getStepMeta(round, index).stepNo }}</span>
                    <span class="qa-tag">{{ getStepMeta(round, index).stepTypeLabel }}</span>
                  </template>
                  <span class="qa-title">{{ item.title || round.queryText }}</span>
                </div>
              </div>
              <div v-if="item.summaryText" class="qa-content">
                <div class="qa-item">{{ item.summaryText }}</div>
              </div>
            </template>

            <!-- 查询/计算/分析：Results 卡片 -->
            <template v-else>
              <div class="results" @click="toggleCollapse(`${round.chatId}-${item.itemId}`)">
                <div class="top-bar">
                  <h2 class="results-title">
                    <span v-if="getStepMeta(round, index)" class="step-badges">
                      <span class="step-no">{{ getStepMeta(round, index).stepNo }}</span>
                      <span
                        :class="[
                          'step-type',
                          {
                            'is-query': item.stepType === 'query',
                            'is-analyze': item.stepType === 'analyze',
                            'is-compute': item.stepType === 'compute',
                          },
                        ]"
                      >
                        {{ getStepMeta(round, index).stepTypeLabel }}
                      </span>
                    </span>
                    <span v-else class="step-type" :class="getStepTypeClass(item.stepType)">
                      {{ item.typeLabel }}
                    </span>
                    <span class="question-text">{{ item.title || round.queryText }}</span>
                  </h2>
                  <i
                    :class="[
                      'results-toggle',
                      isCollapsed(`${round.chatId}-${item.itemId}`) ? 'el-icon-arrow-down' : 'el-icon-arrow-up',
                    ]"
                  />
                </div>
              </div>

              <div v-show="!isCollapsed(`${round.chatId}-${item.itemId}`)" class="results-content">
                <div class="results-content-box">
                  <div class="results-content-box-content">
                    <QueryConfig
                    v-if="item.stepType === 'query'"
                      :dimensions="item.dimensions"
                      :metrics="item.metrics"
                      :filter="item.filter"
                      :view-types="viewTypes"
                      :filter-fields="item.filterFields"
                      :filter-operators="filterOperators"
                      :view-type="item.viewType"
                      :search-loading="item.searchLoading"
                      @remove-dimension="$emit('remove-dimension', roundIndex, index, $event)"
                      @remove-metric="$emit('remove-metric', roundIndex, index, $event)"
                      @add-dimension="$emit('add-dimension', roundIndex, index)"
                      @add-metric="$emit('add-metric', roundIndex, index)"
                      @search="$emit('search', roundIndex, index, $event)"
                      @add-filter="$emit('add-filter', roundIndex, index)"
                      @download="$emit('download', roundIndex, index)"
                      @show-sql="$emit('show-sql', roundIndex, index)"
                      @change-view="$emit('change-view', roundIndex, index, $event)"
                    />

                    <DataTable :data="item.tableData" :columns="item.tableColumns" />
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- 追加提问：新问题与思考过程展示在已有对话之后 -->
    <div v-if="showPendingAnswer" class="query-panel__round">
      <QueryBanner :text="pendingQueryText" />
      <div class="answer">
        <div class="answer-ai">
          <img :src="agentAvatar" alt="" class="ai-avatar" />
          <span class="ai-name">{{ agentName }}</span>
        </div>
        <div class="answer-box">
          <ThinkingProcess
            :content="streamingThinking"
            :loading="thinkingLoading"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import defaultLogo from '@/assets/svgs/logo.svg';
import QueryBanner from './QueryBanner.vue';
import QueryConfig from './QueryConfig.vue';
import DataTable from './DataTable.vue';
import ThinkingProcess from './ThinkingProcess.vue';

const STEP_TYPE_LABEL = {
  query: '查询',
  compute: '计算',
  analyze: '分析',
  summarize: '总结',
};

export default {
  name: 'QueryPanel',
  components: {
    QueryBanner,
    QueryConfig,
    DataTable,
    ThinkingProcess,
  },
  props: {
    chatRounds: {
      type: Array,
      default: () => [],
    },
    pendingQueryText: {
      type: String,
      default: '',
    },
    streamingThinking: {
      type: String,
      default: '',
    },
    viewTypes: {
      type: Array,
      default: () => [],
    },
    filterOperators: {
      type: Array,
      default: () => [],
    },
    thinkingLoading: {
      type: Boolean,
      default: false,
    },
    resultReady: {
      type: Boolean,
      default: false,
    },
    agent: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      collapsedMap: {},
    };
  },
  computed: {
    panelVisible() {
      return (
        this.pendingQueryText ||
        this.streamingThinking ||
        this.chatRounds.length > 0 ||
        this.thinkingLoading ||
        this.resultReady
      );
    },
    agentName() {
      return this.agent?.name || '智能问数助手';
    },
    agentAvatar() {
      return this.agent?.image || this.agent?.avatar || defaultLogo;
    },
    showPendingAnswer() {
      return Boolean(this.pendingQueryText);
    },
  },
  watch: {
    chatRounds() {
      this.collapsedMap = {};
    },
  },
  methods: {
    getStepMeta(round, index) {
      const total = round.resultItems.length;
      if (total <= 1) return null;

      const item = round.resultItems[index];
      return {
        stepNo: index + 1,
        stepType: item.stepType,
        stepTypeLabel: STEP_TYPE_LABEL[item.stepType] || item.typeLabel || item.stepType,
        total,
      };
    },
    getStepTypeClass(stepType) {
      return {
        'is-query': stepType === 'query',
        'is-analyze': stepType === 'analyze',
        'is-compute': stepType === 'compute',
      };
    },
    isCollapsed(key) {
      return this.collapsedMap[key] ?? false;
    },
    toggleCollapse(key) {
      this.$set(this.collapsedMap, key, !this.isCollapsed(key));
    },
  },
};
</script>

<style lang="scss" scoped>
.query-panel {
  .query-panel__round {
    margin-bottom: 16px;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.answer {
  margin-top: 16px;

  .ai-avatar {
    width: 30px;
    height: 30px;
    margin-right: 10px;
    border-radius: 50%;
    object-fit: cover;
    background: #fff;
    flex-shrink: 0;
  }

  .answer-ai {
    display: flex;
    align-items: center;
    margin-bottom: 3px;
  }

  .ai-name {
    font-weight: 500;
    font-size: 16px;
    color: #222;
  }

  .answer-box {
    margin-left: 40px;
    display: flex;
    flex-flow: column;
    justify-content: flex-start;
    background: #fff;
    border: 1px solid #e8ecf2;
    border-radius: 4px 14px 14px 14px;
    padding: 16px 18px;
  }
}

.results-box {
  width: 100%;
  background: #fafbfe;
  border: 1px solid #e8ecf2;
  border-radius: 10px;
  padding: 10px 14px 0;
  margin-top: 12px;
  position: relative;

  &:hover {
    border-color: #bfdbfe;
    box-shadow: 0 2px 12px rgba(59, 130, 246, 0.06);
  }

  .results {
    width: calc(100% + 20px);
    margin-left: -10px;
    margin-right: -10px;
    margin-bottom: 10px;
    cursor: pointer;
    box-sizing: border-box;
  }

  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 10px;
  }

  .results-title {
    font-weight: 500;
    font-size: 16px;
    color: #0b0b0b;
    line-height: 24px;
    flex: 1;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0;
    min-width: 0;
  }

  .step-badges {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    flex: none;

    .step-no {
      background: #3b82f6;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      font-size: 10px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      color: #fff;
    }
  }

  .step-type {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    flex-shrink: 0;

    &.is-query {
      background: #dbeafe;
      color: #1d4ed8;
    }

    &.is-analyze {
      background: #f5f3ff;
      color: #7c3aed;
    }

    &.is-compute {
      background: #dbf0fc;
      color: #007eac;
    }
  }

  .question-text {
    flex: 1;
    font-size: 14px;
    font-weight: 400;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
  }

  .results-toggle {
    flex-shrink: 0;
    color: #94a3b8;
    font-size: 14px;
    margin-left: 12px;
  }

  .results-content {
    background: #fff;
    margin: 0 -14px;
    padding: 14px;
    padding-top: 15px;
    border-radius: 10px;
  }

  .results-content-box {
    border: 1px solid #e8ecf2;
    border-radius: 10px;
    overflow: hidden;
  }

  .results-content-box-content {
    padding: 10px;
    padding-top: 0;
  }
}

.qa-box {
  width: 100%;
  background: #f7f8fa;
  border-radius: 8px;
  border: 1px solid #e8eaed;
  overflow: hidden;
  margin-top: 12px;

  &:hover {
    border-color: #bfdbfe;
    box-shadow: 0 2px 12px rgba(59, 130, 246, 0.06);
  }

  .qa-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 14px;
    background: #fafbfe;
    border-bottom: 1px solid #e8eaed;
    gap: 8px;
  }

  .qa-header-left {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
    flex: 1;
  }

  .qa-number {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #3b82f6;
    color: #fff;
    font-size: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .qa-tag {
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    background: #ecfdf5;
    color: #047857;
    flex-shrink: 0;
  }

  .qa-title {
    font-weight: 400;
    font-size: 14px;
    color: #0b0b0b;
    line-height: 24px;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .qa-content {
    padding: 16px;
    background: #fff;
  }

  .qa-item {
    padding: 14px 16px;
    background: linear-gradient(135deg, #eff6ff, #f0fdfa);
    border: 1px solid #bae6fd;
    border-radius: 10px;
    font-size: 14px;
    line-height: 1.8;
    color: #475569;
    white-space: pre-wrap;
    word-break: break-all;
  }
}
</style>
