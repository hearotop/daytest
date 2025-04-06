<script setup>

import { onMounted, onUnmounted } from 'vue'
import { getCurrentInstance } from 'vue'

const { proxy } = getCurrentInstance()
const echarts = proxy.$echarts

onMounted(() => {
  var chartDom = document.getElementById('carT')
  var myChart = echarts.init(chartDom, 'dark')
  var option = {
    title: {
      text:'发车流量统计',//主标题文本
      left: 'center',
      textStyle:{ // 主标题样式
        fontSize: 20,
        color:"#fff"
      },

    },
    xAxis: {
      type: 'category',
      data: ['一', '二', '三', '四', '五', '六', '日'],
      fontSize: 15
    },
    yAxis: {
      type: 'value',
      fontSize: 15
    },
    series: [
      {
        data: [50, 60, 40, 50, 100, 120, 260],
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
  <div id="carT">

  </div>
</template>

<style>
#carT {
  height: 100%;
  width: 100%;
}
</style>