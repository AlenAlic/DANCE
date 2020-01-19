import Vue from "vue";

const FLOOR_MANAGER = "FLOOR_MANAGER";
const FLOOR_MANAGER_REQUEST = "FLOOR_MANAGER: Getting competitions.";
const FLOOR_MANAGER_SUCCESS = "FLOOR_MANAGER: Successful request.";
const FLOOR_MANAGER_ERROR = "FLOOR_MANAGER: Failed request.";
const SET_FLOOR_MANAGER = "FLOOR_MANAGER: Set competitions.";

export { FLOOR_MANAGER, SET_FLOOR_MANAGER };

export default {
  state: {
    loading: false,
    competitions: []
  },

  mutations: {
    [FLOOR_MANAGER_REQUEST](state) {
      state.loading = true;
    },
    [FLOOR_MANAGER_SUCCESS](state) {
      state.loading = false;
    },
    [FLOOR_MANAGER_ERROR](state) {
      state.loading = false;
    },
    [SET_FLOOR_MANAGER](state, competitions) {
      state.competitions = competitions;
    }
  },
  actions: {
    [FLOOR_MANAGER]({ commit }) {
      commit(FLOOR_MANAGER_REQUEST);
      return Vue.axios
        .get("competition/floor_manager")
        .then(response => {
          commit(SET_FLOOR_MANAGER, response.data);
          commit(FLOOR_MANAGER_SUCCESS);
        })
        .catch(error => {
          commit(FLOOR_MANAGER_ERROR);
          throw error;
        });
    }
  }
};
