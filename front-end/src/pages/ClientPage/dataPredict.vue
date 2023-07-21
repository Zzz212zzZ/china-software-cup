<template>
    <div class="row">
        <div class="col-12 col-lg-6">
            <card title="导入数据">
                <el-upload class="w-100" drag action="http://127.0.0.1:5000/receive_predict_data" :limit="1"
                    v-if="!data_submmited" :on-success="uploadSuccess" accept=".csv, .xls, .xlsx" :headers="headerObj">
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">
                        只能上传.csv文件，应当包含'DATATIME','WINDSPEED','WINDDIRECTION','TEMPERATURE','HUMIDITY','PRESSURE'信息
                    </div>
                </el-upload>
                <!-- <div v-else class="w-100" style="display: inline-block;height: 3em;">
                    <label style="font-size: 1.3em;padding-left: 2%;">使用数据集：{{ data_name }}</label>
                    <el-button size="small" style="float: right;" @click="data_submmited = false">重新上传</el-button>
                </div> -->
                <el-form v-else>
                    <el-form-item label="文件名">{{ data_name }}</el-form-item>
                    <el-form-item label="数据长度">{{ data_length }}</el-form-item>
                    <el-form-item label="预测时间">{{ data_startTime }}-{{ data_endTime }}</el-form-item>
                    <!-- <el-form-item label="结束时间"></el-form-item> -->
                    <el-form-item>
                        <el-button style="float: right;" @click="data_submmited = false">重新上传</el-button>
                    </el-form-item>
                </el-form>
            </card>
        </div>

        <div class="col-12 col-lg-6">
            <card title="选择模型">
                <div>
                    <el-table :data="selected_model" style="width: 100%">
                        <el-table-column prop="analyst" label="数据分析师">
                        </el-table-column>
                        <el-table-column prop="dataset" label="数据集">
                        </el-table-column>
                        <el-table-column prop="model_type" label="模型类型">
                        </el-table-column>
                        <el-table-column prop="score" label="模型得分">
                        </el-table-column>
                    </el-table>
                    <!-- 模型分数：0.999 模型训练师：rich 模型数据集：风机1 模型类型：神经网络 -->
                    <el-button class="w-100" @click="modelSelectDialog = true">
                        选择模型
                    </el-button>
                </div>
            </card>
        </div>
        <div class="col-12">
            <echarts-card ref="preChart" title="预测结果" sub-title="根据输入文件的预测结果可视化" :chart-options="preOption">
                <div slot="footer">
                    <div style="display: flex;align-items: center;justify-content: center;">
                        <el-button type="primary" class="w-50" :disabled="!(data_submmited && model_selected)"
                            @click="predict()">开始预测</el-button>
                        <el-button v-if="hasPredicted" type="success" class="w-25" @click="downloadResult()" icon="el-icon-download">
                            下载预测数据
                        </el-button>
                    </div>
                </div>
            </echarts-card>
        </div>

        <!-- 模型选择对话框 -->
        <el-dialog title="提示" :visible.sync="modelSelectDialog" width="50%" :append-to-body="true">
            <el-table :data="models" style="width: 100%" highlight-current-row @current-change="handleCurrentChange">
                <el-table-column prop="analyst" label="数据分析师" width="120">
                </el-table-column>
                <el-table-column prop="dataset" label="数据集" width="120">
                </el-table-column>
                <el-table-column prop="model_type" label="模型类型" width="120">
                </el-table-column>
                <el-table-column prop="score" label="模型得分" width="120">
                </el-table-column>
                <el-table-column prop="comment" label="备注">
                </el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="modelSelectDialog = false">取 消</el-button>
                <el-button type="primary" @click="selectModelFinished()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { Card, EchartsCard } from "@/components/index";
import { computed } from "vue";

