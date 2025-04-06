<script setup>
import { onMounted, onUnmounted } from 'vue'
import { getCurrentInstance } from 'vue'
import * as myChart from "echarts";

const { proxy } = getCurrentInstance()
const echarts = proxy.$echarts
onMounted(() => {
      var chartDom = document.getElementById('incomeC');
      var myChart = echarts.init(chartDom, 'dark');
      var option;
  option = {
    title: {
      text:'收入流量统计',//主标题文本
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
        data: [
          120,
          {
            value: 200,
            itemStyle: {
              color: '#a90000'
            }
          },
          150,
          80,
          70,
          110,
          130
        ],
        type: 'bar'
      }
    ]
  };

  option && myChart.setOption(option);
}
)
onUnmounted(() => {
  myChart.dispose();
})
</script>

<template>
<div id="incomeC" ></div>
</template>

<style>
#incomeC
{
  width: 100%;
  height: 100%;
}
</style>
