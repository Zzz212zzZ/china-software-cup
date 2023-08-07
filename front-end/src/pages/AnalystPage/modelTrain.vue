<template>
  <div>
    <div class="alert alert-warning" role="alert" v-if="stage === 'nodata'">
      尚未完成数据预处理，请先完成数据预处理
    </div>
    <div class="row">
      <div class="col-md col-12">
        <!-- 参数控制 -->
        <double-card title_1="神经网络参数调整" subTitle_1="调整神经网络相关模型参数" title_2="随机森林参数调整" subTitle_2="调整神经网络相关模型参数"
          style="z-index: auto;">
          <div>
            <!-- 主变量 -->
            <div class="col-12 row">
              <label class="col-auto">主变量：</label>
              <div class="col row">
                <div class="col-auto" v-for="variable in variables">
                  <input type="checkbox" v-model="primaryVars" name="primary" :value="variable"
                    :disabled="secondaryVars.includes(variable) || stage === 'trained'">{{ variable }}
                </div>
              </div>

            </div>

            <!-- 副变量 -->
            <div class="col-12 row">
              <label class="col-auto">副变量：</label>
              <div class="col row">
                <div class="col-auto" v-for="variable in variables">
                  <input type="checkbox" v-model="secondaryVars" name="secondary" :value="variable"
                    :disabled="primaryVars.includes(variable) || stage === 'trained'">{{ variable }}
                </div>
              </div>
            </div>
            <!-- nn参数 -->
            <div class="col-12 row">
              <div class="col-4" v-for="para in parameters">
                <label>{{ para.parameterName }}</label>

                <el-dropdown class="w-100"
                  :hide-on-click="!(typeof para.values[0] === 'number' && typeof para.values[1] === 'number')"
                  trigger="click">
                  <button class="underline" type="button" :id="para.parameterName" :disabled="stage === 'trained'">
                    {{ para.default }}<i class="el-icon-arrow-down el-icon--right underline-arrow"></i>
                  </button>
                  <el-dropdown-menu slot="dropdown" :aria-labelledby="para.parameterName" style="width: 350px;">
                    <el-dropdown-item class="row"
                      v-if="typeof para.values[0] === 'number' && typeof para.values[1] === 'number'">
                      <div class="col-12">
                        <el-slider class="ailgn-center" v-model="para.default" :min="para.values[0]" :max="para.values[1]"
                          :step="para.interval" show-input :show-tooltip="false"></el-slider>
                      </div>
                    </el-dropdown-item>
                    <div v-else>
                      <el-dropdown-item v-for="v in para.values" @click.native="para.default = v">
                        {{ v }}
                      </el-dropdown-item>
                    </div>
                  </el-dropdown-menu>

                </el-dropdown>
              </div>

            </div>
          </div>

          <div slot="body_2">
            <!-- 随机森林变量 -->
            <div class="col-12 row">
              <label class="col-auto">变量：</label>
              <div class="col row">
                <div class="col-auto" v-for="variable in variables">
                  <input type="checkbox" v-model="RandomForestVars" name="random" :value="variable"
                    :disabled="stage === 'trained'">{{ variable }}
                </div>
              </div>
            </div>

            <!-- rf参数 -->
            <div class="col-12 row">
              <div class="col-12" v-for="para in parameters_rf">
                <label>{{ para.parameterName }}</label>

                <el-dropdown class="w-100"
                  :hide-on-click="!(typeof para.values[0] === 'number' && typeof para.values[1] === 'number')"
                  trigger="click">
                  <button class="underline" type="button" :id="para.parameterName" :disabled="stage === 'trained'">
                    {{ para.default }}<i class="el-icon-arrow-down el-icon--right underline-arrow"></i>
                  </button>
                  <el-dropdown-menu slot="dropdown" :aria-labelledby="para.parameterName" style="width: 350px;">
                    <el-dropdown-item class="row"
                      v-if="typeof para.values[0] === 'number' && typeof para.values[1] === 'number'">
                      <div class="col-12">
                        <el-slider class="ailgn-center" v-model="para.default" :min="para.values[0]" :max="para.values[1]"
                          :step="para.interval" show-input :show-tooltip="false"></el-slider>
                      </div>
                    </el-dropdown-item>
                    <div v-else>
                      <el-dropdown-item v-for="v in para.values" @click.native="para.default = v">
                        {{ v }}
                      </el-dropdown-item>
                    </div>
                  </el-dropdown-menu>

                </el-dropdown>
              </div>
            </div>

          </div>
        </double-card>
      </div>
      <div class="col-md-auto col-12">
        <card>
          <p style="font-size: 1em;text-align: center;">神经网络得分</p>
          <p style="font-size: 3em;text-align: center;">{{ nn_score }}</p>
          <el-divider></el-divider>
          <p style="font-size: 1em;text-align: center;">随机森林得分</p>
          <p style="font-size: 3em;text-align: center;">{{ rf_score }}</p>
        </card>
      </div>
    </div>

    <div class="row">

      <div class="col-12 col-lg-7">
        <!-- <el-dialog></el-dialog> -->
        <echarts-card ref="trainChart" title="模型训练" sub-title="展示模型训练的历史数据，模型训练结束后将会可视化模型的预测效果" chartHeight="500px"
          :chart-options="trainOption">
          <!-- <div  slot=""></div> -->

          <div slot="footer" class="row" style="padding-bottom: 10px;">
            <div class="col-lg col-sm-12" style="padding-top: 20px;padding-left: 25px;">
              <vue-slider ref="slider" v-model="samples" :max="dataLength" :process="dataProcess" :height="20"
                :enable-cross="false">
                <template v-slot:dot>
                  <div class="custom-dot"></div>
                </template>
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
            <div class="col-lg-auto col-sm-12" style="display: flex;padding-top: 15px;">
              <el-button-group style="margin: auto;" v-if="stage === 'trained'">
                <el-button type="primary" @click="retrain()" icon="el-icon-refresh-left">重新训练</el-button>
                <el-button type="success" @click="uploadDialog = true" icon="el-icon-upload2">上传模型</el-button>
              </el-button-group>

              <el-button class=" w-100" type="primary" :disabled="stage === 'nodata' || stage === 'training'" v-else
                @click="onTrain()">开始训练
              </el-button>
            </div>

          </div>
        </echarts-card>
      </div>

      <div class="col-12 col-lg-5">
        <echarts-card ref="validChart" title="验证集比较" sub-title="对于验证集的神经网络、随机森林以及真实值的比较可视化" chartHeight="530px" :chart-options="validOption">

        </echarts-card>
      </div>
    </div>

    <!-- 模型上传对话框 -->
    <el-dialog title="提示" :visible.sync="uploadDialog" width="30%" :append-to-body="true">
      <el-form ref="upload" :rules="rules" :model="form">
        <el-form-item label="分析师名称">{{ $cookies.get('username') }}</el-form-item>
        <el-form-item label="数据集">{{ windTurbineName }}</el-form-item>
        <el-form-item label="神经网络得分">{{ nn_score }}</el-form-item>
        <el-form-item label="随机森林得分">{{ rf_score }}</el-form-item>
        <el-form-item label="选择" prop="model">
          <el-checkbox-group v-model="form.model">
            <el-checkbox label="上传神经网络模型" name="model"></el-checkbox>
            <el-checkbox label="上传随机森林模型" name="model"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="输入备注" prop="comment">
          <el-input type="textarea" placeholder="请输入备注" v-model="form.comment"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="uploadDialog = false">取 消</el-button>
        <el-button type="primary" @click="submitForm('upload'); uploadDialog = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { ModelCard, EchartsCard, Card, DoubleCard } from "@/components/index";
