<template>
  <div>
    <!--Stats cards-->
    <div class="row">
      <div class="col-md-6 col-xl-3" v-for="stats in statsCards" :key="stats.title">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i :class="stats.icon"></i>
          </div>
          <div class="numbers" slot="content">
            <p>{{ stats.title }}</p>
            {{ stats.value }}
          </div>
          <div class="stats" slot="footer">
            <i :class="stats.footerIcon"></i> {{ stats.footerText }}
          </div>
        </stats-card>
      </div>
    </div>

    <!--Charts-->

    <div class="row d-flex align-items-center">
      <div class="col-md-6 col-12">
        <echarts-card ref="correlation" title="相关性图" sub-title="不同维度数据相关性的散点展示，左侧为纵坐标，右侧为横坐标"
          :chart-options="correlationOption" chart-height="800px">
          <span slot="footer">
            <div class="flex-column col-12">
              <!-- <div class="row col-12 justify-content-center">
                <div class="col-4">
                  <vue-slider v-model="percentage" :lazy="true" :min="0.1" :max="1" :interval="0.01" :hide-label="true"
                    :height="5">
                  </vue-slider>
                </div>
                <label class="col-auto">显示点百分比</label>
              </div> -->

              <div class="col-12">
                <div class="twoBtnRow">
                  <div class="col-md-6 col-12">
                    <div class="btn-group dropup dropdownAtr">
                      <button type="button" class="btn btn-primary dropdown-toggle btn-block" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                        {{ dropdownTitle1 }}
                      </button>
                      <div class="dropdown-menu">
                        <a v-for="item in dropdownOptions" :key="item + 'a'"
                          @click.prevent="item !== dropdownTitle2 ? changeTitle1(item) : undefined"
                          :class="{ 'dropdown-item': true, disabled: item === dropdownTitle2 || item === dropdownTitle1, selected: item === dropdownTitle1 }"
                          href="#">
                          {{ item }}
                        </a>
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6 col-12 ">
                    <div class="btn-group dropup dropdownAtr">
                      <button type="button" class="btn btn-info dropdown-toggle btn-block" data-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">
                        {{ dropdownTitle2 }}
                      </button>
                      <div class="dropdown-menu">
                        <a v-for="item in dropdownOptions" :key="item + 'a'"
                          @click.prevent="item !== dropdownTitle1 ? changeTitle2(item) : undefined"
                          :class="{ 'dropdown-item': true, disabled: item === dropdownTitle1 || item === dropdownTitle2, selected: item === dropdownTitle2 }"
                          href="#">
                          {{ item }}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </span>
          <!-- <div slot="legend">
            <i class="fa fa-circle text-success"></i> Profit
            <i class="fa fa-circle text-warning"></i> Expenses
          </div> -->
        </echarts-card>
      </div>



      <div class="col-md-6 col-12 d-flex flex-column">
        <div class="flex-grow-1">
          <echarts-card ref="histogramy" :title="dropdownTitle1 + ' 分布直方图'" sub-title="相关性数据的y轴边缘分布直方图，用以分析数据频率分布情况"
            :chart-options="histogramyOption" class="emailStatistics" chart-type="Pie" chart-height="350px">
            <span slot="footer">
              <i class="ti-timer"></i> Campaign set 2 days ago</span>
          </echarts-card>
        </div>



        <div class="flex-grow-1">
          <echarts-card ref="histogramx" :title="dropdownTitle2 + ' 分布直方图'" sub-title="相关性数据的x轴边缘分布直方图，用以分析数据频率分布情况"
            :chart-options="histogramxOption" chart-height="350px">
            <span slot="footer">
              <i class="ti-check"></i> Data information certified
            </span>
          </echarts-card>
        </div>
      </div>

    </div>


    <div class="cards">
      <div class="btnRow row mt-3 mb-5">
        <!-- Btn -->
        <button class="dropBtn">
          <span style="font-size: large;">属性可视化</span>
          <span class="ti-arrow-circle-right rippleIcons"></span>
          <ul class="customDropdown">
            <li v-for="(value, item) in attritems" :key="item" :class="{ active: value }">
              <a href="#" @click.prevent="toggleActive(item)">{{ item }}</a>
            </li>
          </ul>
        </button>
      </div>


      <div v-for="(value, item) in attritems" :key="item">
        <div class="row">
          <div class="col-12">
            <DecoratedEchart v-if="value" :title="item" :chartOptions="options[item]" :ref="() => `echartRef-${item}`" />
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
<script>
import { StatsCard, EchartsCard, DecoratedEchart } from "@/components/index";
import axios from "axios";
// import VueSlider from 'vue-slider-component'
import Chartist from "chartist";
import * as echarts from "echarts";
import ecStat from "echarts-stat";

