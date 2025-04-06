<script setup>

import { onMounted, onUnmounted } from 'vue'
import { getCurrentInstance } from 'vue'

const { proxy } = getCurrentInstance()
const echarts = proxy.$echarts

onMounted(() => {

  var chartDom = document.getElementById('tousuT');
  var myChart = echarts.init(chartDom, 'dark');
  var option;

  let base = +new Date(2025, 1, 3);
  let oneDay = 24 * 3600 * 1000;
  let date = [];
  let data = [Math.random() * 300];
  for (let i = 1; i < 2000; i++) {
    var now = new Date((base += oneDay));
    date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
    data.push(Math.round((Math.random() - 0.5) * 20 + data[i - 1]));
  }
  option = {
    tooltip: {
      trigger: 'axis',
      position: function (pt) {
        return [pt[0], '10%'];
      }
    },
    title: {
      left: 'center',
      text: '投诉量',
      textStyle:{ // 主标题样式
        fontSize: 20,
        color:"#fff"
      },
    },
    toolbox: {
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        restore: {},
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: date
    },
    yAxis: {
      type: 'value',
      boundaryGap: [0, '100%']
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 10
      },
      {
        start: 0,
        end: 10
      }
    ],
    series: [
      {
        name: 'Fake Data',
        type: 'line',
        symbol: 'none',
        sampling: 'lttb',
        itemStyle: {
          color: 'rgb(255, 70, 131)'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgb(255, 158, 68)'
            },
            {
              offset: 1,
              color: 'rgb(255, 70, 131)'
            }
          ])
        },
        data: data
      }
    ]
  };

  option && myChart.setOption(option);

})

onUnmounted(() => {
  window.removeEventListener('resize', myChart.resize)
})
</script>

<template>
  <div id="tousuT">

  </div>
</template>

<style>
#tousuT {
  height: 100%;
  width: 100%;
}
</style>