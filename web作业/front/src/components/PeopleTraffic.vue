<script setup>

import { onMounted, onUnmounted } from 'vue'
import { getCurrentInstance } from 'vue'

const { proxy } = getCurrentInstance()
const echarts = proxy.$echarts

onMounted(() => {
  var chartDom = document.getElementById('container')
  var myChart = echarts.init(chartDom, 'dark')
  var option = {
    title: {
      text:'周人流量统计',//主标题文本

     left: 'center',
      textStyle:{ // 主标题样式
        fontSize: 20,
        color:"#fff"
      },

    },
    xAxis: {
      type: 'category',
      data: ['一', '二', '三', '四', '五', '六', '日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line'
      }
    ]
  }

  option && myChart.setOption(option)

  window.addEventListener('resize', myChart.resize)
})

onUnmounted(() => {
  window.removeEventListener('resize', myChart.resize)
})
</script>

<template>
  <div id="container" >

  </div>
</template>

<style>
#container
{
  width: 100%;
  height: 100%;
}
</style>