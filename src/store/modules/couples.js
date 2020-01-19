import Vue from "vue";

const COUPLES = "COUPLES";
const COUPLES_REQUEST = "COUPLES: Getting couples.";
const COUPLES_SUCCESS = "COUPLES: Successful request.";
const COUPLES_ERROR = "COUPLES: Failed request.";
const SET_COUPLES = "COUPLES: Set couples.";
const UPDATE_COUPLE = "COUPLES: Update couple.";
const DELETE_COUPLE = "COUPLES: Delete couple.";

export { COUPLES, SET_COUPLES, UPDATE_COUPLE, DELETE_COUPLE };

export default {
  state: {
    loading: false,
    couples: []
  },

  mutations: {
    [COUPLES_REQUEST](state) {
      state.loading = true;
    },
    [COUPLES_SUCCESS](state) {
      state.loading = false;
    },
    [COUPLES_ERROR](state) {
      state.loading = false;
    },
    [SET_COUPLES](state, couples) {
      state.couples = couples;
    },
    [UPDATE_COUPLE](state, couple) {
      let couples = [...state.couples];
      let i = couples.findIndex(c => c.couple_id === couple.couple_id);
      couples[i] = couple;
      state.couples = couples;
    },
    [DELETE_COUPLE](state, couple_id) {
      let couples = [...state.couples];
      let i = couples.findIndex(c => c.couple_id === couple_id);
      couples.splice(i, 1);
      state.couples = couples;
    }
  },
  actions: {
    // Get couples
    [COUPLES]({ commit }) {
      commit(COUPLES_REQUEST);
      return Vue.axios
        .get("couples")
        .then(response => {
          commit(SET_COUPLES, response.data);
          commit(COUPLES_SUCCESS);
        })
        .catch(error => {
          commit(COUPLES_ERROR);
          throw error;
        });
    }
  }
};
