<template>
  <div>

    <div class="row">
      <div class="col-8">
        <div class="alert alert-warning" role="alert" v-if="stage === 'nodata'">
          尚未完成数据预处理，请先完成数据预处理
        </div>
        <!-- 参数控制 -->
        <card title="任务" subTitle="大家好啊，我是模型训练控制台" style="z-index: auto;">
          <div>
            <!-- 主变量 -->
            <div class="col-12 row">
              <label class="col-auto">主变量：</label>
              <div class="col-11 row">
                <div class="col-auto" v-for="variable in variables">
                  <input type="checkbox" v-model="primaryVars" name="primary" :value="variable"
                    :disabled="secondaryVars.includes(variable)">{{ variable }}
                </div>
              </div>

            </div>

            <!-- 副变量 -->
            <div class="col-12 row">
              <label class="col-auto">副变量：</label>
              <div class="col-11 row">
                <div class="col-auto" v-for="variable in variables">
                  <input type="checkbox" v-model="secondaryVars" name="secondary" :value="variable"
                    :disabled="primaryVars.includes(variable)">{{ variable }}
                </div>
              </div>
            </div>

            <div class="col-12 row">
              <div class="col-4" v-for="para in parameters">
                <label>{{ para.parameterName }}</label>
                <button class="dropdown-toggle underline" type="button" :id="para.parameterName" data-toggle="dropdown">
                  {{ para.default }}
                </button>
                <div class="dropdown-menu" :aria-labelledby="para.parameterName">
                  <div class="dropdown-item"
                    v-if="typeof para.values[0] === 'number' && typeof para.values[1] === 'number'">
                    <vue-slider v-model="para.default" :lazy="true" :min="para.values[0]" :max="para.values[1]"
                      :interval="para.interval"></vue-slider>
                  </div>
                  <div v-else>
                    <a class="dropdown-item" v-for="v in para.values" @click="para.default = v">{{ v }}</a>
                  </div>
                </div>

              </div>

            </div>
          </div>

          <!-- 分数 -->
          <!-- <div slot="footer">
            <h4>分数</h4>
            <h3 style="color: grey;">{{ score }}</h3>
          </div> -->
        </card>

        <echarts-card ref="mainChart" title="模型训练" sub-title="副标题" chartHeight="600px">
          <!-- <div  slot=""></div> -->

          <div slot="footer" class="row" style="padding-bottom: 10px;">
            <div class="col-10" style="padding-top: 20px;">
              <vue-slider ref="slider" v-model="samples" :max="dataLength" :process="dataProcess" :height="10" :data="data"
                :marks="marks" :enable-cross="false">
                <template v-slot:process="{ start, end, style, index }">
                  <div class="vue-slider-process" :style="style">
                    <div v-if="index !== 1 && index !== 3" :class="[
                      'merge-tooltip',
                      'vue-slider-dot-tooltip-inner',
                      'vue-slider-dot-tooltip-inner-top'
                    ]">
                      {{ samples[index + 1] - samples[index] }}
                    </div>
                    <div v-else-if="index === 3" :class="[
                      'merge-tooltip',
                      'vue-slider-dot-tooltip-inner',
                      'vue-slider-dot-tooltip-inner-top'
                    ]">
                      {{ dataLength - samples[index] }}
                    </div>
                  </div>
                </template>
              </vue-slider>
            </div>
            <div class="col-2">
              <button class="btn btn-primary btn-lg w-100" v-if="stage === 'trained'" @click="retrain()">重新训练</button>
              <button class="btn btn-primary btn-lg w-100" :disabled="stage === 'nodata' || stage==='training'" v-else @click="onTrain()"
              >开始训练
              </button>
            </div>

          </div>
        </echarts-card>
      </div>

      <div class="col-4">
        <echarts-card ref="verifyChart" title="验证集比较" sub-title="副标题" chartHeight="400px">

        </echarts-card>

        <echarts-card ref="predictionChart" title="预测结果" sub-title="副标题" chartHeight="400px">

        </echarts-card>
      </div>
    </div>


  </div>
</template>
<script>
import { ModelCard, EchartsCard, Card} from "@/components/index";
import VueSlider from 'vue-slider-component'
import Chartist from "chartist";
import {ElButton} from 'element-ui'