export default {
  components: {
    StatsCard,
    EchartsCard,
    DecoratedEchart,
    // VueSlider,
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */


  created() {
    this.fetchStatsCardsData(this.$store.state.selectedWindTurbine);

    //-----------------------定义options，是每一个折线面积图的配置-----------------------

  },

  mounted() {
    echarts.registerTransform(ecStat.transform.histogram);
    this.correlationOption.xAxis.name = this.dropdownTitle2;
    this.correlationOption.yAxis.name = this.dropdownTitle1;
    //初始化相关性散点图的数据，因为数据本身只有靠变化才能调用，这里直接手动调用changeTitle
    this.changeTitle1(this.dropdownTitle1);

    for (let attrName in this.attritems) {
      console.log(attrName);
      this.options[attrName] = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          top: '5%',
          left: '3%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
            axisLabel: {
              interval: 'auto'  // 'auto' 或者一个固定的数字
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: attrName,
            type: 'line',
            stack: 'Total',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [0.46047747600517397, 0.21607694057754334, 0.24257963740200394, 0.8025874813305929, 0.9564591682084751, 0.46801213100006533, 0.3128338842662304, 0.5322566850148831, 0.5379962110572074, 0.9516893561704958, 0.348912136297288, 0.8851548770516071, 0.2681822774102822, 0.7392631897202784, 0.08127819614506948, 0.9620397536902456, 0.9223619767453926, 0.8892879458135514, 0.415595817299268, 0.47942852390352275, 0.45404343534681546, 0.8580416241592974, 0.985784569654429, 0.6783363271162972, 0.595089648699179, 0.008073832784263768, 0.47981689897256596, 0.2126219638926108, 0.1510975854859129, 0.12294126289120455, 0.48968568655862055, 0.2310134586998427, 0.40729357965028123, 0.468830128845632, 0.6566587352934139, 0.6119329094513233, 0.6914028545192437, 0.1689468655247992, 0.6434397990959202, 0.889896562396469, 0.26252865994511243, 0.7578527195867397, 0.9572498147493074, 0.49630764499840296, 0.26250467132845, 0.8396543165691728, 0.8542073142835565, 0.6238701860341531, 0.7027355317705921, 0.4579042612652815, 0.8302637423967536, 0.7757375720610802, 0.7279631682928631, 0.8936863653469294, 0.9633622952054299, 0.7405093534694356, 0.16899161055290346, 0.4353884428944286, 0.3618708963424879, 0.7570737535598073, 0.43476163695004777, 0.4217843736865121, 0.22487321363552093, 0.7471808107444606, 0.06528408377245243, 0.32792305760788265, 0.12077776979980004, 0.5687478615452224, 0.6872323903299875, 0.43870524234421593, 0.9323435058158043, 0.44924317946648107, 0.4075531912869834, 0.8324645526164864, 0.017698255277562414, 0.5437729780958773, 0.909920740530175, 0.9450867856887761, 0.07255971970686836, 0.9974100721088257, 0.42560821827258577, 0.8139013368517172, 0.1517837766813046, 0.31846483378838064, 0.7260374792386439, 0.07410895574826615, 0.972620407047837, 0.2566890324001265, 0.4526762713961916, 0.8175324067071599, 0.754693077689097, 0.9535276761165985, 0.509149636837327, 0.734758113665309, 0.25085931944878603, 0.7524177118889885, 0.04448170017944575, 0.8325187111672865, 0.408344950042997, 0.08567221857170759]
          }
        ]
      };

    }
  },


  watch: {
    'correlationOption': {
      handler() {
        const correlation = this.$refs.correlation;
        const histogramx = this.$refs.histogramx;
        const histogramy = this.$refs.histogramy;
        // 如果存在 ref = correlation 并且 setOption 存在
        if (correlation && correlation.setOption) {
          // correlation.setOption(this.correlationOption); //更新相关性图
          histogramx.setOption(this.histogramxOption); //更新直方图x
          histogramy.setOption(this.histogramyOption); //更新直方图y
        }
      },
      deep: true
    },

    '$store.state.selectedWindTurbine': function (newVal) {
      console.log(newVal);
      this.fetchStatsCardsData(newVal);
      const x_name = this.correlationOption.xAxis.name;
      const y_name = this.correlationOption.yAxis.name;
      // const percentage = 0.2;  //显示20%的散点
      const Number = this.getWindTurbineName(this.$store.state.selectedWindTurbine);
      this.getCorrlationData(Number, y_name, x_name);
    },
  },


  methods: {

    //----------------------------------相关性图的方法----------------------

    changeTitle1(item) {
      this.dropdownTitle1 = item;
      this.correlationOption.yAxis.name = item;
      const x_name = this.correlationOption.xAxis.name;
      const y_name = this.correlationOption.yAxis.name;
      const percentage = this.percentage;  //显示指定(默认20%)的散点
      const Number = this.getWindTurbineName(this.$store.state.selectedWindTurbine);
      // 以下是前后端交接功能，这里是接受相关性数据，两个list
      this.getCorrlationData(Number, y_name, x_name, percentage);
    },
    changeTitle2(item) {
      this.dropdownTitle2 = item;
      this.correlationOption.xAxis.name = item;
      const x_name = this.correlationOption.xAxis.name;
      const y_name = this.correlationOption.yAxis.name;
      const percentage = this.percentage;  //显示指定(默认20%)的散点
      const Number = this.getWindTurbineName(this.$store.state.selectedWindTurbine);
      // 以下是前后端交接功能，这里是接受相关性数据，两个list
      this.getCorrlationData(Number, y_name, x_name, percentage);
    },
    //把获取相关性数据封装为函数
    getCorrlationData(Number, y_name, x_name) {
      fetch(`http://127.0.0.1:5000/correlation?number=${Number}&y=${y_name}&x=${x_name}`,{
        headers:{
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.correlationOption.series[0].data = data['data_all'];
          this.histogramxOption.dataset[0].source = data['data_all'];
          this.histogramyOption.dataset[0].source = data['data_all'];
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
    //更新头部四个card内容
    fetchStatsCardsData(windTurbineName) {
      windTurbineName = this.getWindTurbineName(windTurbineName) //截取'风机 ',取后面的数字
      fetch('http://127.0.0.1:5000/basic_info?number=' + windTurbineName,{
        headers:{
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          // console.log(data);
          this.statsCards = this.statsCards.map(card => {
            return {
              ...card,
              value: data[card.title], // 使用字典的键来获取值
            };
          },
            //还要更新最后一个statsCard的footerText: "Until 2022/06/30"
            this.statsCards[3].footerText = "Until " + data['最后一天']
          );
        })
    },


    //----------------------------------属性可视化的方法----------------------
    toggleActive(value) {
      let windTurbineName = this.getWindTurbineName(this.$store.state.selectedWindTurbine) //截取'风机 ',取后面的数字
      const fetchXAxisData = fetch(`http://127.0.0.1:5000/dimension_data?number=${windTurbineName}&dimension=DATATIME`,{
        headers:{
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      })
        .then(response => response.json())
        .then(data => {
          this.options[value].xAxis[0].data = data['DATATIME'];
        });

      const fetchYAxisData = fetch(`http://127.0.0.1:5000/dimension_data?number=${windTurbineName}&dimension=${value}`,{
        headers:{
          'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
          'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
        }
      }) //修改为你的实际URL
        .then(response => response.json())
        .then(data => {
          this.options[value].series[0].data = data[value];
        });

      Promise.all([fetchXAxisData, fetchYAxisData]).then(() => {
        this.attritems[value] = !this.attritems[value];
        this.$nextTick(() => {
          console.log(this.$refs['echartRef-' + value])
          this.$refs['echartRef-' + value].setOption(this.options[value]);
        });
      });
    },



  },






  data() {
    return {
      //----------------------------------相关性图的变量----------------------
      dropdownTitle1: 'YD15',
      dropdownTitle2: 'ROUND(A.POWER,0)',

      dropdownOptions: [
        'WINDSPEED',
        'PREPOWER',
        'WINDDIRECTION',
        'TEMPERATURE',
        'HUMIDITY',
        'PRESSURE',
        'ROUND(A.WS,1)',
        'ROUND(A.POWER,0)',
        'YD15'
      ],
      //相关性option
      correlationOption: {
        xAxis: {
          name: this.dropdownTitle2,
          nameGap: 30,
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#666',
            fontSize: 20,
            fontWeight: 'bold',
          },
          axisLine: {
            lineStyle: {
              color: '#999',
              width: 1,
            },
          },
        },
        yAxis: {
          name: this.dropdownTitle1,
          nameGap: 10,
          nameTextStyle: {
            color: '#666',
            fontSize: 20,
            fontWeight: 'bold',
          },
          axisLine: {
            lineStyle: {
              color: '#999',
              width: 1,
            },
          },
        },
        series: [
          {
            symbolSize: 10,
            data: [],
            type: 'scatter',
            large: true,
            largeThreshold: 500
          }
        ]
      },
      //----------------------------------直方图的变量----------------------
      //直方图x的option
      histogramxOption: {
        dataset: [
          {
            source: [
              [0, 0]
            ]
          },
          {
            transform: {
              type: 'ecStat:histogram',
              config: {}
            }
          },
        ],
        tooltip: {},
        xAxis:
        {
          name: 'Value',
          nameGap: 30,
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#666',
            fontSize: 20,
            fontWeight: 'bold',
          },
          scale: true,
          gridIndex: 0
        },
        yAxis:
        {
          gridIndex: 0
        },
        series: [
          {
            name: 'histogram',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            barWidth: '99.3%',
            encode: { x: 0, y: 1, itemName: 4 },
            datasetIndex: 1
          }
        ]
      },
      //直方图y的option
      histogramyOption: {
        dataset: [
          {
            source: [
              [0, 0],
            ]
          },
          {
            transform: {
              type: 'ecStat:histogram',
              config: { dimensions: [1] }
            }
          },
        ],
        tooltip: {},
        xAxis:
        {
          name: 'Value',
          nameGap: 30,
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#666',
            fontSize: 20,
            fontWeight: 'bold',
          },
          scale: true,
          gridIndex: 0
        },

        yAxis:
        {
          gridIndex: 0
        },
        series: [
          {
            name: 'histogram',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            barWidth: '99.3%',
            encode: { x: 0, y: 1, itemName: 4 },
            datasetIndex: 1
          }
        ]
      },

      statsCards: [
        {
          type: "warning",
          icon: "ti-layers-alt",
          title: "数据维度",
          value: "10",
          footerText: "Data dimension",
          footerIcon: "ti-reload",
        },
        {
          type: "success",
          icon: "ti-layout-menu-v",
          title: "数据记录数",
          value: "23138",
          footerText: "Records number",
          footerIcon: "ti-calendar",
        },
        {
          type: "danger",
          icon: "ti-layout-sidebar-left",
          title: "YD15缺失数",
          value: "2345",
          footerText: "NULL values",
          footerIcon: "ti-timer",
        },
        {
          type: "info",
          icon: "ti-calendar",
          title: "记录天数",
          value: "242",
          footerText: "Until 2022/06/30",
          footerIcon: "ti-reload",
        },
      ],

      usersChart: {
        data: {
          labels: [
            "9:00AM",
            "12:00AM",
            "3:00PM",
            "6:00PM",
            "9:00PM",
            "12:00PM",
            "3:00AM",
            "6:00AM",
          ],
          series: [
            [287, 385, 490, 562, 594, 626, 698, 895, 952],
            [67, 152, 193, 240, 387, 435, 535, 642, 744],
            [23, 113, 67, 108, 190, 239, 307, 410, 410],
          ],
        },
        options: {
          low: 0,
          high: 1000,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3,
          }),
          showLine: true,
          showPoint: false,
        },
      },

      activityChart: {
        data: {
          labels: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "Mai",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
          ],
          series: [
            [542, 543, 520, 680, 653, 753, 326, 434, 568, 610, 756, 895],
            [230, 293, 380, 480, 503, 553, 600, 664, 698, 710, 736, 795],
          ],
        },
        options: {
          seriesBarDistance: 10,
          axisX: {
            showGrid: false,
          },
          height: "250px",
        },
      },

      histoY: {

        chartOptions: {
          dataset: [
            {
              source: [
                [8.3, 143],
                [8.6, 214],
                [8.8, 251],
                [10.5, 26],
                [10.7, 86],
                [10.8, 93],
                [11.0, 176],
                [11.0, 39],
                [11.1, 221],
                [11.2, 188],
                [11.3, 57],
                [11.4, 91],
                [11.4, 191],
                [11.7, 8],
                [12.0, 196],
                [12.9, 177],
                [12.9, 153],
                [13.3, 201],
                [13.7, 199],
                [13.8, 47],
                [14.0, 81],
                [14.2, 98],
                [14.5, 121],
                [16.0, 37],
                [16.3, 12],
                [17.3, 105],
                [17.5, 168],
                [17.9, 84],
                [18.0, 197],
                [18.0, 155],
                [20.6, 125]
              ]
            },
            {
              transform: {
                type: 'ecStat:histogram',
                config: {}
              }
            },
            {
              transform: {
                type: 'ecStat:histogram',
                // print: true,
                config: { dimensions: [1] }
              }
            }
          ],
          tooltip: {},
          xAxis: [
            {
              scale: true,
              gridIndex: 0
            },
          ],
          yAxis: [
            {
              gridIndex: 0
            },
          ],
          series: [
            {
              name: 'histogram',
              type: 'bar',
              subtext: '子图 1',
              xAxisIndex: 0,
              yAxisIndex: 0,
              barWidth: '99.3%',
              label: {
                show: true,
                position: 'top'
              },
              encode: { x: 0, y: 1, itemName: 4 },
              datasetIndex: 1
            }
          ]
        },


      },

      //----------------------------------属性可视化的变量----------------------
      attritems: {
        'WINDSPEED': false,
        'PREPOWER': false,
        'WINDDIRECTION': false,
        'TEMPERATURE': false,
        'HUMIDITY': false,
        'PRESSURE': false,
        'ROUND(A.WS,1)': false,
        'ROUND(A.POWER,0)': false,
        'YD15': false
      },

      options: {},

    };
  },
};




