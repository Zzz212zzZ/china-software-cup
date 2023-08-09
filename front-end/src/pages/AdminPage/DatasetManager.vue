<template>
    <card title="数据集管理">
        <div>
            <el-table :data="datasets" style="width: 100%" height="600px">
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

                <el-table-column fixed="right" width="130" align="center">
                    <template slot="header" slot-scope="scope">
                        <el-button type="primary" size="mini" icon="el-icon-plus"
                            @click="cleanUpload(); uploadDialog = true;">导入数据集</el-button>
                    </template>
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

        <!-- 数据集上传对话框 -->
        <el-dialog title="上传数据集" :visible.sync="uploadDialog" width="30%" :append-to-body="true">
            <el-steps :active="uploadStep" finish-status="success" align-center>
                <el-step title="上传数据集"></el-step>
                <el-step title="填写数据集信息"></el-step>
            </el-steps>
            <el-form ref="upload" :rules="rules" :model="form" v-if="uploadStep == 1">
                <el-form-item label="数据集名" prop="dataset_name">
                    <el-input placeholder="请输入数据集名" v-model="form.dataset_name"></el-input>
                </el-form-item>
                <el-form-item label="表名" prop="table_name">
                    <el-input placeholder="请输入表名" v-model="form.table_name"></el-input>
                </el-form-item>
                <el-form-item label="地点" prop="location">
                    <span style="color: gray;">
                        <template v-if="form.location">{{ form.location }}</template>
                        <template v-else>未选择</template>
                    </span>
                    <!-- 这里是需要呼出对话框的按钮 -->
                    <el-link icon="el-icon-location-outline" type="info" style="margin-left: 2px;">
                    </el-link>
                </el-form-item>
                <el-form-item label="经度" prop="longitude">

                    <span style="color: gray;">
                        <template v-if="form.longitude">{{ form.longitude }}</template>
                        <template v-else>未选择</template>
                    </span>
                </el-form-item>
                <el-form-item label="纬度" prop="latitude">
                    <span style="color: gray;">
                        <template v-if="form.latitude">{{ form.latitude }}</template>
                        <template v-else>未选择</template>
                    </span>
                </el-form-item>
            </el-form>
            <el-upload class="w-100" drag action="http://127.0.0.1:5000/receive_dataset_data" :limit="1" v-else
                :on-success="uploadSuccess" accept=".csv, .xls, .xlsx" :headers="headerObj">
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <div class="el-upload__tip" slot="tip">
                    只能上传.csv文件，应当包含'DATATIME','WINDSPEED','WINDDIRECTION','TEMPERATURE','HUMIDITY','PRESSURE','PREPOWER','ROUND(A.WS,1)','ROUND(A.POWER,0)','YD15'信息
                </div>
            </el-upload>

            <span slot="footer" class="dialog-footer">
                <el-button @click="uploadDialog = false">取 消</el-button>
                <el-button v-if="uploadStep == 0 && data_submmited" type="primary" @click="uploadStep = 1">下一步</el-button>
                <el-button v-if="uploadStep == 1" type="primary" @click="submitForm('upload')">确
                    认</el-button>
            </span>
        </el-dialog>

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
            uploadDialog: false,
            uploadStep: 0, //上传步骤
            data_submmited: false,
            form: {
                dataset_name: '',
                table_name: '',
                location: '',
                longitude: '',
                latitude: '',
            },
            rules: {
                dataset_name: [
                    { required: true, message: '数据集名不能为空', trigger: 'blur' }
                ],
                table_name: [
                    { required: true, message: '表名不能为空', trigger: 'blur' },
                    { pattern: /^\w+$/, message: '表名只能由字母，数字和下划线构成', trigger: 'blur' }
                ],
                location: [
                    { required: true, message: '地点不能为空', trigger: 'change' }
                ],
                longitude: [
                    { required: true, message: '数据集名不能为空', trigger: 'change' }
                ],
                latitude: [
                    { required: true, message: '数据集名不能为空', trigger: 'change' }
                ],
            },
            headerObj: {
                'Authorization': `Bearer ${$cookies.get('token')}`, // 设置授权头部信息
            },
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

        showMapModalInUpload() {

        },


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

            this.form.dataset_name = '风机 '+file.name.split('.')[0]
            this.form.table_name = file.name.split('.')[0]
            this.data_submmited = true

            this.$message({
                message: data['result'],
                type: 'success'
            })
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

        //提交表格
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    // console.log(this.form)
                    fetch(`http://127.0.0.1:5000/add_dataset`, {
                        method: 'post',
                        body: JSON.stringify({
                            dataset_name: this.form.dataset_name,
                            table_name: this.form.table_name,
                            location: this.form.location,
                            longitude: this.form.longitude,
                            latitude: this.form.latitude,
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

                            this.datasets.push(data['dataset'])
                            console.log(data['dataset'])
                            this.$message({
                                message: data['result'],
                                type: 'success'
                            })
                        })

                } else {
                    return false;
                }
            });
        },

        setActive(index, column, content) {
            this.content = content
            this.activeIndex = index
            this.activeColumn = column
        },

        finEdit() {
            this.activeIndex = -1
        },

        cleanUpload() {
            this.uploadStep = 0
            this.data_submmited = false;
        }
    },
}
</script>

<style></style>