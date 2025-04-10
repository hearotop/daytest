<script setup lang="ts">
import { ElHeader, ElMain, ElMenu, ElMenuItem } from 'element-plus';
import {  useRouter } from 'vue-router';

const router = useRouter();

const menuItems = [
  { path: '/', name: 'users', label: '用户管理' },
  { path: '/redis', name: 'redis', label: 'Redis 管理' },
];
const handleSelect = (key) => {
  router.push(key);
}
</script>

<template>
  <el-container>
    <el-header>
      <el-menu :router="true" mode="horizontal"    @select="handleSelect" >
  <el-menu-item
    v-for="item in menuItems"
    :key="item.path"
    :index="item.path"
  >
    {{ item.label }}
  </el-menu-item>
</el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped>
/* 添加样式 */
.el-header {
  background-color: #f0f0f0;
}
</style>