export default {
    components: {
        Card,
        EchartsCard,
    },

    data() {
        return {
            data_submmited: false,
            data_name: 'default',
            data_length: 'default',
            data_startTime: 'default',
            data_endTime: 'default',
            model_selected: false,
            modelSelectDialog: false,

            models: [],

            selected_model: [],

            temp_select_model: null,

            headerObj: {
                'Authorization': `Bearer ${$cookies.get('token')}`, // 设置授权头部信息
            },

            preOption: {
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
                    data: ['未来YD15功率预测值'] // 设置图例名称
                },
                series: [
                    {
                        name: '未来YD15功率预测值',
                        type: 'line',
                        data: [0],
                        itemStyle: {
                            // color: '#91CC75'
                        },
                    },
                ]
            },

            hasPredicted: false
        }
    },

    created() {
        this.getModels()
    },

    methods: {
        //数据完成上传
        uploadSuccess(response, file, fileList) {
            var data = response
            if (data.hasOwnProperty('error')) {
                this.$message({
                    message: data['error'],
                    type: 'warning'
                })
                return
            }

            this.data_name = file.name
            this.data_length = data['length']
            this.data_startTime = data['startTime']
            this.data_endTime = data['endTime']
            this.data_submmited = true

            this.$message({
                message: data['result'],
                type: 'success'
            })
        },
        handleCurrentChange(val) {
            this.temp_select_model = val;
        },
        selectModelFinished() {
            this.$set(this.selected_model, 0, this.temp_select_model);
            this.model_selected = true;
            this.modelSelectDialog = false;
        },
        //获取模型
        getModels() {
            var dataset = this.$store.state.selectedWindTurbine.split(/[\t\r\f\n\s]*/g).join('')
            fetch(`http://127.0.0.1:5000/get_models?dataset=${dataset}`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.models = data
                    // console.log(data)
                })
        },
        //进行模型预测
        predict() {
            // console.log(this.selected_model[0])
            var analyst = this.selected_model[0].analyst
            var number = this.getWindTurbineName(this.selected_model[0].dataset)
            var score = this.selected_model[0].score
            var model_type = this.selected_model[0].model_type
            fetch(`http://127.0.0.1:5000/predict?analyst=${analyst}&number=${number}&score=${score}&model_type=${model_type}`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    // console.log(data)
                    this.hasPredicted = true
                    this.preOption.series[0].data = data['pre_val']
                    this.preOption.xAxis.data = data['time_list']
                    //数据处理
                })
        },
        //下载
        downloadResult() {
            fetch(`http://127.0.0.1:5000/get_predict_csv`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                },
                responseType: 'blob'
            })
                .then(response => response.blob())
                .then(blob => {
                    console.log(blob)
                    const link = document.createElement('a');
                    if (blob.size > 0) {
                        try {
                            let _fileName = this.createPic()+'.csv' 
                            link.style.display = 'none';
                            // 兼容不同浏览器的URL对象
                            const url = window.URL || window.webkitURL || window.moxURL;
                            link.href = url.createObjectURL(blob);
                            link.download = _fileName;
                            link.click();
                            window.URL.revokeObjectURL(url);
                        } catch (e) {
                            console.log('下载的文件出错', e)
                        }
                    }
                })
        },
        //获取风机名称封装函数
        getWindTurbineName(windTurbineName) {
            windTurbineName = windTurbineName.split(/[\t\r\f\n\s]*/g).join('').slice(2);
            //如果windTurbineNumber编号为单个数字，前面加0
            if (windTurbineName.length == 1) {
                windTurbineName = '0' + windTurbineName;
            }
            return windTurbineName
        },
        //产生随机图片名称
        createPic() {
            var now = new Date();
            var year = now.getFullYear(); //得到年份
            var month = now.getMonth();//得到月份
            var date = now.getDate();//得到日期
            var hour = now.getHours();//得到小时
            var minu = now.getMinutes();//得到分钟
            month = month + 1;
            if (month < 10) month = "0" + month;
            if (date < 10) date = "0" + date;
            var number = now.getSeconds() % 43; //这将产生一个基于目前时间的0到42的整数。
            var time = year + month + date + hour + minu;
            return time + "_" + number;
        }
    },

    watch: {
        'preOption': {
            handler() {
                const preChart = this.$refs.preChart;
                if (preChart && preChart.setOption) {
                    preChart.setOption(this.preOption); //更新风速功率曲线图
                }
            },
            deep: true
        },
    }

}

</script>

<style>
.el-upload {
    width: 100%;
}

.el-upload .el-upload-dragger {
    width: 100%;
    height: 7em;

    display: flex;
    justify-content: center;
    align-items: center;
}

.el-form-item {

    margin-bottom: 0px !important;

}
</style>
