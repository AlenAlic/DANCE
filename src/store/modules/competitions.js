import Vue from "vue";
import { dateTimeFromUTC } from "@/assets/js/utilities";

const COMPETITIONS = "COMPETITIONS";
const COMPETITIONS_REQUEST = "COMPETITIONS: Getting competitions.";
const COMPETITIONS_SUCCESS = "COMPETITIONS: Successful request.";
const COMPETITIONS_ERROR = "COMPETITIONS: Failed request.";
const SET_COMPETITIONS = "COMPETITIONS: Set competitions.";
const UPDATE_COMPETITION = "COMPETITIONS: Update competition.";
const DELETE_COMPETITION = "COMPETITIONS: Delete competition.";

export { COMPETITIONS, SET_COMPETITIONS, UPDATE_COMPETITION, DELETE_COMPETITION };

export default {
  state: {
    loading: false,
    competitions: []
  },

  mutations: {
    [COMPETITIONS_REQUEST](state) {
      state.loading = true;
    },
    [COMPETITIONS_SUCCESS](state) {
      state.loading = false;
    },
    [COMPETITIONS_ERROR](state) {
      state.loading = false;
    },
    [SET_COMPETITIONS](state, competitions) {
      state.competitions = competitions;
    },
    [UPDATE_COMPETITION](state, competition) {
      let competitions = [...state.competitions];
      let i = competitions.findIndex(x => x.competition_id === competition.competition_id);
      competitions[i] = competition;
      state.competitions = competitions.sort(
        (a, b) => dateTimeFromUTC(a.date).ts - dateTimeFromUTC(b.date).ts
      );
    },
    [DELETE_COMPETITION](state, competition_id) {
      let competitions = [...state.competitions];
      let i = competitions.findIndex(x => x.competition_id === competition_id);
      competitions.splice(i, 1);
      state.competitions = competitions;
    }
  },
  actions: {
    [COMPETITIONS]({ commit }) {
      commit(COMPETITIONS_REQUEST);
      return Vue.axios
        .get("competition")
        .then(response => {
          commit(SET_COMPETITIONS, response.data);
          commit(COMPETITIONS_SUCCESS);
        })
        .catch(error => {
          commit(COMPETITIONS_ERROR);
          throw error;
        });
    }
  },
  getters: {
    competition: state => id => {
      return state.competitions.find(c => c.competition_id === Number(id));
    }
  }
};
