/*!

 =========================================================
 * Vue Paper Dashboard - v1.0.1
 =========================================================

 * Product Page: http://www.creative-tim.com/product/paper-dashboard
 * Copyright 2023 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard/blob/master/LICENSE.md)

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */
import Vue from "vue";
import App from "./App";
import router from "./router/index";

import PaperDashboard from "./plugins/paperDashboard";
import "vue-notifyjs/themes/default.css";
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import 'popper.js/dist/popper.js';

import {
  Message,
  Loading,
  Dialog,
  Divider,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Input,
  Slider,
  Button,
  ButtonGroup,
} from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';


Vue.use(PaperDashboard);
Vue.component(Message)
Vue.use(Loading)
Vue.use(Dialog)
Vue.use(Divider)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Input)
Vue.use(Slider)
Vue.use(Button)
Vue.use(ButtonGroup)
Vue.prototype.$message = Message

/* eslint-disable no-new */
new Vue({
  store,
  router,
  el: '#app',
  render: (h) => h(App),
}).$mount("#app");
