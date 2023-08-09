<template>
  <div class="wrapper">
    <side-bar :title="this.$cookies.get('username')">
      <template slot="links">
        <sidebar-link :to="'/dashboard/' + role + '/' + route.path" :name="route.name" icon="ti-panel"
          v-for="route in routes" v-if="!route.hide_in_nav"></sidebar-link>
      </template>
      <mobile-menu>
        <drop-down class="nav-item" :title="selectedWindTurbineTitle" title-classes="nav-link">
            <div class="custom-scroll" style="max-height: 240px; overflow-y: auto; background-color: rgb(18, 18, 18);">
              <a v-for="windTurbineNumber in datasets" :key="windTurbineNumber.dataset_id" class="dropdown-item"
                @click="updateSelectedWindTurbine(windTurbineNumber)" href="#">
                {{ windTurbineNumber.dataset_name }}
              </a>
            </div>
          </drop-down>
        <li class="nav-item">
            <a @click="logout()" class="nav-link">
              <!-- <i class="ti-settings"></i> -->
              <p>退出登录</p>
            </a>
          </li>
        <li class="divider"></li>
      </mobile-menu>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu,
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
    logout() {
      this.$cookies.remove("user_id")
      this.$cookies.remove("username")
      this.$cookies.remove("role")
      this.$cookies.remove("token")

      this.$router.push(`/login`)
    }
  },
  computed: {
    // 获取当前路由的子路由
    routes() {
      var mainRoute = this.$router.options.routes[1].children[0]
      const roles = ["client", "analyst", "admin"]
      var roleRoute = mainRoute.children[roles.indexOf(this.role)].children
      return roleRoute
    },

    role() {
      return this.$cookies.get("role");
    },
    selectedWindTurbineTitle() {
      // 如果 Vuex store 中有选中的风机，则使用其作为标题，默认为1
      return this.$store.state.selectedWindTurbine.dataset_name;
    },
    datasets() {
      return this.$store.state.datasets; // 从全局状态中获取数据集
    },
  }
};
</script>
