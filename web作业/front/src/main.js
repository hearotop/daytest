
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router.js'
// 引入 echarts
import * as echarts from 'echarts'
import * as echartsGl   from "echarts-gl/lib/echarts-gl.js";

const app = createApp(App)
// 全局挂载 echarts
app.use(ElementPlus)
app.use(router)
// 全局挂载 echarts
app.config.globalProperties.$echarts = echarts
app.config.globalProperties.$echartsGl = echartsGl

app.mount('#app')
