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
          <!-- <li class="nav-item">
            <a href="#" class="nav-link">
              <i class="ti-panel"></i>
              <p>Stats</p>
            </a>
          </li> -->



          <li class="nav-item d-flex align-items-center">
            <i class="ti-map-alt"></i>
            <a type="button" class="nav-link custom-link" @click="showModal">地图</a>
            <modal name="my-modal" :width="700" height="500" :adaptive="true" classes="modal-background">
              <ChinaMap />
            </modal>

          </li>



          <drop-down class="nav-item" :title="selectedWindTurbineTitle" title-classes="nav-link" icon="ti-bell">
            <div class="custom-scroll" style="max-height: 240px; overflow-y: auto;">
              <a v-for="windTurbineNumber in datasets" :key="windTurbineNumber.dataset_id" class="dropdown-item"
                @click="updateSelectedWindTurbine(windTurbineNumber)" href="#">
                {{ windTurbineNumber.dataset_name }}
              </a>
            </div>
          </drop-down>




          <li class="nav-item d-flex align-items-center">

            <i class="ti-arrow-right"></i>
            <a @click="logout()" class="nav-link custom-link">
              <!-- <i class="ti-settings"></i> -->
              <p>退出登录</p>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import ChinaMap from './ChinaMap.vue'
export default {
  components: {
    ChinaMap
  },
  computed: {
    datasets() {
      return this.$store.state.datasets; // 从全局状态中获取数据集
    },
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    },
    // 从 Vuex store 获取选中的风机
    selectedWindTurbineTitle() {
      return this.$store.state.selectedWindTurbine.dataset_name;
    }
  },
  data() {
    return {
      activeNotifications: false,
      // datasets: [],
    };
  },
  methods: {
    showModal() {
      this.$modal.show('my-modal');
    },

    updateSelectedWindTurbine(windTurbineName) {
      // console.log(windTurbineName.dataset_name)
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
    logout() {
      this.$cookies.remove("user_id")
      this.$cookies.remove("username")
      this.$cookies.remove("role")
      this.$cookies.remove("token")

      this.$router.push(`/login`)
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
          this.$store.commit('setSelectedWindTurbine', data[0]); // 更新全局状态
          this.$store.commit('updateDatasets', data); // 更新全局状态
          // console.log(data)
        });
    },

  },
  created() {
    this.getDatasets()
  },
};
</script>
<style >
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
}



.custom-link {
  cursor: pointer;
  border: none;
  transition: color 0.3s ease;
  padding-left: 5px !important;
}

.modal-background {
  background-color: rgba(0, 0, 0, 0) !important;
  /* 使用 'rgba' 以及 'important' 来覆盖默认的背景色 */
}

.vm--modal {
  background-color: rgba(0, 0, 0, 0) !important;
}
</style>