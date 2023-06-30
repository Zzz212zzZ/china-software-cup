<template>
  <div>

    <div class="row">
      <div class="col-8">
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
          <div slot="footer" class="row">
            <div class="col-10">
              <vue-slider v-model="samples" :lazy="true" :max="dataLength" :process="dataProcess" :height="10"
                :data="data" :marks="marks"></vue-slider>
            </div>
            <div class="col-2">
                <button class="btn btn-primary btn-lg w-100">开始训练</button>
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
import { ModelCard, EchartsCard, Card } from "@/components/index";
import VueSlider from 'vue-slider-component'
import Chartist from "chartist";
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
      samples: [0, 9000, 9800, 9900],
      dataLength: 10000,
      dataProcess: dotPos => [
        [dotPos[0], dotPos[1]],
        [dotPos[2], dotPos[3], { backgroundColor: 'yellow' }],
        [dotPos[3], 100, { backgroundColor: 'lightgreen' }],
      ]
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
          value: this.dataLength - 200,
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
  },

  methods:{
    //获取模型未训练的数据
    getUnprocessedData(Number){
      fetch(`http://127.0.0.1:5000/unprocessedData?number=${Number}`)
        .then(response => response.json())
        .then(data => {
          //处理数据
        })
        .catch(error => console.error(error));
    },
    train(){
      fetch(`http://127.0.0.1:5000/train`,{
        method:'post',
        body:JSON.stringify({
          number: this.getWindTurbineName(),
          primaryVars: this.primaryVars,
          secondaryVars: this.secondaryVars,

          Aggregation_function:this.parameters[0].default,
          embedding_size:this.parameters[1].default,
          GRU_layers:this.parameters[2].default,
          epoch:this.parameters[3].default,
          batchsize:this.parameters[4].default,
          learning_rate:this.parameters[5].default,

          samples:this.samples
        })
      }).then(response => response.json())
      .then(data => {
          console.log(data)
          //输出处理成功/失败
        })
    },
    getTrainedData(Number){
      fetch(`http://127.0.0.1:5000/trainedData?number=${Number}`)
        .then(response => response.json())
        .then(data => {
          //处理数据
        })
        .catch(error => console.error(error));
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
</style>