import VueSlider from 'vue-slider-component'
import { Dialog, Dropdown, DropdownMenu, DropdownItem, Slider, Button, ButtonGroup, Divider, Form, FormItem, Checkbox, CheckboxGroup } from 'element-ui'
export default {
  components: {
    ModelCard,
    EchartsCard,
    Card,
    DoubleCard,
    VueSlider,
    Dialog,
    Dropdown,
    DropdownMenu,
    DropdownItem,
    Slider,
    Button,
    ButtonGroup,
    Divider,
    Form,
    FormItem,
    Checkbox,
    CheckboxGroup
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
          values: [64, 1024],
          default: 256,
          interval: 64,
        },
        {
          parameterName: "GRU layers",
          values: [1, 10],
          default: 3,
          interval: 1,
        },
        {
          parameterName: "epoch",
          values: [5, 100],
          default: 20,
          interval: 5,
        },
        {
          parameterName: "batchsize",
          values: ['32', '64', '128', '256', '512', '1024'],
          default: '256',
        },
        {
          parameterName: "learning rate",
          values: ['0.05', '0.02', '0.005', '0.002', '0.0005', '0.0002'],
          default: '0.0002',
        },
      ],

      parameters_rf: [
        {
          parameterName: "max depth",
          values: [0, 20],
          default: 12,
          interval: 1,
        },
        {
          parameterName: "n estimators",
          values: [0, 100],
          default: 50,
          interval: 1,
        },
      ],

      nn_score: '未训练',
      rf_score: '未训练',
      primaryVars: [],
      secondaryVars: [],
      RandomForestVars: [],

      //进度条属性
      samples: [0, 7500, 8000, 10000],
      dataLength: 10000,
      dataProcess: dotPos => [
        [dotPos[0], dotPos[1], { backgroundColor: '#5470C6' }],
        [dotPos[1], dotPos[2], { backgroundColor: '#ccc' }],
        [dotPos[2], dotPos[3], { backgroundColor: '#91CC75' }],
      ],
      //状态
      stage: 'nodata', //nodata没有数据 untrain尚未训练 trained完成训练 training训练中
      model_saved: false,

      validOption: {
        xAxis:
        {
          type: 'category',
          data: [1],
          boundaryGap: false,
          axisLabel: {
            interval: 'auto'  // 'auto' 或者一个固定的数字
          }
        },
        yAxis:
        {
          type: 'value'
        },
        legend: {
          data: ['真实值', '神经网络预测值', '随机森林预测值'] // 设置图例名称
        },
        series: [
          {
            name: '真实值',
            type: 'line',
            data: [0],
            itemStyle: {
              color: '#91CC75'
            },
          },
          {
            name: '神经网络预测值',
            type: 'line',
            data: [0],
            itemStyle: {
              color: '#FAC858'
            },
          },
          {
            name: '随机森林预测值',
            type: 'line',
            data: [0],
            itemStyle: {
              color: '#EE6666'
            },
          },
        ]
      },


      trainOption: {
        xAxis:
        {
        },
        yAxis:
        {
          type: 'value'
        },
        legend: {
          data: ['训练集-历史数据', '验证集-历史数据', '神经网络预测值', '随机森林预测值'] // 设置图例名称
        },
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            filterMode: 'none'
          }
        ],
        series: [
          {
            name: '训练集-历史数据',
            type: 'line',
            data: [[0, 1]],
            symbol: 'none',
            // sampling: 'lttb',
          },
          {
            name: '验证集-历史数据',
            type: 'line',
            symbol: 'none',
            data: [[0, 3]]
          },
          {
            name: '神经网络预测值',
            type: 'line',
            symbol: 'none',
            data: [[0, 4]]
          }
          ,
          {
            name: '随机森林预测值',
            type: 'line',
            symbol: 'none',
            data: [[0, 6]]
          }
        ]
      },

      uploadDialog: false,

      form: {
        model: [],
        comment: '',
      },

      rules: {
        model: [
          { type: 'array', required: true, message: '至少选择一个模型', trigger: 'change' }
        ]
      }
    }
  },

  computed: {
    windTurbineName() {
      return this.$store.state.selectedWindTurbine.dataset_name
    }
  },

  created() {
    this.initalize()
  },


  methods: {
    //初始化
    async initalize() {
      await this.getUnprocessedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine))
      // setTimeout(() => {
      //   this.getTrainedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine));
      // }, 500);

      // if(this.stage!=='trained'){
      // }
    },
    //获取模型未训练的数据
    getUnprocessedData(Number) {
      fetch(`http://127.0.0.1:5000/unprocessed_data?number=${Number}`, {
        headers: {
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.hasOwnProperty('error')) {
            console.log(data['error'])
            this.stage = 'nodata'
            return
          }
          this.dataLength = data['length']
          this.stage = 'untrain'
          this.trainOption.series[0].data = data['data']
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
      if (this.RandomForestVars.length == 0) {
        this.$message({
          message: '随机森林变量不能为空',
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
      this.stage = 'training'
      const loading = this.$loading({
        lock: true,
        text: '正在训练模型，请勿退出',
      });
      await fetch(`http://127.0.0.1:5000/train`, {
        method: 'post',
        body: JSON.stringify({
          number: this.getWindTurbineName(this.$store.state.selectedWindTurbine),
          primaryVars: this.primaryVars,
          secondaryVars: this.secondaryVars,
          RandomForestVars: this.RandomForestVars,

          Aggregation_function: this.parameters[0].default,
          embedding_size: this.parameters[1].default,
          GRU_layers: this.parameters[2].default,
          epoch: this.parameters[3].default,
          batchsize: this.parameters[4].default,
          learning_rate: this.parameters[5].default,

          max_depth: this.parameters_rf[0].default,
          n_estimators: this.parameters_rf[1].default,

          samples: this.samples,

          analyst: this.$cookies.get("username")
        }),
        headers: {
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      }).then(response => response.json())
        .then(data => {
          this.model_saved = false
          this.$message({
            message: '训练完成',
            type: 'success'
          })

        })

      await this.getTrainedData(this.getWindTurbineName(this.$store.state.selectedWindTurbine))
      loading.close()
      this.stage = 'trained'
    },
    //获取验证集数据
    getTrainedData(Number) {
      fetch(`http://127.0.0.1:5000/trained_data`, {
        method: 'post',
        body: JSON.stringify({
          number: Number,
          samples: this.samples,
          analyst: this.$cookies.get("username")
        }),
        headers: {
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.hasOwnProperty('error')) {
            console.log(data['error'])
            return
          }

          this.stage = 'trained'
          console.log(data)
          this.validOption.series[1].data = data['nn_pre_val']
          this.validOption.series[2].data = data['random_pre_val']
          this.validOption.series[0].data = data['tru_val']
          this.validOption.xAxis.data = data['x']

          this.trainOption.series[0].data = data['data_train']
          this.trainOption.series[1].data = data['data_valid']
          this.trainOption.series[2].data = data['nn_pre_valid']
          this.trainOption.series[3].data = data['random_pre_valid']

          this.nn_score = data['nn_score']
          this.rf_score = data['random_score']
          //处理数据
        })
        .catch(error => console.error(error));
    },
    //重新训练
    retrain() {
      const analyst = 'rich'
      fetch(`http://127.0.0.1:5000/retrain?analyst=${analyst}`, {
        headers: {
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          this.$message({
            message: '重新训练',
            type: 'success'
          })
          this.stage = 'untrain'
        })
    },
    //提交表格
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // console.log(this.form)
          fetch(`http://127.0.0.1:5000/save_model`, {
            method: 'post',
            body: JSON.stringify({
              // analyst_id: this.$cookies.get("user_id"),
              analyst: this.$cookies.get("username"),
              number: this.getWindTurbineName(this.$store.state.selectedWindTurbine),
              dataset: this.windTurbineName,
              nn_score: this.nn_score,
              rf_score: this.rf_score,
              models: this.form.model,
              comment: this.form.comment
            }),
            headers: {
              'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
              'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
            }
          })
            .then(response => response.json())
            .then(data => {
              if (data.hasOwnProperty('error')) {
                this.$message({
                  message: data['error'],
                  type: 'warning'
                })
                return
              }

              this.model_saved = true
              this.$message({
                message: data['result'],
                type: 'success'
              })
            })

        } else {
          return false;
        }
      });
    },
    //获取风机名称封装函数
    getWindTurbineName(windTurbineName) {
      // windTurbineName = windTurbineName.slice(3);
      // //如果windTurbineNumber编号为单个数字，前面加0
      // if (windTurbineName.length == 1) {
      //   windTurbineName = '0' + windTurbineName;
      // }
      return windTurbineName.table_name
    },
  },

  watch: {
    'dataLength': {
      handler(newDatalength) {
        this.samples = [0, (this.dataLength - 2500) - ((this.dataLength - 2500) % 10), this.dataLength - 2000 - ((this.dataLength - 2000) % 10), this.dataLength]
        this.$refs.slider.control.setDotsValue(this.samples, true)
      }
    },

    'validOption': {
      handler() {
        const validChart = this.$refs.validChart;
        if (validChart && validChart.setOption) {
          validChart.setOption(this.validOption); //更新风速功率曲线图
        }
      },
      deep: true
    },

    'trainOption': {
      handler() {
        const trainChart = this.$refs.trainChart;
        if (trainChart && trainChart.setOption) {
          trainChart.setOption(this.trainOption); //更新风速功率曲线图
        }
      },
      deep: true
    },

    '$store.state.selectedWindTurbine': {
      handler() {
        this.stage = 'untrain'
      }
    }
  },

  beforeRouteLeave(to, from, next) {
    if (this.stage !== 'trained' || this.model_saved) {
      next();
      return;
    }
    this.$confirm('你的模型尚未保存，确定要退出吗')
      .then(() => {
        next()
      })
      .catch(() => {
        next(false)
      })
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

.underline-arrow {
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

.ailgn-center {
  top: calc(50% - 8px);
}

.custom-dot {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: rgb(239, 240, 244);
  margin-top: -7px;
  margin-left: -7px;
  box-shadow: .5px .5px 2px 1px rgba(0, 0, 0, .32);
}
</style>
