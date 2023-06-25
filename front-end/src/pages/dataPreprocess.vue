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
            <div class="col-12">
              <div class="row">
                <!--sigma值进度条-->
                <div class="col-10">
                  <vue-slider v-model="sigma" :lazy="true" :min="0.5" :max="3" :interval="0.01" :marks="sigmaMarks" />
                </div>
                <div class="col-2">
                  <p>sigma</p>
                </div>

                <!--死值进度条-->
                <div class="col-10">
                  <vue-slider v-model="deadCount" :lazy="true" :min="2" :max="10" :interval="1" :marks="true" />
                </div>
                <div class="col-2">
                  <p>死值</p>
                </div>

                <!--步长进度条-->
                <div class="col-10">
                  <vue-slider v-model="step" :lazy="true" :min="0.1" :max="2" :interval="0.1" :marks="true" />
                </div>
                <div class="col-2">
                  <p>步长</p>
                </div>

                <!-- 缺失值处理 -->
                <div class="col-12">
                  <label>缺失值处理</label>
                  <input type="radio" name="missingValue" value="delete" v-model="missingValueOption">删除
                  <input type="radio" name="missingValue" value="fill" v-model="missingValueOption">填充
                </div>

                <!-- 缺失值处理 -->
                <div class="col-12">
                  <label>A类异常点处理</label>
                  <input type="radio" name="aValue" value="delete" v-model="aValueOption">删除
                  <input type="radio" name="aValue" value="fill" v-model="aValueOption">填充
                </div>

                <!-- 缺失值处理 -->
                <div class="col-12">
                  <label>B类异常点处理</label>
                  <input type="radio" name="bValue" value="delete" v-model="bValueOption">删除
                  <input type="radio" name="bValue" value="fill" v-model="bValueOption">填充
                </div>
              </div>

              <div>
                <button type="button" class="btn btn-primary float-right">进行模型训练</button>
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
      sigmaMarks: [1, 2, 3],
      deadCount: 3,
      step: 0.2,

      missingValueOption: 'delete',
      aValueOption: 'delete',
      bValueOption: 'delete'
    };
  },
};
</script>
<style></style>
