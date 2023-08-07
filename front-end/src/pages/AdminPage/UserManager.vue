<template>
    <card title="用户管理">
        <div>
            <el-table :data="models" style="width: 100%">
                <el-table-column prop="username" label="用户名">
                </el-table-column>
                <el-table-column prop="role" label="角色">
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="100">
                    <template slot-scope="scope">
                        <el-button @click="promote(scope.row)" type="text" size="small"
                            v-if="scope.row['role'] === 'client'">提升</el-button>
                        <el-button @click="demote(scope.row)" type="text" size="small"
                            v-if="scope.row['role'] === 'analyst'">降级</el-button>
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
        }
    },

    created() {
        this.getUsers()
    },

    methods: {
        promote(row) {
            this.$confirm('确定提升？')
                .then(() => {
                    //后端操作
                    fetch(`http://127.0.0.1:5000/promote`, {
                        method: 'post',
                        body: JSON.stringify({
                            user_id: row.user_id,
                        }),
                        headers: {
                            'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                            'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            row.role = 'analyst'
                            this.$message({
                                message: data['result'],
                                type: 'success'
                            })
                        })
                })
        },
        demote(row) {
            this.$confirm('确定降级？')
                .then(() => {
                    //后端操作
                    fetch(`http://127.0.0.1:5000/demote`, {
                        method: 'post',
                        body: JSON.stringify({
                            user_id: row.user_id,
                        }),
                        headers: {
                            'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                            'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            row.role = 'client'
                            this.$message({
                                message: data['result'],
                                type: 'success'
                            })
                        })
                })
        },
        //获取模型
        getUsers() {
            fetch(`http://127.0.0.1:5000/get_users`, {
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