<template>
    <card>
        <template #header>
            <h4 v-if="$slots.title || title" class="card-title">
                <slot name="title">
                    {{ title }}
                </slot>
            </h4>
            <p class="card-category">
                <slot name="subTitle">
                    {{ subTitle }}
                </slot>
            </p>
        </template>
        <div>
            <div ref="echarts" class="echarts-chart" :style="{height: chartHeight}"></div>
            <div> <!-- 这里用footer类会导致进度条显示错误 -->
                <div class="chart-legend" v-if="$slots.legend">
                    <slot name="legend"></slot>
                </div>
                <hr />
                <div class="stats">
                    <slot name="footer"></slot>
                </div>
                <div class="pull-right"></div>
            </div>
        </div>
    </card>
</template>
  
<script>
import Card from "./Card.vue";
import * as echarts from "echarts";
import ecStat from "echarts-stat"
export default {
    name: "echarts-card",
    components: {
        Card,
    },
    props: {
        title: {
            type: String,
            default: "",
        },
        subTitle: {
            type: String,
            default: "",
        },
        chartOptions: {
            type: Object,
            default: () => {
                return {};
            },
        },
        chartHeight: { // 添加chartHeight属性
            type: String,
            default: '400px'
        }
    },
    data(){
        return{
            chartInstance: null // 添加此行来存储图表实例}
    }
    },
    mounted() {
        echarts.registerTransform(ecStat.transform.histogram); 
        this.initEcharts();
        window.addEventListener("resize", this.handleResize);
    },
    beforeUnmount() {
        window.removeEventListener("resize", this.handleResize);
    },
   
    methods: {
        // 初始化图片
        initEcharts() {
            const chartDom = this.$refs.echarts;
            this.chartInstance = echarts.init(chartDom);
            this.chartInstance.setOption(this.chartOptions);
            console.log(this.chartOptions)
        },
        handleResize() {
            if (this.chartInstance) {
                this.chartInstance.resize();
            }
        },
        setOption(){
            this.chartInstance.setOption(this.chartOptions);
        }
    },
    

};
</script>
  
<style>

</style>
  