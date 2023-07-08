<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links">
        <sidebar-link :to="'/dashboard/'+role+'/'+route.path" :name="route.name" icon="ti-panel"  v-for="route in routes"></sidebar-link>
        <!-- <sidebar-link to="/dashboard/client/dataAnalysis" name="数据特征分析" icon="ti-panel" />
        <sidebar-link to="/dashboard/client/dataPreprocess" name="数据预处理" icon="ti-panel" />
        <sidebar-link to="/dashboard/client/modelTrain" name="模型训练" icon="ti-panel" /> -->
      </template>
      <!-- <p>{{ routes }}</p> -->
      <mobile-menu>
        <li class="nav-item">
          <a class="nav-link">
            <i class="ti-panel"></i>
            <p>213</p>
          </a>
        </li>
        <drop-down class="nav-item" title="5 Notifications" title-classes="nav-link" icon="ti-bell">
          <a class="dropdown-item">Notification 4</a>
          <a class="dropdown-item">Notification 2</a>
          <a class="dropdown-item">Notification 3</a>
          <a class="dropdown-item">Notification 6</a>
          <a class="dropdown-item">Another notification</a>
        </drop-down>
        <li class="nav-item">
          <a class="nav-link">
            <i class="ti-settings"></i>
            <p>Settings</p>
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
  },
  computed: {
    // 获取当前路由的子路由
    routes() {
      var mainRoute=this.$router.options.routes[1].children[0]
      const roles=["client","analyst","admin"]
      var roleRoute=mainRoute.children[roles.indexOf(this.role)].children
      console.log(roleRoute)
      return roleRoute
    },

    role(){
      return localStorage.getItem('role')
    }
  }
};
</script>
