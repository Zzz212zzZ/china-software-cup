<template>
    <card title="模型管理">
        <div>
            <el-button type="primary" round v-if="!isAdmin" @click="onlyMine = !onlyMine">
                <template v-if="onlyMine">全部</template>
                <template v-else>我的</template>
            </el-button>

            <el-table :data="showData" style="width: 100%">
                <el-table-column prop="analyst" label="数据分析师">
                </el-table-column>
                <el-table-column prop="dataset" label="数据集">
                </el-table-column>
                <el-table-column prop="model_type" label="模型类型">
                </el-table-column>
                <el-table-column prop="score" label="模型得分">
                </el-table-column>
                <el-table-column prop="comment" label="备注" width="300">
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="100">
                    <template slot-scope="scope">
                        <el-button @click="deleteModel(scope.$index, scope.row)" type="text" size="small"
                            v-if="isAdmin || analyst === scope.row['analyst']">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </card>
</template>

<script>
import { Card } from "@/components/index";
export default {
    components: {
        Card,
    },

    data() {
        return {
            models: [],

            analyst: this.$cookies.get("username"),

            onlyMine: false,
        }
    },

    created() {
        this.getModels()
    },

    methods: {
        deleteModel(index, row) {
            this.$confirm('确定删除模型？')
                .then(() => {
                    //后端操作
                    fetch(`http://127.0.0.1:5000/delete_model`, {
                        method: 'post',
                        body: JSON.stringify({
                            model_id: row.model_id,
                            number: this.getWindTurbineName(row.dataset)
                        }),
                        headers: {
                            'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                            'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            this.models.splice(index, 1)
                            this.$message({
                                message: data['result'],
                                type: 'success'
                            })
                        })
                })
        },
        //获取模型
        getModels() {
            fetch(`http://127.0.0.1:5000/get_models?dataset=None`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.models = data
                    console.log(data)
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
    },

    computed: {
        isAdmin() {
            return this.$cookies.get("role") === 'admin'
        },

        showData() {
            if (this.onlyMine)
                return this.models.filter(item => item.analyst === this.analyst)
            else
                return this.models
        }
    }
}
</script>

<style></style>