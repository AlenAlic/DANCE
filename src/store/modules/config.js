import Vue from "vue";

const CONFIG = "CONFIG";
const CONFIG_REQUEST = "CONFIG: Getting config.";
const CONFIG_SUCCESS = "CONFIG: Successful request.";
const CONFIG_ERROR = "CONFIG: Failed request.";

export { CONFIG };

export default {
  state: {
    loading: false,
    config: null
  },

  mutations: {
    [CONFIG_REQUEST](state) {
      state.loading = true;
    },
    [CONFIG_SUCCESS](state, config) {
      state.config = config;
      state.loading = false;
    },
    [CONFIG_ERROR](state) {
      state.loading = false;
    }
  },
  actions: {
    // Get config
    [CONFIG]({ commit }) {
      commit(CONFIG_REQUEST);
      return Vue.axios
        .get("config")
        .then(response => {
          commit(CONFIG_SUCCESS, response.data);
        })
        .catch(error => {
          commit(CONFIG_ERROR);
          throw error;
        });
    }
  }
};
