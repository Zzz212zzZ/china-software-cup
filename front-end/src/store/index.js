import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selectedWindTurbine: '风机 1',
  },
  mutations: {
    setSelectedWindTurbine(state, windTurbineName) {
      state.selectedWindTurbine = windTurbineName;
      console.log('selectedWindTurbine: ' + state.selectedWindTurbine);
    },
  },
});
