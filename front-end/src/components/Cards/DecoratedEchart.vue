<template>
    <div class="decorated-echart">
      <div class="title-container">
        <h4 class="echart-title">{{ title }}</h4>
      </div>
      <div ref="echarts" class="echarts-chart" :style="{height: chartHeight}"></div>
    </div>
</template>
  
  <script>
  import * as echarts from "echarts";
  import ecStat from "echarts-stat";
  
  export default {
    name: "DecoratedEchart",
    props: {
      title: {
        type: String,
        default: "",
      },
      chartOptions: {
        type: Object,
        default: () => {
          return {};
        },
      },
      chartHeight: {
        type: String,
        default: '200px'
      }
    },
    data() {
      return {
        chartInstance: null
      };
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
      initEcharts() {
        const chartDom = this.$refs.echarts;
        this.chartInstance = echarts.init(chartDom);
        this.chartInstance.setOption(this.chartOptions);
      },
      handleResize() {
        if (this.chartInstance) {
          this.chartInstance.resize();
        }
      },
      setOption() {
        this.chartInstance.setOption(this.chartOptions);
      }
    },
  };
  </script>
  
  <style scoped>
  .decorated-echart {
    width: 100%;
  }
  .echarts-chart {
    width: 100%;
  }

  .echart-title {
  text-align: center;
}

  </style>
  