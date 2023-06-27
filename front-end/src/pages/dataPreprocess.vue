<template>
  <div>
    <div class="d-flex flex-column">
      <!--Charts-->
      <div class="row d-flex align-items-center">
        <div class="col-md-7 col-12 d-flex flex-column">
          <!-- 数据图 -->
          <div class="flex-grow-1">
            <EchartsCard ref="preprocessMain" title="数据散点图" sub-title="subtitle">

            </EchartsCard>
          </div>

          <!-- 参数控制 -->

          <Card ref="control" title="参数调整" subTitle="我是介绍信息">
            <div class="container">
              <div class="row align-items-center">

                <div class="row col-12">
                  <div class="row col-7">
                    <!--sigma值进度条-->
                    <div class="col-9 align-self-center">
                      <vue-slider v-model="sigma" :lazy="true" :min="0.5" :max="3" :interval="0.01" :hide-label="true"
                        :height="5">
                        <template v-slot:step="{ active }">
                          <div :class="['custom-step', { active }]"></div>
                        </template>
                      </vue-slider>
                    </div>
                    <div class="col-3 align-self-center">
                      <label>sigma</label>
                    </div>
                  </div>

                  <div class="btn-group btn-group-toggle col-5" data-toggle="buttons">
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
                </div>


                <div class="row col-12" style="margin-top: 5px;">
                  <div class="row col-7">
                    <!--死值进度条-->
                    <div class="col-9 align-self-center">
                      <vue-slider v-model="deadCount" :lazy="true" :min="2" :max="5" :interval="1" :hide-label="true"
                        :height="5">
                        <template v-slot:step="{ active }">
                          <div :class="['custom-step', { active }]"></div>
                        </template>
                      </vue-slider>
                    </div>
                    <div class="col-3 align-self-center">
                      <label>死值</label>
                    </div>
                  </div>

                  <div class="btn-group btn-group-toggle col-5" data-toggle="buttons">
                    <label class="btn btn-outline-primary active btn-sm">
                      <input type="radio" name="aValue" value="delete" v-model="aValueOption" autocomplete="off" checked>
                      删除A类值
                    </label>
                    <label class="btn btn-outline-primary btn-sm">
                      <input type="radio" name="aValue" value="fill" v-model="aValueOption" autocomplete="off"> 填充A类值
                    </label>
                  </div>
                </div>

                <div class="row col-12" style="margin-top: 5px;">
                  <div class="row col-7">
                    <!--步长进度条-->
                    <div class="col-9 align-self-center">
                      <vue-slider v-model="step" :lazy="true" :min="0.1" :max="1" :interval="0.1" :hide-label="true"
                        :height="5">
                        <template v-slot:step="{ active }">
                          <div :class="['custom-step', { active }]"></div>
                        </template>
                      </vue-slider>
                    </div>
                    <div class="col-3 align-self-center">
                      <label>步长</label>
                    </div>
                  </div>

                  <div class="btn-group btn-group-toggle col-5" data-toggle="buttons">
                    <label class="btn btn-outline-primary active btn-sm">
                      <input type="radio" name="bValue" value="delete" v-model="bValueOption" autocomplete="off" checked>
                      删除B类值
                    </label>
                    <label class="btn btn-outline-primary btn-sm">
                      <input type="radio" name="bValue" value="fill" v-model="bValueOption" autocomplete="off"> 填充B类值
                    </label>
                  </div>
                </div>
              </div>

              <div style="margin-top: 5px;">
                <button type="button" class="btn btn-primary  btn-lg btn-block">进行模型训练</button>
              </div>
            </div>
          </Card>

        </div>

        <div class="col-md-5 col-12 d-flex flex-column">
          <div class="flex-grow-1">
            <EchartsCard ref="abnormalPie" title="异常值比例" sub-title="subtitle" chartHeight="300px">

            </EchartsCard>
          </div>
          <div class="flex-grow-1">
            <EchartsCard ref="missingPie" title="缺失值比例" sub-title="subtitle" chartHeight="300px">

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
      deadCount: 3,
      step: 0.2,

      missingValueOption: 'delete',
      aValueOption: 'delete',
      bValueOption: 'delete'
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
    missingValueOption: {
      handler() {
        // this.getBinProcessedData()
      }
    },
    aValueOption: {
      handler() {
        // this.getBinProcessedData()
      }
    },
    bValueOption: {
      handler() {
        // this.getBinProcessedData()
      }
    },
    '$store.state.selectedWindTurbine': function () {
      this.getBinProcessedData()
    }
  },

  methods: {
    //获取bin算法处理结果
    getBinProcessedData() {
      this.fetchBinProcessedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine), this.sigma, this.deadCount, this.step, this.missingValueOption, this.aValueOption, this.bValueOption)
    },
    fetchBinProcessedData(number, sigma, deadCount, step, missingValueOption, aValueOption, bValueOption) {
      fetch(`http://127.0.0.1:5000/bin_data?number=${number}&sigma=${sigma}&deadCount=${deadCount}&step=${step}&missingValueOption=${missingValueOption}&aValueOption=${aValueOption}&bValueOption=${bValueOption}`)
        .then(response => response.json())
        .then(data => {
          console.log(data)
          //这里对数据进行操作
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