export default {
  components: {
    ModelCard,
    EchartsCard,
    Card,
    VueSlider,
  },


  data() {
    return {
      variables: [
        'WINDSPEED',
        'WINDDIRECTION',
        'TEMPERATURE',
        'HUMIDITY',
        'PRESSURE',
      ],

      parameters: [
        {
          parameterName: "Aggregation function",
          values: ["sum", "concat", "attention_sum"],
          default: "sum",
        },
        {
          parameterName: "embedding size",
          values: [0, 1],
          default: 0.5,
          interval: 0.01,
        },
        {
          parameterName: "GRU layers",
          values: [0, 1],
          default: 0.5,
          interval: 0.01,
        },
        {
          parameterName: "epoch",
          values: [0, 1],
          default: 0.5,
          interval: 0.01,
        },
        {
          parameterName: "batchsize",
          values: [0, 1],
          default: 0.5,
          interval: 0.01,
        },
        {
          parameterName: "learning rate",
          values: [0, 1],
          default: 0.5,
          interval: 0.01,
        },
      ],

      score: 1,
      primaryVars: [],
      secondaryVars: [],

      //进度条属性
      samples: [0, 7500, 8000, 9900],
      dataLength: 10000,
      dataProcess: dotPos => [
        [dotPos[0], dotPos[1]],
        [dotPos[1], dotPos[2], { backgroundColor: '#ccc' }],
        [dotPos[2], dotPos[3], { backgroundColor: 'yellow' }],
        [dotPos[3], 100, { backgroundColor: 'lightgreen' }],
      ],
      //状态
      stage: 'nodata' //nodata没有数据 untrain尚未训练 trained完成训练 training训练中
    }
  },

  computed: {
    points: function () {
      return [
        {
          value: 0,
          step: 10,
        },
        {
          value: this.dataLength - 100,
          step: 1,
        },
        {
          value: this.dataLength,
          step: 1,
        },
      ];
    },

    data: function () {
      let result = [];

      this.points.forEach((point, idx) => {
        const lastPointValue = this.points[this.points.length - 1].value;

        if (point.value === lastPointValue) {
          return;
        } else {
          const nextPoint = this.points[idx + 1];

          for (let i = point.value; i <= nextPoint.value; i += point.step) {
            result.push(i);
          }
        }
      });

      const uniqueValues = new Set(result);
      return [...uniqueValues];
    },
    marks: function () {
      return this.points.map(point => point.value);
    },

    hasError: function () {
      return !(typeof this.errorinfo === "undefined" || this.errorinfo === null || this.errorinfo.trim() === "")
    }
  },

  created() {
    this.initalize()
  },

  methods: {
    async initalize(){
      await this.getUnprocessedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine))
      setTimeout(() => {
          this.getTrainedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine));
        }, 500);
      
      // if(this.stage!=='trained'){
      // }
    },
    //获取模型未训练的数据
    getUnprocessedData(Number) {
      fetch(`http://127.0.0.1:5000/unprocessed_data?number=${Number}`)
        .then(response => response.json())
        .then(data => {
          if (data.hasOwnProperty('error')) {
            console.log(data['error'])
            this.stage = 'nodata'
            return
          }
          this.dataLength=data['length']

          this.stage = 'untrain'
          //处理数据

        })
        .catch(error => console.error(error));
    },
    onTrain() {
      if (this.primaryVars.length == 0) {
        this.$message({
          message: '主变量不能为空',
          type: 'warning'
        })
        return;
      }
      if (this.secondaryVars.length == 0) {
        this.$message({
          message: '副变量不能为空',
          type: 'warning'
        })
        return;
      }
      if (this.samples[1] - this.samples[0] < 1000) {
        this.$message({
          message: '训练集过小',
          type: 'warning'
        })
        return;
      }
      if (this.samples[3] - this.samples[2] < 1000) {
        this.$message({
          message: '验证集过小',
          type: 'warning'
        })
        return;
      }
      this.errorinfo = '';
      this.train()
    },
    //训练函数
    async train() {
      this.stage='training'
      const loading=this.$loading({
          lock: true,
          text: '正在训练模型，请勿退出',
        });
      await fetch(`http://127.0.0.1:5000/train`, {
        method: 'post',
        body: JSON.stringify({
          number: this.getWindTurbineName(this.$store.state.selectedWindTurbine),
          primaryVars: this.primaryVars,
          secondaryVars: this.secondaryVars,

          Aggregation_function: this.parameters[0].default,
          embedding_size: this.parameters[1].default,
          GRU_layers: this.parameters[2].default,
          epoch: this.parameters[3].default,
          batchsize: this.parameters[4].default,
          learning_rate: this.parameters[5].default,

          samples: this.samples,

          analyst:'rich'
        })
      }).then(response => response.json())
        .then(data => {
          console.log(data)
          this.$message({
            message: '训练完成',
            type: 'success'
          })

        })
      
      await this.getTrainedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine))
      loading.close()
      this.stage='trained'
    },
    getTrainedData(Number) {
      fetch(`http://127.0.0.1:5000/trained_data`, {
        method: 'post',
        body: JSON.stringify({
          number: Number,
          samples: this.samples,
          analyst:'rich'
        })
      })
        .then(response => response.json())
        .then(data => {
          console.log(data)
          if (data.hasOwnProperty('error')) {
            console.log(data['error'])
            return
          }

          this.stage = 'trained'
          //处理数据
        })
        .catch(error => console.error(error));
    },
    //重新训练
    retrain(){
      const analyst='rich'
      fetch(`http://127.0.0.1:5000/retrain?analyst=${analyst}`)
        .then(response => response.json())
        .then(data => {
          this.$message({
            message: '重新训练',
            type: 'success'
          })
          this.stage='untrain'
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

  watch: {
    'dataLength': {
      handler(newDatalength) {
        this.samples=[0,(this.dataLength- 2500)-((this.dataLength- 2500)%10),this.dataLength-2000-((this.dataLength- 2000)%10),this.dataLength-100]
        this.$refs.slider.control.setDotsValue(this.samples,true)
      }
    }
  }
};
</script>
<style>
.underline {
  background: transparent;
  border-bottom: 2px grey solid;
  border-top: 0px;
  border-left: 0px;
  border-right: 0px;
  width: 100%;
  display: flex;
}

.underline::after {
  margin-top: auto;
  margin-bottom: auto;
  margin-left: auto !important;
}

.merge-tooltip {
  position: absolute;
  left: 50%;
  bottom: 100%;
  transform: translate(-50%, -10px);
}

.button-tooltip {
  position: absolute !important;
  bottom: 100%;
  left: 50%;
  transform: translate(-50%, 0);
  width: fit-content;
  /* transform: translate(0%, -20px); */
}

.button-tooltip::after {
  bottom: 100%;
  left: 50%;
  transform: translate(-50%, 0);
  height: 0;
  width: 0;
  border-color: transparent;
  border-bottom-color: transparent;
  border-style: solid;
  border-width: 5px;
  border-bottom-color: inherit;
}
</style>
