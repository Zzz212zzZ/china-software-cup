<template>
  <div>
    <div class="d-flex flex-column">
      <!--Charts-->
      <div class="row d-flex align-items-center">
        <div class="col-md-7 col-12 d-flex flex-column">
          <!-- 数据图 -->
          <div class="flex-grow-1">
            <EchartsCard ref="preprocessMain" title="风速-功率曲线图"
              sub-title="正常数据表示满足风速-功率曲线规律的数据；甲类异常点表示长时间保持完全停滞的数据；乙类异常点表示不满足风速-功率曲线的数据" :chart-options="windPowerOption"
              chartHeight="600px">

            </EchartsCard>
          </div>

          <div class="row">
            <!-- 参数控制 -->
            <div class="col-6">
              <Card ref="control" title="参数调整" subTitle="本模型采用bin算法修正风速-功率曲线，异常阈值和区间宽度为bin算法参数；停滞阈值表示能够容忍数据停滞的最大时间点步数">
                <div class=" no-gutters">
                  <div class="row align-items-center col-12 no-gutters">

                    <div class="row col-12">
                      <!--sigma值进度条-->
                      <div class="col-8 align-self-center">
                        <vue-slider v-model="sigma" :lazy="true" :min="0.5" :max="3" :interval="0.01" :hide-label="true"
                          :height="5">
                          <template v-slot:step="{ active }">
                            <div :class="['custom-step', { active }]"></div>
                          </template>
                        </vue-slider>
                      </div>
                      <div class="col-4 align-self-center">
                        <label>异常阈值</label>
                      </div>

                    </div>


                    <div class="row col-12" style="margin-top: 10px;">
                      <!--停滞阈值进度条-->
                      <div class="col-8 align-self-center">
                        <vue-slider v-model="deadCount" :lazy="true" :min="3" :max="20" :interval="1" :hide-label="true"
                          :height="5">
                          <template v-slot:step="{ active }">
                            <div :class="['custom-step', { active }]"></div>
                          </template>
                        </vue-slider>
                      </div>
                      <div class="col-4 align-self-center">
                        <label>停滞阈值</label>
                      </div>


                    </div>

                    <div class="row col-12" style="margin-top: 10px;">
                      <!--bin算法区间进度条-->
                      <div class="col-8 align-self-center">
                        <vue-slider v-model="step" :lazy="true" :min="0.1" :max="1" :interval="0.1" :hide-label="true"
                          :height="5">
                          <template v-slot:step="{ active }">
                            <div :class="['custom-step', { active }]"></div>
                          </template>
                        </vue-slider>
                      </div>
                      <div class="col-4 align-self-center">
                        <label>区间宽度</label>
                      </div>


                    </div>
                  </div>

                </div>
              </Card>
            </div>
            <div class="col-6">
              <Card title="处理调整" subTitle="提交参数调整">
                <div>
                  <div class="btn-group btn-group-toggle col" data-toggle="buttons">
                    <label class="btn btn-outline-primary active btn-sm">
                      <input type="radio" name="missingValue" value="delete" v-model="missingValueOption"
                        autocomplete="off" checked> 删除缺失值
                    </label>
                    <label class="btn btn-outline-primary btn-sm">
                      <input type="radio" name="missingValue" value="fill" v-model="missingValueOption"
                        autocomplete="off">
                      填充缺失值
                    </label>
                  </div>

                  <div class="btn-group btn-group-toggle col" data-toggle="buttons" style="margin-top: 10px;">
                    <label class="btn btn-outline-primary active btn-sm">
                      <input type="radio" name="aValue" value="delete" v-model="aValueOption" autocomplete="off" checked>
                      删除A类值
                    </label>
                    <label class="btn btn-outline-primary btn-sm">
                      <input type="radio" name="aValue" value="fill" v-model="aValueOption" autocomplete="off"> 填充A类值
                    </label>
                  </div>

                  <div class="btn-group btn-group-toggle col" data-toggle="buttons" style="margin-top: 10px;">
                    <label class="btn btn-outline-primary active btn-sm">
                      <input type="radio" name="bValue" value="delete" v-model="bValueOption" autocomplete="off" checked>
                      删除B类值
                    </label>
                    <label class="btn btn-outline-primary btn-sm">
                      <input type="radio" name="bValue" value="fill" v-model="bValueOption" autocomplete="off"> 填充B类值
                    </label>
                  </div>

                  <div style="margin-top: 10px;" class="col-12">
                    <button type="button" class="btn btn-primary btn-block" @click="doDataProcess()">进行模型训练</button>
                  </div>
                </div>
              </Card>
            </div>
          </div>

        </div>

        <div class="col-md-5 col-12 d-flex flex-column">
          <div class="flex-grow-1">
            <EchartsCard ref="abnormalPie" title="异常值比例" sub-title="甲类和乙类异常点的数量，用以分析随参数变化，异常点的占比情况" chartHeight="400px"
              :chart-options="abnormalOption">

            </EchartsCard>
          </div>
          <div class="flex-grow-1">
            <EchartsCard ref="missingPie" title="缺失值比例" sub-title="数据缺失值的占比情况" chartHeight="400px"
              :chart-options="missingOption">

            </EchartsCard>
          </div>
        </div>
      </div>


    </div>
  </div>
