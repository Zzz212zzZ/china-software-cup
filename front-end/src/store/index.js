import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selectedWindTurbine: '', // 初始值为空字符串
    datasets: [],
  },
  mutations: {
    setSelectedWindTurbine(state, windTurbineName) {
      state.selectedWindTurbine = windTurbineName;
      console.log('selectedWindTurbine: ' + state.selectedWindTurbine);
    },
    updateDatasets(state, datasets) {
      state.datasets = datasets;
    },
    updateDatasetName(state, { dataset_id, newDatasetName }) {
      const datasetToUpdate = state.datasets.find(dataset => dataset.dataset_id === dataset_id);
      if (datasetToUpdate) {
        datasetToUpdate.dataset_name = newDatasetName;
      }
    },
  }
});
