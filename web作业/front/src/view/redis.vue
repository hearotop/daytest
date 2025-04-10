<script setup>
import {onMounted, ref} from 'vue';
import { getRedisList, addRedisItem, deleteRedisItem, updateRedisItem } from '@/api/redis.js';

import {ElMessageBox} from 'element-plus';
import { ElNotification } from 'element-plus';
const editDialogVisible = ref(false);
const isAddingRedisItem = ref(false);
const editedRedisItem = ref({});

// 使用 ref 创建响应式变量
const redisList = ref([]);

const handleAddRedisItem = () => {
  isAddingRedisItem.value = true;
  editedRedisItem.value = {
    id: null,
    key: '',
    value: ''
  };
  editDialogVisible.value = true;
}

const editRedisItem = (row) => {
  console.log('editRedisItem method triggered');
  editedRedisItem.value = {...row};
  console.log('Before setting editDialogVisible:', editDialogVisible.value);
  editDialogVisible.value = true;
  console.log('After setting editDialogVisible:', editDialogVisible.value);
};
const saveEditedRedisItem = () => {
  if (isAddingRedisItem.value) {
    addRedisItem({
      key: editedRedisItem.value.key,
      value: editedRedisItem.value.value
    }).then(res => {
      redisList.value.push(res.data);
      editDialogVisible.value = false;
      isAddingRedisItem.value = false;
      ElNotification({ title: '成功', message: '添加成功', type:'success' });
      getRedisList().then(res => {
        redisList.value = res.data;
      });
    }).catch(err => {
      console.error('添加失败:', err);
      ElNotification({ title: '失败', message: '添加失败', type: 'error' });
    });
  } else {
    updateRedisItem({
      id: editedRedisItem.value.id,
      key: editedRedisItem.value.key,
      value: editedRedisItem.value.value
    }).then(res => {
      if (res.data) {
        const index = redisList.value.findIndex(item => item.id === editedRedisItem.value.id);
        if (index!== -1) {
          redisList.value[index] = {...editedRedisItem.value};
        }
        editDialogVisible.value = false;
        ElNotification({ title: '成功', message: '更新成功', type:'success' });
      } else {
        console.error('更新失败');
        ElNotification({ title: '失败', message: '更新失败', type: 'error' });
      }
    }).catch(err => {
      console.error('更新失败:', err);
      ElNotification({ title: '失败', message: '更新失败', type: 'error' });
    });
  }
};

const deleteRedisItemAction = (row) => {
  console.log('删除Redis项', row);
  ElMessageBox.confirm(
    '确定要删除该项吗?',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    console.log(row.key);
    deleteRedisItem(row.key).then(
      res => {
        console.log(res);
        if (res.data > 0) {
          ElNotification({ title: '成功', message: '删除成功', type: 'success' });
          // 从 redisList 中移除已删除的项
          redisList.value = redisList.value.filter(item => item.key!== row.key);
        } else {
          ElNotification({ title: '失败', message: '删除失败', type: 'error' });
        }
      }
    ).catch(
      err => {
        console.log(err);
        ElNotification({ title: '失败', message: '删除失败', type: 'error' });
      }
    );
  }).catch(() => {
    console.log('取消删除');
  });
}

onMounted(() => {
  console.log('Component mounted.');
  getRedisList().then(
    res => {
      console.log(res);
      redisList.value = res.data;
    }
  ).catch(
    err => {
      console.error('获取Redis列表失败:', err);
      ElNotification({ title: '失败', message: '获取Redis列表失败', type: 'error' });
      console.log(err);
    }
  );
});
</script>

<template>
  <el-button type="primary" @click="handleAddRedisItem">添加Redis项</el-button>
  <el-table :data="redisList">
    <el-table-column type="index" label="序号" width="50"></el-table-column>
    <el-table-column prop="key" label="名称" width="180"></el-table-column>
    <el-table-column prop="value" label="值" width="180"></el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <el-button type="warning" @click="editRedisItem(scope.row)">编辑</el-button>
        <el-button type="danger" @click="deleteRedisItemAction(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog v-model="editDialogVisible" :title="isAddingRedisItem? '添加Redis项' : '编辑Redis项信息'">
    <el-form :model="editedRedisItem">
      <el-form-item label="名称">
        <el-input v-model="editedRedisItem.key" :disabled="!isAddingRedisItem"></el-input>
      </el-form-item>
      <el-form-item label="值">
        <el-input v-model="editedRedisItem.value"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEditedRedisItem">保存</el-button>
      </span>
    </template>
  </el-dialog>
</template>

