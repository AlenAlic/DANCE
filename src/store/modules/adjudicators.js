import Vue from "vue";

const ADJUDICATORS = "ADJUDICATORS";
const ADJUDICATORS_REQUEST = "ADJUDICATORS: Getting adjudicators.";
const ADJUDICATORS_SUCCESS = "ADJUDICATORS: Successful request.";
const ADJUDICATORS_ERROR = "ADJUDICATORS: Failed request.";
const SET_ADJUDICATORS = "ADJUDICATORS: Set adjudicators.";
const UPDATE_ADJUDICATOR = "ADJUDICATORS: Update adjudicator.";

export { ADJUDICATORS, SET_ADJUDICATORS, UPDATE_ADJUDICATOR };

export default {
  state: {
    loading: false,
    adjudicators: []
  },

  mutations: {
    [ADJUDICATORS_REQUEST](state) {
      state.loading = true;
    },
    [ADJUDICATORS_SUCCESS](state) {
      state.loading = false;
    },
    [ADJUDICATORS_ERROR](state) {
      state.loading = false;
    },
    [SET_ADJUDICATORS](state, adjudicators) {
      state.adjudicators = adjudicators;
    },
    [UPDATE_ADJUDICATOR](state, adjudicator) {
      let adjudicators = [...state.adjudicators];
      let i = adjudicators.findIndex(c => c.adjudicator_id === adjudicator.adjudicator_id);
      adjudicators[i] = adjudicator;
      state.adjudicators = adjudicators;
    }
  },
  actions: {
    // Get adjudicators
    [ADJUDICATORS]({ commit }) {
      commit(ADJUDICATORS_REQUEST);
      return Vue.axios
        .get("adjudicators")
        .then(response => {
          commit(SET_ADJUDICATORS, response.data);
          commit(ADJUDICATORS_SUCCESS);
        })
        .catch(error => {
          commit(ADJUDICATORS_ERROR);
          throw error;
        });
    }
  }
};
