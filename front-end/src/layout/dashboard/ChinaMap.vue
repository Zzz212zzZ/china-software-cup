<template>
  <div class="content">
    <div ref="charts" class="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import china from '@/assets/json/china.json'
export default {
  data() {
    return {
      selectedPoint: this.getAreaNameFromWindTurbine(this.$store.state.selectedWindTurbine), // 初始化时选中的地名
      chart: null,
      windTurbineMapping: {
        '北京': '风机 1',
        '新疆': '风机 2',
        '四川': '风机 3',
        '甘肃': '风机 4',
        '云南': '风机 5',
        '广西': '风机 6',
        '湖南': '风机 7',
        '山东': '风机 8',
        '河南': '风机 9',
        '山西': '风机 10',
        '福建': '风机 11',
        '浙江': '风机 12',
        '江苏': '风机 13',
        '陕西': '风机 14',
        '广东': '风机 15',
        '重庆': '风机 16',
        '青海': '风机 17',
        '贵州': '风机 18',
        '吉林': '风机 19',
        '海南': '风机 20'
      },

      points: [
      { name: '北京', value: [116.407387, 39.904179] },
      { name: '新疆', value: [87.628579, 43.793301] },
      { name: '四川', value: [104.076452, 30.651696] },
      { name: '甘肃', value: [103.826777, 36.060634] },
      { name: '云南', value: [102.709372, 25.046432] },
      { name: '广西', value: [108.327537, 22.816659] },
      { name: '湖南', value: [112.982951, 28.116007] },
      { name: '山东', value: [117.020725, 36.670201] },
      { name: '河南', value: [113.753094, 34.767052] },
      { name: '山西', value: [112.578781, 37.813948] },
      { name: '福建', value: [119.296194, 26.101082] },
      { name: '浙江', value: [120.152575, 29.966619] },
      { name: '江苏', value: [119.763563, 32.061377] },
      { name: '陕西', value: [108.953939, 34.266611] },
      { name: '广东', value: [113.266887, 23.133306] },
      { name: '重庆', value: [107.551643, 29.562849] },
      { name: '青海', value: [97.780199, 36.620901] },
      { name: '贵州', value: [106.70546, 26.600055] },
      { name: '吉林', value: [125.32568, 43.897016] },
      { name: '海南', value: [110.349228, 20.017377] }
    ],
    }
  },
  mounted() {
    this.selectedPoint = this.getAreaNameFromWindTurbine(this.$store.state.selectedWindTurbine);
    // console.log(this.selectedPoint)
    this.points = this.points.map(point => {
      point.itemStyle = this.getItemStyle(point.name);
      return point;
    })
    this.initCharts()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    getAreaNameFromWindTurbine(windTurbine) {
      // 从风机名称映射回地名
      for (let area in this.windTurbineMapping) {
        if (this.windTurbineMapping[area] === windTurbine) {
          return area;
        }
      }
      return null;
    },
    getItemStyle(name) {
      return { color: name === this.selectedPoint ? '#F9B384' : '#00EEFF' };
    },
    initCharts() {
      this.chart = echarts.init(this.$refs['charts'])

      const option = {
        backgroundColor: '#0E2152',// 背景颜色
        geo: {// 地图配置
          map: 'china',
          label: { // 图形上的文本标签
            normal: {// 通常状态下的样式
              show: true,
              textStyle: {
                color: '#fff'
              }
            },
            emphasis: {// 鼠标放上去高亮的样式
              textStyle: {
                color: '#fff'
              }
            }
          },
          itemStyle: {// 地图区域的样式设置
            normal: { // 通常状态下的样式
              borderColor: '#5089EC',
              borderWidth: 1,
              areaColor: { //地图区域的颜色
                type: 'radial', // 径向渐变
                x: 0.5, // 圆心
                y: 0.5,// 圆心
                r: 0.8,// 半径
                colorStops: [
                  { // 0% 处的颜色
                    offset: 0,
                    color: 'rgba(0, 102, 154, 0)'
                  },
                  { // 100% 处的颜色
                    offset: 1,
                    color: 'rgba(0, 102, 154, .4)'
                  }
                ]
              }
            },
            // 鼠标放上去高亮的样式
            emphasis: {
              areaColor: '#2386AD',
              borderWidth: 0
            }
          }
        },
        series: [
          { // 散点系列数据
            type: 'effectScatter',// 带有涟漪特效动画的散点（气泡）图
            coordinateSystem: 'geo', //该系列使用的坐标系:地理坐标系
            // 特效类型,目前只支持涟漪特效'ripple'，意为“涟漪”
            effectType: 'ripple',
            // 配置何时显示特效。可选'render'和'emphasis' 。
            showEffectOn: 'render',
            rippleEffect: { // 涟漪特效相关配置。
              period: 10, // 动画的周期，秒数。
              scale: 4,// 动画中波纹的最大缩放比例。
              // 波纹的绘制方式，可选 'stroke' 和 'fill'。
              brushType: 'fill'
            },
            zlevel: 1, // 所有图形的 zlevel 值。
            data: this.points,
            itemStyle: {
              emphasis: {
                borderColor: '#fff',
                borderWidth: 3
              }
            },
          },
        ]
      }
      // 地图注册，第一个参数的名字必须和option.geo.map一致
      echarts.registerMap('china', china)
      this.chart.setOption(option)
      this.chart.on('click', (params) => {
        if (params.componentType === 'series') {
          this.selectedPoint = params.name;
          this.$store.commit('setSelectedWindTurbine', this.windTurbineMapping[params.name]);
          console.log(this.$store.state.selectedWindTurbine)  
          const newData = this.points.map(point => {
            point.itemStyle = this.getItemStyle(point.name);
            return point;
          })
          // Update the chart with the new data
          option.series[0].data = newData
          this.chart.setOption(option, true)
        }
      })


    },
    handleResize() {
      if (this.chart) {
        this.chart.resize();
        console.log('resize')
      }
    }
  }
}
</script>
<style scoped>
.content {
  background: transparent;
  width: 100%;
  height: 100%;
  position: fixed;
  overflow: auto;
  max-width: 700px;
  max-height: 500px;
  display: flex;
  /* 新增的代码 */
  justify-content: center;
  /* 新增的代码 */
  align-items: center;
  /* 新增的代码 */
  border: 4px solid #aec2f1;
  border-radius: 20px;
  /* 添加圆角，你可以根据需要更改数值 */
  box-shadow: 0 0 20px rgb(154, 151, 216); /* 新增的代码 */
}

.chart {
  background: transparent;
  width: 100%;
  height: 100%;
  max-width: 700px;
  max-height: 500px;
}
</style>
