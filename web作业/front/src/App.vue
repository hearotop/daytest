<script setup lang="ts">
import './assets/globe.css'
</script>

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<style>
.globe
{
  width: 100%;
  height: 100%;
}
.center {
 width: 100%;
  height: 100%;
}
#app {
  width: 100%;
  color: #2c3e50;
padding: 0;
  margin: 0 auto;
  background: #100C2A;

}
.rcontainer{
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}
</style>
