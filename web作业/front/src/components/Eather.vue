<script setup>
import { onMounted, onUnmounted } from 'vue'
import { getCurrentInstance } from 'vue'
import 'echarts-gl';


onMounted(() => {
  const { proxy } = getCurrentInstance();
  const echarts = proxy.$echarts
  var ROOT_PATH = 'src/assets';
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom, 'dark');
  var option;
  option = {
    backgroundColor: '#000',
    globe: {
      baseTexture: ROOT_PATH + '/world.topo.bathy.200401.jpg',
      heightTexture: ROOT_PATH + '/world.topo.bathy.200401.jpg',
      displacementScale: 0.04,
      shading: 'realistic',
      environment: ROOT_PATH + '/starfield.jpg',
      realisticMaterial: {
        roughness: 0.9
      },
      postEffect: {
        enable: true
      },
      light: {
        main: {
          intensity: 5,
          shadow: true
        },
        ambientCubemap: {
          texture: ROOT_PATH + '/data-gl/asset/pisa.hdr',
          diffuseIntensity: 0.2
        }
      }
    }
  };

  option && myChart.setOption(option);
})

onUnmounted(() => {
  window.removeEventListener('resize', myChart.resize);
  if (myChart) {
    myChart.dispose();
  }
})
</script>

<template>
  <div id="main"></div>
</template>

<style>
#main {
  width: 100%;
  height: 100%;
}
</style>
