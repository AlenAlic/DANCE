import Vue from "vue";

const ADJUDICATION = "ADJUDICATION";
const ADJUDICATION_REQUEST = "ADJUDICATION: Getting adjudication data.";
const ADJUDICATION_SUCCESS = "ADJUDICATION: Successful request.";
const ADJUDICATION_ERROR = "ADJUDICATION: Failed request.";
const SET_ADJUDICATION = "ADJUDICATION: Set adjudication data.";
const UPDATE_MARK = "ADJUDICATION: Update mark";
const SET_MARKS = "ADJUDICATION: Set marks";
const SET_PLACINGS = "ADJUDICATION: Set placings";

export { ADJUDICATION, SET_ADJUDICATION, UPDATE_MARK, SET_MARKS, SET_PLACINGS };

export default {
  state: {
    loading: true,
    adjudicator: {},
    round: null,
    dance: null,
    marks: {},
    placings: [],
    previous_dance: null,
    next_dance: null
  },

  mutations: {
    [ADJUDICATION_REQUEST](state) {
      state.loading = true;
    },
    [ADJUDICATION_SUCCESS](state) {
      state.loading = false;
    },
    [ADJUDICATION_ERROR](state) {
      state.loading = false;
    },
    [SET_ADJUDICATION](state, data) {
      state.adjudicator = data.adjudicator;
      state.round = data.round;
      state.dance = data.dance;
      state.marks = data.marks;
      state.placings = data.placings;
      state.previous_dance = data.previous_dance;
      state.next_dance = data.next_dance;
    },
    [UPDATE_MARK](state, mark) {
      let heat;
      for (heat of Object.keys(state.marks)) {
        let marks = [...state.marks[heat]];
        let i = marks.findIndex(m => m.mark_id === mark.mark_id);
        if (i !== -1) {
          marks[i] = mark;
          state.marks[heat] = marks;
        }
      }
    },
    [SET_MARKS](state, marks) {
      state.marks = marks;
    },
    [SET_PLACINGS](state, placings) {
      state.placings = placings;
    }
  },
  actions: {
    // Get adjudication data
    [ADJUDICATION]({ commit }, { round_id, dance_id }) {
      commit(ADJUDICATION_REQUEST);
      return Vue.axios
        .get(`adjudication/round/${round_id}/dance/${dance_id}`)
        .then(response => {
          commit(SET_ADJUDICATION, response.data);
          commit(ADJUDICATION_SUCCESS);
        })
        .catch(error => {
          commit(ADJUDICATION_ERROR);
          throw error;
        });
    }
  }
};
