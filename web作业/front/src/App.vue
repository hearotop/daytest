<script setup lang="ts">
import './assets/globe.css'

import View from "@/view/view.vue";
import Eather from "@/components/Eather.vue";
import Users from "@/view/users.vue";
</script>

<template>
  <div id="app">
    <div class="rcontainer">
    <div class="globe"> <Users/></div>
    </div>
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
