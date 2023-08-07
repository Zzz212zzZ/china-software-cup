<template>
    <card title="数据集管理">
        <div>
            <el-table :data="models" style="width: 100%">
                <el-table-column prop="dataset_name" label="数据集名">
                </el-table-column>
                <el-table-column prop="table_name" label="表名">
                </el-table-column>
                <el-table-column prop="upload_date" label="上传时间">
                </el-table-column>
                <!-- <el-table-column fixed="right" label="操作" width="100">
                    <template slot-scope="scope">
                        <el-button @click="promote(scope.row)" type="text" size="small"
                            v-if="scope.row['role'] === 'client'">提升</el-button>
                        <el-button @click="demote(scope.row)" type="text" size="small"
                            v-if="scope.row['role'] === 'analyst'">降级</el-button>
                    </template>
                </el-table-column> -->
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
        }
    },

    created() {
        this.getDatasets()
    },

    methods: {
        //获取数据集
        getDatasets() {
            fetch(`http://127.0.0.1:5000/get_datasets`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.models = data
                })
        },

        // //获取风机名称封装函数
        // getWindTurbineName(windTurbineName) {
        //     windTurbineName = windTurbineName.split(/[\t\r\f\n\s]*/g).join('').slice(2);
        //     //如果windTurbineNumber编号为单个数字，前面加0
        //     if (windTurbineName.length == 1) {
        //         windTurbineName = '0' + windTurbineName;
        //     }
        //     return windTurbineName
        // },
    },
}
</script>

<style></style>