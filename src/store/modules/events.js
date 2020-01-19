import Vue from "vue";

const EVENTS = "EVENTS";
const EVENTS_REQUEST = "EVENTS: Getting events.";
const EVENTS_SUCCESS = "EVENTS: Successful request.";
const EVENTS_ERROR = "EVENTS: Failed request.";
const EVENTS_CLEAR = "EVENTS: Clear events";

export { EVENTS, EVENTS_CLEAR };

export default {
  state: {
    loading: false,
    events: [],
    activeEvent: null
  },

  mutations: {
    [EVENTS_REQUEST](state) {
      state.loading = true;
    },
    [EVENTS_SUCCESS](state, events) {
      state.events = events;
      let activeEvent = events.filter(e => e.is_active);
      state.activeEvent = activeEvent.length > 0 ? activeEvent[0] : null;
      state.loading = false;
    },
    [EVENTS_ERROR](state) {
      state.loading = false;
    },

    [EVENTS_CLEAR](state) {
      state.activeEvent = null;
      state.events = [];
    }
  },
  actions: {
    // Get events
    [EVENTS]({ commit }) {
      commit(EVENTS_REQUEST);
      return Vue.axios
        .get("event")
        .then(response => {
          commit(EVENTS_SUCCESS, response.data);
        })
        .catch(error => {
          commit(EVENTS_ERROR);
          throw error;
        });
    }
  }
};
