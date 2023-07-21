<template>
  <div class="sidebar" :data-background-color="backgroundColor" :data-active-color="activeColor">
    <!--
            Tip 1: you can change the color of the sidebar's background using: data-background-color="white | black | darkblue"
            Tip 2: you can change the color of the active button using the data-active-color="primary | info | success | warning | danger"
        -->
    <!-- -->
    <div class="sidebar-wrapper" id="style-3">
      <el-popover placement="top-start" width="200" trigger="hover">
        <div class="logo" slot="reference">
          <el-link :underline="false" class="simple-text" style="height: 4em;line-height: 4em;">
            <!-- <div class="logo-img">
            <img src="@/assets/img/defaultAvatar.png" alt="" style="max-width: none;width: 75%;height: 75%;"/>
          </div> -->
            <el-avatar v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl"
              style="height: 40px;width: 40px;vertical-align: middle;"></el-avatar>
            <el-avatar v-else style="height: 40px;width: 40px;vertical-align: middle;">
              <p style="font-size: 27px;">{{ userInfo.username.charAt(0).toLocaleUpperCase() }}</p>
            </el-avatar>
            <p style="display: inline;float: none;font: 1em sans-serif;">
              {{ userInfo.username }}
            </p>
          </el-link>
        </div>

        <div>
          <el-avatar v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl"
            style="height: 40px;width: 40px;vertical-align: middle;"></el-avatar>
          <el-avatar v-else style="height: 40px;width: 40px;vertical-align: middle;">
            <p style="font-size: 27px;">{{ userInfo.username.charAt(0).toLocaleUpperCase() }}</p>
          </el-avatar>
          <p style="display: inline;margin-left: 10px;">{{ userInfo.username }}</p>
        </div>

        <p style="color: gray;font: 0.9em sans-serif;">{{ userInfo.description }}</p>
        <el-link @click="logout()" style="float: right;" :underline="false">退出登录</el-link>
      </el-popover>
      <slot> </slot>
      <ul class="nav">
        <!--By default vue-router adds an active class to each route link. This way the links are colored when clicked-->
        <slot name="links">
          <sidebar-link v-for="(link, index) in sidebarLinks" :key="index" :to="link.path" :name="link.name"
            :icon="link.icon">
          </sidebar-link>
        </slot>
      </ul>
      <moving-arrow :move-y="arrowMovePx"> </moving-arrow>
    </div>
  </div>
</template>
<script>
import MovingArrow from "./MovingArrow.vue";
import SidebarLink from "./SidebarLink";
import defaultAvatarURL from '@/assets/img/defaultAvatar.png'
export default {
  props: {
    title: {
      type: String,
      default: "你好",
    },
    backgroundColor: {
      type: String,
      default: "black",
      validator: (value) => {
        let acceptedValues = ["white", "black", "darkblue"];
        return acceptedValues.indexOf(value) !== -1;
      },
    },
    activeColor: {
      type: String,
      default: "success",
      validator: (value) => {
        let acceptedValues = [
          "primary",
          "info",
          "success",
          "warning",
          "danger",
        ];
        return acceptedValues.indexOf(value) !== -1;
      },
    },
    sidebarLinks: {
      type: Array,
      default: () => [],
    },
    autoClose: {
      type: Boolean,
      default: true,
    },
  },
  provide() {
    return {
      autoClose: this.autoClose,
      addLink: this.addLink,
      removeLink: this.removeLink,
    };
  },
  components: {
    MovingArrow,
    SidebarLink,
  },
  computed: {
    /**
     * Styles to animate the arrow near the current active sidebar link
     * @returns {{transform: string}}
     */
    arrowMovePx() {
      return this.linkHeight * this.activeLinkIndex;
    },
  },
  data() {
    return {
      linkHeight: 65,
      activeLinkIndex: 0,
      windowWidth: 0,
      isWindows: false,
      hasAutoHeight: false,
      links: [],

      userInfo: {
        username: '',
        description: '',
      }
    };
  },
  methods: {
    findActiveLink() {
      this.links.forEach((link, index) => {
        if (link.isActive()) {
          this.activeLinkIndex = index;
        }
      });
    },
    addLink(link) {
      const index = this.$slots.links.indexOf(link.$vnode);
      this.links.splice(index, 0, link);
    },
    removeLink(link) {
      const index = this.links.indexOf(link);
      if (index > -1) {
        this.links.splice(index, 1);
      }
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
          if (blob.size > 0)
            // this.userInfo.avatarUrl = window.URL.createObjectURL(blob)
            this.$set(this.userInfo, 'avatarUrl', window.URL.createObjectURL(blob))
          // this.userInfo.avatarUrl=window.URL.createObjectURL(response.data)
        })
    },

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

    logout() {
      this.$cookies.remove("user_id")
      this.$cookies.remove("username")
      this.$cookies.remove("role")
      this.$cookies.remove("token")

      this.$router.push(`/login`)
    }
  },
  mounted() {
    this.$watch("$route", this.findActiveLink, {
      immediate: true,
    });
  },

  created() {
    this.getAvatar()
    this.getUserInfo()
  }
};
</script>
<style></style>
