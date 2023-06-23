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
    <div class="row">

      <div class="col-md-6 col-12">
        <echarts-card ref="correlation" title="相关性图" sub-title="不同维度数据相关性的散点展示，左侧为纵坐标，右侧为横坐标"
          :chart-options="CorrelationData.chartOptions" chart-height="500px">
          <span slot="footer">
            <!-- <i class="ti-timer"></i> Last updated 1 hour ago -->
            <!-- <button class="your-button-class">Your Button Text</button> -->

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

              <div class="col-md-6 col-12">
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


          </span>
          <!-- <div slot="legend">
            <i class="fa fa-circle text-success"></i> Profit
            <i class="fa fa-circle text-warning"></i> Expenses
          </div> -->
        </echarts-card>




      </div>


      <div class="col-12">
        <chart-card title="Users behavior" sub-title="24 Hours performance" :chart-data="usersChart.data"
          :chart-options="usersChart.options">
          <span slot="footer">
            <i class="ti-reload"></i> Updated 3 minutes ago
          </span>
          <div slot="legend">
            <i class="fa fa-circle text-info"></i> Open
            <i class="fa fa-circle text-danger"></i> Click
            <i class="fa fa-circle text-warning"></i> Click Second Time
          </div>
        </chart-card>
      </div>

      <div class="col-md-6 col-12">
        <chart-card title="Email Statistics" sub-title="Last campaign performance" :chart-data="preferencesChart.data"
          chart-type="Pie">
          <span slot="footer">
            <i class="ti-timer"></i> Campaign set 2 days ago</span>
          <div slot="legend">
            <i class="fa fa-circle text-info"></i> Open
            <i class="fa fa-circle text-danger"></i> Bounce
            <i class="fa fa-circle text-warning"></i> Unsubscribe
          </div>
        </chart-card>
      </div>

      <div class="col-md-6 col-12">
        <chart-card title="2015 Sales" sub-title="All products including Taxes" :chart-data="activityChart.data"
          :chart-options="activityChart.options">
          <span slot="footer">
            <i class="ti-check"></i> Data information certified
          </span>
          <div slot="legend">
            <i class="fa fa-circle text-info"></i> Tesla Model S
            <i class="fa fa-circle text-warning"></i> BMW 5 Series
          </div>
        </chart-card>
      </div>



    </div>
  </div>
</template>
<script>
import { StatsCard, ChartCard, EchartsCard } from "@/components/index";
import Chartist from "chartist";
export default {
  components: {
    StatsCard,
    ChartCard,
    EchartsCard,
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */


   created() {
    this.fetchStatsCardsData(this.$store.state.selectedWindTurbine);
  },


  methods: {
    changeTitle1(item) {
      this.dropdownTitle1 = item;
      this.CorrelationData.chartOptions.yAxis.name = item;
      const x_name = this.CorrelationData.chartOptions.xAxis.name;
      const y_name = this.CorrelationData.chartOptions.yAxis.name;
      // 以下是前后端交接功能，这里是接受相关性数据，两个list
      fetch(`http://127.0.0.1:5000/correlation?number=01&y=${y_name}&x=${x_name}`)
      .then(response => response.json())
      .then(data => {
        console.log(data['Combine']);
        this.CorrelationData.chartOptions.series[0].data = data['Combine'];
      })
      .catch(error => console.error(error));

    },
    changeTitle2(item) {
      this.dropdownTitle2 = item;
      this.CorrelationData.chartOptions.xAxis.name = item;
      const x_name = this.CorrelationData.chartOptions.xAxis.name;
      const y_name = this.CorrelationData.chartOptions.yAxis.name;
      // 以下是前后端交接功能，这里是接受相关性数据，两个list
      fetch(`http://127.0.0.1:5000/correlation?number=01&y=${y_name}&x=${x_name}`)
      .then(response => response.json())
      .then(data => {
        console.log(data['Combine']);
        this.CorrelationData.chartOptions.series[0].data = data['Combine'];
      })
      .catch(error => console.error(error));
    },

    fetchStatsCardsData(windTurbineName) {
      //截取'风机 ',取后面的数字
      let windTurbineNumber = windTurbineName.slice(3)
      //如果windTurbineNumber编号为单个数字，前面加0
      if (windTurbineNumber.length == 1) {
        windTurbineNumber = '0' + windTurbineNumber
      }

      console.log(windTurbineNumber)
      fetch('http://127.0.0.1:5000/basic_info?number=' + windTurbineNumber)
        .then(response => response.json())
        .then(data => {
          console.log(data);
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


  },

  watch: {
      'CorrelationData.chartOptions': {
        handler(newVal, oldVal) {    
          const correlation = this.$refs.correlation;  
        // 如果存在 ref = correlation 并且 setOption 存在
          if (correlation && correlation.setOption) {
          correlation.setOption(this.chartOptions);
        }
      },
      deep: true
    },

    '$store.state.selectedWindTurbine': function(newVal) {
    console.log(newVal);
    this.fetchStatsCardsData(newVal);
  },
  },

 


  data() {
    return {
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
      CorrelationData: {
        chartOptions: {
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
            nameLocation: 'middle',
            nameGap: 30,
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
              symbolSize: 20,
              data: [[10.0, 8.04], [8.07, 6.95], [13.0, 7.58], [9.05, 8.81], [11.0, 8.33]],
              type: 'scatter'
            }
          ]
        }
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
          height: "245px",
        },
      },

      preferencesChart: {
        data: {
          labels: ["62%", "32%", "6%"],
          series: [62, 32, 6],
        },
        options: {},
      },
    };
  },
};

</script>
<style>
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
</style>
