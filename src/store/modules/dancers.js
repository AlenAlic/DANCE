import Vue from "vue";
import { LEAD, FOLLOW } from "@/constants";

const DANCERS = "DANCERS";
const DANCERS_REQUEST = "DANCERS: Getting dancers.";
const DANCERS_SUCCESS = "DANCERS: Successful request.";
const DANCERS_ERROR = "DANCERS: Failed request.";
const SET_DANCERS = "DANCERS: Set dancers.";
const UPDATE_DANCER = "DANCERS: Update dancer.";
const DELETE_DANCER = "DANCERS: Delete dancer.";

export { DANCERS, SET_DANCERS, UPDATE_DANCER, DELETE_DANCER };

export default {
  state: {
    loading: false,
    dancers: [],
    leads: [],
    follows: []
  },

  mutations: {
    [DANCERS_REQUEST](state) {
      state.loading = true;
    },
    [DANCERS_SUCCESS](state) {
      state.loading = false;
    },
    [DANCERS_ERROR](state) {
      state.loading = false;
    },
    [SET_DANCERS](state, dancers) {
      state.dancers = dancers;
      state.leads = dancers.filter(d => d.role === LEAD);
      state.follows = dancers.filter(d => d.role === FOLLOW);
    },
    [UPDATE_DANCER](state, dancer) {
      let dancers = [...state.dancers];
      let i = dancers.findIndex(d => d.dancer_id === dancer.dancer_id);
      dancers[i] = dancer;
      this.commit(SET_DANCERS, dancers);
    },
    [DELETE_DANCER](state, dancer_id) {
      let dancers = [...state.dancers];
      let i = dancers.findIndex(d => d.dancer_id === dancer_id);
      dancers.splice(i, 1);
      this.commit(SET_DANCERS, dancers);
    }
  },
  actions: {
    // Get dancers
    [DANCERS]({ commit }) {
      commit(DANCERS_REQUEST);
      return Vue.axios
        .get("dancers")
        .then(response => {
          commit(SET_DANCERS, response.data);
          commit(DANCERS_SUCCESS);
        })
        .catch(error => {
          commit(DANCERS_ERROR);
          throw error;
        });
    }
  }
};
