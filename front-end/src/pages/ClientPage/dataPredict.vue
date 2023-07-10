<template>
    <div class="row">
        <div class="col-12 col-lg-6">
            <card title="导入数据">
                <el-upload class="w-100" drag action="http://127.0.0.1:5000/receive_predict_data" :limit="1"
                    v-if="!data_submmited" :on-success="uploadSuccess" accept=".csv, .xls, .xlsx">
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">
                        只能上传.csv文件，应当包含'DATATIME','WINDSPEED','WINDDIRECTION','TEMPERATURE','HUMIDITY','PRESSURE'信息
                    </div>
                </el-upload>
                <div v-else class="w-100" style="display: inline-block;height: 3em;">
                    <label style="font-size: 1.3em;padding-left: 2%;">使用数据集：{{ data_name }}</label>
                    <el-button size="small" style="float: right;" @click="data_submmited = false">重新上传</el-button>
                </div>
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
            <echarts-card ref="validChart" title="预测结果" sub-title="副标题">
                <div slot="footer">
                    <div style="display: flex;align-items: center;justify-content: center;">
                        <el-button type="primary" class="w-50"
                            :disabled="!(data_submmited && model_selected)">开始预测</el-button>
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
            model_selected: false,
            modelSelectDialog: false,

            models: [{
                model_id:0,
                analyst: 'rich',
                dataset: '风机1',
                model_type: '神经网络',
                score: 0.999,
                comment: '你好世界'
            }, {
                model_id:1,
                analyst: 'rich',
                dataset: '风机2',
                model_type: '随机森林',
                score: 0.988,
                comment: '你好世界'
            },],

            selected_model: [],

            temp_select_model: null
        }
    },

    methods: {
        //数据完成上传
        uploadSuccess(response, file, fileList) {
            console.log(response)
            var data = response
            if (data.hasOwnProperty('error')) {
                this.$message({
                    message: data['error'],
                    type: 'warning'
                })
                return
            }

            this.data_name = file.name
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
            var number = this.getWindTurbineName(this.$store.state.selectedWindTurbine)
            fetch(`http://127.0.0.1:5000/get_models?number=${number}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                })
        },
        //进行模型预测
        predict() {
            var analyst = this.selected_model.analyst
            var number = this.getWindTurbineName(this.selected_model.dataset)
            var score = this.selected_model.score
            var model_type = this.selected_model.model_type
            fetch(`http://127.0.0.1:5000/predict?analyst=${analyst}&number=${number}&score=${score}&model_type=${model_type}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    //数据处理
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
    }

}

</script>

<style>
.el-upload {
    width: 100%;
}

.el-upload .el-upload-dragger {
    width: 100%;
    height: 3em;

    display: flex;
    justify-content: center;
    align-items: center;
}
</style>