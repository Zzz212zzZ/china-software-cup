<template>
  <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">{{ routeName }}</a>
      <button class="navbar-toggler navbar-burger" type="button" @click="toggleSidebar"
        :aria-expanded="$sidebar.showSidebar" aria-label="Toggle navigation">
        <span class="navbar-toggler-bar"></span>
        <span class="navbar-toggler-bar"></span>
        <span class="navbar-toggler-bar"></span>
      </button>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a href="#" class="nav-link">
              <i class="ti-panel"></i>
              <p>Stats</p>
            </a>
          </li>


          <drop-down class="nav-item" :title="selectedWindTurbineTitle" title-classes="nav-link" icon="ti-bell">
            <div class="custom-scroll" style="max-height: 240px; overflow-y: auto;">
              <a v-for="windTurbineNumber in 20" :key="windTurbineNumber" class="dropdown-item"
                @click="updateSelectedWindTurbine(`风机 ${windTurbineNumber}`)" href="#">
                风机 {{ windTurbineNumber }}
              </a>
            </div>
          </drop-down>


          <li class="nav-item">
            <a href="#" class="nav-link">
              <i class="ti-settings"></i>
              <p>Settings</p>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
export default {
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    },
     // 从 Vuex store 获取选中的风机
     selectedWindTurbineTitle() {
        // 如果 Vuex store 中有选中的风机，则使用其作为标题，否则使用默认标题 "风机数据集"
        return this.$store.state.selectedWindTurbine || '风机数据集';
    }
  },
  data() {
    return {
      activeNotifications: false,
    };
  },
  methods: {
    updateSelectedWindTurbine(windTurbineName) {
      this.$store.commit('setSelectedWindTurbine', windTurbineName);
    },

    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
  },
};
</script>
<style scoped>
/* WebKit 浏览器（例如 Chrome 和 Safari） */
.custom-scroll::-webkit-scrollbar {
  width: 12px !important;
  /* 滚动条宽度 */
}

.custom-scroll::-webkit-scrollbar-track {
  background-color: #f1f1f1 !important;
  /* 滚动条轨道颜色 */
}

.custom-scroll::-webkit-scrollbar-thumb {
  background-color: #82827c !important;
  /* 滚动条颜色 */
  border-radius: 6px !important;
  /* 滚动条圆角 */
}

.custom-scroll::-webkit-scrollbar-thumb:hover {
  background-color: #fdf3626b !important;
  /* 鼠标悬停时滚动条颜色 */
}

/* Firefox 浏览器 */
.custom-scroll {
  scrollbar-width: thin !important;
  /* 滚动条宽度 */
  scrollbar-color: #888 #f1f1f1 !important;
  /* 滚动条颜色和滚动条轨道颜色 */
}</style>