</template>
<script>
import { Card, EchartsCard } from "@/components/index";
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import Chartist from "chartist";
export default {
  components: {
    Card,
    EchartsCard,
    VueSlider
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */
  data() {
    return {
      sigma: 2,
      // sigmaMarks: [1, 2, 3],
      deadCount: 8,
      step: 0.2,

      missingValueOption: 'delete',
      aValueOption: 'delete',
      bValueOption: 'delete',


      windPowerOption: {
        xAxis: {},
        yAxis: {},
        legend: {
          data: ['正常数据', '甲类异常数据', '乙类异常数据'] // 设置图例名称
        },
        series: [
          {
            name: '甲类异常数据',
            type: 'scatter',
            data: [],
            symbolSize: 7,
            itemStyle: {
              color: '#F3BB45'
            },
            large: true,
            largeThreshold: 500
          },
          {
            name: '乙类异常数据',
            type: 'scatter',
            data: [],
            symbolSize: 7,
            itemStyle: {
              color: '#EB5E28'
            },
            large: true,
            largeThreshold: 500
          },
          {
            name: '正常数据',
            type: 'scatter',
            data: [],
            symbolSize: 7,
            itemStyle: {
              color: '#68B3C8'
            },
            large: true,
            largeThreshold: 500
          },
        ],
      },

      abnormalOption: {
        tooltip: {
          trigger: 'item'
        },
        // legend: {
        //   orient: 'vertical',
        //   left: 'left'
        // },
        series: [
          {
            name: '各类数据点数量',
            type: 'pie',
            radius: '70%',
            color: ['#68B3C8', '#F3BB45', '#EB5E28'],
            data: [
              { value: 0, name: '正常数据量' },
              { value: 0, name: '甲类异常数据量' },
              { value: 0, name: '乙类异常数据量' },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },

      missingOption: {
        tooltip: {
          trigger: 'item'
        },
        series: [
          {
            name: '缺失数据量占比',
            type: 'pie',
            radius: '70%',
            color: ['#68B3C8', '#EB5E28'],
            data: [
              { value: 0, name: '完整数据量' },
              { value: 0, name: '缺失数据量' },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },


    };
  },

  created() {
    this.getBinProcessedData()
  },
  watch: {
    sigma: {
      handler() {
        this.getBinProcessedData()
      }
    },
    deadCount: {
      handler() {
        this.getBinProcessedData()
      }
    },
    step: {
      handler() {
        this.getBinProcessedData()
      }
    },
    '$store.state.selectedWindTurbine': function () {
      this.getBinProcessedData()
    },
    //风速功率曲线重渲染
    'windPowerOption': {
      handler() {
        const preprocessMain = this.$refs.preprocessMain;
        const abnormalPie = this.$refs.abnormalPie;
        const missingPie = this.$refs.missingPie;
        if (preprocessMain && preprocessMain.setOption) {
          preprocessMain.setOption(this.windPowerOption); //更新风速功率曲线图
        }
        if (abnormalPie && abnormalPie.setOption) {
          abnormalPie.setOption(this.abnormalOption); //更新
        }
        if (missingPie && missingPie.setOption) {
          missingPie.setOption(this.missingOption); //更新
        }
      },
      deep: true
    }
  },

  methods: {
    //获取bin算法处理结果
    getBinProcessedData() {
      this.fetchBinProcessedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine), this.sigma, this.deadCount, this.step, this.missingValueOption, this.aValueOption, this.bValueOption)
    },
    fetchBinProcessedData(number, sigma, deadCount, step, missingValueOption, aValueOption, bValueOption) {
      fetch(`http://127.0.0.1:5000/bin_data?number=${number}&sigma=${sigma}&deadCount=${deadCount}&step=${step}`)
        .then(response => response.json())
        .then(data => {
          console.log(data)
          this.windPowerOption.series[2].data = data['bin_data'];
          this.windPowerOption.series[0].data = data['a_data'];
          this.windPowerOption.series[1].data = data['b_data']
          this.abnormalOption.series[0].data[0].value = data['bin_data_percentage']
          this.abnormalOption.series[0].data[1].value = data['a_data_percentage']
          this.abnormalOption.series[0].data[2].value = data['b_data_percentage']
          this.missingOption.series[0].data[0].value = data['not_missing_percentage']
          this.missingOption.series[0].data[1].value = data['missing_percentage']
          //这里对数据进行操作
        })
    },
    //完成数据预处理，进入模型训练
    doDataProcess() {
      const missingValueOption = this.missingValueOption
      const aValueOption = this.aValueOption
      const bValueOption = this.bValueOption

      fetch(`http://127.0.0.1:5000/do_data_process?missingValueOption=${missingValueOption}&aValueOption=${aValueOption}&bValueOption=${bValueOption}`)
        .then(response => response.json())
        .then(data => {
          console.log(data)
          console.log('进入模型训练')
          this.$router.push('/modelTrain')
        })
        
    },
    //获取风机名称封装函数
    getWindTurbineName(windTurbineName) {
      windTurbineName = windTurbineName.slice(3);
      //如果windTurbineNumber编号为单个数字，前面加0
      if (windTurbineName.length == 1) {
        windTurbineName = '0' + windTurbineName;
      }
      return windTurbineName
    },
  },
};
</script>

<style>
.custom-step {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  box-shadow: 0 0 0 3px #ccc;
  background-color: #fff;
}

.custom-step.active {
  box-shadow: 0 0 0 3px #3498db;
  background-color: #3498db;
}
</style>
