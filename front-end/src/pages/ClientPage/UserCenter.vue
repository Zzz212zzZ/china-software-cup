<template>
    <card title="个人中心">
        <el-link :underline="false" @click="showChangeAvatar = !showChangeAvatar">
            <el-avatar v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl" style="height: 100px;width: 100px;"></el-avatar>
            <el-avatar v-else style="height: 100px;width: 100px;vertical-align: middle;">
                <p style="font-size: 70px;">{{ userInfo.username.charAt(0).toLocaleUpperCase() }}</p></el-avatar>
            <el-collapse-transition>
                <div v-show="showChangeAvatar" style="float: right;padding-left: 10px;">
                    <el-upload class="avatar-uploader" action="http://127.0.0.1:5000/change_avatar" :limit="1"
                        :on-success="uploadSuccess" :show-file-list="false" accept=".png, .jpg, .jpeg" :headers="headerObj">
                        <i class="el-icon-refresh-left avatar-uploader-icon"></i>
                    </el-upload>
                </div>
            </el-collapse-transition>
        </el-link>
        <el-descriptions>
            <el-descriptions-item v-for="(value, key) in displays" :label="value">
                <template v-if="edit == key">
                    <el-input size="mini" v-model="temp" :placeholder="`请输入${value}`" style="max-width: 300px;"></el-input>
                    <el-link class="margins" type="success" icon="el-icon-check" :underline="false"
                        @click="commonChange(key, temp)"></el-link>
                    <el-link class="margins" type="danger" icon="el-icon-close" :underline="false"
                        @click="edit = 'none'"></el-link>
                </template>
                <template v-else>
                    <template v-if="userInfo[key]">
                        {{ userInfo[key] }}
                    </template>
                    <div v-else style="color:grey">
                        无
                    </div>
                    <el-button class="margins" type="text" icon="el-icon-edit" size="mini"
                        @click="temp = userInfo[key]; edit = key;"></el-button>
                </template>
            </el-descriptions-item>
        </el-descriptions>
    </card>
</template>

<script>
import { Card } from "@/components/index";
import defaultAvatarURL from '@/assets/img/defaultAvatar.png'

export default {
    components: {
        Card,
    },

    data() {
        return {
            userInfo: {
                username: this.$cookies.get('username'),
                email: '',
                phone: '',
                description: ''
            },
            displays: {
                username: '用户名',
                email: '邮箱',
                phone: '电话号码',
                description: '个人简介'
            },

            edit: 'none',

            temp: '',

            showChangeAvatar: false,

            headerObj: {
                'Authorization': `Bearer ${$cookies.get('token')}`, // 设置授权头部信息
            },
        }
    },

    created() {
        this.getUserInfo()
        this.getAvatar()
    },

    methods: {
        getUserInfo() {
            fetch(`http://127.0.0.1:5000/get_userinfo`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.userInfo.username = data.username
                    this.userInfo.email = data.email
                    this.userInfo.phone = data.phone
                    this.userInfo.description = data.description
                })
        },

        getAvatar() {
            fetch(`http://127.0.0.1:5000/get_avatar`, {
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                },
                responseType: 'blob'
            })
                .then(response => response.blob())
                .then(blob => {
                    // console.log(blob)
                    if (blob.length > 0)
                        this.userInfo.avatarUrl = window.URL.createObjectURL(blob)
                    // this.userInfo.avatarUrl=window.URL.createObjectURL(response.data)
                })
        },

        commonChange(key, value) {
            fetch(`http://127.0.0.1:5000/change_userinfo`, {
                method: 'post',
                body: JSON.stringify({
                    key: key,
                    value: value
                }),
                headers: {
                    'Content-Type': 'application/json', // 设置内容类型头部信息为 JSON
                    'Authorization': `Bearer ${this.$cookies.get('token')}`, // 设置授权头部信息
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.userInfo[key] = value
                    this.edit = 'none'
                })
        },

        uploadSuccess(response, file, fileList) {
            var data = response
            if (data.hasOwnProperty('error')) {
                this.$message({
                    message: data['error'],
                    type: 'warning'
                })
                return
            }

            // console.log(file)
            // this.userInfo.avatarUrl = window.URL.createObjectURL(file)
            this.getAvatar()

            this.$message({
                message: data['result'],
                type: 'success'
            })
        },
    }
}

</script>

<style>
.margins {
    margin: 0px 2px !important;
}

.el-descriptions-item__content {
    align-items: normal !important;
}

.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.avatar-uploader .el-upload:hover {
    border-color: #409EFF;
}

.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    line-height: 100px !important;
    text-align: center;
}

.avatar {
    width: 100px;
    height: 100px;
    display: block;
}
</style>