</script>
<style lang="scss">
.dropdown-item {
  transition: background-color 0.3s ease, color 0.3s ease;
}

.dropdown-item.selected {
  background-color: #007bff !important;
  /* A deep, bright blue */
  color: #ffffff !important;
  /* White for contrast against the blue background */
}

.stats {
  display: block !important;
}


.twoBtnRow {
  display: flex !important;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}




.btn-group.dropup.dropdownAtr {
  width: 100%;

}






.cards {
  border: #cab2f1 1px solid;
  box-shadow: 10px 10px 20px 1px rgba(247, 147, 26, .15);
  border-radius: 30px;
}

.btnRow {
  position: relative;
  width: 100%;
  margin-left: 3% !important;
}

// Fonts

// Font Weights
$thin: 100;
$light: 300;
$regular: 400;
$semibold: 600;
$bold: 700;
$ultra: 800;

// Colors
$black: #000000;
$white: #FFFFFF;


// Pen Colors
$accent: #5380F7;


// .col-12 {
//   flex: 1;
// }

.cards {
  width: 100%;
  // display: flex;
  // flex-direction: column;
  // justify-content: center;
  // align-items: center;
}



.dropBtn {
  outline: 0;
  display: flex;
  justify-content: space-between; // 在横轴上分散对齐子元素
  align-items: center; // 在纵轴上居中对齐子元素
  position: relative;

  background: $accent;
  width: 20%; // 修改这里，使按钮占满整个宽度
  border: 0;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba($black, .1);
  box-sizing: border-box;
  padding: 16px 20px;
  color: $white;
  font-size: 12px;
  font-weight: $semibold;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  // overflow: hidden;
  cursor: pointer;

  &:hover .rippleIcons {
    font-size: 30px;
  }


  &:focus,
  &:active {
    .customDropdown {
      transform: translate(20px, 0);
      opacity: 1;
      visibility: visible;

    }
  }

  .rippleIcons {
    position: absolute;
    right: 10px; // 根据实际情况调整
    top: 50%;
    transform: translateY(-50%); // 让图标垂直居中
    border-radius: 100%;
    animation: ripple 0.6s linear infinite;
    font-size: 24px; // 或者更大的值
    transition: font-size 0.3s ease; // 为 font-size 添加过渡效果
    // &:hover{
    //   font-size: 30px; // 当鼠标悬停在图标上时，图标的大小会变大

    // }
  }

  .customDropdown {
    position: absolute;
    bottom: 0; // 让下拉菜单和父元素的底部对齐
    left: 95%; // 让下拉菜单出现在右边
    background: $white;
    // width: 100%;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba($black, .1);
    text-align: left;
    opacity: 0;
    visibility: hidden;
    transition: 0.3s ease;
    padding-left: 0;
    z-index: 9999;

    // &:before {
    //   content: '';
    //   position: absolute;
    //   bottom: 0; // 使箭头和父元素的底部对齐
    //   right: 20px; // 修改这里，使箭头出现在右边
    //   width: 0;
    //   height: 0;

    //   border-top: 13px solid transparent; // 修改这里，使箭头更大
    //   border-right: 13px solid transparent; // 修改这里，使箭头指向左边
    //   border-bottom: 13px solid transparent; // 修改这里，使箭头更大
    //   border-left: 13px solid $white; // 修改这里，使箭头指向左边
    //   mix-blend-mode: multiple;
    // }


    li {
      list-style-type: none;
      z-index: 1;
      position: relative;
      background: $white;
      padding: 0px 40px; // 增加垂直方向的padding以改善触摸设备的用户体验
      color: #666;

      // 悬停效果
      &:hover {
        background: #f8f8f8; // 稍微变暗的背景色
        color: #333; // 稍微加深的文字颜色
      }

      // 当前活动的选项
      &.active {
        color: $accent;
        background: rgba($accent, 0.1); // 活动选项背景色设为弱化的accent色
      }

      &:first-child {
        border-radius: 4px 4px 0 0;
      }

      &:last-child {
        border-radius: 0 0 4px 4px;

        a {
          border-bottom: 0;
        }
      }
    }

    a {
      display: block;
      border-bottom: 1px solid rgba($black, .05);
      padding: 10px 0; // 垂直padding同样增加，以匹配li的padding
      color: inherit;
      font-size: 14px; // 增大字体以提升可读性
      text-decoration: none;

      // 悬停效果
      &:hover {
        color: $accent; // 文字颜色变为accent色
      }
    }


  }
}

@keyframes ripple {
  0% {
    box-shadow: 0 0 0 0 rgba($white, 0.1),
      0 0 0 20px rgba($white, 0.1),
      0 0 0 40px rgba($white, 0.1),
      0 0 0 60px rgba($white, 0.1);
  }

  100% {
    box-shadow: 0 0 0 20px rgba($white, 0.1),
      0 0 0 40px rgba($white, 0.1),
      0 0 0 60px rgba($white, 0.1),
      0 0 0 80px rgba($white, 0);
  }
}

// .card .footer div{
//   display: initial;
// }

// .container button.dropBtn {
//   transition: background-color 0.5s ease;
// }

// .container ul.dropdown li a {
//   transition: color 0.5s ease;
// }

// .container ul.dropdown li a:hover {
//   color: #ff0000;
// }
</style>
