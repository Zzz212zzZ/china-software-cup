<template>
    <card title="模型管理">
        <div>
            <el-button type="primary" round v-if="!isAdmin" @click="onlyMine=!onlyMine">
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
            models: [{
                model_id: 0,
                analyst: 'rich',
                dataset: '风机1',
                model_type: '神经网络',
                score: 0.999,
                comment: '你好世界'
            }, {
                model_id: 1,
                analyst: 'rich',
                dataset: '风机2',
                model_type: '随机森林',
                score: 0.988,
                comment: '你好世界'
            }, {
                model_id: 2,
                analyst: 'poor',
                dataset: '风机1',
                model_type: '随机森林',
                score: 0.888,
                comment: '机器学习'
            },],

            analyst: 'rich',

            onlyMine: false,
        }
    },

    methods: {
        deleteModel(index, row) {
            this.$confirm('确定删除模型？')
                .then(() => {
                    //后端操作
                    this.models.splice(index, 1)
                })
        }
    },

    computed: {
        isAdmin() {
            return localStorage.getItem('role') === 'admin'
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