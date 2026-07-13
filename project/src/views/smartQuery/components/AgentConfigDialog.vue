<!-- 智能体配置弹窗：数据表与行业知识静态配置界面 -->
<template>
  <el-dialog :visible.sync="dialogVisible" :show-close="false" :close-on-click-modal="false" width="720px" top="8vh" append-to-body custom-class="agent-config-dialog smart-query" @close="handleClose">
    <div class="agent-config" v-loading="detailLoading">
      <div class="agent-config__header">
        <span class="agent-config__title">智能体配置</span>
        <div class="agent-config__tabs">
          <span :class="['agent-config__tab', {'is-active': activeTab === 'table'}]" @click="activeTab = 'table'">数据表</span>
          <span :class="['agent-config__tab', {'is-active': activeTab === 'knowledge'}]" @click="activeTab = 'knowledge'">行业知识</span>
        </div>
        <i class="el-icon-close agent-config__close" @click="handleClose" />
      </div>

      <!-- 数据表 -->
      <div v-show="activeTab === 'table'" class="agent-config__body">
        <div class="agent-config__form-row">
          <div class="agent-config__field agent-config__field--name">
            <label class="agent-config__label">智能体名称</label>
            <el-input v-model="form.name" placeholder="请输入智能体名称" />
          </div>
          <div class="agent-config__field agent-config__field--desc">
            <label class="agent-config__label">描述</label>
            <el-input v-model="form.description" placeholder="智能体用途描述..." />
          </div>
        </div>
        <div class="agent-config__form-row">
          <div class="agent-config__field agent-config__field--source">
            <label class="agent-config__label">数据源</label>
            <el-select v-model="form.sourceId" placeholder="请选择数据源" clearable :loading="dataSourceLoading" @change="handleSourceChange">
              <el-option v-for="item in dataSourceOptions" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </div>
          <div class="agent-config__field agent-config__field--search">
            <el-input v-model="tableSearch" placeholder="搜索表名..." prefix-icon="el-icon-search" :disabled="!form.sourceId" @input="handleTableSearch" />
          </div>
        </div>

        <div class="agent-config__transfer">
          <div class="agent-config__panel">
            <div class="agent-config__panel-header">
              <span>待选表</span>
              <span class="agent-config__panel-count">{{ pendingTables.length }}</span>
            </div>
            <div class="agent-config__panel-body" v-loading="tablesLoading">
              <div v-if="!form.sourceId" class="agent-config__panel-empty">请先选择数据源</div>
              <div v-else-if="!tablesLoading && !pendingTables.length" class="agent-config__panel-empty">暂无待选表</div>
              <ul v-else class="agent-config__panel-list">
                <li
                  v-for="item in pendingTables"
                  :key="item.relationId"
                  :class="['agent-config__panel-item', {'is-selected': pendingSelected.includes(item.relationId)}]"
                  @click="togglePendingSelect(item.relationId)"
                >
                  <span class="agent-config__panel-name">{{ item.tableName }}</span>
                  <span v-if="item.tableComment" class="agent-config__panel-comment">{{ item.relationComment }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="agent-config__transfer-actions">
            <el-button class="agent-config__transfer-btn" :disabled="!pendingSelected.length" @click="moveToSelected">
              <i class="el-icon-arrow-right" />
            </el-button>
            <el-button class="agent-config__transfer-btn" :disabled="!selectedSelected.length" @click="moveToPending">
              <i class="el-icon-arrow-left" />
            </el-button>
          </div>

          <div class="agent-config__panel">
            <div class="agent-config__panel-header">
              <span>已选表</span>
              <span class="agent-config__panel-count">{{ selectedTables.length }}</span>
            </div>
            <div class="agent-config__panel-body">
              <div v-if="!selectedTables.length" class="agent-config__panel-empty">暂未选择表</div>
              <ul v-else class="agent-config__panel-list">
                <li
                  v-for="item in selectedTables"
                  :key="getTableKey(item)"
                  :class="['agent-config__panel-item', {'is-selected': selectedSelected.includes(getTableKey(item))}]"
                  @click="toggleSelectedSelect(getTableKey(item))"
                >
                  <span class="agent-config__panel-name">{{ item.tableName }}</span>
                  <span v-if="item.tableComment" class="agent-config__panel-comment">{{ item.relationComment }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 行业知识 -->
      <div v-show="activeTab === 'knowledge'" class="agent-config__body">
        <div class="agent-config__knowledge-actions">
          <el-button type="primary" size="small" @click="addKnowledge">添加</el-button>
          <!-- <el-button size="small" @click="handleImport">导入</el-button> -->
        </div>
        <ul class="agent-config__knowledge-list">
          <li v-for="(item, index) in knowledgeList" :key="item.id" class="agent-config__knowledge-item">
            <span class="agent-config__knowledge-index">{{ index + 1 }}</span>
            <el-input v-model="item.content" type="textarea" :rows="2" placeholder="请输入行业知识..." class="agent-config__knowledge-input" />
            <i class="el-icon-close agent-config__knowledge-delete" @click="removeKnowledge(index)" />
          </li>
        </ul>
      </div>

      <div class="agent-config__footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="saveLoading" @click="handleSave">保存</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import {getCandidateTables, getAibodyInfo, saveAibody} from '@/api/smartQuery/aibody';
import {getDataSourcesListAPI} from '@/api/fieldMappingManager/fieldMappingAPI';

let knowledgeId = 3;

export default {
  name: 'AgentConfigDialog',
  props: {
    visible: {
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
      activeTab: 'table',
      form: {
        name: '',
        description: '',
        sourceId: null,
      },
      dataSourceOptions: [],
      dataSourceLoading: false,
      tablesLoading: false,
      detailLoading: false,
      saveLoading: false,
      agentDetail: null,
      tableSearch: '',
      searchTimer: null,
      pendingTables: [],
      selectedTables: [],
      pendingSelected: [],
      selectedSelected: [],
      knowledgeList: [],
      lastSourceId: null,
    };
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible;
      },
      set(val) {
        this.$emit('update:visible', val);
      },
    },
  },
  watch: {
    visible(val) {
      if (val) {
        this.initForm();
      }
    },
  },
  methods: {
    getAgentCode() {
      return this.agent?.aicode || this.agent?.code;
    },
    normalizeRelationItem(item, sourceId = null) {
      return {
        relationId: item.relationId ?? item.id ?? item.tableId,
        tableName: item.tableName ?? item.tableName ?? '',
        tableComment: item.tableComment ?? item.tableComment ?? '',
        relationType: item.type ?? item.relationType,
        sourceId: item.sourceId ?? sourceId,
      };
    },
    getTableKey(item) {
      return `${item.sourceId}-${item.relationId}`;
    },
    async initForm() {
      this.activeTab = 'table';
      this.agentDetail = null;
      this.form = {
        name: '',
        description: '',
        sourceId: null,
      };
      this.tableSearch = '';
      this.pendingTables = [];
      this.selectedTables = [];
      this.pendingSelected = [];
      this.selectedSelected = [];
      this.knowledgeList = [];
      this.lastSourceId = null;
      knowledgeId = 1;

      const code = this.getAgentCode();
      this.detailLoading = true;
      try {
        await this.fetchDataSources();
        if (code) {
          const res = await getAibodyInfo(code);
          this.applyDetail(res.data);
        }
      } catch (e) {
        if (code) {
          this.handleClose();
        }
      } finally {
        this.detailLoading = false;
      }
    },
    applyDetail(detail) {
      if (!detail) return;
      this.agentDetail = detail;
      this.form.name = detail.name || '';
      this.form.description = detail.description || '';

      const relations = detail.tableRelations || [];
      this.selectedTables = relations.map((rel, index) =>
        this.normalizeRelationItem({
          ...rel,
          relationId: rel.relationId ?? rel.id ?? rel.tableId ?? `rel-${index}`,
        })
      );

      const knowledge = detail.knowledgeList || [];
      this.knowledgeList = knowledge.map((item, index) => ({
        id: item.id || index + 1,
        content: item.knowledgeElement || '',
        knowledgeAlias: item.knowledgeAlias,
      }));
      knowledgeId = this.knowledgeList.length + 1;
    },
    async fetchDataSources() {
      this.dataSourceLoading = true;
      try {
        const res = await getDataSourcesListAPI();
        this.dataSourceOptions = res.data || [];
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.dataSourceLoading = false;
      }
    },
    handleSourceChange(sourceId) {
      const prevSourceId = this.lastSourceId;
      this.tableSearch = '';
      this.pendingTables = [];
      this.pendingSelected = [];
      this.selectedSelected = [];

      if (prevSourceId != null && prevSourceId !== sourceId) {
        this.selectedTables = [];
      }

      this.lastSourceId = sourceId ?? null;
      this.fetchCandidateTables();
    },
    handleTableSearch() {
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.fetchCandidateTables();
      }, 300);
    },
    async fetchCandidateTables() {
      if (!this.form.sourceId) {
        this.pendingTables = [];
        return;
      }
      this.tablesLoading = true;
      try {
        const res = await getCandidateTables({
          sourceId: this.form.sourceId,
          keyword: this.tableSearch || undefined,
        });
        const list = (res.data || []).map(item => this.normalizeRelationItem(item, this.form.sourceId));
        const selectedIds = this.selectedTables
          .filter(t => t.sourceId === this.form.sourceId)
          .map(t => t.relationId);
        this.pendingTables = list.filter(t => !selectedIds.includes(t.relationId));
        this.pendingSelected = [];
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.tablesLoading = false;
      }
    },
    togglePendingSelect(id) {
      const idx = this.pendingSelected.indexOf(id);
      if (idx > -1) {
        this.pendingSelected.splice(idx, 1);
      } else {
        this.pendingSelected.push(id);
      }
    },
    toggleSelectedSelect(id) {
      const idx = this.selectedSelected.indexOf(id);
      if (idx > -1) {
        this.selectedSelected.splice(idx, 1);
      } else {
        this.selectedSelected.push(id);
      }
    },
    moveToSelected() {
      const items = this.pendingTables
        .filter(t => this.pendingSelected.includes(t.relationId))
        .map(t => ({
          ...t,
          sourceId: this.form.sourceId,
        }));
      this.selectedTables.push(...items);
      this.pendingTables = this.pendingTables.filter(t => !this.pendingSelected.includes(t.relationId));
      this.pendingSelected = [];
    },
    moveToPending() {
      const keys = [...this.selectedSelected];
      const items = this.selectedTables.filter(t => keys.includes(this.getTableKey(t)));
      this.pendingTables.push(...items);
      this.selectedTables = this.selectedTables.filter(t => !keys.includes(this.getTableKey(t)));
      this.selectedSelected = [];
    },
    addKnowledge() {
      this.knowledgeList.push({id: knowledgeId++, content: ''});
    },
    removeKnowledge(index) {
      this.knowledgeList.splice(index, 1);
    },
    handleImport() {
      this.$message.info('导入功能待接入');
    },
    handleClose() {
      this.dialogVisible = false;
    },
    buildSavePayload() {
      const name = this.form.name?.trim();
      if (!name) {
        this.$message.warning('请输入智能体名称');
        return null;
      }

      const tableRelations = this.selectedTables.map(t => {
        const sourceId = t.sourceId || this.form.sourceId;
        if (!sourceId) {
          return null;
        }
        return {
          sourceId,
          relationId: t.relationId,
          tableName: t.tableName,
          relationType: t.relationType,
          tableComment: t.tableComment
        };
      });

      if (tableRelations.includes(null)) {
        this.$message.warning('关联表缺少数据源信息');
        return null;
      }

      const payload = {
        name,
        description: (this.form.description || '').trim(),
        tableRelations,
        knowledgeList: this.knowledgeList
          .filter(k => k.content && k.content.trim())
          .map(k => {
            const item = {knowledgeElement: k.content.trim()};
            if (k.knowledgeAlias) {
              item.knowledgeAlias = k.knowledgeAlias;
            }
            return item;
          }),
      };

      const aicode = this.agentDetail?.code || this.agentDetail?.aicode || this.getAgentCode();
      if (aicode) {
        payload.aicode = aicode;
      }

      return payload;
    },
    async handleSave() {
      const payload = this.buildSavePayload();
      if (!payload) return;

      this.saveLoading = true;
      try {
        await saveAibody(payload);
        this.$message.success('保存成功');
        this.$emit('saved');
        this.handleClose();
      } catch (e) {
        // 错误已在 request 拦截器中提示
      } finally {
        this.saveLoading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@use '../styles/variables.scss' as *;

.agent-config {
  .agent-config__header {
    display: flex;
    align-items: center;
    padding: 16px 20px 0;
    position: relative;
  }

  .agent-config__title {
    font-size: 16px;
    font-weight: 600;
    color: $text-primary;
    flex-shrink: 0;
  }

  .agent-config__tabs {
    flex: 1;
    display: flex;
    justify-content: center;
    gap: 32px;
  }

  .agent-config__tab {
    font-size: 14px;
    color: $text-regular;
    cursor: pointer;
    padding-bottom: 12px;
    border-bottom: 2px solid transparent;
    transition: color 0.2s, border-color 0.2s;

    &:hover {
      color: $primary-color;
    }

    &.is-active {
      color: $primary-color;
      border-bottom-color: $primary-color;
      font-weight: 500;
    }
  }

  .agent-config__close {
    font-size: 18px;
    color: $text-secondary;
    cursor: pointer;
    flex-shrink: 0;
    transition: color 0.2s;

    &:hover {
      color: $text-primary;
    }
  }

  .agent-config__body {
    padding: 20px 20px 0;
  }

  .agent-config__form-row {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
  }

  .agent-config__field {
    flex: 1;

    .agent-config__label {
      display: block;
      font-size: 13px;
      color: $text-regular;
      margin-bottom: 6px;
    }

    &--name {
      flex: 0 0 200px;
    }

    &--desc {
      flex: 1;
    }

    &--source {
      flex: 0 0 200px;
    }

    &--search {
      flex: 1;
      padding-top: 22px;
    }
  }

  .agent-config__transfer {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 4px;
  }

  .agent-config__panel {
    flex: 1;
    border: 1px solid $border-color;
    border-radius: 4px;
    overflow: hidden;
  }

  .agent-config__panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: #f5f7fa;
    border-bottom: 1px solid $border-color;
    font-size: 13px;
    color: $text-primary;
  }

  .agent-config__panel-count {
    font-size: 12px;
    color: $text-secondary;
  }

  .agent-config__panel-body {
    height: 240px;
    overflow-y: auto;
  }

  .agent-config__panel-empty {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    color: $text-secondary;
  }

  .agent-config__panel-list {
    list-style: none;
    margin: 0;
    padding: 4px 0;
  }

  .agent-config__panel-item {
    padding: 8px 12px;
    font-size: 13px;
    color: $text-regular;
    cursor: pointer;
    transition: background 0.2s;

    &:hover {
      background: rgba($primary-color, 0.06);
    }

    &.is-selected {
      background: $primary-light;
      color: $primary-color;
    }
  }

  .agent-config__panel-name {
    display: block;
    line-height: 1.4;
  }

  .agent-config__panel-comment {
    display: block;
    font-size: 12px;
    color: $text-secondary;
    line-height: 1.4;
    margin-top: 2px;
  }

  .agent-config__transfer-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-shrink: 0;
  }

  .agent-config__transfer-btn {
    width: 32px;
    height: 32px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .agent-config__knowledge-actions {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
  }

  .agent-config__knowledge-list {
    list-style: none;
    margin: 0;
    padding: 0;
    max-height: 360px;
    overflow-y: auto;
  }

  .agent-config__knowledge-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .agent-config__knowledge-index {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    line-height: 24px;
    text-align: center;
    border-radius: 50%;
    background: $primary-light;
    color: $primary-color;
    font-size: 12px;
    font-weight: 500;
    margin-top: 4px;
  }

  .agent-config__knowledge-input {
    flex: 1;
  }

  .agent-config__knowledge-delete {
    flex-shrink: 0;
    font-size: 16px;
    color: $text-secondary;
    cursor: pointer;
    margin-top: 6px;
    transition: color 0.2s;

    &:hover {
      color: #f56c6c;
    }
  }

  .agent-config__footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 16px 20px 20px;
  }
}
</style>

<style lang="scss">
.agent-config-dialog {
  border-radius: 8px;

  .el-dialog__header {
    display: none;
  }

  .el-dialog__body {
    padding: 0;
  }
}
</style>
