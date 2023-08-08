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
      selectedPoint: { longitude: null, latitude: null },
      chart: null,
      windTurbineMapping: {},
      points: [],
    }
  },
  created() {
    console.log("created")
    // 从后端获取风机名称和地名的映射
    this.getWindTurbines();
  },



  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    getWindTurbines() {
      fetch(`http://127.0.0.1:5000/get_datasets`, {
        headers: {
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          // 将数据转换为地图组件所需的格式
          this.points = data.map(item => {
            return {
              name: item.dataset_name,
              value: [item.longitude, item.latitude]
            };
          });

          // 更新风机映射
          this.windTurbineMapping = data.reduce((mapping, item) => {
            mapping[item.dataset_name] = { longitude: item.longitude, latitude: item.latitude };
            return mapping;
          }, {});


          // 初始化选中的经纬度
          const windTurbine = this.$store.state.selectedWindTurbine;
          const selectedTurbine = data.find(item => item.dataset_name === windTurbine);
          if (selectedTurbine) {
            this.selectedPoint = {
              longitude: selectedTurbine.longitude,
              latitude: selectedTurbine.latitude
            };
          }

          console.log(this.selectedPoint)

          this.points = this.points.map(point => {
            point.itemStyle = this.getItemStyle(point.name);
            return point;
          })
          this.initCharts()
          window.addEventListener('resize', this.handleResize)
        });
    },


    getItemStyle(name) {
      const point = this.points.find(point => point.name === name);
      if (point && point.value[0] === this.selectedPoint.longitude && point.value[1] === this.selectedPoint.latitude) {
        return { color: '#F9B384' };
      }
      return { color: '#00EEFF' };
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
          const [longitude, latitude] = params.value;
          this.selectedPoint = { longitude, latitude };

          // 找到对应的风机数据
          const selectedTurbine = Object.keys(this.windTurbineMapping).find(
            key => this.windTurbineMapping[key].longitude === longitude && this.windTurbineMapping[key].latitude === latitude
          );

          // 如果找到了对应的风机数据，更新全局状态
          if (selectedTurbine) {
            this.$store.commit('setSelectedWindTurbine', selectedTurbine);
          }

          // 创建新的points数组
          const newData = this.points.map(point => {
            point.itemStyle = this.getItemStyle(point.name);
            return point;
          });

          // 更新图表选项
          option.series[0].data = newData;
          this.chart.setOption(option, true);
        }
      });



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
  box-shadow: 0 0 20px rgb(154, 151, 216);
  /* 新增的代码 */
}

.chart {
  background: transparent;
  width: 100%;
  height: 100%;
  max-width: 700px;
  max-height: 500px;
}
</style>
