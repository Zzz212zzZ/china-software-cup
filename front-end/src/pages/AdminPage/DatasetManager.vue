<template>
    <card title="数据集管理">
        <div>
            <el-table :data="datasets" style="width: 100%">
                <el-table-column label="数据集名">
                    <template slot-scope="scope">
                        <template v-if="activeColumn == 'dataset_name' && activeIndex == scope.$index">
                            <el-input size="mini" v-model="content" :placeholder="`请输入数据集名`"
                                style="max-width: 300px;"></el-input>
                            <el-link class="margins" type="success" icon="el-icon-check" :underline="false"
                                @click="update_dataset(scope.row, 'dataset_name');"></el-link>
                            <el-link class="margins" type="danger" icon="el-icon-close" :underline="false"
                                @click="finEdit()"></el-link>
                        </template>
                        <template v-else>
                            <span>{{ scope.row.dataset_name }}</span>
                            <el-link icon="el-icon-edit-outline" type="info" style="margin-left: 2px;"
                                @click="setActive(scope.$index, 'dataset_name', scope.row.dataset_name)"></el-link>
                        </template>
                    </template>
                </el-table-column>
                <el-table-column prop="table_name" label="表名">
                </el-table-column>
                <!-- <el-table-column prop="upload_date" label="上传时间">
                </el-table-column> -->
                <el-table-column prop="location" label="所在城市">
                </el-table-column>
                <el-table-column label="具体位置">
                    <template slot-scope="scope">
                        <span>({{ scope.row.longitude.toFixed(3) }},{{ scope.row.latitude.toFixed(3) }})</span>
                        <el-link icon="el-icon-location-outline" type="info" style="margin-left: 2px;"
                            @click="showMapModal(scope.row)">
                        </el-link>
                    </template>
                </el-table-column>

                <el-table-column fixed="right" label="操作" width="100">
                    <template slot-scope="scope">
                        <el-button @click="delete_dataset(scope.$index, scope.row)" type="text" size="small">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 模态框代码 -->
        <modal name="map-modal" :width="880" height="580" :adaptive="true" classes="modal-background">
            <ModifyChinaMap :longitude="selectedPoint.longitude" :latitude="selectedPoint.latitude"
                :dataset_id="selectedPoint.dataset_id" :dataset_name="selectedPoint.dataset_name"
                @close-map-modal="hideMapModal" @update-location="handleUpdateLocation" />

        </modal>



    </card>
</template>

<script>
import { Card } from "@/components/index";
import ModifyChinaMap from "./ModifyChinaMap.vue";
export default {
    components: {
        Card,
        ModifyChinaMap
    },

    data() {
        return {
            selectedPoint: {
                longitude: null,
                latitude: null,
            },
            datasets: [],
            activeIndex: -1,     //正在修改的行号
            activeColumn: '',    //正在修改的列名
            content: '',  //临时存储未提交的值
        }
    },

    created() {
        this.getDatasets()
    },

    methods: {

        handleUpdateLocation(newLocation) {
            this.selectedPoint.longitude = newLocation.longitude;
            this.selectedPoint.latitude = newLocation.latitude;

            // 更新数据集中的位置信息
            const rowToUpdate = this.datasets.find(row => row.dataset_id === newLocation.dataset_id);
            if (rowToUpdate) {
                rowToUpdate.longitude = newLocation.longitude;
                rowToUpdate.latitude = newLocation.latitude;
                rowToUpdate.location = newLocation.location;
            }
        },


        hideMapModal() {
            // 关闭名为'map-modal'的模态框
            this.$modal.hide('map-modal');
        },

        showMapModal(row) {
            this.selectedPoint.longitude = row.longitude;
            this.selectedPoint.latitude = row.latitude;
            this.selectedPoint.dataset_id = row.dataset_id; // 修改这一行
            this.selectedPoint.dataset_name = row.dataset_name; // 修改这一行
            this.$modal.show('map-modal');
        },




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
                    this.datasets = data
                })
        },

        delete_dataset(index, row) {
            this.$confirm('确定删除？')
                .then(() => {
                    //后端操作
                    fetch(`http://127.0.0.1:5000/delete_dataset`, {
                        method: 'post',
                        body: JSON.stringify({
                            'dataset_id': row.dataset_id,
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
                            this.datasets.splice(index, 1)
                            this.$message({
                                message: data['result'],
                                type: 'success'
                            })
                        })
                })
        },

        update_dataset(row, key) {
            fetch(`http://127.0.0.1:5000/update_dataset`, {
                method: 'post',
                body: JSON.stringify({
                    'dataset_id': row.dataset_id,
                    'key': key,
                    'value': this.content,
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
                    // 提交 mutation 来更新全局状态
                    this.$store.commit('updateDatasetName', {
                        dataset_id: row.dataset_id,
                        newDatasetName: this.content
                    });
                    row.dataset_name = this.content; // 这行可能不再需要，因为数据已经绑定到全局状态
                    this.finEdit();
                    this.$message({
                        message: data['result'],
                        type: 'success'
                    });
                });
        },


        update_location(row, location, longitude, latitude) {
            fetch(`http://127.0.0.1:5000/update_location`, {
                method: 'post',
                body: JSON.stringify({
                    'dataset_id': row.dataset_id,
                    'location': location,
                    'longitude': longitude,
                    'latitude': latitude,
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
                    this.finEdit()
                    this.$message({
                        message: data['result'],
                        type: 'success'
                    })
                })
        },

        setActive(index, column, content) {
            this.content = content
            this.activeIndex = index
            this.activeColumn = column
        },

        finEdit() {
            this.activeIndex = -1
        }
    },
}
</script>

<style></style>