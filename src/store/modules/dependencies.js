import Vue from "vue";

const DANCES = "DANCES";
const DANCES_REQUEST = "DANCES: Getting dances.";
const DANCES_SUCCESS = "DANCES: Successful request.";
const DANCES_ERROR = "DANCES: Failed request.";
const SET_DANCES = "DANCES: Setting dances.";

const DISCIPLINES = "DISCIPLINES";
const DISCIPLINES_REQUEST = "DISCIPLINES: Getting disciplines.";
const DISCIPLINES_SUCCESS = "DISCIPLINES: Successful request.";
const DISCIPLINES_ERROR = "DISCIPLINES: Failed request.";
const SET_DISCIPLINES = "DISCIPLINES: Setting disciplines.";

const CLASSES = "CLASSES";
const CLASSES_REQUEST = "CLASSES: Getting classes.";
const CLASSES_SUCCESS = "CLASSES: Successful request.";
const CLASSES_ERROR = "CLASSES: Failed request.";
const SET_CLASSES = "CLASSES: Setting classes.";

const ALL_DEPENDENCIES = "ALL_DEPENDENCIES";
const ALL_DEPENDENCIES_REQUEST = "ALL_DEPENDENCIES: Getting all dependencies.";
const ALL_DEPENDENCIES_SUCCESS = "ALL_DEPENDENCIES: Successful request.";
const ALL_DEPENDENCIES_ERROR = "ALL_DEPENDENCIES: Failed request.";
const SET_ALL_DEPENDENCIES = "ALL_DEPENDENCIES: Setting all dependencies.";

export {
  DANCES,
  DISCIPLINES,
  CLASSES,
  ALL_DEPENDENCIES,
  SET_DANCES,
  SET_DISCIPLINES,
  SET_CLASSES,
  SET_ALL_DEPENDENCIES
};

export default {
  state: {
    loadingDances: false,
    dances: [],
    loadingDisciplines: false,
    disciplines: [],
    loadingClasses: false,
    classes: []
  },

  mutations: {
    [DANCES_REQUEST](state) {
      state.loadingDances = true;
    },
    [DANCES_SUCCESS](state) {
      state.loadingDances = false;
    },
    [DANCES_ERROR](state) {
      state.loadingDances = false;
    },
    [SET_DANCES](state, dances) {
      state.dances = dances;
    },

    [DISCIPLINES_REQUEST](state) {
      state.loadingDisciplines = true;
    },
    [DISCIPLINES_SUCCESS](state) {
      state.loadingDisciplines = false;
    },
    [DISCIPLINES_ERROR](state) {
      state.loadingDisciplines = false;
    },
    [SET_DISCIPLINES](state, disciplines) {
      state.disciplines = disciplines;
    },

    [CLASSES_REQUEST](state) {
      state.loadingClasses = true;
    },
    [CLASSES_SUCCESS](state) {
      state.loadingClasses = false;
    },
    [CLASSES_ERROR](state) {
      state.loadingClasses = false;
    },
    [SET_CLASSES](state, classes) {
      state.classes = classes;
    },

    [ALL_DEPENDENCIES_REQUEST](state) {
      state.loadingDances = true;
      state.loadingDisciplines = true;
      state.loadingClasses = true;
    },
    [ALL_DEPENDENCIES_SUCCESS](state) {
      state.loadingDances = false;
      state.loadingDisciplines = false;
      state.loadingClasses = false;
    },
    [ALL_DEPENDENCIES_ERROR](state) {
      state.loadingDances = false;
      state.loadingDisciplines = false;
      state.loadingClasses = false;
    },
    [SET_ALL_DEPENDENCIES](state, dependencies) {
      state.dances = dependencies.dances;
      state.disciplines = dependencies.disciplines;
      state.classes = dependencies.classes;
    }
  },
  actions: {
    // Get dances
    [DANCES]({ commit }) {
      commit(DANCES_REQUEST);
      return Vue.axios
        .get("dependencies/dances")
        .then(response => {
          commit(SET_DANCES, response.data);
          commit(DANCES_SUCCESS);
        })
        .catch(error => {
          commit(DANCES_ERROR);
          throw error;
        });
    },
    // Get disciplines
    [DISCIPLINES]({ commit }) {
      commit(DISCIPLINES_REQUEST);
      return Vue.axios
        .get("dependencies/disciplines")
        .then(response => {
          commit(SET_DISCIPLINES, response.data);
          commit(DISCIPLINES_SUCCESS);
        })
        .catch(error => {
          commit(DISCIPLINES_ERROR);
          throw error;
        });
    },
    // Get classes
    [CLASSES]({ commit }) {
      commit(CLASSES_REQUEST);
      return Vue.axios
        .get("dependencies/classes")
        .then(response => {
          commit(SET_CLASSES, response.data);
          commit(CLASSES_SUCCESS);
        })
        .catch(error => {
          commit(CLASSES_ERROR);
          throw error;
        });
    },
    // Get all dependencies
    [ALL_DEPENDENCIES]({ commit }) {
      commit(ALL_DEPENDENCIES_REQUEST);
      return Vue.axios
        .get("dependencies")
        .then(response => {
          commit(SET_ALL_DEPENDENCIES, response.data);
          commit(ALL_DEPENDENCIES_SUCCESS);
        })
        .catch(error => {
          commit(ALL_DEPENDENCIES_ERROR);
          throw error;
        });
    }
  },
  getters: {
    danceMap: state => discipline_id => {
      return state.disciplines.find(d => d.discipline_id === discipline_id).dances;
    }
  }
};
