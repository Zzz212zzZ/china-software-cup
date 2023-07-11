
<template>
    <div class="mainContainer">
        <img src="@/assets/img/tempBackground.jpg"
            style="height: 100%;width: 100%;position: absolute;z-index: -1;object-fit: cover;">

        <div class="logInContainer">
            <el-form ref="login" :model="logInData" label-width="70px" :rules="rules">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="logInData.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="logInData.password" show-password></el-input>
                </el-form-item>
                <el-form-item>
                    <el-checkbox v-model="logInData.remember">记住我</el-checkbox>
                    <!-- <div style="width: 100%;"></div> -->
                    <el-button type="text" @click="signUpDialog = true" size="small" style="float: right">没有账号?点击注册</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="logIn()" style="float: right">登录</el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 注册对话框 -->
        <el-dialog title="注册账号" :visible.sync="signUpDialog" width="500px" :append-to-body="true">
            <el-form ref="signup" :rules="rules" :model="signUpData" label-width="70px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="signUpData.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="signUpData.password" show-password></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="password_repeat">
                    <el-input v-model="signUpData.password_repeat" show-password></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="signUpDialog = false">取 消</el-button>
                <el-button type="primary" @click="signUp()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
  
<script>
export default {
    name: 'LoginPage',
    data() {
        var validatePassRepeat = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.signUpData.password) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        }
        return {
            signUpData: {
                username: '',
                password: '',
                password_repeat: '',
            },
            logInData: {
                username: '',
                password: '',
                remember:false
            },
            signUpDialog: false,
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' }
                ],
                password_repeat: [
                    { validator: validatePassRepeat, trigger: 'blur' }
                ],
            },
        };
    },
    methods: {
        signUp() {
            // Handle the sign-up logic here...
            this.$refs['signup'].validate((valid) => {
                if (valid) {
                    fetch(`http://127.0.0.1:5000/sign_up`, {
                        method: 'post',
                        body: JSON.stringify({
                            username: this.signUpData.username,
                            password: this.signUpData.password
                        })
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

                            this.signUpDialog = false
                            this.signUpData = {
                                username: '',
                                password: '',
                                password_repeat: '',
                            }
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
        logIn() {
            // Handle the log-in logic here...
            this.$refs['login'].validate((valid) => {
                if (valid) {
                    fetch(`http://127.0.0.1:5000/login`, {
                        method: 'post',
                        body: JSON.stringify({
                            username: this.logInData.username,
                            password: this.logInData.password
                        })
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
                            // localStorage.setItem('role',data['role'])
                            // localStorage.setItem('token',data['user_id'])
                            var expire='0'
                            if(this.logInData.remember) expire='7D'
                            this.$cookies.set("user_id",data["user_id"],expire)
                            this.$cookies.set("username",data["username"],expire)
                            this.$cookies.set("role",data["role"],expire)

                            this.$router.push(`/dashboard/${data["role"]}`)
                        })

                } else {
                    return false;
                }
            });
        }
    }
};
</script>

<style>
.mainContainer {
    display: flex;
    width: 100%;
    height: 100vh;
    align-items: center;
    justify-content: center;
}

.logInContainer {
    height: auto;
    width: 450px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 30px 15px;
    border-radius: 10px;
}
</style>