<script setup>
import {onMounted, ref} from 'vue';
import {deleteUserById, getUserList, addUser, updateUserAPI} from "@/api/user.js";
import {ElMessageBox} from "element-plus";
import { GENDER_MAP, formatter } from '@/utils/dict.js';
import { ElNotification } from 'element-plus';
const editDialogVisible = ref(false);
const isAddingUser = ref(false);
const editedUser = ref({});

// 使用 ref 创建响应式变量
const userList = ref([]);

const handleAddUser = () => {
  isAddingUser.value = true;
  editedUser.value = { 
    userId: null,
    nickName: '',
    phone: '',
    password: '123456',
    sex: 0,
    email: '' 
  };
  editDialogVisible.value = true;
}

const editUser = (row) => {
  console.log('editUser method triggered');
  editedUser.value = { ...row };
  console.log('Before setting editDialogVisible:', editDialogVisible.value);
  editDialogVisible.value = true;
  console.log('After setting editDialogVisible:', editDialogVisible.value);
};
const saveEditedUser = () => {
  if (isAddingUser.value) {
    addUser({
    nickName: editedUser.value.nickName,
    phone: editedUser.value.phone,
    sex: editedUser.value.sex,
    email: editedUser.value.email,
    password: editedUser.value.password
  }).then(res => {
      userList.value.push(res.data);
      editDialogVisible.value = false;
      isAddingUser.value = false;
      ElNotification({ title: '成功', message: '添加成功', type:'success' });
      getUserList().then(res => {
        userList.value = res.data;
      });
    }).catch(err => {
      console.error('添加失败:', err);
      ElNotification({ title: '失败', message: '添加失败', type:'error' });
    });
  } else {
    updateUserAPI( {
      userId: editedUser.value.userId,
      nickName: editedUser.value.nickName,
      phone: editedUser.value.phone,
      sex: editedUser.value.sex,
      email: editedUser.value.email,
      password: editedUser.value.password
    }).then(res => {
      const index = userList.value.findIndex(user => user.userId === editedUser.value.userId);
      if (index !== -1) {
        userList.value[index] = { ...editedUser.value };
      }
      editDialogVisible.value = false;
      ElNotification({ title: '成功', message: '更新成功', type:'success' });
    }).catch(err => {
      console.error('更新失败:', err);
      ElNotification({ title: '失败', message: '更新失败', type:'error' });
    });
  }
};

const deleteUser = (row) => {
  console.log('删除用户', row);
  ElMessageBox.confirm(
      '确定要删除该用户吗?',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
  ).then(() => {
console.log(row.userId);
    deleteUserById(row.userId).then(
        res => {
          console.log(res);
          if (res.data > 0) {
        
ElNotification({ title: '成功', message: '删除成功', type: 'success' });
            // 从 userList 中移除已删除的用户
            userList.value = userList.value.filter(user => user.userId !== row.userId);
          } else {
          
            ElNotification({ title: '失败', message: '删除失败', type:'error' });
          }
        }
    ).catch(
        err => {
          console.log(err);
          ElNotification({ title: '失败', message: '删除失败', type:'error' });
        }
    );
  }).catch(() => {
    console.log('取消删除');
  });
}


onMounted(()=>
    {
      console.log("Component mounted.");
      getUserList().then(
          res=>
          { 
            console.log(res);
            userList.value = res.data;
          }
      ).catch(
          err=>
          { 
            ElNotification({ title: '失败', message: '获取用户列表失败', type: 'error' });
            console.log(err);
          }
      )
    }
);
</script>

<template>
  <el-button type="primary" @click="handleAddUser">添加用户</el-button>
  <el-table :data="userList">
    <el-table-column prop="nickName" label="昵称" width="180"></el-table-column>
    <el-table-column prop="phone" label="电话" width="180"></el-table-column>
    <el-table-column 
      prop="sex" 
      label="性别" 
      width="180"
      :formatter="(row) => formatter(row.sex, GENDER_MAP)"
    ></el-table-column>
    <el-table-column prop="email" label="邮箱" width="180"></el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <el-button type="warning" @click="editUser(scope.row)">编辑</el-button>
        <el-button type="danger" @click="deleteUser(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog v-model="editDialogVisible" :title="isAddingUser ? '添加用户' : '编辑用户信息'">
    <el-form :model="editedUser">
      <el-form-item label="昵称">
        <el-input v-model="editedUser.nickName"></el-input>
      </el-form-item>
      <el-form-item label="电话">
        <el-input v-model="editedUser.phone"></el-input>
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="editedUser.sex">
          <el-option label="男" :value="0" />
          <el-option label="女" :value="1" />
        </el-select>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="editedUser.email"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="editedUser.password" show-password></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEditedUser">保存</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
/* 你的样式 */
</style>
