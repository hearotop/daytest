<script setup>

import CarTraffic from "@/components/CarTraffic.vue";
import DayIncome from "@/components/DayIncome.vue";
import BigScreen from "@/components/PeopleTraffic.vue";
import  "@/assets/globe.css";
import Eather from "@/components/Eather.vue";
import CaseT from "@/components/CaseT.vue";
</script>

<template>
  <div class="container">
  <div class="traffic"> <BigScreen/><CarTraffic/></div>
  <div class="income"><DayIncome/><CaseT/></div>

  </div>
</template>

<style>
.traffic{
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}
.income{
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}
.container{
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

</style>